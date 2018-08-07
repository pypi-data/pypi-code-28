#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import logging

from uamqp import c_uamqp
from uamqp import utils
from uamqp import constants, errors


_logger = logging.getLogger(__name__)


class Message:
    """An AMQP message.

    When sending, depending on the nature of the data,
    different body encoding will be used. If the data is str or bytes,
    a single part DataBody will be sent. If the data is a list or str/bytes,
    a multipart DataBody will be sent. Any other type of list will be sent
    as a SequenceBody, where as any other type of data will be sent as
    a ValueBody. An empty payload will also be sent as a ValueBody.

    :ivar on_send_complete: A custom callback to be run on completion of
     the send operation of this message. The callback must take two parameters,
     a result (of type ~uamqp.constants.MessageSendResult) and an error (of type
     Exception). The error parameter may be None if no error ocurred or the error
     information was undetermined.
    :vartype on_send_complete: callable[~uamqp.constants.MessageSendResult, Exception]

    :param body: The data to send in the message.
    :type body: Any Python data type.
    :param properties: Properties to add to the message.
    :type properties: ~uamqp.message.MessageProperties
    :param application_properties: Service specific application properties.
    :type application_properties: dict
    :param annotations: Service specific message annotations. Keys in the dictionary
     must be ~uamqp.types.AMQPSymbol or ~uamqp.types.AMQPuLong.
    :type annotations: dict
    :param header: The message header.
    :type header: ~uamqp.message.MessageHeader
    :param msg_format: A custom message format. Default is 0.
    :type msg_format: int
    :param message: Internal only. This is used to wrap an existing message
     that has been received from an AMQP service. If specified, all other
     parameters will be ignored.
    :type message: uamqp.c_uamqp.cMessage
    :param settled: Internal only. This is used when wrapping an existing message
     that has been received from an AMQP service. Should only be specified together
     with `message` and is to determine receive-settled mode of the client.
    :type settled: int
    :param encoding: The encoding to use for parameters supplied as strings.
     Default is 'UTF-8'
    :type encoding: str
    """

    def __init__(self,
                 body=None,
                 properties=None,
                 application_properties=None,
                 annotations=None,
                 header=None,
                 msg_format=None,
                 message=None,
                 settler=None,
                 encoding='UTF-8'):
        self.state = constants.MessageState.WaitingToBeSent
        self.idle_time = 0
        self.retries = 0
        self._response = None
        self._settler = None
        self._encoding = encoding
        self.on_send_complete = None
        self.properties = None
        self.application_properties = None
        self.annotations = None
        self.header = None
        self.footer = None
        self.delivery_annotations = None

        if message:
            if settler:
                self.state = constants.MessageState.ReceivedUnsettled
                self._response = None
            else:
                self.state = constants.MessageState.ReceivedSettled
                self._response = errors.MessageAlreadySettled()
            self._settler = settler
            self._parse_message(message)
        else:
            self._message = c_uamqp.create_message()
            if isinstance(body, (bytes, str)):
                self._body = DataBody(self._message)
                self._body.append(body)
            elif isinstance(body, list) and all([isinstance(b, (bytes, str)) for b in body]):
                self._body = DataBody(self._message)
                for value in body:
                    self._body.append(value)
            elif isinstance(body, list):
                self._body = SequenceBody(self._message)
                for value in body:
                    self._body.append(value)
            else:
                self._body = ValueBody(self._message)
                self._body.set(body)
            if msg_format:
                self._message.message_format = msg_format
            self.properties = properties
            self.application_properties = application_properties
            self.annotations = annotations
            self.header = header

    def __str__(self):
        if not self._message:
            return ""
        return str(self._body)

    def _parse_message(self, message):
        """Parse a message received from an AMQP service.

        :param message: The received C message.
        :type message: uamqp.c_uamqp.cMessage
        """
        self._message = message
        body_type = message.body_type
        if body_type == c_uamqp.MessageBodyType.NoneType:
            self._body = None
        elif body_type == c_uamqp.MessageBodyType.DataType:
            self._body = DataBody(self._message)
        elif body_type == c_uamqp.MessageBodyType.SequenceType:
            self._body = SequenceBody(self._message)
        else:
            self._body = ValueBody(self._message)
        _props = self._message.properties
        if _props:
            self.properties = MessageProperties(properties=_props, encoding=self._encoding)
        _header = self._message.header
        if _header:
            self.header = MessageHeader(header=_header)
        _footer = self._message.footer
        if _footer:
            self.footer = _footer.map
        _app_props = self._message.application_properties
        if _app_props:
            self.application_properties = _app_props.map
        _ann = self._message.message_annotations
        if _ann:
            self.annotations = _ann.map
        _delivery_ann = self._message.delivery_annotations
        if _delivery_ann:
            self.delivery_annotations = _delivery_ann.map

    def _can_settle_message(self):
        if self.state not in constants.RECEIVE_STATES:
            raise TypeError("Only received messages can be settled.")
        elif self.settled:
            return False
        return True

    @property
    def settled(self):
        """Whether the message transaction for this message has been completed.
        If this message is to be sent, the message will be `settled=True` once a
        disposition has been received from the service.
        If this message has been received, the message will be `settled=True` once
        a disposition has been sent to the service.

        :rtype: bool
        """
        if self._response:
            return True
        return False

    def get_message_encoded_size(self):
        """Pre-emptively get the size of the message once it has been encoded
        to go over the wire so we can raise an error if the message will be
        rejected for being to large.

        :rtype: int
        """
        if self.state in constants.RECEIVE_STATES:
            # We only need this for messages being sent.
            return None
        # TODO: This no longer calculates the metadata accurately.
        return 0  # c_uamqp.get_encoded_message_size(self._message)

    def get_data(self):
        """Get the body data of the message. The format may vary depending
        on the body type.

        :rtype: generator
        """
        if not self._message or not self._body:
            return None
        return self._body.data

    def gather(self):
        """Return all the messages represented by this object.
        This will always be a list of a single message.

        :rtype: list[~uamqp.message.Message]
        """
        if self.state in constants.RECEIVE_STATES:
            raise TypeError("Only new messages can be gathered.")
        try:
            raise self._response
        except TypeError:
            pass
        return [self]

    def get_message(self):
        """Get the underlying C message from this object.

        :rtype: uamqp.c_uamqp.cMessage
        """
        if not self._message:
            return None
        if self.properties:
            self._message.properties = self.properties.get_properties_obj()
        if self.application_properties:
            if not isinstance(self.application_properties, dict):
                raise TypeError("Application properties must be a dictionary.")
            amqp_props = utils.data_factory(self.application_properties, encoding=self._encoding)
            self._message.application_properties = amqp_props
        if self.annotations:
            if not isinstance(self.annotations, dict):
                raise TypeError("Message annotations must be a dictionary.")
            ann_props = c_uamqp.create_message_annotations(
                utils.data_factory(self.annotations, encoding=self._encoding))
            self._message.message_annotations = ann_props
        if self.header:
            self._message.header = self.header.get_header_obj()
        return self._message

    def accept(self):
        """Send a response disposition to the service to indicate that
        a received message has been accepted. If the client is running in PeekLock
        mode, the service will wait on this disposition. Otherwise it will
        be ignored. Returns `True` is message was accepted, or `False` if the message
        was already settled.

        :rtype: bool
        :raises: TypeError if the message is being sent rather than received.
        """
        if self._can_settle_message():
            self._response = errors.MessageAccepted()
            self._settler(self._response)
            self.state = constants.MessageState.ReceivedSettled
            return True
        return False

    def reject(self, condition=None, description=None):
        """Send a response disposition to the service to indicate that
        a received message has been rejected. If the client is running in PeekLock
        mode, the service will wait on this disposition. Otherwise it will
        be ignored. A rejected message will increment the messages delivery count.
        Returns `True` is message was rejected, or `False` if the message
        was already settled.

        :param condition: The AMQP rejection code. By default this is `amqp:internal-error`.
        :type condition: bytes or str
        :param description: A description/reason to accompany the rejection.
        :type description: bytes or str
        :rtype: bool
        :raises: TypeError if the message is being sent rather than received.
        """
        if self._can_settle_message():
            self._response = errors.MessageRejected(
                condition=condition,
                description=description,
                encoding=self._encoding)
            self._settler(self._response)
            self.state = constants.MessageState.ReceivedSettled
            return True
        return False

    def release(self):
        """Send a response disposition to the service to indicate that
        a received message has been released. If the client is running in PeekLock
        mode, the service will wait on this disposition. Otherwise it will
        be ignored. A released message will not incremenet the messages
        delivery count. Returns `True` is message was released, or `False` if the message
        was already settled.

        :rtype: bool
        :raises: TypeError if the message is being sent rather than received.
        """
        if self._can_settle_message():
            self._response = errors.MessageReleased()
            self._settler(self._response)
            self.state = constants.MessageState.ReceivedSettled
            return True
        return False

    def modify(self, failed, deliverable, annotations=None):
        """Send a response disposition to the service to indicate that
        a received message has been modified. If the client is running in PeekLock
        mode, the service will wait on this disposition. Otherwise it will
        be ignored. Returns `True` is message was released, or `False` if the message
        was already settled.

        :param failed: Whether this delivery of this message failed. This does not
         indicate whether subsequence deliveries of this message would also fail.
        :type failed: bool
        :param deliverable: Whether this message will be deliverable to this client
         on subsequent deliveries - i.e. whether delivery is retryable.
        :type deliverable: bool
        :param annotations: Annotations to attach to response.
        :type annotations: dict
        :rtype: bool
        :raises: TypeError if the message is being sent rather than received.
        """
        if self._can_settle_message():
            self._response = errors.MessageModified(
                failed,
                deliverable,
                annotations=annotations,
                encoding=self._encoding)
            self._settler(self._response)
            self.state = constants.MessageState.ReceivedSettled
            return True
        return False


