import grpc
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

import qa.basicQA_pb2 as qa_dot_basicQA__pb2
import qa.basicQA_pb2 as qa_dot_basicQA__pb2


class BasicQAServiceStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Question = channel.unary_unary(
        '/minds.qa.BasicQAService/Question',
        request_serializer=qa_dot_basicQA__pb2.QuestionInput.SerializeToString,
        response_deserializer=qa_dot_basicQA__pb2.AnswerOutput.FromString,
        )


class BasicQAServiceServicer(object):

  def Question(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_BasicQAServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Question': grpc.unary_unary_rpc_method_handler(
          servicer.Question,
          request_deserializer=qa_dot_basicQA__pb2.QuestionInput.FromString,
          response_serializer=qa_dot_basicQA__pb2.AnswerOutput.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'minds.qa.BasicQAService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
