#coding=utf-8

import os, sys
from scipy.signal import decimate
import scipy.ndimage
from utils.ServerLog import get_log
import json
import numpy as np
import warnings
import struct
import librosa
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)

logger = get_log()

def change_sample_rate(src_data, src_sample_rate, dst_sample_rate):
    info_json = {'change_sample': 'start convert sample rate {} to {}'.format(src_sample_rate, dst_sample_rate)}
    info = json.dumps(info_json)
    logger.info(info)
    src_data = np.frombuffer(src_data, dtype=np.int16).astype(np.float32)
    dst_data = librosa.core.resample(src_data, src_sample_rate, dst_sample_rate)
    info_json = {'change_sample': 'convert sample rate {} to {} successfully'.format(src_sample_rate, dst_sample_rate)}
    info = json.dumps(info_json)
    logger.info(info)
    dst_data = dst_data.astype(np.int16).tobytes()
    return dst_data


def down_sample_rate(src_data, src_sample_rate, dst_sample_rate):
    info_json = {'downsample': 'start convert sample rate {} to {}'.format(src_sample_rate, dst_sample_rate)}
    info = json.dumps(info_json)
    logger.info(info)
    src_data = np.frombuffer(src_data, dtype=np.int16).astype(np.float32)
    if src_sample_rate <= dst_sample_rate:
        info_json = {'downsample': 'src <= dst, src sample rate: {}, dst sample rate: {}'.format(src_sample_rate, dst_sample_rate)}
        info = json.dumps(info_json)
        logger.error(info)
        return False
    if src_sample_rate % dst_sample_rate != 0:
        info_json = {'downsample': 'Multiple error, src sample rate: {}, dst sample rate: {}'.format(src_sample_rate, dst_sample_rate)}
        info = json.dumps(info_json)
        logger.error(info)
        return False
    scale = src_sample_rate // dst_sample_rate
    dst_data = decimate(src_data, scale, n=16, ftype='iir')
    info_json = {'downsample': 'convert sample rate {} to {} successfully'.format(src_sample_rate, dst_sample_rate)}
    info = json.dumps(info_json)
    logger.info(info)
    dst_data = dst_data.astype(np.int16).tobytes()
    return dst_data

def up_sample_rate(src_data, src_sample_rate, dst_sample_rate):
    info_json = {'downsample': 'start convert sample rate {} to {}'.format(src_sample_rate, dst_sample_rate)}
    info = json.dumps(info_json)
    logger.info(info)
    src_data = np.frombuffer(src_data, dtype=np.int16).astype(np.float32)
    if src_sample_rate >= dst_sample_rate:
        info_json = {'downsample': 'src >= dst, src sample rate: {}, dst sample rate: {}'.format(src_sample_rate, dst_sample_rate)}
        info = json.dumps(info_json)
        logger.error(info)
        return False
    scale = dst_sample_rate / src_sample_rate
    dst_data = scipy.ndimage.zoom(src_data, scale)
    info_json = {'downsample': 'convert sample rate {} to {} successfully'.format(src_sample_rate, dst_sample_rate)}
    info = json.dumps(info_json)
    logger.info(info)
    dst_data = dst_data.astype(np.int16).tobytes()
    return dst_data

def add_wav_header(src_data, sample_rate):
    header = b'RIFF'
    total_length = len(src_data) + 36
    audio_length = len(src_data)
    header += struct.pack('i', total_length)
    header += b'\x57\x41\x56\x45\x66\x6D\x74\x20\x10\x00\x00\x00\x01\x00\x01\x00'
    header += struct.pack('i', sample_rate)
    header += struct.pack('i', sample_rate * 2)
    header += b'\x02\x00'
    header += struct.pack('H', 16)
    header += b'data'
    header += struct.pack('i', audio_length)
    return header + src_data

def volumn_normalize(data, has_head=False):
    if has_head:
        head = data[:44]
        data = data[44:]
        data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        data = data * 1.0 / (np.max(np.abs(data)))
        data = data * 65535
        data = data.astype(np.int16).tobytes()
        return head + data
    else:
        data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        data = data * 1.0 / (np.max(np.abs(data)))
        data = data * 65535
        data = data.astype(np.int16).tobytes()
        return data