class BatchMessage(Message):
    """A Batched AMQP message.

    This batch message encodes multiple message bodies into a single message
    to increase through-put over the wire. It requires server-side support
    to unpackage the batched messages and so will not be universally supported.

    :ivar on_send_complete: A custom callback to be run on completion of
     the send operation of this message. The callback must take two parameters,
     a result (of type ~uamqp.constants.MessageSendResult) and an error (of type
     Exception). The error parameter may be None if no error ocurred or the error
     information was undetermined.
    :vartype on_send_complete: callable[~uamqp.constants.MessageSendResult, Exception]
    :ivar batch_format: The is the specific message format to inform the service the
     the body should be interpreted as multiple messages. The value is 0x80013700.
    :vartype batch_format: int
    :ivar max_message_length: The maximum data size in bytes to allow in a single message.
     By default this is 256kb. If sending a single batch message, an error will be raised
     if the supplied data exceeds this maximum. If sending multiple batch messages, this
     value will be used to divide the supplied data between messages.
    :vartype max_message_length: int

    :param data: An iterable source of data, where each value will be considered the
     body of a single message in the batch.
    :type data: iterable
    :param properties: Properties to add to the message. If multiple messages are created
     these properties will be applied to each message.
    :type properties: ~uamqp.message.MessageProperties
    :param application_properties: Service specific application properties. If multiple messages
     are created these properties will be applied to each message.
    :type application_properties: dict
    :param annotations: Service specific message annotations. If multiple messages are created
     these properties will be applied to each message. Keys in the dictionary
     must be ~uamqp.types.AMQPSymbol or ~uamqp.types.AMQPuLong.
    :type annotations: dict
    :param header: The message header. This header will be applied to each message in the batch.
    :type header: ~uamqp.message.MessageHeader
    :param multi_messages: Whether to send the supplied data across multiple messages. If set to
     `False`, all the data will be sent in a single message, and an error raised if the message
     is too large. If set to `True`, the data will automatically be divided across multiple messages
     of an appropriate size. The default is `False`.
    :type multi_messages: bool
    :param encoding: The encoding to use for parameters supplied as strings.
     Default is 'UTF-8'
    :type encoding: str
    :raises: ValueError if data is sent in a single message and that message exceeds the max size.
    """

    batch_format = 0x80013700
    max_message_length = constants.MAX_MESSAGE_LENGTH_BYTES
    _size_buffer = 65000

    def __init__(self,
                 data=None,
                 properties=None,
                 application_properties=None,
                 annotations=None,
                 header=None,
                 multi_messages=False,
                 encoding='UTF-8'):
        # pylint: disable=super-init-not-called
        self._multi_messages = multi_messages
        self._body_gen = data
        self._encoding = encoding
        self.on_send_complete = None
        self.properties = properties
        self.application_properties = application_properties
        self.annotations = annotations
        self.header = header

    def _create_batch_message(self):
        """Create a ~uamqp.message.Message for a value supplied by the data
        generator. Applies all properties and annotations to the message.

        :rtype: ~uamqp.message.Message
        """
        return Message(body=[],
                       properties=self.properties,
                       annotations=self.annotations,
                       msg_format=self.batch_format,
                       header=self.header,
                       encoding=self._encoding)

    def _multi_message_generator(self):
        """Generate multiple ~uamqp.message.Message objects from a single data
        stream that in total may exceed the maximum individual message size.
        Data will be continuously added to a single message until that message
        reaches a max allowable size, at which point it will be yielded and
        a new message will be started.

        :rtype: generator[~uamqp.message.Message]
        """
        while True:
            new_message = self._create_batch_message()
            message_size = new_message.get_message_encoded_size() + self._size_buffer
            body_size = 0
            try:
                for data in self._body_gen:
                    message_segment = []
                    if isinstance(data, str):
                        data = data.encode(self._encoding)
                    batch_data = c_uamqp.create_data(data)
                    c_uamqp.enocde_batch_value(batch_data, message_segment)
                    combined = b"".join(message_segment)
                    body_size += len(combined)
                    if (body_size + message_size) > self.max_message_length:
                        new_message.on_send_complete = self.on_send_complete
                        yield new_message
                        raise StopIteration()
                    else:
                        new_message._body.append(combined)  # pylint: disable=protected-access
            except StopIteration:
                _logger.debug("Sent partial message.")
                continue
            else:
                new_message.on_send_complete = self.on_send_complete
                yield new_message
                _logger.debug("Sent all batched data.")
                break

    def gather(self):
        """Return all the messages represented by this object. This will convert
        the batch data into individual ~uamqp.message.Message objects, which may be one
        or more if multi_messages is set to `True`.

        :rtype: list[~uamqp.message.Message]
        """
        if self._multi_messages:
            return self._multi_message_generator()

        new_message = self._create_batch_message()
        message_size = new_message.get_message_encoded_size() + self._size_buffer
        body_size = 0

        for data in self._body_gen:
            message_segment = []
            if isinstance(data, str):
                data = data.encode(self._encoding)
            batch_data = c_uamqp.create_data(data)
            c_uamqp.enocde_batch_value(batch_data, message_segment)
            combined = b"".join(message_segment)
            body_size += len(combined)
            if (body_size + message_size) > self.max_message_length:
                raise ValueError(
                    "Data set too large for a single message."
                    "Set multi_messages to True to split data across multiple messages.")
            new_message._body.append(combined)  # pylint: disable=protected-access
        new_message.on_send_complete = self.on_send_complete
        return [new_message]


