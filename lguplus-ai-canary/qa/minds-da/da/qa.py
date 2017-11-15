# /usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import requests
import json
import grpc
import urllib, urllib2, time, random
import re

reload(sys)
sys.setdefaultencoding('utf-8')

# from google.protobuf import json_format

from util import Util
from basicQA import BasicQA
from mindsMRC import MrcClient
from hyperNet import HNetClient
import ConfigParser

# ========== CONFIGURATION FILE ==========
__CONFIG_FILE__ = "qa.cfg"
# ========================================

# WIKI_PATTERN = re.compile("((위키피디아|위키피디어|위키야|위키))")
# WIKI_STRING_PATTERN = re.compile("((위키|위키피디아|위키피디어)(.+)(알아|검색|확인)(.+))")

# ====================================================
# 정상
SUCCESS_STATUS_CODE = "20000000"
SUCCESS_STATUS_MESSAGE = "정상입니다."
# 기본QA Engine Down
BASICQA_STATUS_CODE_1 = "40000101"
BASICQA_STATUS_MESSAGE_1 = "Basic QA Engine 서버에 접속할 수 없습니다."
# 기본QA Engine Timeout
BASICQA_STATUS_CODE_2 = "40000102"
BASICQA_STATUS_MESSAGE_2 = "Basic QA Engine 서버 request timeout이 발생하였습니다."
# Wiki QA Engine Down
WIKI_STATUS_CODE_1 = "40000201"
WIKI_STATUS_MESSAGE_1 = "Wiki QA Engine 서버에 접속할 수 없습니다."
# Wiki QA Engine Timeout
WIKI_STATUS_CODE_2 = "40000202"
WIKI_STATUS_MESSAGE_2 = "Wiki QA Engine 서버 request timeout이 발생하였습니다."
# WiseQA Engine Down
WISEQA_STATUS_CODE_1 = "40000301"
WISEQA_STATUS_MESSAGE_1 = "WiseQA Engine 서버에 접속할 수 없습니다."
# WiseQA Engine Timeout
WISEQA_STATUS_CODE_2 = "40000302"
WISEQA_STATUS_MESSAGE_2 = "WiseQA Engine 서버 request timeout이 발생하였습니다."
# MRC QA Engine Down
MRC_STATUS_CODE_1 = "40000401"
MRC_STATUS_MESSAGE_1 = "MRC QA Engine 서버에 접속할 수 없습니다."
# MRC QA Engine Timeout
MRC_STATUS_CODE_2 = "40000402"
MRC_STATUS_MESSAGE_2 = "MRC QA Engine 서버 request timeout이 발생하였습니다."
# HyperNet QA Engine Down
HYPERNET_STATUS_CODE_1 = "40000501"
HYPERNET_STATUS_MESSAGE_1 = "HyperNet QA Engine 서버에 접속할 수 없습니다."
# HyperNet QA Engine Timeout
HYPERNET_STATUS_CODE_2 = "40000502"
HYPERNET_STATUS_MESSAGE_2 = "HyperNet QA Engine 서버 request timeout이 발생하였습니다."

ENGINE_STATUS_CODE = ""
ENGINE_STATUS_MESSAGE = ""


# ====================================================


