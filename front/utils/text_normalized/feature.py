# -*- coding:utf-8 -*-

import os, time, re, json
import operator
import utils.text_normalized.helper, utils.text_normalized.const
import utils.text_normalized.parse

helper = helper.get_norm_helper()

class FeatureExtractor(object):
    '''
    特征提取器
    '''

    def __init__(self, sent, feature_type, generator):
        sent = sent.replace('\n', '')
        sent = sent.replace('\r', '')
        if not isinstance(sent, unicode):
            sent = unicode(sent, 'utf-8')
        self.raw_sent = sent
        self.sent = sent
        self.generator = generator

        self.feature_type = feature_type
        self.all_tag_info = []
        self.feature = []

        self.all_raw_tag_info = helper.get_all_tag_info(self.raw_sent)
        self.sent =  helper.replace_tag(self.raw_sent)
        self.all_tag_info = helper.get_all_replaced_tag_info(self.sent, self.all_raw_tag_info)

    def extract_common_gram(self):
        final_uni_gram = []
        final_bi_gram = []
        final_tri_gram = []
        final_four_gram = []

        for index, tag_info in enumerate(self.all_tag_info):
            uni_gram, bi_gram, tri_gram, four_gram = self.extract_one_common_gram(index)

            final_uni_gram.extend(uni_gram)
            final_bi_gram.extend(bi_gram)
            final_tri_gram.extend(tri_gram)
            final_four_gram.extend(four_gram)

        return (final_uni_gram, final_bi_gram, final_tri_gram, final_four_gram)

    def extract_one_common_gram(self, index):
        uni_gram = []
        bi_gram = []
        tri_gram = []
        four_gram = []

        tag_info = self.all_tag_info[index]
        start_index = tag_info['start_index']
        end_index = tag_info['end_index']

        # print "extract_one_common_gram", tag_info['num_type'], tag_info['sub_num_type'], self.feature_type

        if tag_info['num_type'] != self.feature_type or tag_info['sub_num_type'] != -1:
            return (uni_gram, bi_gram, tri_gram, four_gram) 

        for i in xrange(-4, 5):
            begin = start_index+i
            end = start_index+i+1
            if begin >= 0 and end < len(self.sent) and end >= 0 and end < len(self.sent):
                uni_gram.append(self.sent[begin:end])

        for i in xrange(-4, 4):
            begin = start_index+i
            end = start_index+i+2
            if begin >= 0 and end < len(self.sent) and end >= 0 and end < len(self.sent):
                bi_gram.append(self.sent[begin:end])

        for i in xrange(-4, 3):
            begin = start_index+i
            end = start_index+i+3
            if begin >= 0 and end < len(self.sent) and end >= 0 and end < len(self.sent):
                tri_gram.append(self.sent[begin:end])

        for i in xrange(-4, 2):
            begin = start_index+i
            end = start_index+i+4
            if begin >= 0 and end < len(self.sent) and end >= 0 and end < len(self.sent):
                four_gram.append(self.sent[begin:end])

        return (uni_gram, bi_gram, tri_gram, four_gram)

    def extract_one_feature(self, index):
        one_common_feature = self.extract_one_common_feature(index)
        one_special_feature = self.extract_one_special_feature(index)

        return one_common_feature.extend(one_special_feature)

    def extract_all_feature(self, train=False):
        all_feature = []
        for index, tag_info in enumerate(self.all_tag_info):
            if tag_info['num_type'] != self.feature_type:
                continue

            if train:
                if tag_info['sub_num_type'] == -1:
                    continue
            else:
                if tag_info['sub_num_type'] != -1:
                    continue

            all_feature.append((index, self.extract_one_feature(index), tag_info['num_type'], tag_info['sub_num_type']))

        return all_feature

    def extract_one_common_feature(self, index):
        uni_gram, bi_gram, tri_gram, four_gram = extractor.extract_one_common_gram(index)

        gram_lst = [uni_gram, bi_gram, tri_gram, four_gram]
        feature_lst = []
        for index, grams in enumerate(gram_lst):
            length = self.generator.get_feature_len(index)
            feture = [0 for i in range(0, length)]
            feature_lst.append(feature)

        for index, grams in enumerate(gram_lst):
            for gram in grams:
                index_value = self.generator.get_index_by_gram(index, gram)
                if index_value > 0:
                    feature_lst[index][index_value] = 1

        final_feature = []
        for feature in feature_lst:
            final_feature.extend(feture)

        return final_feature

    def extract_one_special_feature(self, index):
        feature = []

        num_str = tag_info['num_str']
        start_index = tag_info['start_index']
        end_index = tag_info['end_index']

        if len(num_str) > 0 and num_str[0] == '0':
          feature.append(1)
        else:
          feature.append(0)

        if len(num_str) > 0 and num_str[len(num_str)-1] == '0':
            feature.append(1)
        else:
            feature.append(0)

        for i in xrange(1, 5):
            if len(num_str) == i:
                feature.append(1)
            else:
                feature.append(0)

        if len(num_str) > 4:
            feature.append(1)
        else:
            feature.append(0)

        if num_str in ['110', '120', '119', '12306', '911']:
            feture.append(1)
        else:
            feture.append(0)

        try:
            v = int(float(num_str))
        except:
            v = 0

        num_range = [[1000, 1900], [1900, 2000], [2000, 2030]]
        for r in num_range:
            if v >= r[0] and v < r[1]:
                feture.append(1)
            else:
                feture.append(0)

        if start_index-1>=0 and self.sent[start_index].isalpha():
            feature.append(1)
        else:
            feature.append(0)

        if end_index<len(self.sent) and self.sent[end_index].isalpha():
            feature.append(1)
        else:
            feature.append(0)

        if end_index == len(self.sent) or end_index < len(self.sent) and self.sent[end_index] == ' ':
            feature.append(1)
        else:
            feature.append(0)

        return feture

