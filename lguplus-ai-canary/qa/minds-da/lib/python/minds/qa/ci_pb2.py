# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: minds/qa/ci.proto

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
  name='minds/qa/ci.proto',
  package='minds.qa',
  syntax='proto3',
  serialized_pb=_b('\n\x11minds/qa/ci.proto\x12\x08minds.qa\"S\n\x1bInferenceCandidateInputText\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x13\n\x0bstart_index\x18\x02 \x01(\x05\x12\x11\n\tend_index\x18\x03 \x01(\x05\"2\n InferenceCandidateResultDocument\x12\x0e\n\x06result\x18\x01 \x01(\tb\x06proto3')
)




_INFERENCECANDIDATEINPUTTEXT = _descriptor.Descriptor(
  name='InferenceCandidateInputText',
  full_name='minds.qa.InferenceCandidateInputText',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='minds.qa.InferenceCandidateInputText.text', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='start_index', full_name='minds.qa.InferenceCandidateInputText.start_index', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='end_index', full_name='minds.qa.InferenceCandidateInputText.end_index', index=2,
      number=3, type=5, cpp_type=1, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=31,
  serialized_end=114,
)


_INFERENCECANDIDATERESULTDOCUMENT = _descriptor.Descriptor(
  name='InferenceCandidateResultDocument',
  full_name='minds.qa.InferenceCandidateResultDocument',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='minds.qa.InferenceCandidateResultDocument.result', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=116,
  serialized_end=166,
)

DESCRIPTOR.message_types_by_name['InferenceCandidateInputText'] = _INFERENCECANDIDATEINPUTTEXT
DESCRIPTOR.message_types_by_name['InferenceCandidateResultDocument'] = _INFERENCECANDIDATERESULTDOCUMENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

InferenceCandidateInputText = _reflection.GeneratedProtocolMessageType('InferenceCandidateInputText', (_message.Message,), dict(
  DESCRIPTOR = _INFERENCECANDIDATEINPUTTEXT,
  __module__ = 'minds.qa.ci_pb2'
  # @@protoc_insertion_point(class_scope:minds.qa.InferenceCandidateInputText)
  ))
_sym_db.RegisterMessage(InferenceCandidateInputText)

InferenceCandidateResultDocument = _reflection.GeneratedProtocolMessageType('InferenceCandidateResultDocument', (_message.Message,), dict(
  DESCRIPTOR = _INFERENCECANDIDATERESULTDOCUMENT,
  __module__ = 'minds.qa.ci_pb2'
  # @@protoc_insertion_point(class_scope:minds.qa.InferenceCandidateResultDocument)
  ))
_sym_db.RegisterMessage(InferenceCandidateResultDocument)


try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)