class QA:
    global qa_util
    qa_util = Util()

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(__CONFIG_FILE__)
        self.basic_qa = BasicQA(config.get("URL", "BASICQA"))
        self.__WIKI_URL__ = config.get("URL", "WIKI")
        self.__WISE_QA_URL__ = config.get("URL", "WISEQA")
        self.mrc = MrcClient(config.get("URL", "MRC"))
        self.hnet = HNetClient(config.get("URL", "HNET"))
        self.__FILTER_WORD_LIST__ = config.get("FILTER", "WORD").strip().split(",")
        self.__TIMEOUT__ = int(config.get("TIMEOUT", "TIMEOUT"))

    def general_wiki(self, text, meta):
        value_output_result = ""
        full_value_output_result = ""
        flag = False
        text = qa_util.delete_wiki_keyword_and_stopword(text)
        try:
            query_url = self.__WIKI_URL__ + text
            request = requests.post(url=query_url, data=qa_util.dict_upper(meta), timeout=self.__TIMEOUT__, headers={'Connection': 'close', 'Content-Type': 'application/x-www-form-urlencoded'})
            if (request.status_code != 200):
                value_output_result = qa_util.get_def_error_msg()
                ENGINE_STATUS_CODE = WIKI_STATUS_CODE_1
                ENGINE_STATUS_MESSAGE = WIKI_STATUS_MESSAGE_1
            else:
                request_text = request.text
                json_loads = json.loads(request_text)
                hits = json_loads['hits']
                value_output_result = self.__get_object_values__(hits).encode('utf-8')
                full_value_output_result = self.__get_object_full_values__(hits).encode('utf-8')
                ENGINE_STATUS_CODE = SUCCESS_STATUS_CODE
                ENGINE_STATUS_MESSAGE = SUCCESS_STATUS_MESSAGE
        except requests.exceptions.Timeout as e:
            print(e)
            value_output_result = qa_util.get_def_error_msg()
            ENGINE_STATUS_CODE = WIKI_STATUS_CODE_2
            ENGINE_STATUS_MESSAGE = WIKI_STATUS_MESSAGE_2
        except Exception as e:
            print(e)
            value_output_result = qa_util.get_def_error_msg()
            ENGINE_STATUS_CODE = WIKI_STATUS_CODE_1
            ENGINE_STATUS_MESSAGE = WIKI_STATUS_MESSAGE_1

        message, original_answer, flag = qa_util.recognize_answer(text=text, output_result=value_output_result)
        full_value_output_result = qa_util.recognize_full_value_wiki(full_value_output_result)

        return message, full_value_output_result, flag, ENGINE_STATUS_CODE, ENGINE_STATUS_MESSAGE

    # Basic QA
    def base_qa(self, text, meta):
        output_result = ""
        json_result = ""
        message = ""
        original_answer = ""
        text = qa_util.delete_wiki_keyword_and_stopword(text)

        try:
            answer, flag = self.basic_qa.run(text,self.__TIMEOUT__, meta)
            ENGINE_STATUS_CODE = SUCCESS_STATUS_CODE
            ENGINE_STATUS_MESSAGE = SUCCESS_STATUS_MESSAGE
        except grpc.RpcError as e:
            print(e)
            answer = ''
            print(e.code().value[0])
            if e.code().value[0] == 4:
                print("time out in basic qa")
                ENGINE_STATUS_CODE = BASICQA_STATUS_CODE_2
                ENGINE_STATUS_MESSAGE = BASICQA_STATUS_MESSAGE_2
            else:
                ENGINE_STATUS_CODE = BASICQA_STATUS_CODE_1
                ENGINE_STATUS_MESSAGE = BASICQA_STATUS_MESSAGE_1

        message, original_answer, flag = qa_util.recognize_answer(text=text, output_result=answer)
        return message, original_answer, flag, ENGINE_STATUS_CODE, ENGINE_STATUS_MESSAGE

    def wise_qa(self, text):
        text = qa_util.delete_wiki_keyword_and_stopword(text)
        # data = [("question", text), ("wsConnID", "")]
        data = {"question": text, "wsConnID": ""}
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        # data = urllib.urlencode(data)
        # url_request = urllib2.Request(self.__WISE_QA_URL__, data)
        # url_request.add_header("Content-type", "application/x-www-form-urlencoded")

        flag = False
        res = None
        nlqa_result = ""
        try:
            # res = urllib2.urlopen(url_request, timeout=self.__TIMEOUT__)
            # res = requests.post(self.__WISE_QA_URL__, data=data, headers=headers, timeout=self.__TIMEOUT__)
            res = requests.post(self.__WISE_QA_URL__, data=data, headers=headers,
                                timeout=self.__TIMEOUT__)
            if (res.status_code != requests.codes.ok):
                answer = qa_util.get_def_error_msg()
                ENGINE_STATUS_CODE = WISEQA_STATUS_CODE_1
                ENGINE_STATUS_MESSAGE = WISEQA_STATUS_MESSAGE_1
            else:
                flag = True
                ENGINE_STATUS_CODE = SUCCESS_STATUS_CODE
                ENGINE_STATUS_MESSAGE = SUCCESS_STATUS_MESSAGE
        except requests.exceptions.Timeout as e:
            print(e)
            ENGINE_STATUS_CODE = WISEQA_STATUS_CODE_2
            ENGINE_STATUS_MESSAGE = WISEQA_STATUS_MESSAGE_2
        except Exception as e:
            print(e)
            ENGINE_STATUS_CODE = WISEQA_STATUS_CODE_1
            ENGINE_STATUS_MESSAGE = WISEQA_STATUS_MESSAGE_1

        if flag == True:
            try:
                res = res.text
                result = qa_util.parse_with_stdlib(res, "info")
                question, answer = result[0].split("||0||", 1)

                # temp
                nlqa_result = result[0].split("||0||")[0]

                question_json = json.loads(question)
                answer_json = json.loads(answer)
                # 2017/08/10 yghwang
                if answer_json["AnswerUnitOut"]["AnsUnit_TotalCnt"] != 0:
                    answer = answer_json["AnswerUnitOut"]["AnsUnit"][0]["answer"]
                else:
                    answer = ""
                    nlqa_result = result[0].split("||0||")[0]
                    flag = False
            except Exception as e:
                print(e)
                answer = ""
                flag = False
        else:
            answer = ""

        message, original_answer, flag = qa_util.recognize_answer(text=text, output_result=answer)
        return message, original_answer, flag, nlqa_result

    def mindsMRC(self, text, nlqa_result):
        text = qa_util.delete_wiki_keyword_and_stopword(text)
        try:
            answer, flag = self.mrc.run(text, nlqa_result, self.__TIMEOUT__)
            ENGINE_STATUS_CODE = SUCCESS_STATUS_CODE
            ENGINE_STATUS_MESSAGE = SUCCESS_STATUS_MESSAGE
        except grpc.RpcError as e:
            print(e)
            answer = ''
            print(e.code().value[0])
            if e.code().value[0] == 4:
                print("time out in mrc")
                ENGINE_STATUS_CODE = MRC_STATUS_CODE_2
                ENGINE_STATUS_MESSAGE = MRC_STATUS_MESSAGE_2
            else:
                ENGINE_STATUS_CODE = MRC_STATUS_CODE_1
                ENGINE_STATUS_MESSAGE = MRC_STATUS_MESSAGE_1

        message, original_answer, flag = qa_util.recognize_answer(text=text, output_result=answer)
        return message, original_answer, flag, ENGINE_STATUS_CODE, ENGINE_STATUS_MESSAGE
    

    def hyperNet(self, text, nlqa_result):
        text = qa_util.delete_wiki_keyword_and_stopword(text)
        try:
            answer, flag = self.hnet.run(text, nlqa_result, self.__TIMEOUT__)
            ENGINE_STATUS_CODE = SUCCESS_STATUS_CODE
            ENGINE_STATUS_MESSAGE = SUCCESS_STATUS_MESSAGE
        except grpc.RpcError as e:
            print(e)
            answer = ''
            print(e.code().value[0])
            if e.code().value[0] == 4:
                print("time out in hyper")
                ENGINE_STATUS_CODE = HYPERNET_STATUS_CODE_2
                ENGINE_STATUS_MESSAGE = HYPERNET_STATUS_MESSAGE_2
            else:
                ENGINE_STATUS_CODE = HYPERNET_STATUS_CODE_1
                ENGINE_STATUS_MESSAGE = HYPERNET_STATUS_MESSAGE_1

        message, original_answer, flag = qa_util.recognize_answer(text=text, output_result=answer)
        return message, original_answer, flag, ENGINE_STATUS_CODE, ENGINE_STATUS_MESSAGE


    # 여기서 괄호 없애도 됨
    def __get_object_values__(self, hits):
        hitsArray = hits['hits']
        search_type = hits['search_type']
        lenHitsArray = len(hitsArray)
        text_list = []
        if lenHitsArray == 0:
            return qa_util.get_nothing_found_msg()
        elif lenHitsArray == 1:
            if search_type == 'abstracts':
                if hits['is_view_subject'] == 1:
                    # if hits['is_view_subject'] == 0:
                    return hitsArray[0]['_source']['value']  # 챗봇 로직
            elif search_type == 'backward':
                return hitsArray[0]['_source']['subject']
            elif search_type == 'triples':
                return (hits['entity'] if hits['entity'] else hitsArray[0]['_source']['subject']) + ' ' + hits[
                    'attribute'] + ' ' + hitsArray[0]['_source']['value']
            return hitsArray[0]['_source']['value']
        else:
            if search_type == 'triples':
                text_list.append(
                    (hits['entity'] if hits['entity'] else hitsArray[0]['_source']['subject']) + ' ' + hits[
                        'attribute'] + ' \n')

        for index, hitElem in enumerate(hitsArray):
            text_list.append(hitElem['_source']['value'])
            if hits['is_view_subject'] == 1:
                text_list.append(' (')
                text_list.append(hitElem['_source']['subject'])
                if hitElem['_source']['gubun']:
                    text_list.append(', ')
                    text_list.append(hitElem['_source']['gubun'])
                text_list.append(')')
            if index != lenHitsArray - 1:
                text_list.append(',')
            text_list.append('\n')

        text_list.append('등 ')

        return ''.join(text_list)

    # 여기서 괄호 없애도 됨
    def __get_object_full_values__(self, hits):
        hitsArray = hits['hits']
        search_type = hits['search_type']
        lenHitsArray = len(hitsArray)
        text_list = []
        if lenHitsArray == 0:
            return qa_util.get_nothing_found_msg()
        elif lenHitsArray == 1:
            if search_type == 'abstracts':
                if hits['is_view_subject'] == 1:
                    # if hits['is_view_subject'] == 0:
                    return hitsArray[0]['_source']['full_value']  # 챗봇 로직
            elif search_type == 'backward':
                return hitsArray[0]['_source']['subject']
            elif search_type == 'triples':
                return (hits['entity'] if hits['entity'] else hitsArray[0]['_source']['subject']) + ' ' + hits[
                    'attribute'] + ' ' + hitsArray[0]['_source']['full_value']
            return hitsArray[0]['_source']['full_value']
        else:
            if search_type == 'triples':
                text_list.append(
                    (hits['entity'] if hits['entity'] else hitsArray[0]['_source']['subject']) + ' ' + hits[
                        'attribute'] + ' \n')

        for index, hitElem in enumerate(hitsArray):
            text_list.append(hitElem['_source']['full_value'])
            if hits['is_view_subject'] == 1:
                text_list.append(' (')
                text_list.append(hitElem['_source']['subject'])
                if hitElem['_source']['gubun']:
                    text_list.append(', ')
                    text_list.append(hitElem['_source']['gubun'])
                text_list.append(')')
            if index != lenHitsArray - 1:
                text_list.append(',')
            text_list.append('\n')

        text_list.append('등 ')

        return ''.join(text_list)

    def filter_question(self, text):
        filter_flag = False
        message = ""
        for filter_word in self.__FILTER_WORD_LIST__:
            if text.lower().find(filter_word) != -1:
                filter_flag = True

        message = qa_util.filter_error_message()

        return message, filter_flag

    def mk_nlqa(self, question):
        nlqa_ch = NaturalLanguageQuestionAnswering("13.124.164.53:9861")
        nlqa_result = nlqa_ch.analyze(question, self.__TIMEOUT__)
        return nlqa_result