class FetureGenerater(object):
    '''
    特征生成器
    '''

    def __init__(self, feature_type):
        self.feature_type = feature_type

        self.uni_gram = {}
        self.bi_gram = {}
        self.tri_gram = {}
        self.four_gram = {}

        self.final_uni_gram = {}
        self.final_bi_gram = {}
        self.final_tri_gram = {}
        self.final_four_gram = {}

        self.MAX_GRAM_LEN = [1000, 1000, 1000, 1000]
        self.MIN_GRAM_CNT = [2, 2, 2, 2]

    def get_index_by_gram(self, gram_type, value):
        src = [self.final_uni_gram, self.final_bi_gram,
         self.final_tri_gram, self.final_four_gram]

        src_gram = src[gram_type]
        if value in src_gram:
            return src_gram[value]

        return -1

    def get_feature_len(self, gram_type):
        src = [self.final_uni_gram, self.final_bi_gram,
         self.final_tri_gram, self.final_four_gram]
        return len(src[gram_type])

    def process_sent(self, sent):
        extractor = FeatureExtractor(sent, self.feature_type, self)
        uni_gram, bi_gram, tri_gram, four_gram = extractor.extract_common_gram()

        src = [uni_gram, bi_gram,
         tri_gram, four_gram]
        dest = [self.uni_gram, self.bi_gram,
         self.tri_gram, self.four_gram]

        for index, grams in enumerate(src):
            for gram in grams:
                if not gram in dest[index]:
                    dest[index][gram] = 0

                dest[index][gram] += 1

    def gen_feature_map(self):
        src = [self.uni_gram, self.bi_gram,
         self.tri_gram, self.four_gram]
        dest = [self.final_uni_gram, self.final_bi_gram,
         self.final_tri_gram, self.final_four_gram]

        for index, gram in enumerate(src):
            sorted_gram = sorted(gram.items(), key=operator.itemgetter(1), reverse=True)

            MAX_UNI_GRAM_LEN = 1000
            MIN_UNI_GRAM_CNT = 2
            for i, item in enumerate(sorted_gram):
                if i >= self.MAX_GRAM_LEN[index]:
                    break

                if item[1] < self.MIN_GRAM_CNT[index]:
                    break

                dest[index][item[0]] = i

    def save_common_feature_map(self):
        file_path = ['../feature/uni_gram_map', '../feature/bi_gram_map',
        '../feature/tri_gram_map', '../feature/four_gram_map']
        src = [self.final_uni_gram, self.final_bi_gram,
         self.final_tri_gram, self.final_four_gram]

        for index, path in enumerate(file_path):
            with open(path, 'w+') as f:
                ret = sorted(src[index].items(), key=operator.itemgetter(1), reverse=True)
                for k, v in ret:
                    if isinstance(k, unicode):
                        s = k.encode('utf-8') + ' ' + ("%d" % v)
                    else:
                        s = k + " " + v

                    f.write(s + "\n")

    def load_common_feature_map(self):
        file_path = ['../feature/uni_gram_map', '../feature/bi_gram_map',
        '../feature/tri_gram_map', '../feature/four_gram_map']
        src = [self.final_uni_gram, self.final_bi_gram,
         self.final_tri_gram, self.final_four_gram]

        for index, path in enumerate(file_path):
            with open(path, 'r') as f:
                src[index] = {}
                lines = f.readlines()

                for line in lines:
                    line = line.replace('\n', '')
                    line = line.replace('\r', '')
                    if len(line) <= 0:
                        continue

                    elems = line.split(' ')
                    index = line.rindex(' ')
                    k, v = line[0:index], line[index+1:]
                    src[index][k.decode('utf-8')] = int(v)

def generate_taged_text():
    # file_path = '../dataset/digit_samples_50000'
    # taged_file_path = '../dataset/digit_samples_50000_taged'
    file_path = '../dataset/digit_samples_50000_digit_unknown'
    taged_file_path = '../dataset/digit_samples_50000_digit_unknown_taged'

    if not os.path.exists(file_path):
        print('error: file_path not exist')
        return

    out_f = open(taged_file_path, 'w+')

    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            ps = parse.NumParser(line)
            ps.prase()
            out_f.write(ps.export().encode('utf-8'))
            out_f.write('\n')

    out_f.close()

def generate_feature():
    taged_file_path = '../dataset/digit_samples_50000_taged'

    if not os.path.exists(taged_file_path):
        print('error: taged_file_path not exist')
        return

    fg = FetureGenerater(const.TYPE_DIGIT)
    with open(taged_file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            fg.process_sent(line)

    fg.gen_feature_map()
    fg.save_common_feature_map()

if __name__=="__main__":
    generate_taged_text()
    # generate_feature()
