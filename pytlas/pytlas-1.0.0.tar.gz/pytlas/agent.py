import logging, random
from .request import Request
from .localization import translations
from .interpreters.intent import Intent
from .interpreters.slot import SlotValue
from .skill import handlers as skill_handlers
from transitions import Machine, MachineError
from fuzzywuzzy import process

# Silent the transitions logger
logging.getLogger('transitions').setLevel(logging.WARNING)

STATE_PREFIX = 'pytlas__'
STATE_ASLEEP = STATE_PREFIX + 'asleep'
STATE_CANCEL = STATE_PREFIX + 'cancel'
STATE_FALLBACK = STATE_PREFIX + 'fallback'
STATE_ASK = STATE_PREFIX + 'ask'

def is_builtin(state):
  """Checks if the given state is a builtin one.
  
  Args:
    state (str): State to check

  Returns:
    bool: True if it's a builtin state, false otherwise

  """

  return state.startswith(STATE_PREFIX)

def keep_one(value):
  """Keeps only one element if value is a list.

  Args:
    value (str, list): Value to check

  Returns:
    str: Random value in the given list if it's a list, else the given value

  """

  if type(value) is list:
    return random.choice(value)

  return value

def find_matches(choices, values):
  """Find elements that fuzzy match the available choices.

  Args:
    choices (list): Available choices
    values (list): List of SlotValue we should compare with available choices

  Returns:
    generator: matched SlotValue updated with matched value if any

  """

  for value in values:
    match = process.extractOne(value.value, choices, score_cutoff=60)

    if match:
      value.value = match[0] # Update the inner value with the matched one
      yield value

