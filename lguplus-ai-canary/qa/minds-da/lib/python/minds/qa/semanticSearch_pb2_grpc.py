# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from minds.qa import semanticSearch_pb2 as minds_dot_qa_dot_semanticSearch__pb2


class SemanticSearchServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SearchBM25 = channel.unary_unary(
        '/minds.qa.SemanticSearchService/SearchBM25',
        request_serializer=minds_dot_qa_dot_semanticSearch__pb2.SemanticSearchInput.SerializeToString,
        response_deserializer=minds_dot_qa_dot_semanticSearch__pb2.SemanticSearchOutput.FromString,
        )
    self.SearchTIC = channel.unary_unary(
        '/minds.qa.SemanticSearchService/SearchTIC',
        request_serializer=minds_dot_qa_dot_semanticSearch__pb2.SemanticSearchInput.SerializeToString,
        response_deserializer=minds_dot_qa_dot_semanticSearch__pb2.SemanticSearchOutput.FromString,
        )
    self.SearchBoolean = channel.unary_unary(
        '/minds.qa.SemanticSearchService/SearchBoolean',
        request_serializer=minds_dot_qa_dot_semanticSearch__pb2.SemanticSearchInput.SerializeToString,
        response_deserializer=minds_dot_qa_dot_semanticSearch__pb2.SemanticSearchOutput.FromString,
        )


class SemanticSearchServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def SearchBM25(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SearchTIC(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SearchBoolean(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SemanticSearchServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SearchBM25': grpc.unary_unary_rpc_method_handler(
          servicer.SearchBM25,
          request_deserializer=minds_dot_qa_dot_semanticSearch__pb2.SemanticSearchInput.FromString,
          response_serializer=minds_dot_qa_dot_semanticSearch__pb2.SemanticSearchOutput.SerializeToString,
      ),
      'SearchTIC': grpc.unary_unary_rpc_method_handler(
          servicer.SearchTIC,
          request_deserializer=minds_dot_qa_dot_semanticSearch__pb2.SemanticSearchInput.FromString,
          response_serializer=minds_dot_qa_dot_semanticSearch__pb2.SemanticSearchOutput.SerializeToString,
      ),
      'SearchBoolean': grpc.unary_unary_rpc_method_handler(
          servicer.SearchBoolean,
          request_deserializer=minds_dot_qa_dot_semanticSearch__pb2.SemanticSearchInput.FromString,
          response_serializer=minds_dot_qa_dot_semanticSearch__pb2.SemanticSearchOutput.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'minds.qa.SemanticSearchService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
