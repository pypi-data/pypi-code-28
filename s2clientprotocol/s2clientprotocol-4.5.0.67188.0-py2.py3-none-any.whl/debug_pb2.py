# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: s2clientprotocol/debug.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from s2clientprotocol import common_pb2 as s2clientprotocol_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='s2clientprotocol/debug.proto',
  package='SC2APIProtocol',
  syntax='proto2',
  serialized_pb=_b('\n\x1cs2clientprotocol/debug.proto\x12\x0eSC2APIProtocol\x1a\x1ds2clientprotocol/common.proto\"\xbb\x03\n\x0c\x44\x65\x62ugCommand\x12)\n\x04\x64raw\x18\x01 \x01(\x0b\x32\x19.SC2APIProtocol.DebugDrawH\x00\x12\x34\n\ngame_state\x18\x02 \x01(\x0e\x32\x1e.SC2APIProtocol.DebugGameStateH\x00\x12\x36\n\x0b\x63reate_unit\x18\x03 \x01(\x0b\x32\x1f.SC2APIProtocol.DebugCreateUnitH\x00\x12\x32\n\tkill_unit\x18\x04 \x01(\x0b\x32\x1d.SC2APIProtocol.DebugKillUnitH\x00\x12\x38\n\x0ctest_process\x18\x05 \x01(\x0b\x32 .SC2APIProtocol.DebugTestProcessH\x00\x12.\n\x05score\x18\x06 \x01(\x0b\x32\x1d.SC2APIProtocol.DebugSetScoreH\x00\x12\x30\n\x08\x65nd_game\x18\x07 \x01(\x0b\x32\x1c.SC2APIProtocol.DebugEndGameH\x00\x12\x37\n\nunit_value\x18\x08 \x01(\x0b\x32!.SC2APIProtocol.DebugSetUnitValueH\x00\x42\t\n\x07\x63ommand\"\xb5\x01\n\tDebugDraw\x12\'\n\x04text\x18\x01 \x03(\x0b\x32\x19.SC2APIProtocol.DebugText\x12(\n\x05lines\x18\x02 \x03(\x0b\x32\x19.SC2APIProtocol.DebugLine\x12\'\n\x05\x62oxes\x18\x03 \x03(\x0b\x32\x18.SC2APIProtocol.DebugBox\x12,\n\x07spheres\x18\x04 \x03(\x0b\x32\x1b.SC2APIProtocol.DebugSphere\"L\n\x04Line\x12!\n\x02p0\x18\x01 \x01(\x0b\x32\x15.SC2APIProtocol.Point\x12!\n\x02p1\x18\x02 \x01(\x0b\x32\x15.SC2APIProtocol.Point\"(\n\x05\x43olor\x12\t\n\x01r\x18\x01 \x01(\r\x12\t\n\x01g\x18\x02 \x01(\r\x12\t\n\x01\x62\x18\x03 \x01(\r\"\xa3\x01\n\tDebugText\x12$\n\x05\x63olor\x18\x01 \x01(\x0b\x32\x15.SC2APIProtocol.Color\x12\x0c\n\x04text\x18\x02 \x01(\t\x12*\n\x0bvirtual_pos\x18\x03 \x01(\x0b\x32\x15.SC2APIProtocol.Point\x12(\n\tworld_pos\x18\x04 \x01(\x0b\x32\x15.SC2APIProtocol.Point\x12\x0c\n\x04size\x18\x05 \x01(\r\"U\n\tDebugLine\x12$\n\x05\x63olor\x18\x01 \x01(\x0b\x32\x15.SC2APIProtocol.Color\x12\"\n\x04line\x18\x02 \x01(\x0b\x32\x14.SC2APIProtocol.Line\"x\n\x08\x44\x65\x62ugBox\x12$\n\x05\x63olor\x18\x01 \x01(\x0b\x32\x15.SC2APIProtocol.Color\x12\"\n\x03min\x18\x02 \x01(\x0b\x32\x15.SC2APIProtocol.Point\x12\"\n\x03max\x18\x03 \x01(\x0b\x32\x15.SC2APIProtocol.Point\"`\n\x0b\x44\x65\x62ugSphere\x12$\n\x05\x63olor\x18\x01 \x01(\x0b\x32\x15.SC2APIProtocol.Color\x12 \n\x01p\x18\x02 \x01(\x0b\x32\x15.SC2APIProtocol.Point\x12\t\n\x01r\x18\x03 \x01(\x02\"k\n\x0f\x44\x65\x62ugCreateUnit\x12\x11\n\tunit_type\x18\x01 \x01(\r\x12\r\n\x05owner\x18\x02 \x01(\x05\x12$\n\x03pos\x18\x03 \x01(\x0b\x32\x17.SC2APIProtocol.Point2D\x12\x10\n\x08quantity\x18\x04 \x01(\r\"\x1c\n\rDebugKillUnit\x12\x0b\n\x03tag\x18\x01 \x03(\x04\"\x80\x01\n\x10\x44\x65\x62ugTestProcess\x12\x33\n\x04test\x18\x01 \x01(\x0e\x32%.SC2APIProtocol.DebugTestProcess.Test\x12\x10\n\x08\x64\x65lay_ms\x18\x02 \x01(\x05\"%\n\x04Test\x12\x08\n\x04hang\x10\x01\x12\t\n\x05\x63rash\x10\x02\x12\x08\n\x04\x65xit\x10\x03\"\x1e\n\rDebugSetScore\x12\r\n\x05score\x18\x01 \x01(\x02\"z\n\x0c\x44\x65\x62ugEndGame\x12:\n\nend_result\x18\x01 \x01(\x0e\x32&.SC2APIProtocol.DebugEndGame.EndResult\".\n\tEndResult\x12\r\n\tSurrender\x10\x01\x12\x12\n\x0e\x44\x65\x63lareVictory\x10\x02\"\xa5\x01\n\x11\x44\x65\x62ugSetUnitValue\x12?\n\nunit_value\x18\x01 \x01(\x0e\x32+.SC2APIProtocol.DebugSetUnitValue.UnitValue\x12\r\n\x05value\x18\x02 \x01(\x02\x12\x10\n\x08unit_tag\x18\x03 \x01(\x04\".\n\tUnitValue\x12\n\n\x06\x45nergy\x10\x01\x12\x08\n\x04Life\x10\x02\x12\x0b\n\x07Shields\x10\x03*\xb2\x01\n\x0e\x44\x65\x62ugGameState\x12\x0c\n\x08show_map\x10\x01\x12\x11\n\rcontrol_enemy\x10\x02\x12\x08\n\x04\x66ood\x10\x03\x12\x08\n\x04\x66ree\x10\x04\x12\x11\n\rall_resources\x10\x05\x12\x07\n\x03god\x10\x06\x12\x0c\n\x08minerals\x10\x07\x12\x07\n\x03gas\x10\x08\x12\x0c\n\x08\x63ooldown\x10\t\x12\r\n\ttech_tree\x10\n\x12\x0b\n\x07upgrade\x10\x0b\x12\x0e\n\nfast_build\x10\x0c')
  ,
  dependencies=[s2clientprotocol_dot_common__pb2.DESCRIPTOR,])

