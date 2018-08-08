#
# Autogenerated by Thrift Compiler (0.11.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys
import koverse.thriftgen.ttypes
import koverse.thriftgen.security.ttypes
import koverse.thriftgen.dataflow.ttypes
import koverse.thriftgen.collection.ttypes

from thrift.transport import TTransport
all_structs = []


class TPySparkTransformJobConfig(object):
    """
    Attributes:
     - sparkMaster
     - jobName
     - rddConfs
     - params
     - outputDatasetName
     - outputVersionedDatasetId
     - schemas
    """


    def __init__(self, sparkMaster=None, jobName=None, rddConfs=None, params=None, outputDatasetName=None, outputVersionedDatasetId=None, schemas=None,):
        self.sparkMaster = sparkMaster
        self.jobName = jobName
        self.rddConfs = rddConfs
        self.params = params
        self.outputDatasetName = outputDatasetName
        self.outputVersionedDatasetId = outputVersionedDatasetId
        self.schemas = schemas

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.sparkMaster = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.jobName = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.MAP:
                    self.rddConfs = {}
                    (_ktype1, _vtype2, _size0) = iprot.readMapBegin()
                    for _i4 in range(_size0):
                        _key5 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        _val6 = {}
                        (_ktype8, _vtype9, _size7) = iprot.readMapBegin()
                        for _i11 in range(_size7):
                            _key12 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                            _val13 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                            _val6[_key12] = _val13
                        iprot.readMapEnd()
                        self.rddConfs[_key5] = _val6
                    iprot.readMapEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.MAP:
                    self.params = {}
                    (_ktype15, _vtype16, _size14) = iprot.readMapBegin()
                    for _i18 in range(_size14):
                        _key19 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        _val20 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.params[_key19] = _val20
                    iprot.readMapEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.STRING:
                    self.outputDatasetName = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.STRING:
                    self.outputVersionedDatasetId = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 7:
                if ftype == TType.MAP:
                    self.schemas = {}
                    (_ktype22, _vtype23, _size21) = iprot.readMapBegin()
                    for _i25 in range(_size21):
                        _key26 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        _val27 = koverse.thriftgen.collection.ttypes.TFlatCollectionSchema()
                        _val27.read(iprot)
                        self.schemas[_key26] = _val27
                    iprot.readMapEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('TPySparkTransformJobConfig')
        if self.sparkMaster is not None:
            oprot.writeFieldBegin('sparkMaster', TType.STRING, 1)
            oprot.writeString(self.sparkMaster.encode('utf-8') if sys.version_info[0] == 2 else self.sparkMaster)
            oprot.writeFieldEnd()
        if self.jobName is not None:
            oprot.writeFieldBegin('jobName', TType.STRING, 2)
            oprot.writeString(self.jobName.encode('utf-8') if sys.version_info[0] == 2 else self.jobName)
            oprot.writeFieldEnd()
        if self.rddConfs is not None:
            oprot.writeFieldBegin('rddConfs', TType.MAP, 3)
            oprot.writeMapBegin(TType.STRING, TType.MAP, len(self.rddConfs))
            for kiter28, viter29 in self.rddConfs.items():
                oprot.writeString(kiter28.encode('utf-8') if sys.version_info[0] == 2 else kiter28)
                oprot.writeMapBegin(TType.STRING, TType.STRING, len(viter29))
                for kiter30, viter31 in viter29.items():
                    oprot.writeString(kiter30.encode('utf-8') if sys.version_info[0] == 2 else kiter30)
                    oprot.writeString(viter31.encode('utf-8') if sys.version_info[0] == 2 else viter31)
                oprot.writeMapEnd()
            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.params is not None:
            oprot.writeFieldBegin('params', TType.MAP, 4)
            oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.params))
            for kiter32, viter33 in self.params.items():
                oprot.writeString(kiter32.encode('utf-8') if sys.version_info[0] == 2 else kiter32)
                oprot.writeString(viter33.encode('utf-8') if sys.version_info[0] == 2 else viter33)
            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        if self.outputDatasetName is not None:
            oprot.writeFieldBegin('outputDatasetName', TType.STRING, 5)
            oprot.writeString(self.outputDatasetName.encode('utf-8') if sys.version_info[0] == 2 else self.outputDatasetName)
            oprot.writeFieldEnd()
        if self.outputVersionedDatasetId is not None:
            oprot.writeFieldBegin('outputVersionedDatasetId', TType.STRING, 6)
            oprot.writeString(self.outputVersionedDatasetId.encode('utf-8') if sys.version_info[0] == 2 else self.outputVersionedDatasetId)
            oprot.writeFieldEnd()
        if self.schemas is not None:
            oprot.writeFieldBegin('schemas', TType.MAP, 7)
            oprot.writeMapBegin(TType.STRING, TType.STRUCT, len(self.schemas))
            for kiter34, viter35 in self.schemas.items():
                oprot.writeString(kiter34.encode('utf-8') if sys.version_info[0] == 2 else kiter34)
                viter35.write(oprot)
            oprot.writeMapEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(TPySparkTransformJobConfig)
TPySparkTransformJobConfig.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'sparkMaster', 'UTF8', None, ),  # 1
    (2, TType.STRING, 'jobName', 'UTF8', None, ),  # 2
    (3, TType.MAP, 'rddConfs', (TType.STRING, 'UTF8', TType.MAP, (TType.STRING, 'UTF8', TType.STRING, 'UTF8', False), False), None, ),  # 3
    (4, TType.MAP, 'params', (TType.STRING, 'UTF8', TType.STRING, 'UTF8', False), None, ),  # 4
    (5, TType.STRING, 'outputDatasetName', 'UTF8', None, ),  # 5
    (6, TType.STRING, 'outputVersionedDatasetId', 'UTF8', None, ),  # 6
    (7, TType.MAP, 'schemas', (TType.STRING, 'UTF8', TType.STRUCT, [koverse.thriftgen.collection.ttypes.TFlatCollectionSchema, None], False), None, ),  # 7
)
fix_spec(all_structs)
del all_structs
