# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import minds_mrc_pb2 as minds__mrc__pb2


class MRCStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SendQuestion = channel.unary_unary(
        '/MRC/SendQuestion',
        request_serializer=minds__mrc__pb2.MrcInput.SerializeToString,
        response_deserializer=minds__mrc__pb2.MrcOutputs.FromString,
        )


class MRCServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def SendQuestion(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_MRCServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SendQuestion': grpc.unary_unary_rpc_method_handler(
          servicer.SendQuestion,
          request_deserializer=minds__mrc__pb2.MrcInput.FromString,
          response_serializer=minds__mrc__pb2.MrcOutputs.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'MRC', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