_DEBUGGAMESTATE = _descriptor.EnumDescriptor(
  name='DebugGameState',
  full_name='SC2APIProtocol.DebugGameState',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='show_map', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='control_enemy', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='food', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='free', index=3, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='all_resources', index=4, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='god', index=5, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='minerals', index=6, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='gas', index=7, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='cooldown', index=8, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='tech_tree', index=9, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='upgrade', index=10, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='fast_build', index=11, number=12,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1897,
  serialized_end=2075,
)
_sym_db.RegisterEnumDescriptor(_DEBUGGAMESTATE)

DebugGameState = enum_type_wrapper.EnumTypeWrapper(_DEBUGGAMESTATE)
show_map = 1
control_enemy = 2
food = 3
free = 4
all_resources = 5
god = 6
minerals = 7
gas = 8
cooldown = 9
tech_tree = 10
upgrade = 11
fast_build = 12


_DEBUGTESTPROCESS_TEST = _descriptor.EnumDescriptor(
  name='Test',
  full_name='SC2APIProtocol.DebugTestProcess.Test',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='hang', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='crash', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='exit', index=2, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1533,
  serialized_end=1570,
)
_sym_db.RegisterEnumDescriptor(_DEBUGTESTPROCESS_TEST)

_DEBUGENDGAME_ENDRESULT = _descriptor.EnumDescriptor(
  name='EndResult',
  full_name='SC2APIProtocol.DebugEndGame.EndResult',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Surrender', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DeclareVictory', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1680,
  serialized_end=1726,
)
_sym_db.RegisterEnumDescriptor(_DEBUGENDGAME_ENDRESULT)

