# -*- coding:utf-8 -*-

import os, time, re, json
import operator
import utils.text_normalized.helper
import utils.text_normalized.const

helper = text_normalized.helper.get_norm_helper()

class NumParser(object):
    '''
    句子数字解析器
    '''

    def __init__(self, sent, mode=text_normalized.const.MODE_RULE):
        # 默认为规则
        self.mode = mode
        sent = sent.replace('\n', '')
        sent = sent.replace('\r', '')
        self.sent = sent
        self.all_num_info = []
        self.cnt = 0

    def prase(self):
        self.all_num_info = helper.get_all_num_info(self.sent)

        for num_info in self.all_num_info:
            self.parse_num_info(num_info)

    def parse_num_info(self, num_info):
        num_str = num_info['num_str']
        start_index = num_info['start_index']
        end_index = num_info['end_index']

        # print 'parse_num_info', num_str, helper.is_number(num_str)
        is_quantifier, quantifier = helper.is_quantifier(self.sent[end_index:])
        if helper.is_number(num_str) and is_quantifier: # 数字后有量词
            num_info['num_type'] = text_normalized.const.TYPE_NUM_QUAN

            if num_str == u'2' and helper.is_quantifier_digit_change(quantifier) and \
             (start_index-1 < 0 or start_index-1 >= 0 and self.sent[start_index-1] != u'第'):
                num_info['sub_num_type'] = text_normalized.const.SUB_TYPE_DIGIT_CHANGE
            else:
                num_info['sub_num_type'] = text_normalized.const.SUB_TYPE_INTEGER
            return

        if helper.is_percent(num_str): # 百分比
            num_info['num_type'] = text_normalized.const.TYPE_PERCENT
            return

        if helper.is_range_percent(num_str): # 范围百分比
            num_info['num_type'] = text_normalized.const.TYPE_RANGE_PERCENT
            return

        if helper.is_range(num_str) and helper.is_quantifier(self.sent[end_index:]): # 范围后有量词
            num_info['num_type'] = text_normalized.const.TYPE_RANGE_QUAN
            return
        
        if helper.is_time(num_str):
            num_info['num_type'] = text_normalized.const.TYPE_TIME
            return

        if helper.is_date(num_str):
            num_info['num_type'] = text_normalized.const.TYPE_DATE
            return

        if helper.is_range(num_str):
            num_info['num_type'] = text_normalized.const.TYPE_RANGE
            return

        if helper.is_colon(num_str):
            if u'.' in num_str:
                num_info['num_type'] = text_normalized.const.TYPE_COLON_RATIO
                return

            index = num_str.find(u':')

            if index + 1 < len(self.sent):
                first = num_str[0:index]
                second = num_str[index + 1:]

                if first.startswith(u'0') or second.startswith(u'0'):
                    num_info['num_type'] = text_normalized.const.TYPE_COLON_TIME
                    return

            time_pri = helper.get_feature_pri(self.sent, start_index, end_index, 0)
            ratio_pri = helper.get_feature_pri(self.sent, start_index, end_index, 1)

            if time_pri < ratio_pri:
                num_info['num_type'] = text_normalized.const.TYPE_COLON_TIME
                return
            elif time_pri > ratio_pri:
                num_info['num_type'] = text_normalized.const.TYPE_COLON_RATIO
                return

            else:
                if helper.is_short_time(num_str):
                    num_info['num_type'] = text_normalized.const.TYPE_COLON_TIME
                else:
                    num_info['num_type'] = text_normalized.const.TYPE_COLON_RATIO
                return

        if helper.is_fraction(num_str):
            num_info['num_type'] = text_normalized.const.TYPE_FRACTION
            return

        if helper.is_decimal(num_str):
            num_info['num_type'] = text_normalized.const.TYPE_DECIMAL
            return

        if helper.is_integer(num_str):
            v = 0
            try:
                v = int(num_str)
            except:
                pass

            if len(num_str) and num_str[0] == u'0':
                num_info['num_type'] = text_normalized.const.TYPE_DIGIT
                num_info['sub_num_type'] = text_normalized.const.SUB_TYPE_DIGIT

            if end_index+1 < len(self.sent) and self.sent[end_index:end_index+1] == u'年':
                # print 'sent', self.sent
                num_info['num_type'] = text_normalized.const.TYPE_YEAR

                if self.mode == text_normalized.const.MODE_RULE:
                    if len(num_str) == 3 or len(num_str) == 4 and num_str[0] in [u'1', u'2']:
                        num_info['sub_num_type'] = text_normalized.const.SUB_TYPE_DIGIT
                    elif len(num_str) > 4 or len(num_str) == 1:
                        num_info['sub_num_type'] = text_normalized.const.SUB_TYPE_INTEGER
                    else:
                        num_info['sub_num_type'] = text_normalized.const.SUB_TYPE_INTEGER
                return
            
            if end_index+1 < len(self.sent) and self.sent[end_index:end_index+1] == u'后':
                if len(num_str) == 2:
                    num_info['num_type'] = text_normalized.const.TYPE_DIGIT
                    num_info['sub_num_type'] = text_normalized.const.SUB_TYPE_DIGIT
                    return

            if end_index+1 < len(self.sent) and self.sent[end_index:end_index+1] == u'大':
                if len(num_str) <= 2 or v in [100, 500]:
                    num_info['num_type'] = text_normalized.const.TYPE_DIGIT
                    num_info['sub_num_type'] = text_normalized.const.SUB_TYPE_INTEGER
                    return

            if end_index+1 < len(self.sent) and self.sent[end_index:end_index+1] in [u'中', u'国']:
                if len(num_str) == 4 or v / 100 >= 19:
                    num_info['num_type'] = text_normalized.const.TYPE_DIGIT
                    num_info['sub_num_type'] = text_normalized.const.SUB_TYPE_DIGIT
                    return

            if num_str in [u'110', u'112', u'119', u'911', u'12306', u'315', u'618'] or len(num_str) == 3:
                num_info['num_type'] = text_normalized.const.TYPE_DIGIT
                # start = max(0, start_index-15)
                # end = min(len(self.sent, end_index+16))
                # if num_str[start_index-1] == u'打' or u'警' in self.sent[start:end]:
                #         num_info['sub_num_type'] = const.SUB_TYPE_DIGIT
                #         return
                num_info['sub_num_type'] = text_normalized.const.SUB_TYPE_DIGIT_CHANGE
                return

            num_info['num_type'] = text_normalized.const.TYPE_DIGIT

            if v <= 100:
                num_info['sub_num_type'] == text_normalized.const.SUB_TYPE_INTEGER
            else:
                num_info['sub_num_type'] == text_normalized.const.SUB_TYPE_DIGIT

            # if self.sent[end_index:end_index+1] != u'大':
            #   return

            # global TEST_CNT, TEST_DICT

            # ch = self.sent[end_index:end_index+1]
            # if not ch in TEST_DICT:
            #   TEST_DICT[ch] = 0
            # TEST_DICT[ch] += 1
            
            # TEST_CNT += 1

            # print 'sent', self.sent
            # print num_str
            # print TEST_CNT

    def export(self):
        final_str = u''
        index = 0
        while index < len(self.sent):
            ch = self.sent[index]

            in_num = False
            in_item = None
            for item in self.all_num_info:
                if index >= item['start_index'] and index < item['end_index']:
                    in_num = True
                    in_item = item
                    break

            if in_num:
                tag = helper.type2tag(in_item['num_type'], in_item['sub_num_type'])
                final_str += '<%s>%s</%s>' % (tag, in_item['num_str'], tag)

                index = in_item['end_index']
            else:
                final_str += ch
                index += 1

        return final_str
