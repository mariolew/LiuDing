# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os, time, re

class TextNormTrainer(object):
    '''
    文本归一化训练器
    '''

    def __init__(self, feature_type):
        self.feature_type = feature_type
        self.train_feature = []
        self.model = None

    def process_data(self):
        train_file_path = '../dataset/digit_samples_50000_taged'

        fg = FetureGenerater(self.feature_type)
        fg.load_common_feature_map()

        with open(train_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace(line, '\n', '')
                line = line.replace(line, '\r', '')
                if not line:
                    continue
                if not isinstance(line, unicode):
                    line = unicode(line, 'utf-8')

                fe = FeatureExtractor(line, self.feature_type, fg)
                feature = fe.extract_all_feature(True)

    def train(self):
        self.model = RandomForestClassifier(n_estimators=10, min_samples_split=2, 
            min_samples_leaf=1, max_depth=None, max_features='auto', random_state=10, oob_score=True)

        self.model.fit(self.train_feature, self.train_label)