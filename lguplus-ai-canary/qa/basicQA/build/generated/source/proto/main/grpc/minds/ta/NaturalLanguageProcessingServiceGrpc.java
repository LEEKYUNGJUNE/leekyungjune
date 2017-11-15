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
public final class NaturalLanguageProcessingServiceGrpc {

  private NaturalLanguageProcessingServiceGrpc() {}

  public static final String SERVICE_NAME = "minds.ta.NaturalLanguageProcessingService";

  // Static method descriptors that strictly reflect the proto.
  @io.grpc.ExperimentalApi("https://github.com/grpc/grpc-java/issues/1901")
  public static final io.grpc.MethodDescriptor<com.google.protobuf.Empty,
      minds.ta.Nlp.NlpProvider> METHOD_GET_PROVIDER =
      io.grpc.MethodDescriptor.<com.google.protobuf.Empty, minds.ta.Nlp.NlpProvider>newBuilder()
          .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
          .setFullMethodName(generateFullMethodName(
              "minds.ta.NaturalLanguageProcessingService", "GetProvider"))
          .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              com.google.protobuf.Empty.getDefaultInstance()))
          .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              minds.ta.Nlp.NlpProvider.getDefaultInstance()))
          .build();
  @io.grpc.ExperimentalApi("https://github.com/grpc/grpc-java/issues/1901")
  public static final io.grpc.MethodDescriptor<minds.ta.Nlp.InputText,
      minds.ta.Nlp.Document> METHOD_ANALYZE =
      io.grpc.MethodDescriptor.<minds.ta.Nlp.InputText, minds.ta.Nlp.Document>newBuilder()
          .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
          .setFullMethodName(generateFullMethodName(
              "minds.ta.NaturalLanguageProcessingService", "Analyze"))
          .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              minds.ta.Nlp.InputText.getDefaultInstance()))
          .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              minds.ta.Nlp.Document.getDefaultInstance()))
          .build();
  @io.grpc.ExperimentalApi("https://github.com/grpc/grpc-java/issues/1901")
  public static final io.grpc.MethodDescriptor<minds.ta.Nlp.InputText,
      minds.ta.Nlp.Document> METHOD_ANALYZE_MULTIPLE =
      io.grpc.MethodDescriptor.<minds.ta.Nlp.InputText, minds.ta.Nlp.Document>newBuilder()
          .setType(io.grpc.MethodDescriptor.MethodType.BIDI_STREAMING)
          .setFullMethodName(generateFullMethodName(
              "minds.ta.NaturalLanguageProcessingService", "AnalyzeMultiple"))
          .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              minds.ta.Nlp.InputText.getDefaultInstance()))
          .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              minds.ta.Nlp.Document.getDefaultInstance()))
          .build();
  @io.grpc.ExperimentalApi("https://github.com/grpc/grpc-java/issues/1901")
  public static final io.grpc.MethodDescriptor<minds.ta.Nlp.NlpFeatures,
      minds.ta.Nlp.NlpFeatureSupportList> METHOD_HAS_SUPPORT =
      io.grpc.MethodDescriptor.<minds.ta.Nlp.NlpFeatures, minds.ta.Nlp.NlpFeatureSupportList>newBuilder()
          .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
          .setFullMethodName(generateFullMethodName(
              "minds.ta.NaturalLanguageProcessingService", "HasSupport"))
          .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              minds.ta.Nlp.NlpFeatures.getDefaultInstance()))
          .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              minds.ta.Nlp.NlpFeatureSupportList.getDefaultInstance()))
          .build();
  @io.grpc.ExperimentalApi("https://github.com/grpc/grpc-java/issues/1901")
  public static final io.grpc.MethodDescriptor<minds.ta.Nlp.NlpDict,
      com.google.protobuf.Empty> METHOD_APPLY_DICT =
      io.grpc.MethodDescriptor.<minds.ta.Nlp.NlpDict, com.google.protobuf.Empty>newBuilder()
          .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
          .setFullMethodName(generateFullMethodName(
              "minds.ta.NaturalLanguageProcessingService", "ApplyDict"))
          .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              minds.ta.Nlp.NlpDict.getDefaultInstance()))
          .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
              com.google.protobuf.Empty.getDefaultInstance()))
          .build();

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static NaturalLanguageProcessingServiceStub newStub(io.grpc.Channel channel) {
    return new NaturalLanguageProcessingServiceStub(channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static NaturalLanguageProcessingServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    return new NaturalLanguageProcessingServiceBlockingStub(channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static NaturalLanguageProcessingServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    return new NaturalLanguageProcessingServiceFutureStub(channel);
  }

  /**
   */
  public static abstract class NaturalLanguageProcessingServiceImplBase implements io.grpc.BindableService {

    /**
     */
    public void getProvider(com.google.protobuf.Empty request,
        io.grpc.stub.StreamObserver<minds.ta.Nlp.NlpProvider> responseObserver) {
      asyncUnimplementedUnaryCall(METHOD_GET_PROVIDER, responseObserver);
    }

    /**
     */
    public void analyze(minds.ta.Nlp.InputText request,
        io.grpc.stub.StreamObserver<minds.ta.Nlp.Document> responseObserver) {
      asyncUnimplementedUnaryCall(METHOD_ANALYZE, responseObserver);
    }

    /**
     */
    public io.grpc.stub.StreamObserver<minds.ta.Nlp.InputText> analyzeMultiple(
        io.grpc.stub.StreamObserver<minds.ta.Nlp.Document> responseObserver) {
      return asyncUnimplementedStreamingCall(METHOD_ANALYZE_MULTIPLE, responseObserver);
    }

    /**
     */
    public void hasSupport(minds.ta.Nlp.NlpFeatures request,
        io.grpc.stub.StreamObserver<minds.ta.Nlp.NlpFeatureSupportList> responseObserver) {
      asyncUnimplementedUnaryCall(METHOD_HAS_SUPPORT, responseObserver);
    }

    /**
     */
    public void applyDict(minds.ta.Nlp.NlpDict request,
        io.grpc.stub.StreamObserver<com.google.protobuf.Empty> responseObserver) {
      asyncUnimplementedUnaryCall(METHOD_APPLY_DICT, responseObserver);
    }

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
          .addMethod(
            METHOD_GET_PROVIDER,
            asyncUnaryCall(
              new MethodHandlers<
                com.google.protobuf.Empty,
                minds.ta.Nlp.NlpProvider>(
                  this, METHODID_GET_PROVIDER)))
          .addMethod(
            METHOD_ANALYZE,
            asyncUnaryCall(
              new MethodHandlers<
                minds.ta.Nlp.InputText,
                minds.ta.Nlp.Document>(
                  this, METHODID_ANALYZE)))
          .addMethod(
            METHOD_ANALYZE_MULTIPLE,
            asyncBidiStreamingCall(
              new MethodHandlers<
                minds.ta.Nlp.InputText,
                minds.ta.Nlp.Document>(
                  this, METHODID_ANALYZE_MULTIPLE)))
          .addMethod(
            METHOD_HAS_SUPPORT,
            asyncUnaryCall(
              new MethodHandlers<
                minds.ta.Nlp.NlpFeatures,
                minds.ta.Nlp.NlpFeatureSupportList>(
                  this, METHODID_HAS_SUPPORT)))
          .addMethod(
            METHOD_APPLY_DICT,
            asyncUnaryCall(
              new MethodHandlers<
                minds.ta.Nlp.NlpDict,
                com.google.protobuf.Empty>(
                  this, METHODID_APPLY_DICT)))
          .build();
    }
  }

  /**
   */
  public static final class NaturalLanguageProcessingServiceStub extends io.grpc.stub.AbstractStub<NaturalLanguageProcessingServiceStub> {
    private NaturalLanguageProcessingServiceStub(io.grpc.Channel channel) {
      super(channel);
    }

    private NaturalLanguageProcessingServiceStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected NaturalLanguageProcessingServiceStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new NaturalLanguageProcessingServiceStub(channel, callOptions);
    }

    /**
     */
    public void getProvider(com.google.protobuf.Empty request,
        io.grpc.stub.StreamObserver<minds.ta.Nlp.NlpProvider> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(METHOD_GET_PROVIDER, getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void analyze(minds.ta.Nlp.InputText request,
        io.grpc.stub.StreamObserver<minds.ta.Nlp.Document> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(METHOD_ANALYZE, getCallOptions()), request, responseObserver);
    }

    /**
     */
    public io.grpc.stub.StreamObserver<minds.ta.Nlp.InputText> analyzeMultiple(
        io.grpc.stub.StreamObserver<minds.ta.Nlp.Document> responseObserver) {
      return asyncBidiStreamingCall(
          getChannel().newCall(METHOD_ANALYZE_MULTIPLE, getCallOptions()), responseObserver);
    }

    /**
     */
    public void hasSupport(minds.ta.Nlp.NlpFeatures request,
        io.grpc.stub.StreamObserver<minds.ta.Nlp.NlpFeatureSupportList> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(METHOD_HAS_SUPPORT, getCallOptions()), request, responseObserver);
    }

    /**
     */
    public void applyDict(minds.ta.Nlp.NlpDict request,
        io.grpc.stub.StreamObserver<com.google.protobuf.Empty> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(METHOD_APPLY_DICT, getCallOptions()), request, responseObserver);
    }
  }

  /**
   */
  public static final class NaturalLanguageProcessingServiceBlockingStub extends io.grpc.stub.AbstractStub<NaturalLanguageProcessingServiceBlockingStub> {
    private NaturalLanguageProcessingServiceBlockingStub(io.grpc.Channel channel) {
      super(channel);
    }

    private NaturalLanguageProcessingServiceBlockingStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected NaturalLanguageProcessingServiceBlockingStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new NaturalLanguageProcessingServiceBlockingStub(channel, callOptions);
    }

    /**
     */
    public minds.ta.Nlp.NlpProvider getProvider(com.google.protobuf.Empty request) {
      return blockingUnaryCall(
          getChannel(), METHOD_GET_PROVIDER, getCallOptions(), request);
    }

    /**
     */
    public minds.ta.Nlp.Document analyze(minds.ta.Nlp.InputText request) {
      return blockingUnaryCall(
          getChannel(), METHOD_ANALYZE, getCallOptions(), request);
    }

    /**
     */
    public minds.ta.Nlp.NlpFeatureSupportList hasSupport(minds.ta.Nlp.NlpFeatures request) {
      return blockingUnaryCall(
          getChannel(), METHOD_HAS_SUPPORT, getCallOptions(), request);
    }

    /**
     */
    public com.google.protobuf.Empty applyDict(minds.ta.Nlp.NlpDict request) {
      return blockingUnaryCall(
          getChannel(), METHOD_APPLY_DICT, getCallOptions(), request);
    }
  }

  /**
   */
  public static final class NaturalLanguageProcessingServiceFutureStub extends io.grpc.stub.AbstractStub<NaturalLanguageProcessingServiceFutureStub> {
    private NaturalLanguageProcessingServiceFutureStub(io.grpc.Channel channel) {
      super(channel);
    }

    private NaturalLanguageProcessingServiceFutureStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected NaturalLanguageProcessingServiceFutureStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new NaturalLanguageProcessingServiceFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<minds.ta.Nlp.NlpProvider> getProvider(
        com.google.protobuf.Empty request) {
      return futureUnaryCall(
          getChannel().newCall(METHOD_GET_PROVIDER, getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<minds.ta.Nlp.Document> analyze(
        minds.ta.Nlp.InputText request) {
      return futureUnaryCall(
          getChannel().newCall(METHOD_ANALYZE, getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<minds.ta.Nlp.NlpFeatureSupportList> hasSupport(
        minds.ta.Nlp.NlpFeatures request) {
      return futureUnaryCall(
          getChannel().newCall(METHOD_HAS_SUPPORT, getCallOptions()), request);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.google.protobuf.Empty> applyDict(
        minds.ta.Nlp.NlpDict request) {
      return futureUnaryCall(
          getChannel().newCall(METHOD_APPLY_DICT, getCallOptions()), request);
    }
  }

  private static final int METHODID_GET_PROVIDER = 0;
  private static final int METHODID_ANALYZE = 1;
  private static final int METHODID_HAS_SUPPORT = 2;
  private static final int METHODID_APPLY_DICT = 3;
  private static final int METHODID_ANALYZE_MULTIPLE = 4;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final NaturalLanguageProcessingServiceImplBase serviceImpl;
    private final int methodId;

    MethodHandlers(NaturalLanguageProcessingServiceImplBase serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_GET_PROVIDER:
          serviceImpl.getProvider((com.google.protobuf.Empty) request,
              (io.grpc.stub.StreamObserver<minds.ta.Nlp.NlpProvider>) responseObserver);
          break;
        case METHODID_ANALYZE:
          serviceImpl.analyze((minds.ta.Nlp.InputText) request,
              (io.grpc.stub.StreamObserver<minds.ta.Nlp.Document>) responseObserver);
          break;
        case METHODID_HAS_SUPPORT:
          serviceImpl.hasSupport((minds.ta.Nlp.NlpFeatures) request,
              (io.grpc.stub.StreamObserver<minds.ta.Nlp.NlpFeatureSupportList>) responseObserver);
          break;
        case METHODID_APPLY_DICT:
          serviceImpl.applyDict((minds.ta.Nlp.NlpDict) request,
              (io.grpc.stub.StreamObserver<com.google.protobuf.Empty>) responseObserver);
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
        case METHODID_ANALYZE_MULTIPLE:
          return (io.grpc.stub.StreamObserver<Req>) serviceImpl.analyzeMultiple(
              (io.grpc.stub.StreamObserver<minds.ta.Nlp.Document>) responseObserver);
        default:
          throw new AssertionError();
      }
    }
  }

  private static final class NaturalLanguageProcessingServiceDescriptorSupplier implements io.grpc.protobuf.ProtoFileDescriptorSupplier {
    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return minds.ta.Nlp.getDescriptor();
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (NaturalLanguageProcessingServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new NaturalLanguageProcessingServiceDescriptorSupplier())
              .addMethod(METHOD_GET_PROVIDER)
              .addMethod(METHOD_ANALYZE)
              .addMethod(METHOD_ANALYZE_MULTIPLE)
              .addMethod(METHOD_HAS_SUPPORT)
              .addMethod(METHOD_APPLY_DICT)
              .build();
        }
      }
    }
    return result;
  }
}
