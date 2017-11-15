#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import re, random
import xml.etree.ElementTree as ElementTree
from datetime import datetime
import random
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')

# ========== CONSTANT_VARIABLE ==========
SMALL_BRACKET_PATTERN = re.compile("(\(.*?\))")
MEDIUM_BRACKET_PATTERN = re.compile("(\{.*?\})")
LARGE_BRACKET_PATTERN = re.compile("(\[.*?\])")
SPECIAL_BRACKET_PATTERN = re.compile("(\《.*?\》)")

WIKI_PATTERN = re.compile("(위키피디아|위키피디어|위키야|위키)")
WIKI_STRING_PATTERN = re.compile("((위키피디어|위키|위키피디아)(.+)(알아|검색|확인)(.+))")
# =======================================

# ========== CONFIGURATION FILE ==========
__CONFIG_FILE__ = "util.cfg"
# ========================================

# ============= DEVICE TYPE ==============
__KIDS_WATCH__ = "DEV_002"
__PEPPER__ = "DEV_004"
# ========================================

# ========== CONSTANT_VARIABLE FOR MESSAGE ==========
__EMPTY_QUERY_MSG__ = "입력이 유효하지 않습니다. 다시 시도하세요"
__DEF_EXCEPTION_MSG__ = "일시적으로 사용할 수 없습니다. 잠시후 다시 시도하세요."
__DEF_ERROR_MSG__ = "오류가 발생했습니다. 잠시후 다시 시도하세요."
__NOTHING_FOUND_MSG__ = "정보를 찾을 수 없습니다."


# ====================================================

