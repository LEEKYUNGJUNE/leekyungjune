#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import grpc

exe_path = os.path.realpath(sys.argv[0])
bin_path = os.path.dirname(exe_path)
lib_path = os.path.realpath(bin_path+"/../lib/python")
sys.path.append(lib_path)

from minds.qa import search_pb2
from common.config import Config


def bm25_search_multi(nlqa_result, remote):
    channel = grpc.insecure_channel(remote)
    stub = search_pb2.ExoSearchServiceStub(channel)
    nlqa_result = nlqa_result + "||0||\n"
    search_input = search_pb2.ExoSearchInput(kbResult=nlqa_result)
    bm25_result = stub.SearchBM25(search_input)
    return bm25_result.searchResult.encode("utf-8")

class SearchAnswerCandidate:
    conf = Config()
    stub = None

    def __init__(self, remote):
        channel = grpc.insecure_channel(remote)
        self.stub = search_pb2.ExoSearchServiceStub(channel)

    def bm25_search(self, nlqa_result):
        nlqa_result = nlqa_result + "||0||\n"
        search_input = search_pb2.ExoSearchInput(kbResult=nlqa_result)
        bm25_result = self.stub.SearchBM25(search_input)
        return str(bm25_result.searchResult.encode("utf-8"))

    def tic_search(self, nlqa_result):
        nlqa_result = nlqa_result + "||0||\n"
        search_input = search_pb2.ExoSearchInput(kbResult=nlqa_result)
        tic_result = self.stub.SearchTIC(search_input)
        return tic_result.searchResult.encode("utf-8")

    def boolean_search(self, nlqa_result):
        nlqa_result = nlqa_result + "||0||\n"
        search_input = search_pb2.ExoSearchInput(kbResult=nlqa_result)
        boolean_result = self.stub.SearchBoolean(search_input)
        return boolean_result.searchResult.encode("utf-8")

    def evidence_retrieval(self, passage_result):
        evidence_input = search_pb2.ExoSearchInput(kbResult=passage_result)
        evidence_result = self.stub.SearchEvidenceRetrieval4Distribution_ORG(evidence_input)
        return evidence_result.searchResult.encode("utf-8")

if __name__ == "__main__":
    conf = Config()
    conf.init("minds-qa.conf")
    search = SearchAnswerCandidate("172.31.25.34:40052")
    with open("search_input", "r") as f:
        input_list = f.readlines()

    search_input = ""
    for input_text in input_list:
        search_input += input_text

    bm25_result = search.bm25_search(search_input)
    print(bm25_result)
    #tic_result = search.tic_search(search_input)
    #print(tic_result)
    #boolean_result = search.tic_search(search_input)
    #print(boolean_result)

