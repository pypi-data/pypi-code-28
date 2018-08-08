from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.protos.service_pb2 import Metric as ProtoMetric


class Metric(_MLflowObject):
    """
    Metric object for python client. Backend stores will hydrate this object in APIs.
    """

    def __init__(self, key, value, timestamp):
        self._key = key
        self._value = value
        self._timestamp = timestamp

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @property
    def timestamp(self):
        return self._timestamp

    def to_proto(self):
        metric = ProtoMetric()
        metric.key = self.key
        metric.value = self.value
        metric.timestamp = self.timestamp
        return metric

    @classmethod
    def from_proto(cls, proto):
        return cls(proto.key, proto.value, proto.timestamp)

    @classmethod
    def _properties(cls):
        # TODO: Hard coding this list of props for now. There has to be a clearer way...
        return ["key", "value", "timestamp"]