_DEBUGSETUNITVALUE_UNITVALUE = _descriptor.EnumDescriptor(
  name='UnitValue',
  full_name='SC2APIProtocol.DebugSetUnitValue.UnitValue',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Energy', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Life', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Shields', index=2, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1848,
  serialized_end=1894,
)
_sym_db.RegisterEnumDescriptor(_DEBUGSETUNITVALUE_UNITVALUE)


_DEBUGCOMMAND = _descriptor.Descriptor(
  name='DebugCommand',
  full_name='SC2APIProtocol.DebugCommand',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='draw', full_name='SC2APIProtocol.DebugCommand.draw', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='game_state', full_name='SC2APIProtocol.DebugCommand.game_state', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='create_unit', full_name='SC2APIProtocol.DebugCommand.create_unit', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='kill_unit', full_name='SC2APIProtocol.DebugCommand.kill_unit', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='test_process', full_name='SC2APIProtocol.DebugCommand.test_process', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='score', full_name='SC2APIProtocol.DebugCommand.score', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='end_game', full_name='SC2APIProtocol.DebugCommand.end_game', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='unit_value', full_name='SC2APIProtocol.DebugCommand.unit_value', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='command', full_name='SC2APIProtocol.DebugCommand.command',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=80,
  serialized_end=523,
)


_DEBUGDRAW = _descriptor.Descriptor(
  name='DebugDraw',
  full_name='SC2APIProtocol.DebugDraw',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='SC2APIProtocol.DebugDraw.text', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lines', full_name='SC2APIProtocol.DebugDraw.lines', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='boxes', full_name='SC2APIProtocol.DebugDraw.boxes', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='spheres', full_name='SC2APIProtocol.DebugDraw.spheres', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=526,
  serialized_end=707,
)


_LINE = _descriptor.Descriptor(
  name='Line',
  full_name='SC2APIProtocol.Line',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='p0', full_name='SC2APIProtocol.Line.p0', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='p1', full_name='SC2APIProtocol.Line.p1', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=709,
  serialized_end=785,
)


_COLOR = _descriptor.Descriptor(
  name='Color',
  full_name='SC2APIProtocol.Color',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='r', full_name='SC2APIProtocol.Color.r', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='g', full_name='SC2APIProtocol.Color.g', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='b', full_name='SC2APIProtocol.Color.b', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=787,
  serialized_end=827,
)


_DEBUGTEXT = _descriptor.Descriptor(
  name='DebugText',
  full_name='SC2APIProtocol.DebugText',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='color', full_name='SC2APIProtocol.DebugText.color', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='text', full_name='SC2APIProtocol.DebugText.text', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='virtual_pos', full_name='SC2APIProtocol.DebugText.virtual_pos', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='world_pos', full_name='SC2APIProtocol.DebugText.world_pos', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='size', full_name='SC2APIProtocol.DebugText.size', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=830,
  serialized_end=993,
)


_DEBUGLINE = _descriptor.Descriptor(
  name='DebugLine',
  full_name='SC2APIProtocol.DebugLine',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='color', full_name='SC2APIProtocol.DebugLine.color', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='line', full_name='SC2APIProtocol.DebugLine.line', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=995,
  serialized_end=1080,
)


_DEBUGBOX = _descriptor.Descriptor(
  name='DebugBox',
  full_name='SC2APIProtocol.DebugBox',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='color', full_name='SC2APIProtocol.DebugBox.color', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='min', full_name='SC2APIProtocol.DebugBox.min', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max', full_name='SC2APIProtocol.DebugBox.max', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1082,
  serialized_end=1202,
)


_DEBUGSPHERE = _descriptor.Descriptor(
  name='DebugSphere',
  full_name='SC2APIProtocol.DebugSphere',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='color', full_name='SC2APIProtocol.DebugSphere.color', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='p', full_name='SC2APIProtocol.DebugSphere.p', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='r', full_name='SC2APIProtocol.DebugSphere.r', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1204,
  serialized_end=1300,
)


_DEBUGCREATEUNIT = _descriptor.Descriptor(
  name='DebugCreateUnit',
  full_name='SC2APIProtocol.DebugCreateUnit',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='unit_type', full_name='SC2APIProtocol.DebugCreateUnit.unit_type', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='owner', full_name='SC2APIProtocol.DebugCreateUnit.owner', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pos', full_name='SC2APIProtocol.DebugCreateUnit.pos', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='quantity', full_name='SC2APIProtocol.DebugCreateUnit.quantity', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1302,
  serialized_end=1409,
)