class MessageProperties:
    """Message properties.
    The properties that are actually used will depend on the service implementation.
    Not all received messages will have all properties, and not all properties
    will be utilized on a sent message.

    :ivar message_id: Message-id, if set, uniquely identifies a message within the message system.
     The message producer is usually responsible for setting the message-id in such a way that it
     is assured to be globally unique. A broker MAY discard a message as a duplicate if the value
     of the message-id matches that of a previously received message sent to the same node.
    :vartype message_id: str or bytes, uuid.UUID, ~uamqp.types.AMQPType
    :ivar user_id: The identity of the user responsible for producing the message. The client sets
     this value, and it MAY be authenticated by intermediaries.
    :vartype user_id: str or bytes
    :ivar to: The to field identifies the node that is the intended destination of the message.
     On any given transfer this might not be the node at the receiving end of the link.
    :vartype to: str or bytes
    :ivar subject:
    :vartype subject:
    :ivar reply_to:
    :vartype reply_to:
    :ivar correlation_id:
    :vartype correlation_id:
    :ivar content_type:
    :vartype content_type:
    :ivar content_encoding:
    :vartype content_encoding:
    :ivar absolute_expiry_time:
    :vartype absolute_expiry_time:
    :ivar creation_time:
    :vartype creation_time:
    :ivar group_id:
    :vartype group_id:
    :ivar group_sequence:
    :vartype group_sequence:
    :ivar reply_to_group_id:
    :vartype reply_to_group_id:
    """

    def __init__(self,
                 message_id=None,
                 user_id=None,
                 to=None,
                 subject=None,
                 reply_to=None,
                 correlation_id=None,
                 content_type=None,
                 content_encoding=None,
                 absolute_expiry_time=None,
                 creation_time=None,
                 group_id=None,
                 group_sequence=None,
                 reply_to_group_id=None,
                 properties=None,
                 encoding='UTF-8'):
        self._encoding = encoding
        if properties:
            self._message_id = properties.message_id
            self._user_id = properties.user_id
            self._to = properties.to
            self._subject = properties.subject
            self._reply_to = properties.reply_to
            self._correlation_id = properties.correlation_id
            self._content_type = properties.content_type
            self._content_encoding = properties.content_encoding
            self._absolute_expiry_time = properties.absolute_expiry_time
            self._creation_time = properties.creation_time
            self._group_id = properties.group_id
            self._group_sequence = properties.group_sequence
            self._reply_to_group_id = properties.reply_to_group_id
        else:
            self.message_id = message_id
            self.user_id = user_id
            self.to = to
            self.subject = subject
            self.reply_to = reply_to
            self.correlation_id = correlation_id
            self.content_type = content_type
            self.content_encoding = content_encoding
            self.absolute_expiry_time = absolute_expiry_time
            self.creation_time = creation_time
            self.group_id = group_id
            self.group_sequence = group_sequence
            self.reply_to_group_id = reply_to_group_id

    @property
    def message_id(self):
        if self._message_id:
            return self._message_id.value
        return None

    @message_id.setter
    def message_id(self, value):
        if value is None:
            self._message_id = None
        else:
            self._message_id = utils.data_factory(value, encoding=self._encoding)

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if isinstance(value, str):
            value = value.encode(self._encoding)
        elif value is not None and not isinstance(value, bytes):
            raise TypeError("user_id must be bytes or str.")
        self._user_id = value

    @property
    def to(self):
        if self._to:
            return self._to.value
        return None

    @to.setter
    def to(self, value):
        if value is None:
            self._to = None
        else:
            self._to = utils.data_factory(value, encoding=self._encoding)

    @property
    def subject(self):
        if self._subject is not None:
            return self._subject.value
        return None

    @subject.setter
    def subject(self, value):
        if value is None:
            self._subject = None
        else:
            self._subject = utils.data_factory(value, encoding=self._encoding)

    @property
    def reply_to(self):
        if self._reply_to is not None:
            return self._reply_to.value
        return None

    @reply_to.setter
    def reply_to(self, value):
        if value is None:
            self._reply_to = None
        else:
            self._reply_to = utils.data_factory(value, encoding=self._encoding)

    @property
    def correlation_id(self):
        if self._correlation_id is not None:
            return self._correlation_id.value
        return None

    @correlation_id.setter
    def correlation_id(self, value):
        if value is None:
            self._correlation_id = None
        else:
            self._correlation_id = utils.data_factory(value, encoding=self._encoding)

    @property
    def content_type(self):
        if self._content_type is not None:
            return self._content_type.value
        return None

    @content_type.setter
    def content_type(self, value):
        if value is None:
            self._content_type = None
        else:
            self._content_type = utils.data_factory(value, encoding=self._encoding)

    @property
    def content_encoding(self):
        if self._content_encoding is not None:
            return self._content_encoding.value
        return None

    @content_encoding.setter
    def content_encoding(self, value):
        if value is None:
            self._content_encoding = None
        else:
            self._content_encoding = utils.data_factory(value, encoding=self._encoding)

    @property
    def absolute_expiry_time(self):
        if self._absolute_expiry_time is not None:
            return self._absolute_expiry_time.value
        return None

    @absolute_expiry_time.setter
    def absolute_expiry_time(self, value):
        if value is None:
            self._absolute_expiry_time = None
        else:
            self._absolute_expiry_time = utils.data_factory(value, encoding=self._encoding)

    @property
    def creation_time(self):
        if self._creation_time is not None:
            return self._creation_time.value
        return None

    @creation_time.setter
    def creation_time(self, value):
        if value is None:
            self._creation_time = None
        else:
            self._creation_time = utils.data_factory(value, encoding=self._encoding)

    @property
    def group_id(self):
        return self._group_id

    @group_id.setter
    def group_id(self, value):
        self._group_id = value

    @property
    def group_sequence(self):
        if self._group_sequence is not None:
            return self._group_sequence.value
        return None

    @group_sequence.setter
    def group_sequence(self, value):
        if value is None:
            self._group_sequence = None
        else:
            self._group_sequence = utils.data_factory(value, encoding=self._encoding)

    @property
    def reply_to_group_id(self):
        if self._reply_to_group_id is not None:
            return self._reply_to_group_id.value
        return None

    @reply_to_group_id.setter
    def reply_to_group_id(self, value):
        if value is None:
            self._reply_to_group_id = None
        else:
            self._reply_to_group_id = utils.data_factory(value, encoding=self._encoding)

    def _set_attr(self, attr, properties):
        attr_value = getattr(self, "_" + attr)
        if attr_value is not None:
            setattr(properties, attr, attr_value)

    def get_properties_obj(self):
        properties = c_uamqp.cProperties()
        self._set_attr('message_id', properties)
        self._set_attr('user_id', properties)
        self._set_attr('to', properties)
        self._set_attr('subject', properties)
        self._set_attr('reply_to', properties)
        self._set_attr('correlation_id', properties)
        self._set_attr('content_type', properties)
        self._set_attr('content_encoding', properties)
        self._set_attr('absolute_expiry_time', properties)
        self._set_attr('creation_time', properties)
        self._set_attr('group_id', properties)
        self._set_attr('group_sequence', properties)
        self._set_attr('reply_to_group_id', properties)
        return properties


