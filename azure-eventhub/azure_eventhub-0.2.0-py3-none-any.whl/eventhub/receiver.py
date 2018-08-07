# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import uuid

from uamqp import types, errors
from uamqp import ReceiveClient, Source

from azure.eventhub.common import EventHubError, EventData, _error_handler


class Receiver:
    """
    Implements a Receiver.
    """
    timeout = 0
    _epoch = b'com.microsoft:epoch'

    def __init__(self, client, source, offset=None, prefetch=300, epoch=None, keep_alive=None, auto_reconnect=True):
        """
        Instantiate a receiver.

        :param client: The parent EventHubClient.
        :type client: ~azure.eventhub.client.EventHubClient
        :param source: The source EventHub from which to receive events.
        :type source: str
        :param prefetch: The number of events to prefetch from the service
         for processing. Default is 300.
        :type prefetch: int
        :param epoch: An optional epoch value.
        :type epoch: int
        """
        self.client = client
        self.source = source
        self.offset = offset
        self.prefetch = prefetch
        self.epoch = epoch
        self.keep_alive = keep_alive
        self.auto_reconnect = auto_reconnect
        self.retry_policy = errors.ErrorPolicy(max_retries=3, on_error=_error_handler)
        self.properties = None
        self.redirected = None
        self.error = None
        partition = self.source.split('/')[-1]
        self.name = "EHReceiver-{}-partition{}".format(uuid.uuid4(), partition)
        source = Source(self.source)
        if self.offset is not None:
            source.set_filter(self.offset.selector())
        if epoch:
            self.properties = {types.AMQPSymbol(self._epoch): types.AMQPLong(int(epoch))}
        self._handler = ReceiveClient(
            source,
            auth=self.client.get_auth(),
            debug=self.client.debug,
            prefetch=self.prefetch,
            link_properties=self.properties,
            timeout=self.timeout,
            error_policy=self.retry_policy,
            keep_alive_interval=self.keep_alive,
            client_name=self.name,
            properties=self.client.create_properties())

    def open(self):
        """
        Open the Receiver using the supplied conneciton.
        If the handler has previously been redirected, the redirect
        context will be used to create a new handler before opening it.

        :param connection: The underlying client shared connection.
        :type: connection: ~uamqp.connection.Connection
        """
        # pylint: disable=protected-access
        if self.redirected:
            self.source = self.redirected.address
            source = Source(self.source)
            if self.offset is not None:
                source.set_filter(self.offset.selector())
            alt_creds = {
                "username": self.client._auth_config.get("iot_username"),
                "password":self.client._auth_config.get("iot_password")}
            self._handler = ReceiveClient(
                source,
                auth=self.client.get_auth(**alt_creds),
                debug=self.client.debug,
                prefetch=self.prefetch,
                link_properties=self.properties,
                timeout=self.timeout,
                error_policy=self.retry_policy,
                keep_alive_interval=self.keep_alive,
                client_name=self.name,
                properties=self.client.create_properties())
        self._handler.open()
        while not self.has_started():
            self._handler._connection.work()

    def reconnect(self):
        """If the Receiver was disconnected from the service with
        a retryable error - attempt to reconnect."""
        # pylint: disable=protected-access
        alt_creds = {
            "username": self.client._auth_config.get("iot_username"),
            "password":self.client._auth_config.get("iot_password")}
        self._handler.close()
        source = Source(self.source)
        if self.offset is not None:
            source.set_filter(self.offset.selector())
        self._handler = ReceiveClient(
            source,
            auth=self.client.get_auth(**alt_creds),
            debug=self.client.debug,
            prefetch=self.prefetch,
            link_properties=self.properties,
            timeout=self.timeout,
            error_policy=self.retry_policy,
            keep_alive_interval=self.keep_alive,
            client_name=self.name,
            properties=self.client.create_properties())
        self._handler.open()
        while not self.has_started():
            self._handler._connection.work()

    def get_handler_state(self):
        """
        Get the state of the underlying handler with regards to start
        up processes.

        :rtype: ~uamqp.constants.MessageReceiverState
        """
        # pylint: disable=protected-access
        return self._handler._message_receiver.get_state()

    def has_started(self):
        """
        Whether the handler has completed all start up processes such as
        establishing the connection, session, link and authentication, and
        is not ready to process messages.

        :rtype: bool
        """
        # pylint: disable=protected-access
        timeout = False
        auth_in_progress = False
        if self._handler._connection.cbs:
            timeout, auth_in_progress = self._handler._auth.handle_token()
        if timeout:
            raise EventHubError("Authorization timeout.")
        elif auth_in_progress:
            return False
        elif not self._handler._client_ready():
            return False
        else:
            return True

    def close(self, exception=None):
        """
        Close down the handler. If the handler has already closed,
        this will be a no op. An optional exception can be passed in to
        indicate that the handler was shutdown due to error.

        :param exception: An optional exception if the handler is closing
         due to an error.
        :type exception: Exception
        """
        if self.error:
            return
        elif isinstance(exception, errors.LinkRedirect):
            self.redirected = exception
        elif isinstance(exception, EventHubError):
            self.error = exception
        elif exception:
            self.error = EventHubError(str(exception))
        else:
            self.error = EventHubError("This receive handler is now closed.")
        self._handler.close()

    @property
    def queue_size(self):
        """
        The current size of the unprocessed Event queue.

        :rtype: int
        """
        # pylint: disable=protected-access
        if self._handler._received_messages:
            return self._handler._received_messages.qsize()
        return 0

    def receive(self, max_batch_size=None, timeout=None):
        """
        Receive events from the EventHub.

        :param max_batch_size: Receive a batch of events. Batch size will
         be up to the maximum specified, but will return as soon as service
         returns no new events. If combined with a timeout and no events are
         retrieve before the time, the result will be empty. If no batch
         size is supplied, the prefetch size will be the maximum.
        :type max_batch_size: int
        :rtype: list[~azure.eventhub.common.EventData]
        """
        if self.error:
            raise self.error
        data_batch = []
        try:
            timeout_ms = 1000 * timeout if timeout else 0
            message_batch = self._handler.receive_message_batch(
                max_batch_size=max_batch_size,
                timeout=timeout_ms)
            for message in message_batch:
                event_data = EventData(message=message)
                self.offset = event_data.offset
                data_batch.append(event_data)
            return data_batch
        except (errors.LinkDetach, errors.ConnectionClose) as shutdown:
            if shutdown.action.retry and self.auto_reconnect:
                self.reconnect()
                return data_batch
            else:
                error = EventHubError(str(shutdown), shutdown)
                self.close(exception=error)
                raise error
        except errors.MessageHandlerError as shutdown:
            if self.auto_reconnect:
                self.reconnect()
                return data_batch
            else:
                error = EventHubError(str(shutdown), shutdown)
                self.close(exception=error)
                raise error
        except Exception as e:
            error = EventHubError("Receive failed: {}".format(e))
            self.close(exception=error)
            raise error