_DEBUGKILLUNIT = _descriptor.Descriptor(
  name='DebugKillUnit',
  full_name='SC2APIProtocol.DebugKillUnit',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tag', full_name='SC2APIProtocol.DebugKillUnit.tag', index=0,
      number=1, type=4, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1411,
  serialized_end=1439,
)


_DEBUGTESTPROCESS = _descriptor.Descriptor(
  name='DebugTestProcess',
  full_name='SC2APIProtocol.DebugTestProcess',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='test', full_name='SC2APIProtocol.DebugTestProcess.test', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='delay_ms', full_name='SC2APIProtocol.DebugTestProcess.delay_ms', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DEBUGTESTPROCESS_TEST,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1442,
  serialized_end=1570,
)


_DEBUGSETSCORE = _descriptor.Descriptor(
  name='DebugSetScore',
  full_name='SC2APIProtocol.DebugSetScore',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='score', full_name='SC2APIProtocol.DebugSetScore.score', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1572,
  serialized_end=1602,
)


_DEBUGENDGAME = _descriptor.Descriptor(
  name='DebugEndGame',
  full_name='SC2APIProtocol.DebugEndGame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='end_result', full_name='SC2APIProtocol.DebugEndGame.end_result', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DEBUGENDGAME_ENDRESULT,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1604,
  serialized_end=1726,
)


_DEBUGSETUNITVALUE = _descriptor.Descriptor(
  name='DebugSetUnitValue',
  full_name='SC2APIProtocol.DebugSetUnitValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='unit_value', full_name='SC2APIProtocol.DebugSetUnitValue.unit_value', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='SC2APIProtocol.DebugSetUnitValue.value', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='unit_tag', full_name='SC2APIProtocol.DebugSetUnitValue.unit_tag', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DEBUGSETUNITVALUE_UNITVALUE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1729,
  serialized_end=1894,
)

_DEBUGCOMMAND.fields_by_name['draw'].message_type = _DEBUGDRAW
_DEBUGCOMMAND.fields_by_name['game_state'].enum_type = _DEBUGGAMESTATE
_DEBUGCOMMAND.fields_by_name['create_unit'].message_type = _DEBUGCREATEUNIT
_DEBUGCOMMAND.fields_by_name['kill_unit'].message_type = _DEBUGKILLUNIT
_DEBUGCOMMAND.fields_by_name['test_process'].message_type = _DEBUGTESTPROCESS
_DEBUGCOMMAND.fields_by_name['score'].message_type = _DEBUGSETSCORE
_DEBUGCOMMAND.fields_by_name['end_game'].message_type = _DEBUGENDGAME
_DEBUGCOMMAND.fields_by_name['unit_value'].message_type = _DEBUGSETUNITVALUE
_DEBUGCOMMAND.oneofs_by_name['command'].fields.append(
  _DEBUGCOMMAND.fields_by_name['draw'])
_DEBUGCOMMAND.fields_by_name['draw'].containing_oneof = _DEBUGCOMMAND.oneofs_by_name['command']
_DEBUGCOMMAND.oneofs_by_name['command'].fields.append(
  _DEBUGCOMMAND.fields_by_name['game_state'])
_DEBUGCOMMAND.fields_by_name['game_state'].containing_oneof = _DEBUGCOMMAND.oneofs_by_name['command']
_DEBUGCOMMAND.oneofs_by_name['command'].fields.append(
  _DEBUGCOMMAND.fields_by_name['create_unit'])
_DEBUGCOMMAND.fields_by_name['create_unit'].containing_oneof = _DEBUGCOMMAND.oneofs_by_name['command']
_DEBUGCOMMAND.oneofs_by_name['command'].fields.append(
  _DEBUGCOMMAND.fields_by_name['kill_unit'])
_DEBUGCOMMAND.fields_by_name['kill_unit'].containing_oneof = _DEBUGCOMMAND.oneofs_by_name['command']
_DEBUGCOMMAND.oneofs_by_name['command'].fields.append(
  _DEBUGCOMMAND.fields_by_name['test_process'])
