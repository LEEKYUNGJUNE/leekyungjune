package minds.ta;

import static io.grpc.stub.ClientCalls.asyncUnaryCall;
import static io.grpc.stub.ClientCalls.asyncServerStreamingCall;
import static io.grpc.stub.ClientCalls.asyncClientStreamingCall;
import static io.grpc.stub.ClientCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ClientCalls.blockingUnaryCall;
import static io.grpc.stub.ClientCalls.blockingServerStreamingCall;
import static io.grpc.stub.ClientCalls.futureUnaryCall;
import static io.grpc.MethodDescriptor.generateFullMethodName;
import static io.grpc.stub.ServerCalls.asyncUnaryCall;
import static io.grpc.stub.ServerCalls.asyncServerStreamingCall;
import static io.grpc.stub.ServerCalls.asyncClientStreamingCall;
import static io.grpc.stub.ServerCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedStreamingCall;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.6.1)",
    comments = "Source: minds/ta/nlp.proto")
public final class SplitSentenceServiceGrpc {

  private SplitSentenceServiceGrpc() {}

  public static final String SERVICE_NAME = "minds.ta.SplitSentenceService";

  // Static method descriptors that strictly reflect the proto.
  @io.grpc.ExperimentalApi("https://github.com/grpc/grpc-java/issues/1901")
  public static final io.grpc.MethodDescriptor<minds.ta.Nlp.Text,
      minds.ta.Nlp.TextArray> METHOD_SPLIT =
      io.grpc.MethodDescriptor.<minds.ta.Nlp.Text, minds.ta.Nlp.TextArray>newBuilder()
          .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
          .setFullMethodName(generateFullMethodName(
              "minds.ta.SplitSentenceService", "Split"))
          .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              minds.ta.Nlp.Text.getDefaultInstance()))
          .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              minds.ta.Nlp.TextArray.getDefaultInstance()))
          .build();

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static SplitSentenceServiceStub newStub(io.grpc.Channel channel) {
    return new SplitSentenceServiceStub(channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static SplitSentenceServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    return new SplitSentenceServiceBlockingStub(channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static SplitSentenceServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    return new SplitSentenceServiceFutureStub(channel);
  }

  /**
   */
  public static abstract class SplitSentenceServiceImplBase implements io.grpc.BindableService {

    /**
     */
    public void split(minds.ta.Nlp.Text request,
        io.grpc.stub.StreamObserver<minds.ta.Nlp.TextArray> responseObserver) {
      asyncUnimplementedUnaryCall(METHOD_SPLIT, responseObserver);
    }

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
          .addMethod(
            METHOD_SPLIT,
            asyncUnaryCall(
              new MethodHandlers<
                minds.ta.Nlp.Text,
                minds.ta.Nlp.TextArray>(
                  this, METHODID_SPLIT)))
          .build();
    }
  }

  /**
   */
  public static final class SplitSentenceServiceStub extends io.grpc.stub.AbstractStub<SplitSentenceServiceStub> {
    private SplitSentenceServiceStub(io.grpc.Channel channel) {
      super(channel);
    }

    private SplitSentenceServiceStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected SplitSentenceServiceStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new SplitSentenceServiceStub(channel, callOptions);
    }

    /**
     */
    public void split(minds.ta.Nlp.Text request,
        io.grpc.stub.StreamObserver<minds.ta.Nlp.TextArray> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(METHOD_SPLIT, getCallOptions()), request, responseObserver);
    }
  }

  /**
   */
  public static final class SplitSentenceServiceBlockingStub extends io.grpc.stub.AbstractStub<SplitSentenceServiceBlockingStub> {
    private SplitSentenceServiceBlockingStub(io.grpc.Channel channel) {
      super(channel);
    }

    private SplitSentenceServiceBlockingStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected SplitSentenceServiceBlockingStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new SplitSentenceServiceBlockingStub(channel, callOptions);
    }

    /**
     */
    public minds.ta.Nlp.TextArray split(minds.ta.Nlp.Text request) {
      return blockingUnaryCall(
          getChannel(), METHOD_SPLIT, getCallOptions(), request);
    }
  }

  /**
   */
  public static final class SplitSentenceServiceFutureStub extends io.grpc.stub.AbstractStub<SplitSentenceServiceFutureStub> {
    private SplitSentenceServiceFutureStub(io.grpc.Channel channel) {
      super(channel);
    }

    private SplitSentenceServiceFutureStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected SplitSentenceServiceFutureStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new SplitSentenceServiceFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<minds.ta.Nlp.TextArray> split(
        minds.ta.Nlp.Text request) {
      return futureUnaryCall(
          getChannel().newCall(METHOD_SPLIT, getCallOptions()), request);
    }
  }

  private static final int METHODID_SPLIT = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final SplitSentenceServiceImplBase serviceImpl;
    private final int methodId;

    MethodHandlers(SplitSentenceServiceImplBase serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_SPLIT:
          serviceImpl.split((minds.ta.Nlp.Text) request,
              (io.grpc.stub.StreamObserver<minds.ta.Nlp.TextArray>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  private static final class SplitSentenceServiceDescriptorSupplier implements io.grpc.protobuf.ProtoFileDescriptorSupplier {
    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return minds.ta.Nlp.getDescriptor();
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (SplitSentenceServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new SplitSentenceServiceDescriptorSupplier())
              .addMethod(METHOD_SPLIT)
              .build();
        }
      }
    }
    return result;
  }
}
