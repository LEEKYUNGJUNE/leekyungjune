#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
reload(sys)
sys.setdefaultencoding('utf-8')

exe_path = os.path.realpath(sys.argv[0])
bin_path = os.path.dirname(exe_path)
lib_path = os.path.realpath(bin_path+"/../lib/python")
sys.path.append(lib_path)
log_path = os.path.realpath(bin_path+"/../logs")

from minds.maum.da import provider_pb2
from minds.maum.da import provider_pb2_grpc

from concurrent import futures

import grpc
from google.protobuf import empty_pb2
import time
import logging
from logging.handlers import TimedRotatingFileHandler


def run():
    logger = logging.getLogger("da")
    logger.setLevel(logging.DEBUG)
    fileHandler = TimedRotatingFileHandler(log_path + '/da_hang.log', when='midnight', interval=1, backupCount=5)
    formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    channel = grpc.insecure_channel('localhost:9907')
    stub = provider_pb2_grpc.DialogAgentProviderStub(channel)

    while True:
        response = stub.IsReady(empty_pb2.Empty())
        print (response)
        logger.info("Success!!")
        time.sleep(60)



if __name__ == "__main__":
    run()

