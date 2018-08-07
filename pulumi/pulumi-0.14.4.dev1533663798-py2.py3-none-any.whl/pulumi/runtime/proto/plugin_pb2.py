# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: plugin.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='plugin.proto',
  package='pulumirpc',
  syntax='proto3',
  serialized_pb=_b('\n\x0cplugin.proto\x12\tpulumirpc\"\x1d\n\nPluginInfo\x12\x0f\n\x07version\x18\x01 \x01(\t\"?\n\x10PluginDependency\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04kind\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\tb\x06proto3')
)




_PLUGININFO = _descriptor.Descriptor(
  name='PluginInfo',
  full_name='pulumirpc.PluginInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='pulumirpc.PluginInfo.version', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=27,
  serialized_end=56,
)


_PLUGINDEPENDENCY = _descriptor.Descriptor(
  name='PluginDependency',
  full_name='pulumirpc.PluginDependency',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='pulumirpc.PluginDependency.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='kind', full_name='pulumirpc.PluginDependency.kind', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='version', full_name='pulumirpc.PluginDependency.version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=58,
  serialized_end=121,
)

DESCRIPTOR.message_types_by_name['PluginInfo'] = _PLUGININFO
DESCRIPTOR.message_types_by_name['PluginDependency'] = _PLUGINDEPENDENCY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PluginInfo = _reflection.GeneratedProtocolMessageType('PluginInfo', (_message.Message,), dict(
  DESCRIPTOR = _PLUGININFO,
  __module__ = 'plugin_pb2'
  # @@protoc_insertion_point(class_scope:pulumirpc.PluginInfo)
  ))
_sym_db.RegisterMessage(PluginInfo)

PluginDependency = _reflection.GeneratedProtocolMessageType('PluginDependency', (_message.Message,), dict(
  DESCRIPTOR = _PLUGINDEPENDENCY,
  __module__ = 'plugin_pb2'
  # @@protoc_insertion_point(class_scope:pulumirpc.PluginDependency)
  ))
_sym_db.RegisterMessage(PluginDependency)


# @@protoc_insertion_point(module_scope)
