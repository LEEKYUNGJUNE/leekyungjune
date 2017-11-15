#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys

import grpc
from google.protobuf import empty_pb2
from google.protobuf import json_format

from minds.qa import qa_pb2
from minds.qa import nlqa_pb2
from minds import lang_pb2
from common.config import Config

from mrc.mrc_search import SearchAnswerCandidate
from mrc.mrc_passage import GenerateUnstructuredCandidate

conf = Config()
stub = None
class NaturalLanguageQuestionAnswering:

    def __init__(self):
        #remote = "125.132.250.243:9861"
        remote = "172.31.30.213:" + conf.get("minds-qa.question-analysis.port")
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


if __name__ == '__main__':
    print("1. File")
    print("2. Command")

    select_menu = raw_input("선택 : ")
    select_menu = int(select_menu)

    if select_menu > 2 or select_menu < 1:
        print("Wrong Select")
        sys.exit(1)

    conf = Config()
    conf.init("minds-qa.conf")
    nlqa = NaturalLanguageQuestionAnswering()
    nlqa.get_provider()
    
    print("결과는 nlqa_output.txt에 저장됩니다.")
    if select_menu == 1:
        file_path = raw_input("File을 입력하세요(경로 포함) : ")
        file_path = file_path.strip()
        with open(file_path, "r") as f:
            question_list = f.readlines()

        for question in question_list:
            nlqa_result = nlqa.analyze(question)
            print(nlqa_result)
            result_file.write(nlqa_result.strip()+"\n")

    elif select_menu == 2:
        while True:
            input_text = raw_input("입력 : ")
            if input_text == "q" or input_text =="quit":
                break
            else:
                nlqa_result = nlqa.analyze(input_text)
                print(nlqa_result)
                result_file.write(nlqa_result.strip()+"\n")

    result_file.close()
