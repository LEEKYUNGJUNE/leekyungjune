package ai.mindslab.util;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class PropertiesManager {

  private static Properties properties;

  private static Logger logger = LoggerFactory.getLogger(PropertiesManager.class);

  private PropertiesManager() {
  }

  public static Properties getProperties() {
    if (properties == null) {
      properties = new Properties();
      InputStream is = null;
      try {
        String propertiesPath = System.getProperty("propertiesPath");
        if (propertiesPath != null) {
          is = new FileInputStream(propertiesPath);
        } else {
          logger.warn("System Property is Null. PropertyName is 'propertiesPath'");
          is = PropertiesManager.class.getClassLoader().getResourceAsStream("qa.properties");
        }
        properties.load(is);
      } catch (FileNotFoundException e) {
        e.printStackTrace();
      } catch (IOException e) {
        e.printStackTrace();
      } finally {
        try {
          is.close();
        } catch (IOException e) {
          e.printStackTrace();
        }
      }
    }
    return properties;
  }
}
