#coding=utf-8

import re
import os, sys


tan_words = [u'啊', u'哦', u'呀', u'吧', u'呢', u'哈']
wen_words = [u'吗', u'啥', u'么']

def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'u0030' and uchar <= u'u0039' or uchar.isdigit():
        return True
    else:
        return False

def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'u0041' and uchar <= u'u005a') or (uchar >= u'u0061' and uchar <= u'u007a') or uchar.isalpha():
        return True
    else:
        return False


def symbol_handle(sequence):
    if sequence == '' or len(sequence) == 0 or sequence == None:
        return ''
    if is_chinese(sequence[-1]) and sequence[-1] in tan_words:
        sequence += '！'
    elif is_chinese(sequence[-1]) and sequence[-1] in wen_words:
        sequence += '？'
    else:
        if is_chinese(sequence[-1]) or is_number(sequence[-1]) or is_alphabet(sequence[-1]):
            sequence += '。'
    return sequence