class Util:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(__CONFIG_FILE__)
        self.__FORMAL_LIST__ = config.get("ANSWER", "FORMAL")
        self.__INFORMAL_LIST__ = config.get("ANSWER", "INFORMAL")
        self.__FILTER_ANSWER_LIST__ = config.get("ANSWER", "FILTER_ANSWER")
        self.__PREFIX_TEMPLATE_LIST__ = config.get("ANSWER", "PREFIX_TEMPLATE")
        self.__POSTFIX_TEMPLATE_LIST__ = config.get("ANSWER", "POSTFIX_TEMPLATE")
        self.__DEF_ERROR_MSG__ = config.get("ANSWER", "DEF_ERROR_MSG")
        self.__NOTHING_FOUND_MSG__ = config.get("ANSWER", "NOTHING_FOUND_MSG")

    def get_def_error_msg(self):
        return self.__DEF_ERROR_MSG__

    def has_jongsung(self, text):
        text = text.decode('utf-8')
        code = ord(text)
        if code < 0xAC00 or code > 0xD7A3:
            return True
        offset = code - 0xAC00
        if offset % 28 == 0:
            return False
        return True

    def delete_wiki_keyword_and_stopword(self, text):
        text = text.encode('utf-8')
        if WIKI_STRING_PATTERN.search(text):
            d = WIKI_STRING_PATTERN.search(text)
            found_str = d.group()
            text = text.replace(found_str, '').strip()
        elif WIKI_PATTERN.search(text):
            d = WIKI_PATTERN.search(text)
            found_str = d.group()
            text = text.replace(found_str, '').strip()
        return text

    def delete_bracket(self, output):
        output = unicode(output)
        if (output.find('(') and output.find(')')):
            i = 0
            start_index = 0
            end_index = 0
            while True:
                if i >= len(output):
                    break
                if output[i] == "(":
                    start_index = i
                elif output[i] == ")":
                    end_index = i
                    output = output.replace(output[start_index:end_index + 1], "").strip()
                    output = output.replace("  ", " ")
                    i = 0
                    continue
                i += 1
        output = output.replace("《", "")
        output = output.replace("》", "")
        return output.strip()

    def parse_with_stdlib(self, content, tag):
        result_list = list()
        root = ElementTree.fromstring(content)
        for log in root.iter(tag):
            result_list.append(log.text)
        return result_list

    def recognize_answer(self, text, output_result):
        flag = False
        message = ""
        original_answer = ""
        if len(
                output_result.strip()) == 0 or output_result == self.__DEF_ERROR_MSG__ or output_result == self.__NOTHING_FOUND_MSG__:
            flag = False
            message = output_result
        elif (text.find(" ") == -1) and len(output_result) < 5:
            flag = False
        else:
            flag = True
            message, original_answer = self.make_correct_message(output_result)
        return message, original_answer, flag

    def classify_wiki(self, device_type):
        if device_type == __KIDS_WATCH__ or device_type == __PEPPER__:
            return True
        else:
            return False

    def filter_error_message(self):
        message = self.__FILTER_ANSWER_LIST__[random.randrange(0, len(self.__FILTER_ANSWER_LIST__))]

        return message

    def not_found_error_message(self, text, output_result):
        message = self.__FORMAL_LIST__[random.randrange(0, len(self.__FORMAL_LIST__))]
        return self.__FORMAL_LIST__[random.randrange(0, len(self.__FORMAL_LIST__))]

    def recognize_full_value_wiki(self, full_value_output_result):
        full_value_output_result = full_value_output_result.strip()
        if full_value_output_result.endswith("다") or full_value_output_result.endswith("다."):
            return full_value_output_result
        else:
            return full_value_output_result + "입니다."

    def make_correct_message(self, output):
        output = output.strip().replace("\n", ",")
        temp_tokens = output.split()
        output = ""
        for temp in temp_tokens:
            output = output + " " + temp
        output = output.strip()
        original_answer = output  # no header, footer
        if not output.endswith('다.'):
            output = output + self.__POSTFIX_TEMPLATE_LIST__
            # self.__POSTFIX_TEMPLATE_LIST__가 2개 이상이 될 경우 사용
            #output = output + self.__POSTFIX_TEMPLATE_LIST__[random.randrange(0, len(self.__POSTFIX_TEMPLATE_LIST__))# ]
        output = output.strip()
        output = self.delete_bracket(output=output)
        return output, original_answer

    def get_tree_result(sentences, original_token=False):
        final_list = list()
        word_list = list()
        depen_list = list()
        for sent in sentences:

            if original_token:
                for word in sent["word"]:
                    word_list.append(word["text"])
            sent_list = list()
            for morp in sent["morp_eval"]:
                tokens = morp["result"].replace("+", "\t").replace("\t/SW", "+/SW").split("\t")
                item_list = list()
                for token in tokens:
                    item = token.split("/")
                    if len(item) > 2:
                        item = ["/"] + [item[-1]]
                    t = "/".join([item[0], item[1].lower()])
                    if type(t) == unicode:
                        item_list.append(t)
                    else:
                        item_list.append(unicode(t, "utf-8"))
                sent_list.append(item_list)
            for i, depen in enumerate(sent["dependency"]):
                depen["id"] = i
                depen_list.append(depen)
            final_list.append(sent_list)
            q = sent["text"]
        if original_token:
            return final_list, word_list, depen_list
        else:
            return q, final_list, depen_list

    def map_original_idx(self, morph, original):
        flatten_morph = list()
        for s in morph:
            flatten_morph += s
        map_dic = dict()
        m_idx = 0
        o_idx = 0
        for m, o in zip(flatten_morph, original):
            max_o_idx = o_idx + len(o)
            if len(m) == 1:
                map_dic[m_idx] = (o_idx, o_idx + len(o))
                m_idx += 1
                o_idx += len(o) + 1
            else:
                pass_list = list()  # splitted morph ex. 나서+었
                start_from = 0
                fail = False  # beforehand
                for each_m in m:
                    splitted_m = each_m.rsplit("/", 1)[0]
                    location = o.find(splitted_m, start_from)
                    if location >= 0:
                        if fail:
                            o_idx += location
                            fail = False
                        map_dic[m_idx] = (o_idx, o_idx + len(splitted_m))
                        o_idx += len(splitted_m)
                        start_from = location
                    else:
                        pass_list.append((m_idx, m, start_from + o_idx, o))
                        fail = True
                    m_idx += 1
                pass_list_tmp = pass_list
                if len(pass_list) > 0:  # if there is a splitted morphs
                    for pass_item in pass_list:
                        # m_idx, m, start_position
                        backward_until = 1
                        while m_idx > (pass_item[0] + backward_until):
                            try:
                                # 만약 그 다음 것도 찾지 못하면 하나 더 뒤로 감
                                map_dic[pass_item[0]] = (pass_item[2], map_dic[pass_item[0] + backward_until][0])
                                pass_list_tmp.remove(pass_item)
                                break
                            except KeyError:
                                backward_until += 1
                if len(pass_list_tmp) > 0:
                    for pass_item in pass_list_tmp:
                        map_dic[pass_item[0]] = (pass_item[2], max_o_idx)
                o_idx = max_o_idx
                o_idx += 1  # space
        # for </s> tag
        map_dic[m_idx] = (o_idx - 1, o_idx - 1)
        return map_dic

    def time_check(self, type=1):
        if type == 1:
            return datetime.today().strftime("%Y%m%d%H%M%S%f")[:-4]
        elif type == 0:
            return datetime.today().strftime("%Y%m%d%H%M%S%f")[:-3] + str(random.random())[2:6]

    def insert_meta(self, meta, LOG_TIME='', LOG_TYPE='', RESULT_CODE='', REQ_TIME='', RSP_TIME='', QA_ENGINE=''):
        if LOG_TIME is not '':
            meta['log_time'] = LOG_TIME
        if LOG_TYPE is not '':
            meta['log_type'] = LOG_TYPE
        if RESULT_CODE is not '':
            meta['result_code'] = RESULT_CODE
        if REQ_TIME is not '':
            meta['req_time'] = REQ_TIME
        if RSP_TIME is not '':
            meta['rsp_time'] = RSP_TIME
        if QA_ENGINE is not '':
            meta['qa_engine'] = QA_ENGINE

        return meta

    def dict_upper(self, meta):
        meta_temp = dict()
        for key in meta.keys():
            if key == 'message_id':
                meta_temp['MSG_ID'] = meta['message_id']
            elif key == 'transaction_id':
                meta_temp['TR_ID'] = meta['transaction_id']
            else:
                meta_temp[key.upper()] = meta[key]
        return meta_temp