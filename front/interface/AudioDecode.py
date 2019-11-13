#coding=utf-8

import os
import sys
from interface.AMRInterface import get_model
from utils.ServerLog import get_log
import json

logger = get_log()

class AudioDecoder():
    def __init__(self):
        self.amr_decode = get_model()
        if not self.amr_decode:
            info_json = {'initialization': 'init amr model error'}
            info = json.dumps(info_json)
            logger.error(info)
            exit(1)

    def decode(self, uttid, data):
        try:
            if data[:5] == b'#!AMR':
                status, message, pcm, pcm_length, sample_rate = self.decode_amr(data)
            elif data[:4] == b'RIFF':
                status, message, pcm, pcm_length, sample_rate = self.decode_wav(data)
            else:
                raise Exception('not allowed format')
            if not status:
                raise Exception(message)
            info_json = {'uttid': uttid, 'AudioDeocde': message}
            info = json.dumps(info_json)
            logger.info(info)
            return True, 'audio decode sucessfully', pcm, pcm_length, sample_rate
        except Exception as e:
            info_json = {'AudioDecode_amr': 'error: {}'.format(str(e)), 'uttid': uttid}
            info = json.dumps(info_json)
            logger.info(info)
            return False, str(e), None, None, None


    def decode_amr(self, data):
        try:
            if data[:6] == b'#!AMR\n':
                info_json = {'AudioDecode_amr': 'get amrnb header'}
                info = json.dumps(info_json)
                logger.info(info)
                pcm, pcm_length = self.amr_decode.LittleAmrnb(data)
                sample_rate = 8000
            elif data[:9] == b'#!AMR-WB\n':
                info_json = {'AudioDecode_amr': 'get amrwb header'}
                info = json.dumps(info_json)
                logger.info(info)
                pcm, pcm_length = self.amr_decode.LittleAmrwb(data)
                sample_rate = 16000
            else:
                return False, 'failed by amr decode', None, None, None
            return True, 'amr decode sucessfully', pcm, pcm_length, sample_rate
        except Exception as e:
            info_json = {'AudioDecode_amr': 'error: {}'.format(str(e))}
            info = json.dumps(info_json)
            logger.info(info)
            return False, str(e), None, None, None

    def decode_wav(self, data):
        try:
            if data[:4] == b'RIFF' and data[8:16] == b'WAVEfmt ':
                info_json = {'AudioDecode_wav': 'get standard wav header'}
                info = json.dumps(info_json)
                logger.info(info)
                pcm = data[44:]
                sample_rate = int.from_bytes(data[24:28], 'little')
                pcm_length = len(pcm)
            elif data[:4] == b'RIFF' and data[12:16] == b'JUNK':
                info_json = {'AudioDecode_wav': 'get junk wav header'}
                info = json.dumps(info_json)
                logger.info(info)
                junk_length = int.from_bytes(data[16:20], 'little')
                fmt_start = 20 + junk_length
                fmt = data[fmt_start: fmt_start + 4]
                if fmt != b'fmt ':
                    raise Exception('fmt check error')
                sample_rate = int.from_bytes(data[fmt_start + 12: fmt_start + 16], 'little')
                fmt_length = int.from_bytes(data[fmt_start + 4: fmt_start + 8], 'little')
                fllr_start = fmt_start + 8 + fmt_length
                fllr = data[fllr_start:fllr_start + 4]
                if fllr != b'FLLR':
                    raise Exception('fllr check error')
                fllr_length = int.from_bytes(data[fllr_start + 4: fllr_start + 8], 'little')
                data_start = fllr_start + 8 + fllr_length
                data_syn = data[data_start: data_start+4]
                if data_syn != b'data':
                    raise Exception('data syn check error')
                pcm = data[data_start + 4:]
                pcm_length = len(pcm)
            else:
                return False, 'failed by wav decode', None, None, None
            return True, 'wav decode sucessfully', pcm, pcm_length, sample_rate
        except Exception as e:
            info_json = {'AudioDecode_amr': 'error: {}'.format(str(e))}
            info = json.dumps(info_json)
            logger.info(info)
            return False, str(e), None, None, None




