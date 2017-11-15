package ai.mindslab.basicQA;

import ai.mindslab.util.PropertiesManager;
import ai.mindslab.util.SqlSessionManager;
import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.LoggerContext;
import ch.qos.logback.classic.encoder.PatternLayoutEncoder;
import ch.qos.logback.classic.joran.JoranConfigurator;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.Appender;
import ch.qos.logback.core.FileAppender;
import ch.qos.logback.core.joran.spi.JoranException;
import ch.qos.logback.core.util.StatusPrinter;
import io.grpc.Server;
import io.grpc.netty.NettyServerBuilder;
import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Properties;
import java.util.concurrent.TimeUnit;
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.lang3.time.DateUtils;
import org.apache.ibatis.session.SqlSession;
import org.apache.solr.client.solrj.SolrClient;
import org.apache.solr.client.solrj.impl.HttpSolrClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class BasicQAServerMain {

  private static Properties properties = PropertiesManager.getProperties();

  private static Logger logger = LoggerFactory.getLogger(BasicQAServerMain.class);

  private Server server;

  private SolrClient solrClient;

  public static void main(String[] args) {
    BasicQAServerMain qaServerMain = new BasicQAServerMain();
    qaServerMain.setLog();
    qaServerMain.execute();
    qaServerMain.blockUntilShutdown();
  }

  private void setLog() {
    LoggerContext loggerContext = (LoggerContext) LoggerFactory.getILoggerFactory();
    JoranConfigurator joranConfigurator = new JoranConfigurator();
    joranConfigurator.setContext(loggerContext);
    loggerContext.reset();
    try {
      joranConfigurator.doConfigure(properties.getProperty("TLO_CONFIG_PATH"));

      FileAppender fileAppender = new FileAppender();
      fileAppender.setContext(loggerContext);
      fileAppender.setName("FILE");
      fileAppender.setFile(getLogFileName());

      PatternLayoutEncoder encoder = new PatternLayoutEncoder();
      encoder.setContext(loggerContext);
      encoder.setPattern("%msg%n");
      encoder.start();

      fileAppender.setEncoder(encoder);
      fileAppender.start();

      ch.qos.logback.classic.Logger logbackLogger = loggerContext.getLogger("TLO");
      logbackLogger.setLevel(Level.INFO);
      logbackLogger.addAppender(fileAppender);


      new ClassPathXmlApplicationContext("classpath:/spring/spring-quartz.xml");
    } catch (JoranException e) {
      e.printStackTrace();
    }
    StatusPrinter.printInCaseOfErrorsOrWarnings(loggerContext);

  }

  private void execute() {
    try {
      logger.info("{}", "Basic QA Server Start");
      long idleTimeout = Integer.parseInt(properties.getProperty("TIMEOUT", "5"));
      long ageTimeout = Integer.parseInt(properties.getProperty("TIMEOUT", "5"));
      int port = Integer.parseInt(properties.getProperty("QA_PORT", "50051"));
      SqlSession sqlSession = SqlSessionManager.getSqlSession();
      solrClient = new HttpSolrClient.Builder(properties.getProperty("SOLR_URL", "http://127.0.0.1:8983/solr/wiseQA")).build();
      server = NettyServerBuilder.forPort(port)
          .maxConnectionIdle(idleTimeout, TimeUnit.SECONDS)
          .maxConnectionAge(ageTimeout, TimeUnit.SECONDS)
          .addService(new BasicQAService(sqlSession, solrClient)).build().start();
      Runtime.getRuntime().addShutdownHook(new Thread() {
        @Override
        public void run() {
          BasicQAServerMain.this.stop();
        }
      });
    } catch (IOException e) {
      e.printStackTrace();
    }

  }

  private void blockUntilShutdown() {
    if (server != null) {
      try {
        server.awaitTermination();
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
    }
  }

  private void stop() {
    if (server != null) {
      server.shutdown();
    }
  }

  public String getLogFileName() {
    SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyyMMddHHmm");
    Date now = new Date();
    String nowDT = simpleDateFormat.format(now);
    int min = Integer.parseInt(StringUtils.substring(nowDT, -2));
    int amount = min % 5;
    Date logDate = DateUtils.addMinutes(now, -amount);
    String dt = simpleDateFormat.format(logDate);
    String logFileName = properties.getProperty("TLO_FILE_PRE_FORMAT", "BASICQA.001.")  + dt + ".log";
    String logPathName = properties.getProperty("TLO_OUTPUT_PATH") + File.separator + StringUtils.substring(dt, 0, 8);
    File logPath = new File(logPathName);
    if (!logPath.exists()) {
      logPath.mkdirs();
    }
    String fullPathName = logPathName + File.separator + logFileName;
    File logFile = new File(fullPathName);
    if (!logFile.exists()) {
      try {
        logFile.createNewFile();
      } catch (IOException e) {
        e.printStackTrace();
      }
    }
    return fullPathName;
  }
}
