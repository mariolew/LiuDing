#coding=utf-8
import urllib
import urllib.parse
import urllib.error
import urllib.request
import requests
import hashlib
import time
import json
import base64
from utils.ServerLog import get_log
from aip import AipSpeech
import os

logger = get_log()


def hangyan_interface(audio_data, audio_duration, uttid, request_id):
    info_json = {'interface': 'hanyan', 'uttid': uttid, 'request_id': request_id}
    info = json.dumps(info_json)
    logger.info(info)
    hang_start = time.time()
    url = 'http://api.vop.netease.com/asr_api?cuid=gtvoice_http&lan=zh&token=b71857dc52e718d31c878b967293da86'
    req = urllib.request.Request(url = url, data = audio_data)
    req.add_header('Content-Type', 'audio')
    hang_result = ''
    try:
        rsp = urllib.request.urlopen(req)
        ret_str = rsp.read().decode('utf-8')
        hang_result = json.loads(ret_str)['result'][0]
    except Exception as e:
        info_json = {'hangyan': 'failed', 'bad_str': str(e), 'uttid': uttid, 'request_id': request_id}
        info = json.dumps(info_json)
        logger.error(info)
        return False, ''
    elasped = time.time() - hang_start
    hang_rtf = -1
    if audio_duration > 0:
        hang_rtf = elasped / audio_duration
    return hang_result, hang_rtf


def baidu_interface(audio_data, dst_sample_rate, audio_duration, uttid, request_id):
    info_json = {'interface': 'baiudu', 'uttid': uttid, 'request_id': request_id}
    info = json.dumps(info_json)
    logger.info(info)
    APP_ID = '11225401'
    API_KEY = 'LssfY4Gj7UCqDQS8Zx8jRtqH'
    SECRET_KEY = 'ceG5vE8anSUT8DV1EUu1vwMGNNYiuzjR'
    baidu_start = time.time()
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    respond = client.asr(audio_data, 'wav', dst_sample_rate)
    baidu_result = ''
    try:
        if 'result' in respond:
            baidu_result = respond['result'][0]
        else:
            info_json = {'baidu': 'failed', 'bad_str': str(respond), 'uttid': uttid, 'request_id': request_id}
            info = json.dumps(info_json)
            logger.error(info)
            return False, ''
    except Exception as e:
        info_json = {'baidu': 'failed', 'bad_str': str(e), 'uttid': uttid, 'request_id': request_id}
        info = json.dumps(info_json)
        logger.error(info)
        return False, ''
    elasped = time.time() - baidu_start
    baidu_rtf = -1
    if audio_duration > 0:
        baidu_rtf = elasped / audio_duration
    return baidu_result, baidu_rtf

def ali_interface(audio_data, dst_sample_rate, audio_duration, uttid, token, request_id):
    try:
        info_json = {'interface': 'ali', 'uttid': uttid, 'request_id': request_id}
        info = json.dumps(info_json)
        logger.info(info)
        ali_start = time.time()
        ali_result = ''
        headers = {
                    'X-NLS-Token': token,
                    'Content-Type': 'application/octet-stream',
                    'Content-Length': bytes(len(audio_data)),
                    'Host': 'nls-gateway.cn-shanghai.aliyuncs.com',
                    }
        params = {
                'appkey': 'ErzvYLUAqBTRYzAV',
                'format': 'pcm',
                'enable_punctuation_prediction': False,
                'enable_inverse_text_normalization': False,
                'sample_rate': dst_sample_rate,
                }
        url = 'http://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/asr'
        r = requests.post(url, data=audio_data, headers=headers,  params=params)
        response = json.loads(r.text)
        ali_result = response['result']
        elasped = time.time() - ali_start
        ali_rtf = -1
        if audio_duration > 0:
            ali_rtf = elasped / audio_duration
        return ali_result, ali_rtf
    except Exception as e:
        info_json = {'ali': 'failed', 'bad_str': str(e), 'uttid': uttid, 'request_id': request_id}
        info = json.dumps(info_json)
        logger.error(info)
        return False, ''

def xunfei_interface(audio_data, dst_sample_rate, audio_duration, uttid, request_id):
    try:
        info_json = {'interface': 'xunfei', 'uttid': uttid, 'request_id': request_id}
        info = json.dumps(info_json)
        logger.info(info)
        audio_base64 = base64.b64encode(audio_data)
        audio_urlencode = urllib.parse.quote(audio_data, safe='')
        url = 'http://api.xfyun.cn/v1/service/v1/iat'
        params = {
            'engine_type': 'sms16k',
            'aue': 'raw'
        }
        params_json = json.dumps(params)
        params_base64 = base64.b64encode(params_json)
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'charset': 'utf-8',
            'X-Appid': '5c347190',
            'X-CurTime': '',
            'X-Param': '',
            'X-CheckSum': ''
        }
    except Exception as e:
        info_json = {'xunfei': 'failed', 'bad_str': str(e), 'uttid': uttid, 'request_id': request_id}
        info = json.dumps(info_json)
        logger.error(info)
        return False, ''

