// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: minds/lang.proto

package minds;

public final class Lang {
  private Lang() {}
  public static void registerAllExtensions(
      com.google.protobuf.ExtensionRegistryLite registry) {
  }

  public static void registerAllExtensions(
      com.google.protobuf.ExtensionRegistry registry) {
    registerAllExtensions(
        (com.google.protobuf.ExtensionRegistryLite) registry);
  }
  /**
   * <pre>
   * minds::LangCode_Name(minds::LangCode::kor)
   * minds::LangCode::kor
   * </pre>
   *
   * Protobuf enum {@code minds.LangCode}
   */
  public enum LangCode
      implements com.google.protobuf.ProtocolMessageEnum {
    /**
     * <pre>
     * KOREAN
     * </pre>
     *
     * <code>kor = 0;</code>
     */
    kor(0),
    /**
     * <pre>
     * ENGLISH
     * </pre>
     *
     * <code>eng = 1;</code>
     */
    eng(1),
    UNRECOGNIZED(-1),
    ;

    /**
     * <pre>
     * KOREAN
     * </pre>
     *
     * <code>kor = 0;</code>
     */
    public static final int kor_VALUE = 0;
    /**
     * <pre>
     * ENGLISH
     * </pre>
     *
     * <code>eng = 1;</code>
     */
    public static final int eng_VALUE = 1;


    public final int getNumber() {
      if (this == UNRECOGNIZED) {
        throw new java.lang.IllegalArgumentException(
            "Can't get the number of an unknown enum value.");
      }
      return value;
    }

    /**
     * @deprecated Use {@link #forNumber(int)} instead.
     */
    @java.lang.Deprecated
    public static LangCode valueOf(int value) {
      return forNumber(value);
    }

    public static LangCode forNumber(int value) {
      switch (value) {
        case 0: return kor;
        case 1: return eng;
        default: return null;
      }
    }

    public static com.google.protobuf.Internal.EnumLiteMap<LangCode>
        internalGetValueMap() {
      return internalValueMap;
    }
    private static final com.google.protobuf.Internal.EnumLiteMap<
        LangCode> internalValueMap =
          new com.google.protobuf.Internal.EnumLiteMap<LangCode>() {
            public LangCode findValueByNumber(int number) {
              return LangCode.forNumber(number);
            }
          };

    public final com.google.protobuf.Descriptors.EnumValueDescriptor
        getValueDescriptor() {
      return getDescriptor().getValues().get(ordinal());
    }
    public final com.google.protobuf.Descriptors.EnumDescriptor
        getDescriptorForType() {
      return getDescriptor();
    }
    public static final com.google.protobuf.Descriptors.EnumDescriptor
        getDescriptor() {
      return minds.Lang.getDescriptor().getEnumTypes().get(0);
    }

    private static final LangCode[] VALUES = values();

    public static LangCode valueOf(
        com.google.protobuf.Descriptors.EnumValueDescriptor desc) {
      if (desc.getType() != getDescriptor()) {
        throw new java.lang.IllegalArgumentException(
          "EnumValueDescriptor is not for this type.");
      }
      if (desc.getIndex() == -1) {
        return UNRECOGNIZED;
      }
      return VALUES[desc.getIndex()];
    }

    private final int value;

    private LangCode(int value) {
      this.value = value;
    }

    // @@protoc_insertion_point(enum_scope:minds.LangCode)
  }


  public static com.google.protobuf.Descriptors.FileDescriptor
      getDescriptor() {
    return descriptor;
  }
  private static  com.google.protobuf.Descriptors.FileDescriptor
      descriptor;
  static {
    java.lang.String[] descriptorData = {
      "\n\020minds/lang.proto\022\005minds*\034\n\010LangCode\022\007\n" +
      "\003kor\020\000\022\007\n\003eng\020\001B\003\370\001\001b\006proto3"
    };
    com.google.protobuf.Descriptors.FileDescriptor.InternalDescriptorAssigner assigner =
        new com.google.protobuf.Descriptors.FileDescriptor.    InternalDescriptorAssigner() {
          public com.google.protobuf.ExtensionRegistry assignDescriptors(
              com.google.protobuf.Descriptors.FileDescriptor root) {
            descriptor = root;
            return null;
          }
        };
    com.google.protobuf.Descriptors.FileDescriptor
      .internalBuildGeneratedFileFrom(descriptorData,
        new com.google.protobuf.Descriptors.FileDescriptor[] {
        }, assigner);
  }

  // @@protoc_insertion_point(outer_class_scope)
}