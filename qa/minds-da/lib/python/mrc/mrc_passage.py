#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import sys

import grpc

from mrc_passage_search import PassageSearch

from minds.qa import qa_pb2
from minds.qa import cangen_pb2
from common.config import Config

# ========== CONSTANT VARIABLE ==========
WINDOW_SIZE = 6
# =======================================


class GenerateUnstructuredCandidate:
    conf = Config()
    stub = None
    global passage_search
    passage_search = PassageSearch()

    def __init__(self):
        remote = "172.31.30.213:" + self.conf.get("minds-qa.generate-unstructured-candidate.port")
        #remote = "13.124.164.53:" + self.conf.get("minds-qa.generate-unstructured-candidate.port")
        channel = grpc.insecure_channel(remote)
        self.stub = qa_pb2.QuestionAnswerServiceStub(channel)

    def search_unstructured_candidate(self, text):
        in_text = cangen_pb2.UnstructuredCandidateInputText()
        in_text.text = text 
        result = self.stub.GenerateUnstructuredCandidate(in_text)
        result_unstructured_candidate = result.result
        result_unstructured_candidate = result_unstructured_candidate.encode("utf-8")
        token = result_unstructured_candidate.split("||0||")
        json_result = json.loads(token[1])
        result_dict = passage_search.get_passage_search_result_list(json_result, WINDOW_SIZE)
        return result_dict