class MessageBody:
    """Base class for an AMQP message body. This should
    not be used directly.
    """

    def __init__(self, c_message, encoding='UTF-8'):
        self._message = c_message
        self._encoding = encoding

    def __str__(self):
        if self.type == c_uamqp.MessageBodyType.NoneType:
            return ""
        return str(self.data)

    @property
    def type(self):
        return self._message.body_type

    @property
    def data(self):
        raise NotImplementedError("Only MessageBody subclasses have data.")


class DataBody(MessageBody):
    """An AMQP message body of type Data. This represents
    a list of bytes sections.

    :ivar type: The body type. This should always be DataType
    :vartype type: uamqp.c_uamqp.MessageBodyType
    :ivar data: The data contained in the message body. This returns
     a generator to iterate over each section in the body, where
     each section will be a byte string.
    :vartype data: generator[bytes]
    """

    def __str__(self):
        return "".join(d.decode(self._encoding) for d in self.data)

    def __len__(self):
        return self._message.count_body_data()

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError("Index is out of range.")
        data = self._message.get_body_data(index)
        return data.value

    def append(self, data):
        """Addend a section to the body.

        :param data: The data to append.
        :type data: str or bytes.
        """
        if isinstance(data, str):
            self._message.add_body_data(data.encode(self._encoding))
        elif isinstance(data, bytes):
            self._message.add_body_data(data)

    @property
    def data(self):
        for i in range(len(self)):
            yield self._message.get_body_data(i)


