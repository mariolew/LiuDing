# -*- coding:utf-8 -*-

import os, time, re
import utils.text_normalized.helper
import utils.text_normalized.const

helper = text_normalized.helper.get_norm_helper()

class ChConverter(object):
    '''
    字符转换器
    '''

    def __init__(self, sent):
        sent = sent.replace('\n', '')
        sent = sent.replace('\r', '')
        #if not isinstance(sent, unicode):
        #    sent = unicode(sent, 'utf-8')
        self.sent = sent
        self.all_raw_tag_info = []
        self.index = 0
        self.start_index = 0
        self.end_index = 0
        self.cnt = 0

    def convert(self):
        self.all_raw_tag_info = helper.get_all_tag_info(self.sent)

        final_str = u''
        self.index = 0
        while self.index < len(self.sent):
            ch = self.sent[self.index]

            in_num_str = False
            for tag_info in self.all_raw_tag_info:
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

                # print num_str, num_type, sub_num_type

                if num_type == text_normalized.const.TYPE_NUM_QUAN:
                    if sub_num_type == text_normalized.const.SUB_TYPE_DIGIT_CHANGE:
                        final_str += self.process_digit_change(num_str)
                    else:
                        final_str += self.process_num(num_str)

                elif num_type == text_normalized.const.TYPE_PERCENT:
                    final_str += self.process_percent(num_str)

                elif num_type == text_normalized.const.TYPE_RANGE_PERCENT:
                    final_str += self.process_range_percent(num_str)

                elif num_type == text_normalized.const.TYPE_RANGE_QUAN:
                    final_str += self.process_range_quan(num_str)

                elif num_type == text_normalized.const.TYPE_RANGE:
                    final_str += self.process_range(num_str)

                elif num_type == text_normalized.const.TYPE_TIME:
                    final_str += self.process_time(num_str)

                elif num_type == text_normalized.const.TYPE_DATE:
                    final_str += self.process_date(num_str)

                elif num_type == text_normalized.const.TYPE_COLON_TIME:
                    final_str += self.process_colon_time(num_str)

                elif num_type == text_normalized.const.TYPE_COLON_RATIO:
                    final_str += self.process_colon_ratio(num_str)

                elif num_type == text_normalized.const.TYPE_FRACTION:
                    final_str += self.process_fraction(num_str)

                elif num_type == text_normalized.const.TYPE_DECIMAL:
                    final_str += self.process_num(num_str)

                elif num_type == text_normalized.const.TYPE_YEAR:
                    final_str += self.process_year(num_str)

                elif num_type == text_normalized.const.TYPE_DIGIT:
                    if sub_num_type == text_normalized.const.SUB_TYPE_DIGIT:
                        final_str += self.process_digit(num_str)
                    elif sub_num_type == text_normalized.const.SUB_TYPE_INTEGER:
                        final_str += self.process_num(num_str)
                    elif sub_num_type == text_normalized.const.SUB_TYPE_DIGIT_CHANGE:
                        final_str += self.process_digit_change(num_str)
                    else:
                        final_str += self.process_unknown_digit(num_str)

                else:
                    final_str += self.process_unknown(num_str)

            else:
                self.index += 1

                final_str += ch

        return final_str
        
    def process_num(self, num_str, process_two=True):
        # print 'process_num', num_str
        final_str = u''
        if num_str.startswith(u'-'):
            final_str += u'负'
            num_str = num_str[1:]

        elif num_str.startswith(u'+'):
            final_str += u'正'
            num_str = num_str[1:] 

        if not u'.' in num_str:
            # if process_two and num_str.isdigit() and int(num_str) == 2 and self.start_index-1 >= 0 and self.sent[self.start_index-1] != u'第':
            #     final_str = u'两'
            # else:
            final_str = self.process_integer(num_str)
        else:
            index = num_str.index(u'.')
            final_str += self.process_integer(num_str[:index])

            if index < len(num_str):
                tmp_str = self.process_digit(num_str[index+1:], True)
                if len(tmp_str) > 0:
                    final_str += u'点'
                final_str += tmp_str

        return final_str

    def process_digit(self, num_str, handle_all_zero=False):
        final_str = u''

        is_all_zero = True
        zero_cnt = 0
        for ch in num_str:
            if ch.isdigit():
                final_str += helper.num_2_ch(int(ch))
                if ch != '0':
                    is_all_zero = False
                else:
                    zero_cnt += 1
            else:
                final_str += ch

        if handle_all_zero and is_all_zero and zero_cnt != 1:
            return u''

        return final_str

    def process_integer(self, num_str):
        final_str = u''

        v = int(num_str)
        v1 = (v // 10000 // 10000) % 10000
        v2 = (v // 10000) % 10000
        v3 = v % 10000

        process = False

        if v1 > 0:
            final_str += self.convert_interger_num(0, v1)
            final_str += u'亿'
            process = True

        if v2 > 0:
            final_str += self.convert_interger_num(v/10000/10000, v2)
            final_str += u'万'
            process = True

        if v3 > 0:
            final_str += self.convert_interger_num(v/10000, v3)
            process = True

        if not process:
            final_str += u'零'

        return final_str

    def convert_interger_num(self, pre_v, v):
        final_str = u''
        if pre_v > 0 and (v / 1000) % 10 == 0 or pre_v > 0 and pre_v % 10000 == 0:
            final_str += u'零'

        v1 = (v // 1000) % 10
        v2 = (v // 100) % 10
        v3 = (v // 10) % 10
        v4 = v % 10

        if v1 > 0:
            final_str += self.convert_sub_interger_num(0, v1)
            final_str += u'千'

        if v2 > 0:
            final_str += self.convert_sub_interger_num(v/1000, v2)
            final_str += u'百'

        if v3 > 0:
            if not (v3 == 1 and v1 == 0 and v2 == 0):
                final_str += self.convert_sub_interger_num(v/100, v3)
            final_str += u'十'

        if v4 > 0:
            final_str += self.convert_sub_interger_num(v/10, v4)

        return final_str

    def convert_sub_interger_num(self, pre_v, v):
        final_str = u''
        if pre_v%10 == 0 and pre_v%100 != 0:
            final_str += u'零'

        final_str += helper.num_2_ch(v)

        return final_str

    def process_date(self, num_str):
        flag, date = helper.get_date(num_str)
        if not flag:
            return u''

        if len(date) == 3:
            return self.process_digit(date[0]) + u'年' + self.process_num(date[1]) + u'月' + self.process_num(date[2]) + u'日'
        elif len(date) == 2:
            return self.process_digit(date[0]) + u'年' + self.process_num(date[1]) + u'月'
        else:
            return num_str

    def process_short_date(self, num_str):
        flag, date = helper.get_short_date(num_str)
        if not flag:
            return u''

        return self.process_digit(date[0]) + u'年' + self.process_num(date[1]) + u'月'

    def process_time(self, num_str):
        lst = num_str.split(u':')

        if len(lst) == 3:
            return self.process_num(lst[0]) + u'点' + self.process_num(lst[1]) + u'分' + self.process_num(lst[2]) + u'秒'
        elif len(lst) == 2:
            return self.process_num(lst[0]) + u'点' + self.process_num(lst[1]) + u'分'
        else:
            return num_str

    def process_colon_time(self, num_str):
        return self.process_time(num_str)

    def process_colon_ratio(self, num_str):
        if not u':' in num_str:
            return num_str

        index = num_str.find(u':')

        return self.process_num(num_str[0:index]) + u'比' + self.process_num(num_str[index+1:])

    def process_fraction(self, num_str):
        if not u'/' in num_str:
            return num_str

        index = num_str.find(u'/')

        return self.process_num(num_str[index+1:]) + u'分之' + self.process_num(num_str[0:index])

    def process_year(self, num_str):
        if num_str.isdigit():
            v = int(num_str)
            if v < 1000:
                return self.process_num(num_str)

        return self.process_digit(num_str)

    def process_unknown_digit(self, num_str): # 暂时无用
        if num_str.isdigit():
            v = int(num_str)
            if v <= 100:
                return self.process_num(num_str, process_two=False)

        return self.process_digit(num_str)

    def process_digit_change(self, num_str):
        final_str = u''

        for ch in num_str:
            if ch.isdigit():
                final_str += helper.num_2_ch(int(ch), digit_change=True)
            else:
                final_str += ch

        return final_str

    def process_unknown(self, num_str):
        final_str = u''

        for ch in num_str:
            if ch.isdigit():
                final_str += helper.num_2_ch(int(ch))
            elif helper.is_symbol(ch):
              final_str += helper.symbol_2_ch(ch)
            else:
                final_str += ch

        return final_str

    def process_percent(self, num_str):
        return u'百分之' + self.process_num(num_str[:-1])

    def process_range_percent(self, num_str):
        s = num_str[:-1]
        s = s.replace('%', '')
        return u'百分之' + self.process_range(s)

    def process_range_quan(self, num_str):
        return self.process_range(num_str)

    def process_range(self, num_str):
        if not u'-' in num_str:
            return num_str

        index = num_str.find(u'-')

        return self.process_num(num_str[0:index]) + u'到' + self.process_num(num_str[index+1:])


    def is_alphabet(self, uchar):
        if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
            return True
        else:
            return False


def generate_ch():
    # tagged_file_path = '../dataset/digit_samples_50000_taged'
    # ch_file_path = '../dataset/digit_samples_50000_ch'

    tagged_file_path = '../dataset/digit_samples_50000_digit_unknown_taged'
    ch_file_path = '../dataset/digit_samples_50000_digit_unknown_ch'

    if not os.path.exists(tagged_file_path):
        print('error: file_path not exist')
        return

    out_f = open(ch_file_path, 'w+')

    with open(tagged_file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            cc = ChConverter(line)
            final_str = cc.convert()

            out_f.write(final_str.encode('utf-8') + '\n')

    out_f.close()

def convert_one_sent(line):
    import text_normalized.parse

    ps = text_normalized.parse.NumParser(line)
    ps.prase()
    line = ps.export()

    # print "parse", line

    cc = ChConverter(line)
    final_str = cc.convert()
    return final_str

def test():
    line = u"比分23:24，12/22楼2楼第2只猫咪锤子2代手机1+1=2四川跨年玩创新互动 2.3萌物队23:55:11吃货队123年32-235个，10%，30度，编号124235235"
    print(line)
    print(convert_one_sent(line))

if __name__=="__main__":
    # generate_ch()
    test()
