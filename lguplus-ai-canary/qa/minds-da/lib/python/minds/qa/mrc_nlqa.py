#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys

import grpc
from google.protobuf import empty_pb2
from google.protobuf import json_format

exe_path = os.path.realpath(sys.argv[0])
bin_path = os.path.dirname(exe_path)
lib_path = os.path.realpath(bin_path + "/../minds/lib/python")
from minds.qa import qa_pb2
from minds.qa import nlqa_pb2
from common.config import Config


conf = Config()
stub = None
class NaturalLanguageQuestionAnswering:

    def __init__(self, remote):
        #remote = "125.132.250.243:" + conf.get("minds-qa.question-analysis.port")
        #remote = "172.31.30.213:" + conf.get("minds-qa.question-analysis.port")
        channel = grpc.insecure_channel(remote)
        self.stub = qa_pb2.QuestionAnswerServiceStub(channel)

    def get_provider(self):
        ret = self.stub.GetProvider(empty_pb2.Empty())
        json_ret = json_format.MessageToJson(ret, True)
        print(json_ret)

    def analyze(self, text):
        in_text = nlqa_pb2.QuestionAnalysisInputText()
        in_text.text = text

        ret = self.stub.QuestionAnalyze(in_text)
        nlqa_result = ret.result.encode("utf-8")
        return nlqa_result
