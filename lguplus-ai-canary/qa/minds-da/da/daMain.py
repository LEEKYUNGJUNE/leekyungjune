#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
reload(sys)
sys.setdefaultencoding('utf-8')

exe_path = os.path.realpath(sys.argv[0])
bin_path = os.path.dirname(exe_path)
lib_path = os.path.realpath(bin_path+"/../lib/python")
sys.path.append(lib_path)

from minds.maum.server import pool_pb2
from elsa.facade import userattr_pb2

from minds.maum.da import provider_pb2

from concurrent import futures
import argparse
import grpc
from google.protobuf import empty_pb2
import time, json, random

from util import *
from qa import QA
from hyperNet import HNetClient
from logger import TLO
from datetime import datetime
from mkFD import Make_FD
#import workerpool


__ONE_DAY_IN_SECONDS__ = 60 * 60 * 24

class WiseQAClient(provider_pb2.DialogAgentProviderServicer):

    # initialize the parameters
    init_param = provider_pb2.InitParameter()

    # inform information for provider
    provider = provider_pb2.DialogAgentProviderParam()
    provider.name = "wiseQAClient"
    provider.description = "wiseQAClient Dialog Agent"
    provider.version = '0.1'
    provider.single_turn = True
    provider.require_user_privacy = True

    # initialize state
    def __init__(self):
        self.state = provider_pb2.DIAG_STATE_IDLE
        self.logger = TLO()

    def IsReady(self, empty, context):
        print("is_ready", "called")
        status = provider_pb2.DialogAgentStatus()
        status.state = self.state
        return status

    def Init(self, init_param, context):
        print("initialize", "called")
        self.state = provider_pb2.DIAG_STATE_INITIALIZING
        # copy all
        self.init_param.CopyFrom(init_param)
        # direct method
        self.remote = init_param.params["remote"]
        print("remote")
        self.state = provider_pb2.DIAG_STATE_RUNNING
        # returns provider
        result = pool_pb2.DialogAgentProviderParam()
        result.CopyFrom(self.provider)
        print("result called")
        return result

    def Terminate(self, empty, context):
        print("terminate", "called")
        # do nothing
        self.state = provider_pb2.DIAG_STATE_TERMINATED
        return empty_pb2.Empty()

    def GetUserAttributes(self, empty, context):
        print("get_user_attributes", "called")
        result = userattr_pb2.UserAttributeList()
        return result

    def GetProviderParameter(self, empty, context):
        print("get_provider_parameter", "called")
        params = list()
        result = provider_pb2.RuntimeParameterList()
        remote = provider_pb2.RuntimeParameter()
        remote.name = "remote"
        remote.type = userattr_pb2.DATA_TYPE_STRING
        remote.desc = "remote"
        remote.default_value = ""
        remote.required = True
        params.append(remote)
        result.params.extend(params)
        return result

    def Talk(self, talk, context):
        req_full_time = util.time_check()
        session_id = talk.session_id
        print("Session ID : " + str(session_id))
        print("[Question] ", talk.text)
        print("[Device Type] ", talk.device.type)

        question = talk.text
        device_type = talk.device.type
        metadata = context.invocation_metadata()
        meta = dict()
        for key, value in metadata:
            meta[key] = value
        meta['seq_id'] = util.time_check(0)
        meta['log_type'] = 'SVC'
        meta['svc_name'] = 'QA'
        meta['to_svc_name'] = 'QA'

        output_result = ""
        original_answer = ""
        # FILTER the dialog included with the specific words
        output, filter_flag = qa.filter_question(question)
        
        if filter_flag == True:
            talk_res = provider_pb2.TalkResponse()
            talk_res.text = output
            talk_res.state = provider_pb2.DIAG_CLOSED
            talk_res.meta["selvas.tts"] = '<service="qna">' + output + '</service>'
            print(talk_res)
            return talk_res
        # wiki qa for kids watch
        else:
            output = ""
            if False:
            #if util.classify_wiki(device_type=device_type):
                talk_res = provider_pb2.TalkResponse()
                #talk_res.text = qa.kids_watch_for_wiki(text=question)
                output, original_answer, flag, status_code, status_message = qa.general_wiki(text=question)
                if flag == False:
                    original_answer = output
                talk_res.text = original_answer
                talk_res.state = provider_pb2.DIAG_CLOSED
                talk_res.meta["selvas.tts"] = '<service="qna">' + output + '</service>'
                talk_res.meta["status.code"] = status_code
                talk_res.meta["status.message"] = status_message
                return talk_res
            # if not kids watch
            else:
                # basic qa
                req_time = util.time_check()
                output_result, original_answer_result, flag, status_code, status_message = qa.base_qa(text=question, meta=meta)
                rsp_time = util.time_check()
                meta = util.insert_meta(meta= meta,RESULT_CODE=status_code, REQ_TIME=req_time, RSP_TIME=rsp_time, LOG_TIME=rsp_time, QA_ENGINE='BASICQA')
                self.logger.write(meta= meta)
                if flag == True:
                    output = output_result
                    original_answer = original_answer_result
                    print("Answer is BasicQA")
                    pass
                else:
                    # wiki
                    req_time = util.time_check()
                    output_result, original_answer_result, flag, status_code, status_message = qa.general_wiki(text=question, meta=meta)
                    rsp_time = util.time_check()
                    meta = util.insert_meta(meta=meta, RESULT_CODE=status_code, REQ_TIME=req_time, RSP_TIME=rsp_time, LOG_TIME=rsp_time, QA_ENGINE='TWE')
                    self.logger.write(meta=meta)
                    if flag == True:
                        output = output_result
                        original_answer = original_answer_result
                        print("Answer is Wiki")
                        pass
                    else:
                        # wise
                        req_time = util.time_check()
                        output_result, original_answer_result, flag, nlqa_result = qa.wise_qa(text=question)
                        rsp_time = util.time_check()
                        meta = util.insert_meta(meta=meta, RESULT_CODE=status_code, REQ_TIME=req_time, RSP_TIME=rsp_time, LOG_TIME=rsp_time, QA_ENGINE='EXOBRAIN')
                        self.logger.write(meta=meta)
                        if flag == True:
                            output = output_result
                            original_answer = original_answer_result
                            print("Answer is Exobrain")
                            pass
                        else:
                            if len(nlqa_result) == 0:
                                try:
                                    nlqa_result = qa.mk_nlqa(question)
                                except Exception as e:
                                    print e
                                    output = util.not_found_error_message(text=question, output_result=output_result)
                                    original_answer = output
                                    pass
                            # MRC
                            req_time = util.time_check()
                            output_result, original_answer_result, flag, status_code, status_message = qa.mindsMRC(text=question, nlqa_result=nlqa_result)
                            rsp_time = util.time_check()
                            meta = util.insert_meta(meta=meta, RESULT_CODE=status_code, REQ_TIME=req_time, RSP_TIME=rsp_time, LOG_TIME=rsp_time, QA_ENGINE='MRC')
                            self.logger.write(meta=meta)
                            if flag == True:
                                output = output_result
                                original_answer = original_answer_result
                                print("Answer is MRC")
                                pass
                            else:
                                # HyperNet
                                req_time = util.time_check()
                                output_result, original_answer_result, flag, status_code, status_message = qa.hyperNet(text=question, nlqa_result=nlqa_result)
                                rsp_time = util.time_check()
                                meta = util.insert_meta(meta=meta, RESULT_CODE=status_code, REQ_TIME=req_time, RSP_TIME=rsp_time, LOG_TIME=rsp_time, QA_ENGINE='HYPERNET')
                                self.logger.write(meta=meta)
                                if flag == True:
                                    output = output_result
                                    original_answer = original_answer_result
                                    print("Answer is HyperNet")
                                    pass
                                else:
                                    output = util.not_found_error_message(text=question, output_result=output_result)
                                    original_answer = output
                                    pass

            talk_res = provider_pb2.TalkResponse()
            talk_res.text = original_answer
            talk_res.meta["selvas.tts"] = '<service="qna">' + output + '</service>'
            talk_res.meta["status.code"] = status_code
            talk_res.meta["status.message"] = status_message
            talk_res.state = provider_pb2.DIAG_CLOSED
            print talk_res.text
            print talk_res.meta["selvas.tts"]
            rsp_time = util.time_check()
            meta = util.insert_meta(meta=meta, RESULT_CODE=status_code, REQ_TIME=req_full_time, RSP_TIME=rsp_time, LOG_TIME=rsp_time, QA_ENGINE='DA')
            self.logger.write(meta=meta)
            return talk_res

def serve():
    
    parser = argparse.ArgumentParser(description="wiseQAClient DA")
    parser.add_argument("-p", "--port",
                        nargs="?",
                        dest="port",
                        required=True,
                        type=int,
                        help="port to access server")
    args = parser.parse_args()
    data = [
        ('grpc.max_connection_idle_ms', 10000),
        ('grpc.max_connection_age_ms', 10000)
    ]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2000), None, data, None)

    provider_pb2.add_DialogAgentProviderServicer_to_server(WiseQAClient(), server)
    listen = "[::]" + ":" + str(args.port)
    server.add_insecure_port(listen)

    server.start()
    #
    # pool = workerpool.WorkerPool(size=1)
    # pool.map(aa)

    try:
        while True:
            time.sleep(__ONE_DAY_IN_SECONDS__)
    except KeyboardInterrupt:
        #pool.shutdown()
        server.stop(0)

if __name__ == "__main__":
    util = Util()
    qa = QA()
    serve()
