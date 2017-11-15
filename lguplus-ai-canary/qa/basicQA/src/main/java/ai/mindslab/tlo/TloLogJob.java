package ai.mindslab.tlo;

import lombok.Setter;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
import org.springframework.scheduling.quartz.QuartzJobBean;

public class TloLogJob extends QuartzJobBean {

  @Setter
  private TloLogTask tloLogTask;

  @Override
  protected void executeInternal(JobExecutionContext context) throws JobExecutionException {
    tloLogTask.rollingLog();
  }
}
