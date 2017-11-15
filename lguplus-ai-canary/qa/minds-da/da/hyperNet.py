#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import operator
import json
import logging

import grpc

sys.path.append("/srv/minds/lib/python")
from minds.qa.mrc_nlqa import NaturalLanguageQuestionAnswering
from minds.qa import semanticSearch_pb2
from minds.qa import semanticSearch_pb2_grpc
from minds.qa.hyper_util import get_tree_result, map_original_idx
import HNet_pb2
import HNet_pb2_grpc

def list_dic_to_string(list):
    list_string = ""
    frist = True
    for i in list:
        if frist:
            list_string = "[" + json.dumps(i, ensure_ascii=False)
            frist = False
        else:
            list_string += "," + json.dumps(i, ensure_ascii=False)
    list_string += "]"
    return list_string

class HNetClient:
    search_channel = None
    search_client = None

    def __init__(self, sh):
        # ==========CONSTANT VARIABLE==========
        self.WINDOW_SIZE = 5
        self.DOC_THRESHOLD = 12
        self.DOC_TYPE = "news"
        self.ANSWER_THRESHOLD = 0.7
        # =====================================

        self.nlqa_ch = NaturalLanguageQuestionAnswering("13.124.164.53:9861")

        self.search_channel = grpc.insecure_channel('52.78.110.236:30052')
        self.search = semanticSearch_pb2_grpc.SemanticSearchServiceStub(self.search_channel)

        self.hnet_channel = grpc.insecure_channel(sh)
        #self.hnet_channel = grpc.insecure_channel('147.46.219.124:32795')

        self.hnet_stub = HNet_pb2_grpc.HNetStub(self.hnet_channel)

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
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt='[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s >>> %(message)s',
                                      datefmt='%Y-%m-%d_%T %Z')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        #log.addHandler(fh)
        log.addHandler(ch)
        return log

    def time_check(self, stage):
        self.logger.info("{}: {:.5}s".format(stage, float(time.time()-self.start_time)))
        self.start_time = time.time()

    def hy_test(self, q_dict, para_list, timeout):

        hyper_input = HNet_pb2.HNetInput()
        hyper_input.question_original = q_dict["original"]
        hyper_input.question = str(q_dict["morp"])
        #hyper_input.question = list_dic_to_string(q_morp)
        hyper_input.question_dp = str(q_dict["depen"])
        #hyper_input.question_dp = list_dic_to_string(q_depen)

        for p in para_list:
            p_input = HNet_pb2.HNetDoc()
            p_input.context_original = p["original"]
            p_input.context = str(p["morp"])
            #p_input.context = list_dic_to_string(p["morp"])
            p_input.dp = str(p["depen"])
            #p_input.dp = list_dic_to_string(p["depen"])
            hyper_input.docs.extend([p_input])

        response = self.hnet_stub.Predict(hyper_input, timeout)

        return response.answers

    def mk_q_form(self, nlqa_result):
        q_dict = dict()
        if len(nlqa_result) == 0:
            nlqa_result = self.nlqa_ch.analyze(nlqa_result)
            return nlqa_result
        sentences = json.loads(nlqa_result)["orgQInfo"]["orgQUnit"]["ndoc"]["sentence"]
        q_dict["original"], q_dict["morp"], q_dict["depen"] = get_tree_result(sentences, original_token=False)
        return q_dict

    def semantic_search(self, nlqa_passing):
        exoSearchInput = semanticSearch_pb2.SemanticSearchInput(kbResult=nlqa_passing+ "||0||\n",
                                                                thresHold=self.DOC_THRESHOLD,
                                                                windowSize=self.WINDOW_SIZE)
        bm25_ps = self.search.SearchBM25(exoSearchInput)

        return bm25_ps

    def mk_parsing_form(self, bm25_ps):
        result_dict = dict()

        for p in bm25_ps.semanticResults:
            if self.DOC_TYPE == "news" and p.docType != "news_passage":
                continue
            doc_morp_list = list()
            doc_word_list = list()
            doc_depen_list = list()

            for sent in p.passageMorp:
                morp_list, word_list, depen_list = get_tree_result([eval(sent)["sentence"][1]], True)
                doc_morp_list += morp_list
                doc_word_list += word_list
                doc_depen_list += depen_list

            if p.docType in result_dict:
                result_dict[p.docType].append({"original": " ".join(doc_word_list),
                                               "morp": doc_morp_list,
                                               "words": doc_word_list,
                                               "depen": doc_depen_list})
            else:
                result_dict[p.docType] = [{"original": " ".join(doc_word_list),
                                               "morp": doc_morp_list,
                                               "words": doc_word_list,
                                               "depen": doc_depen_list}]

        passage_cnt_list = [len(result_dict[y]) for y in result_dict]
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

        return para_list

    def mk_answer(self, answers, para_list):
        map_dic_list = list()
        flag = False
        for p in para_list:
            map_dic_list.append(map_original_idx(p["morp"], p["words"]))

        for i, map_dic in enumerate(map_dic_list):
            if answers[i].answer[0] != -1:
                real_answer = para_list[i]["original"][map_dic[answers[i].answer[0]][0]:map_dic[answers[i].answer[1]][1]]
                flag = True
                return real_answer, flag
        return "", flag


    def run(self, question, nlqa_result, timeout):
        self.logger.info("Input: {}".format(question))

        self.start_time = self.entire_start_time = time.time()

        q_dict = self.mk_q_form(nlqa_result)

        bm25_ps = self.semantic_search(nlqa_result)

        para_list = self.mk_parsing_form(bm25_ps)

        self.time_check(stage="Prepare HNet")

        outputs = self.hy_test(q_dict, para_list, timeout)

        self.time_check(stage="End HNet")

        answer, flag = self.mk_answer(outputs, para_list)

        return answer, flag
