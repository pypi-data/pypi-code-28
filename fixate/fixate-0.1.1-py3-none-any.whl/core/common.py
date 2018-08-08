import re
import sys
import threading
import inspect
import ctypes
import logging
from fixate.core.exceptions import ParameterError, InvalidScalarQuantityError

logger = logging.getLogger(__file__)


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


UNITS = {"Hz", "Vpp", "Vmax", "VMin", "V", "%", "Hertz", "Volts", "Percent", "PC", "deg", "Deg", 'C', 'H'}
UNIT_SCALE = {"m": 10 ** -3, "u": 10 ** -6, "n": 10 ** -9, "k": 10 ** 3, "M": 10 ** 6, "G": 10 ** 9}


def required_params(keys):
    """
    searches the keys to see if any optional parameters are present
    :param keys:
    :return:
    """
    for key in keys:
        if re.search(r'\[', key):
            return False
    if len(keys):
        return True
    return False


def match_params(args, kwargs, keys, repl_kwargs):
    matches = []
    tmp_args = args
    for arg in tmp_args:
        matches.append(match_arg(arg, keys))
    for kwarg in kwargs:
        match = match_kwarg(kwarg, keys)
        if match:
            repl_kwargs[kwarg] = match
        matches.append(match_kwarg(kwarg, keys))
    return matches


def match_arg(search, keys):
    for key in keys:
        regex = r'[[:]+' + search.lower()
        if re.search(regex, key.lower()):
            return key
    return None


def match_kwarg(search, keys):
    for key in keys:
        regex = r'[[{]+' + search.lower()
        if re.search(regex, key.lower()):
            return key
    return None


def sanitise_kwargs(kwargs, repl_kwargs):
    for kw in repl_kwargs:
        # Removes all non character symbols
        new_kw = re.sub('[^\w]', '', repl_kwargs[kw])
        kwargs[new_kw] = kwargs.pop(kw)
    return kwargs


def mode_builder(search_dict, repl_kwargs, *args, **kwargs):
    """
    [] indicates an optional parameter. If no argument is given on the level that has an optional argument then it
    can still be parsed.
    If no [] arguments exist and no fitting arguments fit the current pattern then Parameter error will be raised
    :param args:
     These are arguments that don't require an additional argument, identified by : prefix
     eg. voltage
    :param kwargs:
     These are arguments identified by key name and require an additional parameter, identified by {}
     eg. {range} would be called as kwarg range=1
    :return:
    """
    # Search primary parameters
    # Each level of the mode config can contain only one match otherwise fail
    matches = [x for x in match_params(args, kwargs, search_dict, repl_kwargs) if x]
    if len(matches) > 1:
        req_matches = []
        for match in matches:
            if '[' not in match:
                req_matches.append(match)
        if len(req_matches) > 1:
            raise ParameterError("Conflicting parameters: \n{}".format('\n'.join(matches)))
        matches = req_matches

    if len(matches) == 0:
        # No further recursion
        if required_params(search_dict):
            raise ParameterError("Missing a required key \n{}".format('\n'.join(search_dict)))
        return ''
    ret_string = matches[0]
    # Match the next parameter
    ret_string += mode_builder(search_dict[matches[0]], repl_kwargs, *args, **kwargs)

    # Remove the optional '[]' markers
    ret_string = re.sub('[[\]]', '', ret_string)
    kwargs = sanitise_kwargs(kwargs, repl_kwargs)
    ret_string = ret_string.format(**kwargs)
    return ret_string


def unit_convert(value, min_primary_number, max_primary_number, as_int=False):
    """
    :param value:
    An int or float to convert into a scaled unit
    :param min_primary_number:
    min value acceptable for the number
    :param max_primary_number:
    max value acceptable for the number
    usage:

    >>>unit_convert(100e6, 1, 999)
    '100.0M'
    >>>unit_convert(100e6, 0.1, 99)
    '0.1G'
    >>>unit_convert(100e6, 1, 999, as_int=True)
    '100M'
    """
    for unit, scale in UNIT_SCALE.items():
        if min_primary_number * scale <= value <= max_primary_number * scale:
            new_val = value / scale
            if as_int:
                new_val = int(new_val)
            return "{}{}".format(new_val, unit)


def unit_scale(str_value, accepted_units=UNITS):
    """
    :param str_value:
        A Value to search for a number and the acceptable units to then scale the original number
    :param accepted_units:
        Restricts the units to this sequence or if not parsed will use defaults specified in the UNITS set
    :return:
    """
    # If type is a number, no scaling required
    if type(str_value) in [int, float]:
        return str_value

    # None is the reset type used for validation before parsing to the function generator
    if str_value is None:
        return str_value

    if type(str_value) != str:
        raise InvalidScalarQuantityError(
            "Parsed value {} type {} is not a string or number type".format(str_value, type(str_value)))
    # Match Decimal and Integer Values
    p = re.compile('\d+(\.\d+)?')
    num_match = p.search(str_value)
    if num_match:
        num = float(num_match.group())

        comp = '^ ?({unit_scale})(?=($|{units}))'.format(units='|'.join(accepted_units),
                                                         unit_scale='|'.join(UNIT_SCALE.keys()))
        p = re.compile(comp)
        try:
            m = p.search(str_value[num_match.end():])
        except IndexError:
            return num

        if m:
            scale = re.sub(' ?', '', m.group())
            if scale:
                ret_val = UNIT_SCALE.get(scale, None)
            else:
                ret_val = 1

            if ret_val:
                return num * ret_val
            else:
                raise InvalidScalarQuantityError("Unknown Scalar Quantity: {}".format(m.group()))

        else:
            units = re.sub(' ?', '', str_value[num_match.end():])
            if units in accepted_units or len(units) == 0:
                return num
            raise InvalidScalarQuantityError(
                "Could Not Find Scaling Value for \nnumber {} in \n{}".format(num, str_value))
    else:
        raise InvalidScalarQuantityError("No Valid Numbers Found in {}".format(str_value))


