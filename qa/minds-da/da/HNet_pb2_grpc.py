# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import HNet_pb2 as HNet__pb2


class HNetStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Predict = channel.unary_unary(
        '/HNet/Predict',
        request_serializer=HNet__pb2.HNetInput.SerializeToString,
        response_deserializer=HNet__pb2.HNetOutputs.FromString,
        )


class HNetServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Predict(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_HNetServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Predict': grpc.unary_unary_rpc_method_handler(
          servicer.Predict,
          request_deserializer=HNet__pb2.HNetInput.FromString,
          response_serializer=HNet__pb2.HNetOutputs.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'HNet', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
