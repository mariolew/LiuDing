# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../../")

import text_normalized.ch_convert as num_to_ch

a = "你好 123 5%"
a = num_to_ch.convert_one_sent(a)
print(a)