_DEBUGCOMMAND.fields_by_name['test_process'].containing_oneof = _DEBUGCOMMAND.oneofs_by_name['command']
_DEBUGCOMMAND.oneofs_by_name['command'].fields.append(
  _DEBUGCOMMAND.fields_by_name['score'])
_DEBUGCOMMAND.fields_by_name['score'].containing_oneof = _DEBUGCOMMAND.oneofs_by_name['command']
_DEBUGCOMMAND.oneofs_by_name['command'].fields.append(
  _DEBUGCOMMAND.fields_by_name['end_game'])
_DEBUGCOMMAND.fields_by_name['end_game'].containing_oneof = _DEBUGCOMMAND.oneofs_by_name['command']
_DEBUGCOMMAND.oneofs_by_name['command'].fields.append(
  _DEBUGCOMMAND.fields_by_name['unit_value'])
_DEBUGCOMMAND.fields_by_name['unit_value'].containing_oneof = _DEBUGCOMMAND.oneofs_by_name['command']
_DEBUGDRAW.fields_by_name['text'].message_type = _DEBUGTEXT
_DEBUGDRAW.fields_by_name['lines'].message_type = _DEBUGLINE
_DEBUGDRAW.fields_by_name['boxes'].message_type = _DEBUGBOX
_DEBUGDRAW.fields_by_name['spheres'].message_type = _DEBUGSPHERE
_LINE.fields_by_name['p0'].message_type = s2clientprotocol_dot_common__pb2._POINT
_LINE.fields_by_name['p1'].message_type = s2clientprotocol_dot_common__pb2._POINT
_DEBUGTEXT.fields_by_name['color'].message_type = _COLOR
_DEBUGTEXT.fields_by_name['virtual_pos'].message_type = s2clientprotocol_dot_common__pb2._POINT
_DEBUGTEXT.fields_by_name['world_pos'].message_type = s2clientprotocol_dot_common__pb2._POINT
_DEBUGLINE.fields_by_name['color'].message_type = _COLOR
_DEBUGLINE.fields_by_name['line'].message_type = _LINE
_DEBUGBOX.fields_by_name['color'].message_type = _COLOR
_DEBUGBOX.fields_by_name['min'].message_type = s2clientprotocol_dot_common__pb2._POINT
_DEBUGBOX.fields_by_name['max'].message_type = s2clientprotocol_dot_common__pb2._POINT
_DEBUGSPHERE.fields_by_name['color'].message_type = _COLOR
_DEBUGSPHERE.fields_by_name['p'].message_type = s2clientprotocol_dot_common__pb2._POINT
_DEBUGCREATEUNIT.fields_by_name['pos'].message_type = s2clientprotocol_dot_common__pb2._POINT2D
_DEBUGTESTPROCESS.fields_by_name['test'].enum_type = _DEBUGTESTPROCESS_TEST
_DEBUGTESTPROCESS_TEST.containing_type = _DEBUGTESTPROCESS
_DEBUGENDGAME.fields_by_name['end_result'].enum_type = _DEBUGENDGAME_ENDRESULT
_DEBUGENDGAME_ENDRESULT.containing_type = _DEBUGENDGAME
_DEBUGSETUNITVALUE.fields_by_name['unit_value'].enum_type = _DEBUGSETUNITVALUE_UNITVALUE
_DEBUGSETUNITVALUE_UNITVALUE.containing_type = _DEBUGSETUNITVALUE
DESCRIPTOR.message_types_by_name['DebugCommand'] = _DEBUGCOMMAND
DESCRIPTOR.message_types_by_name['DebugDraw'] = _DEBUGDRAW
DESCRIPTOR.message_types_by_name['Line'] = _LINE
DESCRIPTOR.message_types_by_name['Color'] = _COLOR
DESCRIPTOR.message_types_by_name['DebugText'] = _DEBUGTEXT
DESCRIPTOR.message_types_by_name['DebugLine'] = _DEBUGLINE
DESCRIPTOR.message_types_by_name['DebugBox'] = _DEBUGBOX
DESCRIPTOR.message_types_by_name['DebugSphere'] = _DEBUGSPHERE
DESCRIPTOR.message_types_by_name['DebugCreateUnit'] = _DEBUGCREATEUNIT
DESCRIPTOR.message_types_by_name['DebugKillUnit'] = _DEBUGKILLUNIT
DESCRIPTOR.message_types_by_name['DebugTestProcess'] = _DEBUGTESTPROCESS
DESCRIPTOR.message_types_by_name['DebugSetScore'] = _DEBUGSETSCORE
DESCRIPTOR.message_types_by_name['DebugEndGame'] = _DEBUGENDGAME
DESCRIPTOR.message_types_by_name['DebugSetUnitValue'] = _DEBUGSETUNITVALUE
DESCRIPTOR.enum_types_by_name['DebugGameState'] = _DEBUGGAMESTATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DebugCommand = _reflection.GeneratedProtocolMessageType('DebugCommand', (_message.Message,), dict(
  DESCRIPTOR = _DEBUGCOMMAND,
  __module__ = 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugCommand)
  ))
