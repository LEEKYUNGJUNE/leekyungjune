#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import json
import logging

import grpc

#from minds.qa.mrc_nlqa import NaturalLanguageQuestionAnswering
from mrc.minds_mrc_pb2 import MrcInput, MrcPassage, MRCStub
from minds.qa import semanticSearch_pb2
from minds.qa import semanticSearch_pb2_grpc
import mrc.util

def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

class MrcClient:
    search_channel = None
    search_client = None

    def __init__(self, sh):
        # ==========CONSTANT VARIABLE==========
        self.WINDOW_SIZE = 5
        self.DOC_THRESHOLD = 10
        self.DOC_TYPE = "news"
        self.ANSWER_THRESHOLD = 0.7
        # =====================================
        #self.nlqa = NaturalLanguageQuestionAnswering("172.31.30.213:9861")
        self.search_channel = grpc.insecure_channel('172.31.25.34:30052')
        self.search = semanticSearch_pb2_grpc.SemanticSearchServiceStub(self.search_channel)
        #self.mrc_channel = grpc.insecure_channel('{}:{}'.format('172.31.5.106', 50001))
        self.mrc_channel = grpc.insecure_channel(sh)
        self.mrc_client = MRCStub(self.mrc_channel)
        # for time check
        self.entire_start_time = None
        self.start_time = None
        # set logger
        self.logger = self.set_logger()

    def set_logger(self):
        log = logging.getLogger(__name__)
        log.setLevel(logging.DEBUG)
        fh = logging.FileHandler('output.log')
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s >>> %(message)s',
                                      datefmt='%Y-%m-%d_%T %Z')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        log.addHandler(fh)
        log.addHandler(ch)
        return log

    def time_check(self, stage):
        self.logger.info("{}: {:.5}s".format(stage, float(time.time()-self.start_time)))
        self.start_time = time.time()

    def mrc(self, q, para_list, server, port, timeout):
        mrc_input = MrcInput()
        mrc_input.question = q
        for p in para_list:
            p_input = MrcPassage()
            p_input.original = p["original"]
            p_input.morp = str(p["morp"])
            p_input.words.extend(p["words"])
            mrc_input.passages.extend([p_input])
        mrc_outputs = self.mrc_client.SendQuestion(mrc_input,timeout)
        return mrc_outputs.answers

    def run(self, question, nlqa_result, timeout):
        self.logger.info("Input: {}".format(question))
        self.start_time = self.entire_start_time = time.time()

        # question analysis
        #nlqa_result = self.nlqa.analyze(question)  # TODO: replace it with exobrain result
        #self.time_check(stage="nlqa")

        sentences = json.loads(nlqa_result)["orgQInfo"]["orgQUnit"]["ndoc"]["sentence"]
        q_morp = mrc.util.get_tree_result(sentences, original_token=False)
        nlqa_result = nlqa_result + "||0||\n"
        exoSearchInput = semanticSearch_pb2.SemanticSearchInput(kbResult=nlqa_result,
                                                                thresHold=self.DOC_THRESHOLD,
                                                                windowSize=self.WINDOW_SIZE)
        self.time_check(stage="Prepare bm25 search")

        # semantic search
        bm25_ps = self.search.SearchBM25(exoSearchInput)
        #tic_ps = search.SearchTIC(exoSearchInput)
        #boolean_ps = search.SearchBoolean(exoSearchInput)
        self.time_check(stage="Bm25 search")

        result_dict = dict()
        for p in bm25_ps.semanticResults:
            if self.DOC_TYPE == "news" and p.docType != "news_passage":
                continue
            doc_morp_list = list()
            doc_word_list = list()
            for sent in p.passageMorp:
                morp_list, word_list = mrc.util.get_tree_result([eval(sent)["sentence"][1]], True)
                doc_morp_list += morp_list
                doc_word_list += word_list
            if p.docType in result_dict:
                result_dict[p.docType].append({"original": " ".join(doc_word_list),
                                               "morp": doc_morp_list,
                                               "words": doc_word_list,
                                               "rank": p.rank})
            else:
                result_dict[p.docType] = [{"original": " ".join(doc_word_list),
                                           "morp": doc_morp_list,
                                           "words": doc_word_list,
                                           "rank": p.rank}]

        passage_cnt_list = [len(result_dict[y]) for y in result_dict]
        for k in result_dict:
            self.logger.debug("\n".join(["{}: {}".format(x["rank"], x["original"]) for x in result_dict[k]]))
        self.logger.debug("Retrieved document cnt/type: {}".
                          format(zip(result_dict.keys(), passage_cnt_list)))
        if len(passage_cnt_list) <= 0:
            self.logger.error("There's no passage. Return None")
            return "", False
        else:
            para_list = list()
            for k in result_dict.keys():
                for p in result_dict[k]:
                    para_list.append(p)
            self.time_check(stage="Prepare MRC")

            mrc_outputs = self.mrc(str(q_morp), para_list, server='172.31.5.106', port=50001, timeout=timeout)
            self.time_check(stage="MRC")

            answer_dict = dict()
            for mrc_output in mrc_outputs:
                if mrc_output.answer not in answer_dict:
                    answer_dict[mrc_output.answer] = mrc_output.prob
                else:
                    if mrc_output.prob > answer_dict[mrc_output.answer]:
                        answer_dict[mrc_output.answer] = mrc_output.prob
            candi_answers = sorted(answer_dict.iteritems(), key=lambda (k, v): (v, k), reverse=True)
            self.time_check(stage="Find the answer")
            self.logger.info("{}: {:.5}s".format("-- Entire time", time.time() - self.entire_start_time))
            self.logger.debug(u"Candidate answers: {}".
                              format(", ".join([u"{}({:.5})".format(x[0], x[1]) for x in candi_answers])))
            self.logger.info(u"Output: {} ({})".format(candi_answers[0][0],
                                                              candi_answers[0][1]))
            if candi_answers[0][1] >= self.ANSWER_THRESHOLD:
                return candi_answers[0][0], True
            return "", False

if __name__ == "__main__":
    mc = MrcClient()
    q = "호텔현대는 얼마에 매각했는지 알려줘"
    a= mc.run(q)
    print("Q. '{}'".format(q))
    print(u"A. {}".format(a[0]))
