#!/usr/bin/python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import ConfigParser
import logging

CONFIG_FILE = "Tlo.cfg"

config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)

path = config.get("TLO", "PATH")

class Make_FD():
    def __init__(self):
        self.logger = logging.getLogger('TLO')
        self.logger.setLevel(logging.INFO)
        self.fileHandler = ''

    def mkFD(self, flag=True):
        time = datetime.today().strftime("%Y%m%d%H%M%S%f")[:-4]

        if os.path.isdir(path + str(time)[0:8]):
            pass
        else:
            os.mkdir(path + str(time)[0:8])

        temp_path = path + str(time)[0:8] + '/'

        if int(time[11]) < 5:
            time = time[0:11] + "0"
        else:
            time = time[0:11] + "5"

        with open(temp_path + 'DA.' + config.get("TLO", "SERVER") + '.' + str(time) + '.log', 'a') as f:
            f.close()
            pass
        if flag:
            self.logger.removeHandler(self.fileHandler)
        self.fileHandler = logging.FileHandler(temp_path + 'DA.' + config.get("TLO", "SERVER") + '.' + str(time) + '.log')
        self.logger.addHandler(self.fileHandler)
        #fileHandler.__init__()

    def run(self):

        print "mkFD is working"

        self.mkFD(False)

        sched = BackgroundScheduler()

        sched.add_job(self.mkFD, 'cron', minute='*/5')

        sched.start()

mk = Make_FD()
mk.run()