_sym_db.RegisterMessage(DebugCommand)

DebugDraw = _reflection.GeneratedProtocolMessageType('DebugDraw', (_message.Message,), dict(
  DESCRIPTOR = _DEBUGDRAW,
  __module__ = 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugDraw)
  ))
_sym_db.RegisterMessage(DebugDraw)

Line = _reflection.GeneratedProtocolMessageType('Line', (_message.Message,), dict(
  DESCRIPTOR = _LINE,
  __module__ = 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.Line)
  ))
_sym_db.RegisterMessage(Line)

Color = _reflection.GeneratedProtocolMessageType('Color', (_message.Message,), dict(
  DESCRIPTOR = _COLOR,
  __module__ = 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.Color)
  ))
_sym_db.RegisterMessage(Color)

DebugText = _reflection.GeneratedProtocolMessageType('DebugText', (_message.Message,), dict(
  DESCRIPTOR = _DEBUGTEXT,
  __module__ = 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugText)
  ))
_sym_db.RegisterMessage(DebugText)

DebugLine = _reflection.GeneratedProtocolMessageType('DebugLine', (_message.Message,), dict(
  DESCRIPTOR = _DEBUGLINE,
  __module__ = 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugLine)
  ))
_sym_db.RegisterMessage(DebugLine)

DebugBox = _reflection.GeneratedProtocolMessageType('DebugBox', (_message.Message,), dict(
  DESCRIPTOR = _DEBUGBOX,
  __module__ = 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugBox)
  ))
_sym_db.RegisterMessage(DebugBox)

DebugSphere = _reflection.GeneratedProtocolMessageType('DebugSphere', (_message.Message,), dict(
  DESCRIPTOR = _DEBUGSPHERE,
  __module__ = 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugSphere)
  ))
_sym_db.RegisterMessage(DebugSphere)

DebugCreateUnit = _reflection.GeneratedProtocolMessageType('DebugCreateUnit', (_message.Message,), dict(
  DESCRIPTOR = _DEBUGCREATEUNIT,
  __module__ = 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugCreateUnit)
  ))
_sym_db.RegisterMessage(DebugCreateUnit)

DebugKillUnit = _reflection.GeneratedProtocolMessageType('DebugKillUnit', (_message.Message,), dict(
  DESCRIPTOR = _DEBUGKILLUNIT,
  __module__ = 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugKillUnit)
  ))
_sym_db.RegisterMessage(DebugKillUnit)

DebugTestProcess = _reflection.GeneratedProtocolMessageType('DebugTestProcess', (_message.Message,), dict(
  DESCRIPTOR = _DEBUGTESTPROCESS,
  __module__ = 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugTestProcess)
  ))
_sym_db.RegisterMessage(DebugTestProcess)

DebugSetScore = _reflection.GeneratedProtocolMessageType('DebugSetScore', (_message.Message,), dict(
  DESCRIPTOR = _DEBUGSETSCORE,
  __module__ = 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugSetScore)
  ))
_sym_db.RegisterMessage(DebugSetScore)

DebugEndGame = _reflection.GeneratedProtocolMessageType('DebugEndGame', (_message.Message,), dict(
  DESCRIPTOR = _DEBUGENDGAME,
  __module__ = 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugEndGame)
  ))
_sym_db.RegisterMessage(DebugEndGame)

DebugSetUnitValue = _reflection.GeneratedProtocolMessageType('DebugSetUnitValue', (_message.Message,), dict(
  DESCRIPTOR = _DEBUGSETUNITVALUE,
  __module__ = 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugSetUnitValue)
  ))
_sym_db.RegisterMessage(DebugSetUnitValue)


# @@protoc_insertion_point(module_scope)
