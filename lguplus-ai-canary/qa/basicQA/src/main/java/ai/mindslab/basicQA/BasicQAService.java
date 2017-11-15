package ai.mindslab.basicQA;

import ai.mindslab.util.PropertiesManager;
import ai.mindslab.util.SqlSessionManager;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.stub.StreamObserver;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import minds.Lang.LangCode;
import minds.qa.BasicQA.AnswerOutput;
import minds.qa.BasicQA.AnswerOutput.Builder;
import minds.qa.BasicQA.DBResult;
import minds.qa.BasicQA.QuestionInput;
import minds.qa.BasicQA.SearchResult;
import minds.qa.BasicQA.Type;
import minds.qa.BasicQAServiceGrpc.BasicQAServiceImplBase;
import minds.ta.NaturalLanguageProcessingServiceGrpc;
import minds.ta.NaturalLanguageProcessingServiceGrpc.NaturalLanguageProcessingServiceBlockingStub;
import minds.ta.Nlp.Document;
import minds.ta.Nlp.InputText;
import minds.ta.Nlp.KeywordFrequencyLevel;
import minds.ta.Nlp.Morpheme;
import minds.ta.Nlp.NlpAnalysisLevel;
import minds.ta.Nlp.Sentence;
import org.apache.commons.lang3.StringUtils;
import org.apache.ibatis.session.SqlSession;
import org.apache.solr.client.solrj.SolrClient;
import org.apache.solr.client.solrj.SolrQuery;
import org.apache.solr.client.solrj.response.QueryResponse;
import org.apache.solr.common.SolrDocument;
import org.apache.solr.common.SolrDocumentList;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class BasicQAService extends BasicQAServiceImplBase {

  private static Properties properties = PropertiesManager.getProperties();

  private static Logger logger = LoggerFactory.getLogger(BasicQAService.class);

  private static Logger TLO = LoggerFactory.getLogger("TLO");

  private static SqlSession sqlSession;

  private static SolrClient solrClient;

  private static ManagedChannel nlpChannel;

  private static NaturalLanguageProcessingServiceBlockingStub nlpStub;

  public BasicQAService(SqlSession sqlSession,
      SolrClient solrClient) {
    this.sqlSession = sqlSession;
    this.solrClient = solrClient;
    this.nlpChannel = ManagedChannelBuilder.forAddress(properties.getProperty("NLP_SERVER"),
        Integer.parseInt(properties.getProperty("NLP_PORT"))).usePlaintext(true).build();
    this.nlpStub = NaturalLanguageProcessingServiceGrpc.newBlockingStub(nlpChannel);
  }

  @Override
  public void question(QuestionInput questionInput, StreamObserver<AnswerOutput> responseObserver) {
    SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyyMMddHHmmssSSS");
    Map<String, String> meta = new HashMap<>();
    meta.putAll(questionInput.getMetaMap());
    meta.put("req_time", simpleDateFormat.format(new Date()));
    meta.put("qa_engine", "BASICQA");
    try {
      logger.info("Question : " + questionInput.getQuestion());
      Builder resultQA = AnswerOutput.newBuilder();
      resultQA.setQuestion(questionInput.getQuestion());
      if (questionInput.getType() == Type.DB) {
        getDBAnswer(resultQA, questionInput);
      } else if (questionInput.getType() == Type.SEARCH) {
        getSearchAnswer(resultQA, questionInput);
      } else if (questionInput.getType() == Type.ALL) {
        getDBAnswer(resultQA, questionInput);
        getSearchAnswer(resultQA, questionInput);
      }
      responseObserver.onNext(resultQA.build());
      responseObserver.onCompleted();
      meta.put("result_code", "20000000");
    } catch (Exception e) {
      e.printStackTrace();
      meta.put("result_code", "40000103");
    }
    meta.put("rsp_time", simpleDateFormat.format(new Date()));
    writeTLO(meta);
  }

  private void writeTLO(Map<String, String> meta) {
    SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyyMMddHHmmss");
    StringBuffer buffer = new StringBuffer();
    buffer.append("SEQ_ID=");
    buffer.append(meta.get("seq_id"));
    buffer.append("|");
    buffer.append("LOG_TIME=");
    buffer.append(simpleDateFormat.format(new Date()));
    buffer.append("|");
    buffer.append("LOG_TYPE=");
    buffer.append(meta.get("log_type"));
    buffer.append("|");
    buffer.append("SID=");
    buffer.append(meta.get("sid"));
    buffer.append("|");
    buffer.append("RESULT_CODE=");
    buffer.append(meta.get("result_code"));
    buffer.append("|");
    buffer.append("REQ_TIME=");
    buffer.append(meta.get("req_time"));
    buffer.append("|");
    buffer.append("RSP_TIME=");
    buffer.append(meta.get("rsp_time"));
    buffer.append("|");
    buffer.append("CLIENT_IP=");
    buffer.append(meta.get("client_ip"));
    buffer.append("|");
    buffer.append("DEV_INFO=");
    buffer.append(meta.get("dev_info"));
    buffer.append("|");
    buffer.append("OS_INFO=");
    buffer.append(meta.get("os_info"));
    buffer.append("|");
    buffer.append("NW_INFO=");
    buffer.append(meta.get("nw_info"));
    buffer.append("|");
    buffer.append("SVC_NAME=");
    buffer.append(meta.get("svc_name"));
    buffer.append("|");
    buffer.append("DEV_MODEL=");
    buffer.append(meta.get("dev_model"));
    buffer.append("|");
    buffer.append("CARRIER_TYPE=");
    buffer.append(meta.get("carrier_type"));
    buffer.append("|");
    buffer.append("TR_ID=");
    buffer.append(meta.get("transaction_id"));
    buffer.append("|");
    buffer.append("MSG_ID=");
    buffer.append(meta.get("message_id"));
    buffer.append("|");
    buffer.append("FROM_SVC_NAME=");
    buffer.append(meta.get("from_svc_name"));
    buffer.append("|");
    buffer.append("TO_SVC_NAME=");
    buffer.append(meta.get("to_svc_name"));
    buffer.append("|");
    buffer.append("SVC_TYPE=");
    buffer.append(meta.get("svc_type"));
    buffer.append("|");
    buffer.append("DEV_TYPE=");
    buffer.append(meta.get("dev_type"));
    buffer.append("|");
    buffer.append("DEVICE_TOKEN=");
    buffer.append(meta.get("device_token"));
    buffer.append("|");
    buffer.append("QA_ENGINE=");
    buffer.append(meta.get("qa_engine"));
    TLO.info(buffer.toString());
  }


  private Builder getSearchAnswer(Builder answerOutput, QuestionInput questionInput)
      throws Exception {
    String question = questionInput.getQuestion();
//    String question = doNlp(parameterQA.getQuestion());

    SolrQuery solrQuery = new SolrQuery();
    logger.info(
        "NLP Result : " + "question:\"" + question + "\"");
    solrQuery.set("q", "question:\"" + question + "\"");
    solrQuery.setFields("*", "score");
    try {
      logger.info("SOLR URL : " + properties.getProperty("SOLR_URL"));
      QueryResponse queryResponse = solrClient.query(solrQuery);
      SolrDocumentList documentList = queryResponse.getResults();
      int i = 0;
      logger.info("documentList size : " + documentList.size());
      for (SolrDocument document : documentList) {
        if (i >= questionInput.getNtop()) {
          break;
        }

        float qlen = (float) (questionInput.getQuestion().length() * 1.3);
        logger.info("qlen : " + qlen);
        logger.info("document Question : " + String.valueOf(document.get("question")).length());
        if (qlen <= String.valueOf(document.get("question")).length()) {
          i++;
          continue;
        }
        SearchResult searchResult = SearchResult.newBuilder()
            .setSearchQuestion(String.valueOf(document.get("question")))
            .setAnswer(String.valueOf(document.get("answer")))
            .setScore(Float.parseFloat(String.valueOf(document.get("score"))))
            .build();
        answerOutput.addSearchResult(searchResult);
        i++;
      }
    } catch (Exception e) {
      e.printStackTrace();
      throw new Exception();
    }
    return answerOutput;
  }

  private String doNlp(String question) {
    try {
      List<String> strList = new ArrayList<>();
      InputText inputText = InputText.newBuilder().setText(question).setLang(LangCode.kor)
          .setSplitSentence(true).setUseTokenizer(true).setLevel(NlpAnalysisLevel.NLP_ANALYSIS_ALL)
          .setKeywordFrequencyLevel(KeywordFrequencyLevel.KEYWORD_FREQUENCY_ALL).build();
      Document document = nlpStub.analyze(inputText);
      List<Sentence> sentenceList = document.getSentencesList();
      for (Sentence sentence : sentenceList) {
        List<Morpheme> morpsList = sentence.getMorpsList();
        for (int i = 0; i < morpsList.size(); i++) {
          Morpheme morpheme = morpsList.get(i);
          if (i > 0 && ((StringUtils.equals(morpsList.get(i - 1).getType(), "nc") && StringUtils
              .equals(morpheme.getType(), "xsn"))
              || (StringUtils.equals(morpsList.get(i - 1).getType(), "pv") && StringUtils
              .equals(morpheme.getType(), "etn")))) {
            String temp = strList.get(strList.size() - 1);
            strList.remove(strList.size() - 1);
            strList.add(temp + morpheme.getLemma());
          } else if (!StringUtils.startsWithAny(morpheme.getType(), "j", "e", "x", "c", "s")) {
            strList.add(morpheme.getLemma());
          }
        }
      }
      String result = StringUtils.join(strList, " ");
      return result;
    } catch (Exception e) {
      return question;
    }
  }

  private Builder getDBAnswer(Builder resultQA, QuestionInput questionInput) throws Exception {
    Map<String, Object> params = new HashMap<>();
    params.put("question", questionInput.getQuestion());
    params.put("limit", questionInput.getNtop());
    try {
      List<String> list = sqlSession.selectList("mysql.selectQuestion", params);
      for (String answer : list) {
        DBResult dbResult = DBResult.newBuilder().setAnswer((answer == null ? "" : answer)).build();
        resultQA.addDbResult(dbResult);
      }
    } catch (Exception e) {
      e.printStackTrace();
      SqlSessionManager.closeSqlSession();
      throw new Exception();
    }
    return resultQA;
  }
}
