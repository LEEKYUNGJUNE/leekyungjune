# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: minds/qa/nlqa.proto

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
  name='minds/qa/nlqa.proto',
  package='minds.qa',
  syntax='proto3',
  serialized_pb=_b('\n\x13minds/qa/nlqa.proto\x12\x08minds.qa\")\n\x19QuestionAnalysisInputText\x12\x0c\n\x04text\x18\x01 \x01(\t\"0\n\x1eQuestionAnalysisResultDocument\x12\x0e\n\x06result\x18\x01 \x01(\tb\x06proto3')
)




_QUESTIONANALYSISINPUTTEXT = _descriptor.Descriptor(
  name='QuestionAnalysisInputText',
  full_name='minds.qa.QuestionAnalysisInputText',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='minds.qa.QuestionAnalysisInputText.text', index=0,
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
  serialized_start=33,
  serialized_end=74,
)


_QUESTIONANALYSISRESULTDOCUMENT = _descriptor.Descriptor(
  name='QuestionAnalysisResultDocument',
  full_name='minds.qa.QuestionAnalysisResultDocument',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='minds.qa.QuestionAnalysisResultDocument.result', index=0,
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
  serialized_start=76,
  serialized_end=124,
)

DESCRIPTOR.message_types_by_name['QuestionAnalysisInputText'] = _QUESTIONANALYSISINPUTTEXT
DESCRIPTOR.message_types_by_name['QuestionAnalysisResultDocument'] = _QUESTIONANALYSISRESULTDOCUMENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

QuestionAnalysisInputText = _reflection.GeneratedProtocolMessageType('QuestionAnalysisInputText', (_message.Message,), dict(
  DESCRIPTOR = _QUESTIONANALYSISINPUTTEXT,
  __module__ = 'minds.qa.nlqa_pb2'
  # @@protoc_insertion_point(class_scope:minds.qa.QuestionAnalysisInputText)
  ))
_sym_db.RegisterMessage(QuestionAnalysisInputText)

QuestionAnalysisResultDocument = _reflection.GeneratedProtocolMessageType('QuestionAnalysisResultDocument', (_message.Message,), dict(
  DESCRIPTOR = _QUESTIONANALYSISRESULTDOCUMENT,
  __module__ = 'minds.qa.nlqa_pb2'
  # @@protoc_insertion_point(class_scope:minds.qa.QuestionAnalysisResultDocument)
  ))
_sym_db.RegisterMessage(QuestionAnalysisResultDocument)


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
