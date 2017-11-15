package ai.mindslab.util;

import ch.qos.logback.core.rolling.RollingFileAppender;

public class CustomAppender extends RollingFileAppender {

  private static long start = System.currentTimeMillis(); // minutes
  private int rollOverTimeInMinutes = 5;

  @Override
  public void rollover() {
    long currentTime = System.currentTimeMillis();
    int maxIntervalSinceLastLoggingInMillis = rollOverTimeInMinutes * 60 * 1000;

    if ((currentTime - start) >= maxIntervalSinceLastLoggingInMillis)
    {
      super.rollover();
      start = System.currentTimeMillis();
    }
  }
}