class SequenceBody(MessageBody):
    """An AMQP message body of type Sequence. This represents
    a list of encoded objects.

    :ivar type: The body type. This should always be SequenceType
    :vartype type: uamqp.c_uamqp.MessageBodyType
    :ivar data: The data contained in the message body. This returns
     a generator to iterate over each item in the body.
    :vartype data: generator
    """

    def __len__(self):
        return self._message.count_body_sequence()

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError("Index is out of range.")
        data = self._message.get_body_sequence(index)
        return data.value

    def append(self, value):
        """Addend an item to the body. This can be any
        Python data type and it will be automatically encoded
        into an AMQP type. If a specific AMQP type is required, a
        ~uamqp.types.AMQPType can be used.

        :param data: The data to append.
        :type data: ~uamqp.types.AMQPType
        """
        value = utils.data_factory(value, encoding=self._encoding)
        self._message.add_body_sequence(value)

    @property
    def data(self):
        for i in range(len(self)):  # pylint: disable=consider-using-enumerate
            yield self[i]


class ValueBody(MessageBody):
    """An AMQP message body of type Value. This represents
    a single encoded object.

    :ivar type: The body type. This should always be ValueType
    :vartype type: uamqp.c_uamqp.MessageBodyType
    :ivar data: The data contained in the message body. The value
     of the encoded object
    :vartype data: object
    """

    def set(self, value):
        """Set a value as the message body. This can be any
        Python data type and it will be automatically encoded
        into an AMQP type. If a specific AMQP type is required, a
        ~uamqp.types.AMQPType can be used.

        :param data: The data to send in the body.
        :type data: ~uamqp.types.AMQPType
        """
        value = utils.data_factory(value)
        self._message.set_body_value(value)

    @property
    def data(self):
        _value = self._message.get_body_value()
        if _value:
            return _value.value
        return None