class Agent:
  """Manages a conversation with a client.

  Conversation state is represented by a finite state machine. It handle ask states
  when the skill needs more information and trigger appropriate handler upon intent
  parsing.

  """

  def __init__(self, interpreter, handlers=None, 
    on_ask=None, on_answer=None, on_done=None, **kwargs):
    """Initialize an agent.

    Args:
      interpreter (Interpreter): Interpreter used to convert human language to intents
      handlers (dict): Dictionary of intent: handler to use. If no one is provided, all handlers registered will be used instead.
      on_ask (func): Handler called when a skill needs more user input
      on_answer (func): Handler called called when a skill wants to give an answer to the user
      on_done (func): Called when a skill has ended its work
      kwargs (dict): Every other properties will be made available through the self.meta property

    """

    self._logger = logging.getLogger(self.__class__.__name__.lower())
    self._interpreter = interpreter

    # Register handlers
    self.on_ask = on_ask
    self.on_answer = on_answer
    self.on_done = on_done

    self._handlers = handlers or skill_handlers

    self._intents_queue = []
    self._request = None
    self._asked_slot = None
    self._choices = None
    
    self.meta = kwargs

    self._machine = None
    self.setup()

  def setup(self):
    """Setup the state machine based on the interpreter available intents. This is
    especialy useful if you have trained the interpreter after creating this agent.

    This method is also called from the constructor.

    """

    # Ends the conversation if the machine already exists, just to make sure
    if self._machine:
      self.end_conversation()

    intents = [i for i in self._interpreter.intents if not is_builtin(i)]
    states = [STATE_ASLEEP, STATE_ASK, STATE_FALLBACK, STATE_CANCEL] + intents
    
    self._machine = Machine(
      model=self, 
      states=states, 
      send_event=True,
      before_state_change=self._log_transition,
      initial=STATE_ASLEEP)

    self._logger.info('Instantiated agent with "%s" states: %s' % (len(states), ', '.join('"%s"' % s for s in states)))

    # Go to the asleep state from anywhere except the ask state
    self._machine.add_transition(
      STATE_ASLEEP, 
      [STATE_CANCEL, STATE_FALLBACK] + intents,
      STATE_ASLEEP,
      after=self.end_conversation)

    # Go to the cancel state from anywhere except the asleep state
    self._machine.add_transition(
      STATE_CANCEL,
      [STATE_ASK, STATE_FALLBACK] + intents,
      STATE_CANCEL,
      after=self._on_intent)

    # Go to the ask state from every intents
    self._machine.add_transition(
      STATE_ASK,
      [STATE_FALLBACK] + intents,
      STATE_ASK,
      after=self._on_asked)

    # And go to intents state from asleep or ask states
    for intent in [STATE_FALLBACK] + intents:
      self._machine.add_transition(
        intent,
        [STATE_ASLEEP, STATE_ASK],
        intent,
        after=self._on_intent)

  def _log_transition(self, e):
    dest = e.transition.dest
    msg = '⚡ "%s": %s -> %s' % (e.event.name, e.transition.source, dest)

    if dest == STATE_ASK:
      msg += ' (slot: {slot}, choices: {choices})'.format(**e.kwargs)

    self._logger.info(msg)

  def _is_valid(self, data, required_keys=[]):
    if not all(elem in data and data[elem] != None for elem in required_keys):
      self._logger.warning('One of required keys are not present or its value is equal to None in the data, required keys were %s' % required_keys)
      return False

    return True

  def parse(self, msg):
    """Parse a raw message.

    The interpreter will be used to determine which intent(s) has been formulated
    by the user and the state machine will move to the appropriate state calling
    the right skill handler.

    It will also handle some specific intents such as the cancel one and ask states.

    Args:
      msg (str): Raw message to parse

    """

    self._logger.info('Parsing sentence "%s"' % msg)

    intents = self._interpreter.parse(msg) or [Intent(STATE_FALLBACK, text=msg)]
    cancel_intent = next((i for i in intents if i.name == STATE_CANCEL), None)

    # Either way, extend the intent queue with new intents
    if self.state != STATE_ASK: # pylint: disable=E1101
      intents = [i for i in intents if i.name != STATE_CANCEL]

      self._logger.info('"%s" intent(s) found: %s' % (len(intents), ', '.join([str(i) for i in intents])))

      self._intents_queue.extend(intents)
    
    # If the user wants to cancel the current action, immediately go to the cancel state
    if cancel_intent and self.state != STATE_ASLEEP: # pylint: disable=E1101
      self.go(STATE_CANCEL, intent=cancel_intent) # Go to the cancel intent right now!
    else:
      if self.state == STATE_ASK: # pylint: disable=E1101
        values = self._interpreter.parse_slot(self._request.intent.name, self._asked_slot, msg)
        
        if self._choices:
          values = list(find_matches(self._choices, values))

        self._request.intent.update_slots(**{ self._asked_slot: values })
        self._logger.info('Updated slot "%s" with values %s' % (self._asked_slot, ['"%s"' % v for v in values]))
        
        self.go(self._request.intent.name, intent=self._request.intent)
      elif self.state == STATE_ASLEEP: # pylint: disable=E1101
        self._process_next_intent()

  def _process_intent(self, intent):
    self._logger.info('Processing intent %s' % intent)

    handler = self._handlers.get(intent.name)
    
    if not handler:
      self._logger.warning('No handler found for the intent "%s"' % intent.name)
      self.done()
    else:
      if (self._request == None or self._request.intent != intent):
        # Creates the request and load module translations for the interpreter language
        # if any
        self._request = Request(self, intent, 
          translations.get(handler.__module__, {}).get(self._interpreter.lang, {}))
        self._logger.info('💬 New "%s" conversation started with id "%s"' % (intent.name, self._request.id))
      
      try:
        self._logger.debug('Calling handler "%s"' % handler)
        handler(self._request) # TODO multi threaded call
      except Exception as err:
        self._logger.error(err)
        self.done() # Go back to the asleep state

  def _on_intent(self, event):
    if not self._is_valid(event.kwargs, ['intent']):
      return self.done()

    self._process_intent(event.kwargs.get('intent'))

  def _on_asked(self, event):
    if not self._is_valid(event.kwargs, ['slot', 'text']):
      return self.done()

    text = keep_one(event.kwargs.get('text'))
    slot = event.kwargs.get('slot')
    choices = event.kwargs.get('choices')

    self._asked_slot = slot
    self._choices = choices

    if self.on_ask:
      self.on_ask(slot, text, choices)

  def _process_next_intent(self):
    if len(self._intents_queue) > 0:
      intent = self._intents_queue.pop(0)

      self.go(intent.name, intent=intent)

  def go(self, state, **kwargs):
    """Try to move the state machine to the given state.

    Args:
      state (str): Desired state
      kwargs (dict): Arguments

    """

    try:
      self.trigger(state, **kwargs) # pylint: disable=E1101
    except (MachineError, AttributeError) as err:
      self._logger.error('Could not trigger "%s": %s' % (state, err))

  def ask(self, slot, text, choices=None):
    """Ask something to the user.

    Args:
      slot (str): Name of the slot asked for
      text (str, list): Text to show to the user
      choices (list): List of available choices

    """

    if self.on_done:
      self.on_done()

    self.go(STATE_ASK, slot=slot, text=text, choices=choices)

  def answer(self, text, cards=None):
    """Answer something to the user.

    Args:
      text (str, list): Text to show to the user
      cards (list, Card): List of Card to show if any

    """

    if cards and type(cards) is not list:
      cards = [cards]

    if self.on_answer:
      self.on_answer(keep_one(text), cards)

  def done(self):
    """Done should be called by skills when they are done with their stuff. It enables
    threaded scenarii. When asking something to the user, you should not call this method!

    """

    self.go(STATE_ASLEEP)

  def end_conversation(self, event=None):
    """Ends a conversation, means nothing would come from the skill anymore and
    it does not require user inputs. This is especially useful when you are showing
    an activity indicator.

    """

    if self._request:
      self._logger.info('Conversation "%s" has ended' % self._request.id)

    self._request = None
    self._asked_slot = None
    self._choices = None

    if self.on_done:
      self.on_done()
      
    self._process_next_intent()