package ai.mindslab.tlo;

import ai.mindslab.util.PropertiesManager;
import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.LoggerContext;
import ch.qos.logback.core.FileAppender;
import ch.qos.logback.core.util.StatusPrinter;
import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Properties;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component(value = "tloLogTask")
public class TloLogTask {

  private static Properties properties = PropertiesManager.getProperties();

  public void rollingLog() {
    LoggerContext loggerContext = (LoggerContext) LoggerFactory.getILoggerFactory();
    Logger tloLogger = loggerContext.getLogger("TLO");
    FileAppender fileAppender = (FileAppender) tloLogger.getAppender("FILE");
    SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyyMMddHHmm");
    String dt = simpleDateFormat.format(new Date());
    // set the file name
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
    fileAppender.setFile(fullPathName);
    fileAppender.start();
//    tloLogger.addAppender(fileAppender);

//    StatusPrinter.print(loggerContext);
  }
}