def bits(n, num_bytes=1, num_bits=None, order="MSB"):
    if num_bits is None:
        num_bits = num_bytes * 8
    if n >= 1 << num_bits:
        raise ParameterError("Number {} doesn't fit in {} number of bytes".format(n, num_bytes))
    if order.upper() in "MSB":
        b = 1 << num_bits
        while b > 1:
            b >>= 1
            yield bool(b & n)
    elif order.upper() in "LSB":
        target = 1 << num_bits
        b = 1
        while b < target:
            yield bool(b & n)
            b <<= 1
    else:
        raise ParameterError("Unknown order {} please choose MSB or LSB".format(order))


class ExcThread(threading.Thread):
    exec_info = None

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=True, test_index=None):
        super().__init__(group=group, target=target, name=name,
                         args=args, kwargs=kwargs, daemon=daemon)
        self.test_index = test_index

    def run(self):
        """Method representing the thread's activity.

        The standard run() method invokes the callable object passed to the
        object's constructor as the target argument, if any, with sequential
        and keyword arguments taken from the args and kwargs arguments, respectively.
        """
        try:
            self._target(*self._args, **self._kwargs)
        except BaseException:
            self.exec_info = sys.exc_info()[1]
            # raise
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs

    def stop(self):
        try:
            _async_raise(self.ident, SystemExit)
        except (ValueError, SystemError):
            pass  # System could not find thread. Most likely already killed


def deprecated(func):
    def inner(*args, **kwargs):
        logger.warning("Function is deprecated. Please consider updating api calls")
        return func(*args, **kwargs)

    return inner


class TestList:
    def __init__(self, seq=None):
        self.tests = []
        if seq is None:
            seq = []
        self.tests.extend(seq)

        try:
            doc_string = [line.strip() for line in self.__doc__.splitlines() if line.strip()]
        except:
            self.test_desc = self.__class__.__name__
            self.test_desc_long = ""
        else:
            if doc_string:
                self.test_desc = doc_string[0]
                self.test_desc_long = '\\n'.join(doc_string[1:])

    def __getitem__(self, item):
        return self.tests.__getitem__(item)

    def __contains__(self, item):
        return self.tests.__contains__(item)

    def __setitem__(self, key, value):
        return self.tests.__setitem__(key, value)

    def __delitem__(self, key):
        return self.tests.__delitem__(key)

    def __len__(self):
        return self.tests.__len__()

    def append(self, p_object):
        self.tests.append(p_object)

    def extend(self, iterable):
        self.tests.extend(iterable)

    def insert(self, index, p_object):
        self.tests.insert(index, p_object)

    def index(self, value, start=None, stop=None):
        self.tests.index(value, start, stop)

    def set_up(self):
        """
        This is called at the beginning of each test contained within
        """

    def tear_down(self):
        """
        This is called at the conclusion of each test contained within
        """

    def enter(self):
        """
        This is called when being pushed onto the stack
        """

    def exit(self):
        """
        This s called when being popped from the stack
        """


class TestClass:
    """
    This class is an abstract base class to implement tests
    """
    RT_ABORT = 1  # Abort the whole test sequence
    RT_RETRY = 2  # Automatically retry up to "attempts"
    RT_PROMPT = 3  # Prompt the user; Options are Abort the sequence, retry, or fail and continue
    RT_FAIL = 4  # Automatically fail and move on

    test_desc = None
    test_desc_long = None
    attempts = 1
    tests = []
    retry_type = RT_PROMPT
    retry_exceptions = [BaseException]  # Depreciated
    skip_exceptions = []
    abort_exceptions = [KeyboardInterrupt, AttributeError, NameError]
    skip_on_fail = False

    def __init__(self, skip=False):
        self.skip = skip
        if not self.test_desc:
            try:
                doc_string = [line.strip() for line in self.__doc__.splitlines() if line.strip()]
            except:
                self.test_desc = self.__class__.__name__
                self.test_desc_long = ""
            else:
                if doc_string:
                    self.test_desc = doc_string[0]
                    self.test_desc_long = '\\n'.join(doc_string[1:])

    def set_up(self):
        """
        Optionally override this code that is executed before the test method is called
        """

    def tear_down(self):
        """
        Optionally override this code that is always executed last
        """

    def test(self):
        """
        This method should be overridden with the test code
        This is the test sequence code
        You can explicitly call self.result() to add a test result to the class
        """
