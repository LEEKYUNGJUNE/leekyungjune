#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import grpc

from minds.qa import basicQA_pb2
from minds.qa import basicQA_pb2_grpc
from google.protobuf import json_format

class BasicQA:
    def __init__(self,ch):
        self.channel = grpc.insecure_channel(ch)
        self.basic_stub = basicQA_pb2_grpc.BasicQAServiceStub(self.channel)
        
    def print_result(self, json_object):
        try:
            json_object = json.loads(json_object)
            for object in json_object:
                if object == "question":
                    return json_object["answer"]
                elif object == "searchResult":
                    for answer in json_object[object]:
                        return answer["answer"]
        except Exception as e:
            return ""
    
    def run(self, question, timeout, meta):
        parameter_qa = basicQA_pb2.QuestionInput(ntop=3, type=basicQA_pb2.ALL, question=question, meta=meta)
        result_qa = self.basic_stub.Question(parameter_qa, timeout)
        json_result = json_format.MessageToJson(result_qa, True)
        flag = True
        output_result = self.print_result(json_result)
        return output_result, flag

