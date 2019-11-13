# -*- coding:utf-8 -*-

import os, time, re
from . import helper, const

helper = helper.get_norm_helper()

class NumConverter(object):
    '''
    数字转换器
    '''

    def __init__(self, sent):
        sent = sent.replace('\n', '')
        sent = sent.replace('\r', '')
        if not isinstance(sent, str):
            sent = unicode(sent, 'utf-8')
        self.sent = sent
        self.all_ch_info = []
        self.index = 0
        self.start_index = 0
        self.end_index = 0
        self.cnt = 0

    def convert(self):
        self.all_ch_info = helper.get_all_ch_info(self.sent)

        final_str = u''
        self.index = 0
        while self.index < len(self.sent):
            ch = self.sent[self.index]

            in_num_str = False
            for tag_info in self.all_ch_info:
                if self.index >= tag_info['start_index'] and self.index < tag_info['end_index']:
                    in_num_str = True
                    break

            if in_num_str:
                self.index = tag_info['end_index']

                self.start_index = tag_info['start_index']
                self.end_index = tag_info['end_index']

                num_type = tag_info['num_type']
                sub_num_type = tag_info['sub_num_type']
                num_str = tag_info['num_str']

                if len(num_str) == 1:
                    final_str += ch

                elif num_str.startswith(u'百分之'):
                    final_str += self.process_num(num_str[3:]) + u'%'

                elif helper.has_ch_num_sep(num_str):
                    final_str += self.process_num(num_str)

                else:
                    final_str += self.process_digit(num_str)

            else:
                self.index += 1
                final_str += ch

        return final_str

    def process_digit(self, num_str):
        final_str = u''
        for index, ch in enumerate(num_str):
            num = helper.ch_2_num(ch)
            if num < 0:
                if index + 1 < len(num_str):
                    return final_str + num_str[index+1:]
                else:
                    return final_str

            final_str += u"%d" % num

        return final_str

    def process_num(self, num_str):
        if u'点' in num_str:
            index = num_str.find(u'点')
            cnt = num_str.find(u'点')
            if cnt > 1:
                return num_str

            ineteger_str = num_str[:index]
            digit_str = num_str[index+1:]

            if not ineteger_str or not digit_str:
                return num_str

            ineteger_str = self.process_integer(ineteger_str)

            if len(digit_str) >= 1 and digit_str[-1:] in [u'亿', u'万']:
                digit_str = self.process_digit(digit_str[:-1]) + digit_str[-1:]
            elif len(digit_str) >= 2 and digit_str[-2:] in [u'万亿']:
                digit_str = self.process_digit(digit_str[:-2]) + digit_str[-2:]
            else:
                digit_str = self.process_digit(digit_str)

            return ineteger_str + u'.' + digit_str
        else:
            return self.process_integer(num_str)

    def process_integer(self, num_str):
        has_fail = False
        if num_str.endswith(u'万亿'):
            flag, final_str = self._process_integer(num_str[:-2])
            final_str += u'万亿'
        else:
            flag, final_str = self._process_integer(num_str)
            if not flag:
                has_fail = True

        if not flag and len(num_str) > 1:
            flag, final_str = self._process_integer(num_str[:-1])
            if flag:
                final_str += num_str[-1]
                # print 'suc integer cut after'

        if not flag and len(num_str) > 1:
            flag, final_str = self._process_integer(num_str[1:])
            if flag:
                # print 'suc integer cut pre'
                final_str = num_str[0] + final_str

        if not flag:
            if helper.is_ch_all_digit(num_str[:-1]):
                final_str = self.process_digit(num_str[:-1])
                final_str += num_str[-1]
                # print 'suc digit cut after'
                flag = True

            if helper.is_ch_all_digit(num_str[1:]):
                final_str = self.process_digit(num_str[1:])
                final_str = num_str[0] + final_str
                # print 'suc digit cut pre'
                flag = True

        if not flag and len(num_str) > 2:
            flag, final_str = self._process_integer(num_str[:-2])
            if flag:
                final_str += num_str[-2:]
                # print 'suc integer cut after 2'

        if not flag:
            # print 'process_integer fail', num_str
            return num_str

        if has_fail:
            # print 'process_integer suc', final_str
            pass
        return final_str

    def _process_integer(self, num_str):
        if len(num_str) == 1:
            return True, num_str

        yi_index = num_str.find(u'亿')
        yi_cnt = num_str.count(u'亿')
        wan_index = num_str.find(u'万')
        wan_cnt = num_str.count(u'万')        
        
        start_index = 0
        if yi_index >= 0 and wan_index >= 0 and yi_index > wan_index:
            # print 'error: process_integer, yi_index > wan_index', self.sent, num_str
            return False, num_str

        if yi_cnt > 1 or wan_cnt > 1:
            # print 'error: process_integer, cnt error', self.sent, num_str
            return False, num_str

        if yi_index == 0 or wan_index == 0:
            # print 'error: process_integer, index error', self.sent, num_str
            return False, num_str

        yi_value = 0
        if yi_index > 0:
            flag, yi_value = self.process_sub_integer(num_str[start_index:yi_index], exist_pre_value=False)
            if not flag:
                # print 'error: process_sub_integer yi_value', self.sent, num_str, num_str[start_index:yi_index]
                return False, num_str

            start_index = yi_index+1

        if yi_index > 0 and yi_index == len(num_str)-1:
            return True, u'%d亿' % yi_value

        wan_value = 0
        if wan_index > 0:
            exist_pre_value = yi_index >= 0
            flag, wan_value = self.process_sub_integer(num_str[start_index:wan_index], exist_pre_value=exist_pre_value)
            if not flag:
                # print 'error: process_sub_integer wan_value', self.sent, num_str, num_str[start_index:wan_index]
                return False, num_str

            start_index = wan_index+1

        if wan_index > 0 and wan_index == len(num_str)-1:
            if yi_value > 0:
                return True, u'%d亿%d万' % (yi_value, wan_value)
            else:
                return True, u'%d万' % (wan_value)

        exist_pre_value = (yi_index >= 0 or wan_index >= 0)
        flag, sub_value = self.process_sub_integer(num_str[start_index:], exist_pre_value=exist_pre_value)
        if not flag:
            # print 'error: process_sub_integer sub_value', self.sent, num_str, num_str[start_index:]
            return False, num_str

        if yi_value > 0:
            return True, u'%d亿%d万%d' % (yi_value, wan_value, sub_value)
        else:
            return True, u'%d' % (wan_value * 1000 + sub_value)

    def process_sub_integer(self, num_str, exist_pre_value=False):
        index = 0
        final_num = 0

        sep_index_mapping = {
            u'零': -1,
            u'千': 1,
            u'百': 2,
            u'十': 3,
            u'': 4,
        }

        if len(num_str) > 0 and num_str[0] == u'十':
            final_num = 10
            index = 1

        # print 'num_str', num_str, exist_pre_value
        pre_sep_zero = False
        first_sep = False
        sep_index = 0

        while index < len(num_str):
            ch = num_str[index]
            if ch == u'零':
                index += 1

                pre_sep_zero = True
                continue

            num = helper.ch_2_num(ch)
            # print '--', ch, num

            if num < 0:
                return False, num_str

            index += 1
            if index >= len(num_str):
                final_num += num

                sep = u''
                if not first_sep:
                    first_sep = True
                if (exist_pre_value and (sep_index_mapping[sep] == sep_index+1 or pre_sep_zero)) or \
                 ((not exist_pre_value) and (sep_index_mapping[sep] == sep_index+1 or first_sep)):
                    return True, final_num
                else:
                    return False, num_str

            sep = num_str[index]
            if not first_sep:
                first_sep = True

            if sep == u'千':
                final_num += num * 1000
            elif sep == u'百':
                final_num += num * 100
            elif sep == u'十':
                final_num += num * 10
            # elif sep == u'零':
            #     pass
            # elif helper.ch_2_num(sep):
            else:
                return False, num_str

            if (exist_pre_value and (sep_index_mapping[sep] == sep_index+1 or pre_sep_zero)) or \
                ((not exist_pre_value) and (sep_index_mapping[sep] == sep_index+1 or first_sep)):
                pass
            else:
                return False, num_str

            sep_index = sep_index_mapping[sep]
            pre_sep_zero = False

            index += 1

        return True, final_num

def generate_num():
    ch_file_path = '../dataset/digit_samples_50000_digit_unknown_ch'
    num_file_path = '../dataset/digit_samples_50000_digit_unknown_num'

    # ch_file_path = '../dataset/digit_samples_50000_digit_sample_ch'
    # num_file_path = '../dataset/digit_samples_50000_digit_sample_num'
    
    if not os.path.exists(ch_file_path):
        print('error: file_path not exist')
        return

    out_f = open(num_file_path, 'w+')

    with open(ch_file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            nc = NumConverter(line)
            final_str = nc.convert()

            if isinstance(final_str, str):
                final_str = final_str.encode('utf-8')

            out_f.write(final_str + '\n')

    out_f.close()

'''
maybe todo:
1) 年份：二零一八年六月十二日->2018年6月12日
2）时间：三点五十六分->3点45分
'''

if __name__=="__main__":
    generate_num()