class MessageHeader:
    """The Message header. This is only used on received message, and not
    set on messages being sent. The properties set on any given message
    will depend on the Service and not all messages will have all properties.

    :ivar delivery_count: The number of unsuccessful previous attempts to deliver
     this message. If this value is non-zero it can be taken as an indication that the
     delivery might be a duplicate. On first delivery, the value is zero. It is
     incremented upon an outcome being settled at the sender, according to rules
     defined for each outcome.
    :vartype delivery_count: int
    :ivar time_to_live: Duration in milliseconds for which the message is to be considered "live".
     If this is set then a message expiration time will be computed based on the time of arrival
     at an intermediary. Messages that live longer than their expiration time will be discarded
     (or dead lettered). When a message is transmitted by an intermediary that was received
     with a ttl, the transmitted message's header SHOULD contain a ttl that is computed as the
     difference between the current time and the formerly computed message expiration time,
     i.e., the reduced ttl, so that messages will eventually die if they end up in a delivery loop.
    :vartype time_to_live: int
    :ivar durable: Durable messages MUST NOT be lost even if an intermediary is unexpectedly terminated
     and restarted. A target which is not capable of fulfilling this guarantee MUST NOT accept messages
     where the durable header is set to `True`: if the source allows the rejected outcome then the
     message SHOULD be rejected with the precondition-failed error, otherwise the link MUST be detached
     by the receiver with the same error.
    :vartype durable: bool
    :ivar first_acquirer: If this value is `True`, then this message has not been acquired
     by any other link. If this value is `False`, then this message MAY have previously
     been acquired by another link or links.
    :vartype first_acquirer: bool
    :ivar priority: This field contains the relative message priority. Higher numbers indicate higher
     priority messages. Messages with higher priorities MAY be delivered before those with lower priorities.
    :vartype priority: int

    :param header: Internal only. This is used to wrap an existing message header
     that has been received from an AMQP service.
    :type header: uamqp.c_uamqp.cHeader
    """

    def __init__(self, header=None):
        self.delivery_count = None
        self.time_to_live = None
        self.first_acquirer = None
        self.durable = None
        self.priority = None
        if header:
            self.delivery_count = header.delivery_count
            self.time_to_live = header.time_to_live
            self.first_acquirer = header.first_acquirer
            self.durable = header.durable
            self.priority = header.priority

    def get_header_obj(self):
        header = c_uamqp.create_header()
        if self.delivery_count is not None:
            header.delivery_count = self.delivery_count
        if self.time_to_live is not None:
            header.time_to_live = self.time_to_live
        if self.first_acquirer is not None:
            header.first_acquirer = self.first_acquirer
        if self.durable is not None:
            header.durable = self.durable
        if self.priority is not None:
            header.priority = self.priority
        return header