class Weixin():
    def __init__(self):
        self.app_key = '0iyp3zPFgjKcEKxB'
        self.app_id = '1106850505'
        self.data = {}
        self.url = 'https://api.ai.qq.com/fcgi-bin/aai/aai_wxasrs'

    def setParams(self, array, key, value):
        array[key] = value
    
    def genSignString(self, parser):
        uri_str = ''
        for key in sorted(parser.keys()):
            if key == 'app_key':
                continue
            value = parser[key]
            if isinstance(value, bytes):
                uri_str += "%s=%s&" % (key, urllib.parse.quote(parser[key], safe=''))
            else:
                uri_str += "%s=%s&" % (key, urllib.parse.quote(str(parser[key]), safe=''))
        sign_str = uri_str + 'app_key=' + parser['app_key']
        try:
            hash_md5 = hashlib.md5(sign_str)
        except:
            hash_md5 = hashlib.md5(sign_str.encode('utf-8'))
        return hash_md5.hexdigest().upper()

    def invoke(self, params):
        try:
            self.url_data = urllib.parse.urlencode(params).encode("utf-8")
            req = urllib.request.Request(self.url, self.url_data)
            rsp = urllib.request.urlopen(req)
            str_rsp = rsp.read().decode('utf-8')
            dict_rsp = json.loads(str_rsp)
            return dict_rsp
        except urllib.error.URLError as e:
            dict_error = {}
            if hasattr(e,"reason"):
                dict_error['msg'] = 'sdk http post err'
                dict_error['httpcode'] = -1
                dict_error['ret'] = -1
                return dict_error
        else:
            dict_error = {}
            dict_error['ret'] = -1
            dict_error['httpcode'] = -1
            dict_error['msg'] = "system error"
            return dict_error

    def getAaiWxAsrs(self, chunk, speech_id, end_flag, format_id, rate, bits, seq, chunk_len, cont_res):
        self.setParams(self.data, 'app_id', self.app_id)
        self.setParams(self.data, 'app_key', self.app_key)
        self.setParams(self.data, 'time_stamp', int(time.time()))
        self.setParams(self.data, 'nonce_str', int(time.time()))
        speech_chunk = base64.b64encode(chunk)
        self.setParams(self.data, 'speech_chunk', speech_chunk)
        self.setParams(self.data, 'speech_id', speech_id)
        self.setParams(self.data, 'end', end_flag)
        self.setParams(self.data, 'format', format_id)
        self.setParams(self.data, 'rate', rate)
        self.setParams(self.data, 'bits', bits)
        self.setParams(self.data, 'seq', seq)
        self.setParams(self.data, 'len', chunk_len)
        self.setParams(self.data, 'cont_res', cont_res)
        sign_str = self.genSignString(self.data)
        self.setParams(self.data, 'sign', sign_str)
        return self.invoke(self.data)

    def __call__(self, audio_data, dst_sample_rate, audio_duration, uttid, request_id):
        try:
            seq = 0
            for_mat = 2
            rate = dst_sample_rate
            bits = 16
            cont_res = 1  
            md5obj = hashlib.md5()
            md5obj.update(audio_data)
            hash = md5obj.hexdigest()
            speech_id = str(hash).upper()
            file_size = len(audio_data)
            print('file_size:', file_size)
            once_size = min(file_size, 72000)
            weixin_result = ''
            index = 0
            start = time.time()
            while True:
                chunk = audio_data[index * once_size: (index + 1) * once_size]
                if not chunk:
                    break
                else:
                    chunk_size = len(chunk)
                    if (seq + chunk_size) == file_size:
                        end = 1
                    else:
                        end = 0
                print(speech_id, end, for_mat, rate, bits, seq, chunk_size, cont_res)
                rsp = self.getAaiWxAsrs(chunk, speech_id, end, for_mat, rate, bits, seq, chunk_size, cont_res)
                print(rsp)
                seq += chunk_size
                print('seq:', seq)
                if end:
                    weixin_result = rsp['data']['speech_text']
                    break
                index += 1
            elasped = time.time() - start
            if audio_duration > 0:
                weixin_rtf = elasped / audio_duration
            return weixin_result, weixin_rtf
        except Exception as e:
            info_json = {'weixin': 'failed', 'bad_str': str(e), 'uttid': uttid, 'request_id': request_id}
            info = json.dumps(info_json)
            logger.error(info)
            return False, ''
