package ai.mindslab.basicQA;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import java.util.concurrent.TimeUnit;
import minds.qa.BasicQA.AnswerOutput;
import minds.qa.BasicQA.QuestionInput;
import minds.qa.BasicQA.Type;
import minds.qa.BasicQAServiceGrpc;
import minds.qa.BasicQAServiceGrpc.BasicQAServiceBlockingStub;

public class BasicQAClientMain {

  private ManagedChannel channel;


  public static void main(String[] args) {
    BasicQAClientMain qaClientMain = new BasicQAClientMain();
    qaClientMain.connect();
  }

  private void connect() {
    channel = ManagedChannelBuilder.forAddress("localhost", 50051).usePlaintext(true).build();
    BasicQAServiceBlockingStub stub = BasicQAServiceGrpc.newBlockingStub(channel);
    QuestionInput questionInput = QuestionInput.newBuilder().setQuestion("엑소 팬클럽 이름이 뭐야").setType(
        Type.SEARCH).build();
    AnswerOutput answerOutput = stub.question(questionInput);
//    System.out.println(resultQA.getAnswer());
    try {
      channel.shutdown().awaitTermination(5, TimeUnit.SECONDS);
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
  }
}
