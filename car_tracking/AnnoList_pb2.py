# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: AnnoList.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='AnnoList.proto',
  package='protobuf_annolist',
  serialized_pb='\n\x0e\x41nnoList.proto\x12\x11protobuf_annolist\"\x9e\x01\n\x08\x41nnoRect\x12\n\n\x02x1\x18\x01 \x01(\x02\x12\n\n\x02y1\x18\x02 \x01(\x02\x12\n\n\x02x2\x18\x03 \x01(\x02\x12\n\n\x02y2\x18\x04 \x01(\x02\x12\r\n\x05score\x18\x05 \x01(\x02\x12\n\n\x02id\x18\x06 \x01(\x05\x12\x12\n\ndistance3d\x18\x07 \x01(\x02\x12\x0f\n\x07width3d\x18\x08 \x01(\x02\x12\x10\n\x08height3d\x18\t \x01(\x02\x12\x10\n\x08length3d\x18\n \x01(\x02\"o\n\nAnnotation\x12\x11\n\timageName\x18\x01 \x01(\t\x12)\n\x04rect\x18\x02 \x03(\x0b\x32\x1b.protobuf_annolist.AnnoRect\x12\x10\n\x08imgWidth\x18\x03 \x01(\x05\x12\x11\n\timgHeight\x18\x04 \x01(\x05\"=\n\x08\x41nnoList\x12\x31\n\nannotation\x18\x01 \x03(\x0b\x32\x1d.protobuf_annolist.AnnotationB\x0c\x42\nAnnoListPb')




_ANNORECT = _descriptor.Descriptor(
  name='AnnoRect',
  full_name='protobuf_annolist.AnnoRect',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x1', full_name='protobuf_annolist.AnnoRect.x1', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y1', full_name='protobuf_annolist.AnnoRect.y1', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='x2', full_name='protobuf_annolist.AnnoRect.x2', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y2', full_name='protobuf_annolist.AnnoRect.y2', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='score', full_name='protobuf_annolist.AnnoRect.score', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='id', full_name='protobuf_annolist.AnnoRect.id', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='distance3d', full_name='protobuf_annolist.AnnoRect.distance3d', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='width3d', full_name='protobuf_annolist.AnnoRect.width3d', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='height3d', full_name='protobuf_annolist.AnnoRect.height3d', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='length3d', full_name='protobuf_annolist.AnnoRect.length3d', index=9,
      number=10, type=2, cpp_type=6, label=1,
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
  extension_ranges=[],
  serialized_start=38,
  serialized_end=196,
)


_ANNOTATION = _descriptor.Descriptor(
  name='Annotation',
  full_name='protobuf_annolist.Annotation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='imageName', full_name='protobuf_annolist.Annotation.imageName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rect', full_name='protobuf_annolist.Annotation.rect', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='imgWidth', full_name='protobuf_annolist.Annotation.imgWidth', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='imgHeight', full_name='protobuf_annolist.Annotation.imgHeight', index=3,
      number=4, type=5, cpp_type=1, label=1,
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
  extension_ranges=[],
  serialized_start=198,
  serialized_end=309,
)


_ANNOLIST = _descriptor.Descriptor(
  name='AnnoList',
  full_name='protobuf_annolist.AnnoList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='annotation', full_name='protobuf_annolist.AnnoList.annotation', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  extension_ranges=[],
  serialized_start=311,
  serialized_end=372,
)

_ANNOTATION.fields_by_name['rect'].message_type = _ANNORECT
_ANNOLIST.fields_by_name['annotation'].message_type = _ANNOTATION
DESCRIPTOR.message_types_by_name['AnnoRect'] = _ANNORECT
DESCRIPTOR.message_types_by_name['Annotation'] = _ANNOTATION
DESCRIPTOR.message_types_by_name['AnnoList'] = _ANNOLIST

class AnnoRect(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ANNORECT

  # @@protoc_insertion_point(class_scope:protobuf_annolist.AnnoRect)

class Annotation(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ANNOTATION

  # @@protoc_insertion_point(class_scope:protobuf_annolist.Annotation)

class AnnoList(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ANNOLIST

  # @@protoc_insertion_point(class_scope:protobuf_annolist.AnnoList)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), 'B\nAnnoListPb')
# @@protoc_insertion_point(module_scope)
