#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import logging
import ConfigParser

CONFIG_FILE = "Tlo.cfg"

config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)

path = config.get("TLO", "PATH")

class TLO:
    def __init__(self):
        self.logger = logging.getLogger('TLO')

    def write(self, meta):
        self.logger.info('QA_ENGINE=' + str(meta['qa_engine']) + '|' + 'SEQ_ID=' + str(meta['seq_id']) + '|' + 'LOG_TIME=' + str(meta['log_time'])
                         + '|' + 'LOG_TYPE=' + str(meta['log_type']) + '|' + 'SID=' + str(meta['sid']) + '|' + 'RESULT_CODE='
                         + str(meta['result_code']) + '|' + 'REQ_TIME=' + str(meta['req_time']) + '|' + 'RSP_TIME='
                         + str(meta['rsp_time']) + '|' + 'CLIENT_IP=' + str(meta['client_ip']) + '|' + 'DEV_INFO='
                         + str(meta['dev_info']) + '|' + 'OS_INFO=' + str(meta['os_info']) + '|' + 'NW_INFO='
                         + str(meta['nw_info']) + '|' + 'SVC_NAME=' + str(meta['svc_name']) + '|' + 'DEV_MODEL='
                         + str(meta['dev_model']) + '|' + 'CARRIER_TYPE=' + str(meta['carrier_type']) + '|' + 'TR_ID='
                         + str(meta['transaction_id']) + '|' + 'MSG_ID=' + str(meta['message_id']) + '|' + 'FROM_SVC_NAME='
                         + str(meta['from_svc_name']) + '|' + 'TO_SVC_NAME=' + str(meta['to_svc_name']) + '|' + 'SVC_TYPE='
                         + str(meta['svc_type']) + '|' + 'DEV_TYPE=' + str(meta['dev_type']) + '|' + 'DEVICE_TOKEN='
                         + str(meta['device_token']))