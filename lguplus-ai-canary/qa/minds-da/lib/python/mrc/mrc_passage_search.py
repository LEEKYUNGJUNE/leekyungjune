#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import urllib, urllib2, json, time
from lxml import etree
import xml.etree.ElementTree as ElementTree
import grpc

from concurrent import futures
from google.protobuf import empty_pb2
from google.protobuf import json_format

from common.config import Config
from minds.qa import ps_pb2
from minds.qa import qa_pb2
from minds import lang_pb2

#======================================
# CONSTANT VARIABLE

#======================================
_WISE_QA_URL_PATH_ = "http://10.122.64.142:8080/servlet/UIMALangAnalisysServlet"
class PassageSearch:
    conf = Config()
    stub = None

    def __init__(self):
        self.conf.init("minds-qa.conf")
        remote = "172.31.30.213:" + self.conf.get("minds-qa.passage-search.port")
        #remote = "13.124.164.53:" + self.conf.get("minds-qa.passage-search.port")
        channel = grpc.insecure_channel(remote)
        self.stub = qa_pb2.QuestionAnswerServiceStub(channel)
    
    def __parse_with_stdlib__(self, content, tag):
        result_list = list()
        root = ElementTree.fromstring(content)
        for log in root.iter(tag):
            result_list.append(log.text)
        return result_list

    def __get_passage_search_result__(self, answer_json):
        
        count = 0
        passage_result_list = list()

        for answer in answer_json:
            sentence = answer["AnsSent"]["ASent"]
            content_provider_name = sentence[0]["cpname"]
            document_id = sentence[0]["docID"]
            sentence_id = sentence[0]["sentID"]
            for idx in range(int(sentence_id) - 1, int(sentence_id) + 2):
                if idx < 1:
                    continue
                else:
                    in_text = ps_pb2.PassageSearchInput()
                    in_text.provider = content_provider_name

                    if content_provider_name == "wiki_definition" or content_provider_name == "all_infobox":
                        in_text.documentInfo = str(document_id)
                    else:
                        in_text.documentInfo = str(document_id) + ":" + str(sent_id)
                    result = self.stub.PassageSearch(in_text)
                    result = json_format.MessageToJson(result, True, True)

                    json_result_format = json.loads(result)
                    json_result_format = json_result_format["result"]
                    if not json_result_format:
                        continue
                    else:
                        json_result_format = json.loads(json_result_format)
                        passage_result = json_result_format["sentence"][1]["text"]
                        passage_result = json.dumps(json_result_format["sentence"][1]["text"], ensure_ascii=False).encode('utf-8')
                        passage_result_list.append(passage_result)

        return passage_result_list 


    def __do_passage_search__(self, input_text):
        
        passage_result_list = list()
        data = [('question', input_text), ('wsConnId', '')]
        data = urllib.urlencode(data)

        url_request = urllib2.Request(_WISE_QA_URL_PATH_, data)

        url_request.add_header("Content-type", "application/x-www-form-urlencoded")

        url_flag = False

        try:
            request_result = urllib2.urlopen(url_request)
            url_flag = True
        except urllib2.URLError, e:
            print(e)
            url_flag = False

        if url_flag == True:
            request_result = request_result.read()
            result = self.__parse_with_stdlib__(request_result, "info")
            question, answer = result[0].split("||0||", 1)
            question_json = json.loads(question)
            answer_json = json.loads(answer)

            try:
                json_object = answer_json
            except ValueError:
                print("Request Time Out")

            answer = json_object["AnswerUnitOut"]["AnsUnit"]
            passage_result_list = self.__get_passage_search_result__(answer)
            return passage_result_list
        else:
            return list()

    def get_final_answer_result(self, input_text):
        return self.__do_passage_search__(input_text)
    

    def __get_start_and_end_index__(self, sent_id, window_size):
        
        if int(sent_id) - int(window_size) < 0:
            start_index = 0
        else:
            start_index = int(sent_id) - int(window_size)

        end_index = int(sent_id) + int(window_size)

        return start_index, end_index

    def get_passage_search_result_list(self, json_result, window_size):
        answers = json_result["AnswerUnitOut"]["IR_result"]
        result_dict = dict()

        for answer in answers:
            content_provider_name = answer["cpname"]            
            if content_provider_name == "wiki_definition":
                each_dict = {'ctx': [answer["description"]], 'weight': answer["weight"]}
                if "wiki_definition" in result_dict.keys():
                    result_dict["wiki_definition"].append(each_dict)
                else:
                    result_dict["wiki_definition"] = [each_dict]

            elif content_provider_name == "all_infobox":
                each_dict = {'ctx': [answer["description"]], 'weight': answer["weight"]}
                if "all_infobox" in result_dict.keys():
                    result_dict["all_infobox"].append(each_dict)
                else:
                    result_dict["all_infobox"] = [each_dict]
      
            elif content_provider_name == "news_passage":
                each_dict = {'ctx': list(), 'weight': answer["weight"]}
                temp_doc_id = answer["docid"]
                doc_id, sent_id = temp_doc_id.split(":")
                start_index, end_index = self.__get_start_and_end_index__(sent_id, window_size)
                for idx in range(start_index, end_index):
                    in_text = ps_pb2.PassageSearchInput()
                    in_text.provider = content_provider_name
                    in_text.documentInfo = str(doc_id) + ":" + str(idx)
                    
                    passage_search_result = self.stub.PassageSearch(in_text)
                    passage_search_result = json_format.MessageToJson(passage_search_result, True, True)

                    json_result_format = json.loads(passage_search_result)
                    json_result_format = json_result_format["result"]
                    if not json_result_format:
                        continue
                    else:
                        json_result_format = json.loads(json_result_format)
                        passage_result = json.dumps(json_result_format["sentence"][1]["text"],
                                                    ensure_ascii=False).encode("utf-8")
                        each_dict['ctx'].append(passage_result)
                if "news_passage" in result_dict.keys():
                    result_dict["news_passage"].append(each_dict)
                else:
                    result_dict["news_passage"] = [each_dict]

            elif content_provider_name == "wiki_passage":
                each_dict = {'ctx': list(), 'weight': answer["weight"]}
                temp_doc_id = answer["docid"]
                doc_id, sent_id = temp_doc_id.split(":")
                start_index, end_idex = self.__get_start_and_end_index__(sent_id, window_size)
                for idx in range(start_index, end_index):
                    in_text = ps_pb2.PassageSearchInput()
                    in_text.provider = content_provider_name
                    in_text.documentInfo = str(doc_id) + ":" + str(idx)
                    
                    passage_search_result = self.stub.PassageSearch(in_text)
                    passage_search_result = json_format.MessageToJson(passage_search_result, True, True)

                    json_result_format = json.loads(passage_search_result)
                    json_result_format = json_result_format["result"]
                    if not json_result_format:
                        continue
                    else:
                        json_result_format = json.loads(json_result_format)
                        passage_result = json.dumps(json_result_format["sentence"][1]["text"], ensure_ascii=False).encode("utf-8")
                        each_dict['ctx'].append(passage_result)
                if len(each_dict['ctx']) > 0:
                    if "wiki_passage" in result_dict.keys():
                        result_dict["wiki_passage"].append(each_dict)
                    else:
                        result_dict["wiki_passage"] = [each_dict]
        return result_dict

    def get_result(self, search_result, window_size):
        result_token = search_result.split("||0||")
        result_json = json.loads(result_token[2])
        result_dict = dict()
        for result in result_json:
            if "news_passage" in result:
                news_passages = result_json["news_passage"]
                for news_passage in news_passages:
                    each_dict = {'ctx': list(), 'weight': news_passage["weight"]}
                    content_provider_name = news_passage["cpname"]
                    temp_doc_id = news_passage["StructPageID"]
                    doc_id, sent_id = temp_doc_id.split(":")
                    start_index, end_index = self.__get_start_and_end_index__(sent_id, window_size)
                
                    for idx in range(start_index, end_index):
                        in_text = ps_pb2.PassageSearchInput()
                        in_text.provider = content_provider_name
                        in_text.documentInfo = str(doc_id) + ":" + str(idx)

                        passage_search_result = self.stub.PassageSearch(in_text)
                        passage_search_result = json_format.MessageToJson(passage_search_result, True, True)

                        json_result_format = json.loads(passage_search_result)
                        json_result_format = json_result_format["result"]
                        if not json_result_format:
                            continue
                        else:
                            json_result_format = json.loads(json_result_format)
                            passage_result = json.dumps(json_result_format["sentence"][1]["text"], ensure_ascii=False).encode("utf-8")
                            each_dict['ctx'].append(passage_result)
                    if "news_passage" in result_dict.keys():
                        result_dict["news_passage"].append(each_dict)
                    else:
                        result_dict["news_passage"] = [each_dict]
                            
            elif "wiki_definition" in result:
                wiki_definitions = result_json["wiki_definition"]
                for wiki_definition in wiki_definitions:
                    each_dict = {'ctx': list(), 'weight': wiki_definition["weight"]}
                    description = wiki_definition["Description"]
                    each_dict['ctx'].append(description)
                    if "wiki_definition" in result_dict.keys():
                        result_dict["wiki_definition"].append(each_dict)
                    else:
                        result_dict["wiki_definition"] = [each_dict]

            elif "wiki_passage" in result:
                wiki_passages = result_json["wiki_passage"]
                for wiki_passage in wiki_passages:
                    each_dict = {'ctx': list(), 'weight': wiki_passage["weight"]}
                    content_provider_name = wiki_passage["cpname"]
                    doc_id = wiki_passage["StructPageID"]
                    sent_id = wiki_passage["S_ID"]
                    start_index, end_index = self.__get_start_and_end_index__(sent_id, window_size)
                
                    for idx in range(start_index, end_index):
                        in_text = ps_pb2.PassageSearchInput()
                        in_text.provider = content_provider_name
                        in_text.documentInfo = str(doc_id).split(":")[0] + ":" + str(idx)
                        passage_search_result = self.stub.PassageSearch(in_text) #TODO
                        passage_search_result = json_format.MessageToJson(passage_search_result, True, True)

                        json_result_format = json.loads(passage_search_result)
                        json_result_format = json_result_format["result"]
                        if not json_result_format:
                            continue
                        else:
                            json_result_format = json.loads(json_result_format)
                            passage_result = json.dumps(json_result_format["sentence"][1]["text"],
                                                        ensure_ascii=False).encode("utf-8")
                            each_dict['ctx'].append(passage_result)
                    if len(each_dict['ctx']) > 0:
                        if "wiki_passage" in result_dict.keys():
                            result_dict["wiki_passage"].append(each_dict)
                        else:
                            result_dict["wiki_passage"] = [each_dict]

            elif "all_infobox" in result:
                all_infoboxes = result_json["all_infobox"]
                for all_infobox in all_infoboxes:
                    each_dict = {'ctx': list(), 'weight': all_infobox["weight"]}
                    description = all_infobox["Description"]
                    each_dict['ctx'].append(description)
                    if "all_infobox" in result_dict.keys():
                        result_dict["all_infobox"].append(each_dict)
                    else:
                        result_dict["all_infobox"] = [each_dict]
        return result_dict

def is_number(select):
    try:
        return True, int(select)
    except ValueError:
        return False, select

