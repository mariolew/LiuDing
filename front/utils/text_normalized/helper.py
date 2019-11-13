# -*- coding: utf-8 -*-

import os, time, re
import utils.text_normalized.const
import sys
import io

def folder(file):
	import os
	ret = os.path.abspath(file)
	return ret[:max(ret.rfind('\\'), ret.rfind('/')) + 1]

# 文件file所在目录的相对路径_path的绝对路径
def path(file, _path):
		return folder(file) + _path

class NormHelper(object):
	'''
	文本归一化帮助器
	'''

	def __init__(self, file_path="", except_file_path=""):
		file_path = file_path or path(__file__, './quantifier.txt')
		except_file_path = except_file_path or path(__file__, './quantifier_except.txt')

		self.quantifier_dict = {}
		self.except_quantifier_dict = {}

		f = io.open(file_path, "r", encoding="utf8")
		lines = f.readlines()
		f.close()

		for line in lines:
			line = line.replace('\n', '')
			line = line.replace('\r', '')
			lst = line.split(' ')
			if len(lst) <= 1:
				self.quantifier_dict[line] = 0
			else:
				self.quantifier_dict[line] = int(lst[1])
		f.close()


		f = io.open(except_file_path, "r", encoding="utf8")
		lines = f.readlines()
		for line in lines:
			line = line.replace('\n', '')
			line = line.replace('\r', '')
			line = line.replace(' ', '')
			#line = unicode(line, 'utf-8')
			self.except_quantifier_dict[line] = 1
		f.close()

		self.num_dict = {
			0: u'零',
			1: u'一',
			2: u'二',
			3: u'三',
			4: u'四',
			5: u'五',
			6: u'六',
			7: u'七',
			8: u'八',
			9: u'九',
		}

		self.symbol_dict = {
			u'=': u'等于',
			u'.': u'点',
			u':': u'比',
			u'+': u'加',
			# u'-': u'杠',
			u'-': u'减',
			u'%': u'百分之',
			u'~': u'到',
			# u'～': u'到',
		}

		self.tag_dict = {
			-1: "unknown",
			1: "num_quan",
			2: "percent",
			3: "range_percent",
			4: "range_quan",
			5: "time",
			6: "date",
			7: "colon_time",
			8: "colon_ratio",
			9: "decimal",
			10: "year",
			11: "digit",
			12: "range",
			13: "fraction",
		}

		self.sub_tag_dict = {
			-1: "unknown",
			0: "digit",
			1: "integer",
			2: "digit_change",
		}

		self.tag_reverse_dict = dict((v, k) for k, v in self.tag_dict.items())
		self.sub_tag_reverse_dict = dict((v, k) for k, v in self.sub_tag_dict.items())
		self.num_reverse_dict = dict((v, k) for k, v in self.num_dict.items())
		self.num_reverse_dict[u'幺'] = 1
		self.num_reverse_dict[u'两'] = 2

		self.time_keyword = [u'年', u'月', u'日', u'周', u'当天', u'上午', u'下午', u'夜',
		 u'播', u'航线', u'起飞', u'到达', u'返回',]
		self.time_keyword = dict((k,1) for k in self.time_keyword)

		self.ratio_keyword = [u'比分',  u'局',  u'盘', u'决赛', u'首节', u'半场', u'选手',
		 u'对手', u'名将', u'赢', u'胜', u'负', u'败', u'淘汰', u'不敌',  u'领先',  u'落后',
		 u'超出', u'比', u'投入', u'供需', u'率', u'战', u'打',]
		self.ratio_keyword = dict((k,1) for k in self.ratio_keyword)

		# 字符转换器
		self.pat_all_num = re.compile(u'[\d\-\+=~\/\%][\d\.\-\+=~\/\%:]*')

		self.pat_integer = re.compile(u'^([\+\-]?)\d+$')
		self.pat_decimal = re.compile(u'^([\+\-]?)(\d+)\.(\d+)$')
		self.pat_number = re.compile(u'^([\+\-]?)(\d+)(\.\d+)?$')

		self.pat_range_percent = re.compile(u'^((\d+)(\.\d+)?)%?\-((\d+)(\.\d+)?)%$')
		self.pat_percent = re.compile(u'^(\d+)(\.\d+)?%$')
		self.pat_range = re.compile(u'^((\d+)(\.\d+)?)\-((\d+)(\.\d+)?)$')

		self.pat_date = re.compile(u'^(^(\d{4}|\d{2})(\-|\/|\.)(\d{1,2})\3(\d{1,2})$)$')
		self.pat_short_date = re.compile(u'^(^(\d{4})(\-|\/|\.)(\d{1,2})$)$')

		self.pat_time = re.compile(u'^(20|21|22|23|[0-1]\d):([0-5]\d):([0-5]\d)$')
		self.pat_short_time = re.compile(u'^([0-5]\d):([0-5]\d)$')

		self.pat_colon = re.compile(u'^\d+(\.\d+)?:\d+(\.\d+)?$')

		self.pat_fraction = re.compile(u'^\d+(\.\d+)?\/\d+(\.\d+)?$')

		self.pat_all_tag = re.compile(u'<([\w\-]+)>([^<]+)(<\/[\w\-]+>)')

		# 数字转换器
		self.pat_ch_all_num = re.compile(u'(百分之)?([零|幺|一|两|二|三|四|五|六|七|八|九|十|百|千|万|亿]+)点?([零|幺|一|两|二|三|四|五|六|七|八|九|十]+)?')

	def get_all_num_info(self, str):
		'''
		获取句子中的数字
		'''
		all_num_info = []
		i = 0
		for m in self.pat_all_num.finditer(str):
			all_num_info.append({'start_index': m.start(), 'end_index': m.end(),
			 'num_str': m.group(), 'num_type': -1, 'sub_num_type': -1, 'index': i})
			i += 1

		return all_num_info

	def get_all_tag_info(self, str):
		all_tag_info = []
		i = 0
		for m in self.pat_all_tag.finditer(str):
			type, sub_type = self.tag2type(m.group(1))
			all_tag_info.append({'start_index': m.start(), 'end_index': m.end(),
			 'num_str': m.group(2), 'num_type': type, 'sub_num_type': sub_type, 'index': i})
			i += 1

		return all_tag_info

	def replace_tag(self, str):
		return self.pat_all_tag.sub('1', str)

	def get_all_replaced_tag_info(self, str, tag_info):
		all_tag_info = []
		i = 0
		for m in self.pat_all_num.finditer(str):
			all_tag_info.append({'start_index': m.start(), 'end_index': m.end(),
			 'num_str': tag_info[i]['num_str'], 'num_type': tag_info[i]['num_type'], 'sub_num_type': tag_info[i]['sub_num_type'], 'index': i})

			i += 1

		return all_tag_info

	def get_all_ch_info(self, str):
		all_ch_info = []
		i = 0
		for m in self.pat_ch_all_num.finditer(str):
			all_ch_info.append({'start_index': m.start(), 'end_index': m.end(),
			 'num_str': m.group(), 'num_type': -1, 'sub_num_type': -1, 'index': i})
			i += 1

		return all_ch_info

	def is_integer(self, num_str):
		'''
		是否是整数
		'''
		m = self.pat_integer.search(num_str)
		if not m:
			return False

		return True

	def is_decimal(self, num_str):
		'''
		是否是小数
		'''
		m = self.pat_decimal.search(num_str)
		if not m:
			return False

		return True

	def is_number(self, num_str):
		'''
		是否是数字
		'''
		m = self.pat_number.search(num_str)
		if not m:
			return False

		return True

	def is_percent(self, num_str):
		'''
		是否是比例
		'''
		m = self.pat_percent.search(num_str)
		if not m:
			return False

		return True

	def is_range_percent(self, num_str):
		'''
		是否是范围比例
		'''
		m = self.pat_range_percent.search(num_str)
		if not m:
			return False

		return True

	def is_range(self, num_str):
		'''
		是否是范围
		'''
		m = self.pat_range.search(num_str)
		if not m:
			return False

		return True

	def is_quantifier(self, str):
		'''
		字符前面是否是量词
		'''
		l = min(len(str), 5)

		for i in range(0, l):
			sub_str = str[0:(i+1)]

			if not sub_str in self.quantifier_dict:
				continue

			has_except = False
			for j in range(i, l):
				except_str = str[0:(j+1)]
				if except_str in self.except_quantifier_dict:
					has_except = True
					break

			if not has_except:
				return True, sub_str

		return False, None

	def is_quantifier_digit_change(self, str):
		if not str in self.quantifier_dict:
			return False

		if self.quantifier_dict[str] == 0:
			return True

		return False

	def num_2_ch(self, num, digit_change=False):
		'''
		数字转中文字符
		'''
		change_mapping = {
			1: u'幺',
			2: u'两',
		}
		if digit_change and num in change_mapping:
			return change_mapping[num]

		if not num in self.num_dict:
			print("warning: num_2_ch", num)
			return u''

		return self.num_dict[num]

	def symbol_2_ch(self, symbol):
		'''
		字符转中文字符
		'''
		if not symbol in self.symbol_dict:
			print("warning: symbol_2_ch", symbol)
			return u''

		return self.symbol_dict[symbol]

	def is_date(self, num_str):
		'''
		是否是长日期
		'''
		m = self.pat_date.search(num_str)
		if not m:
			return False

		return True

	def get_date(self, num_str):
		ret = self.pat_date.findall(num_str)
		if not ret:
			return False, None

		return True, (ret[0][1], ret[0][3], ret[0][4])
	
	def is_short_date(self, num_str):
		'''
		是否是短日期
		'''
		m = self.pat_short_date.search(num_str)
		if not m:
			return False

		return True

	def get_short_date(self, num_str):
		ret = self.pat_short_date.findall(num_str)
		if not ret:
			return False, None

		return True, (ret[0][1], ret[0][3])

	def is_time(self, num_str):
		'''
		是否是长时间
		'''
		m = self.pat_time.search(num_str)
		if not m:
			return False

		return True

	def is_short_time(self, num_str):
		'''
		是否是短时间
		'''
		m = self.pat_short_time.search(num_str)
		if not m:
			return False

		return True

	def is_colon(self, num_str):
		'''
		是否是冒号
		'''
		m = self.pat_colon.search(num_str)
		if not m:
			return False

		return True

	def is_fraction(self, num_str):
		'''
		是否是分数
		'''
		m = self.pat_fraction.search(num_str)
		if not m:
			return False

		return True

	def get_feature_pri(self, sent, start_index, end_index, keyword_type=0):
		'''
		关键词优先级
		'''
		pri = 10000

		if keyword_type == 0:
			keyword = self.time_keyword
		else:
			keyword = self.ratio_keyword

		for i in range(1, 5):
			start = start_index+i
			if sent[start:start+2] in keyword:
				return i

			if sent[start:start+1] in keyword:
				return i

			start = start_index-i
			if sent[start:start+2] in keyword:
				return i-1

			if sent[start:start+1] in keyword:
				return i

		return pri

	def type2tag(self, type, sub_type=-1):
		if not type in self.tag_dict or not sub_type in self.sub_tag_dict:
			print('warning: type2tag', type, sub_type)
			return "unknown"

		if sub_type != -1:
			return self.tag_dict[type] + '-' + self.sub_tag_dict[sub_type]
		else:
			return self.tag_dict[type]

	def tag2type(self, tag):
		tags = tag.split('-')
		if len(tags) >= 2:
			tag = tags[0]
			sub_tag = tags[1]
		else:
			tag = tag
			sub_tag = "unknown"

		if not tag in self.tag_reverse_dict or not sub_tag in self.sub_tag_reverse_dict:
			print('warning: tag2type', tag, sub_tag)
			return text_normalized.const.TYPE_UNKNOWN, text_normalized.const.SUB_TYPE_UNKNOWN

		return self.tag_reverse_dict[tag], self.sub_tag_reverse_dict[sub_tag]

	def has_ch_num_sep(self, str):
		lst = [u'十', u'百', u'千', u'万', u'亿', u'点']
		dct = dict((k, 1) for k in lst)

		for ch in str:
			if ch in dct: 
				return True

		return False

	def is_ch_all_digit(self, str):
		lst = [u'零', u'幺', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九']
		dct = dict((k, 1) for k in lst)

		for ch in str:
			if not ch in dct: 
				return False

		return True

	def is_symbol(self, ch):
		if not ch in self.symbol_dict:
			return False

		return True

	def symbol_2_ch(self, ch):
		if not ch in self.symbol_dict:
			return u''

		return self.symbol_dict[ch]

	def ch_2_num(self, ch):
		'''
		中文字符转数字
		'''
		if not ch in self.num_reverse_dict:
			return -1

		return self.num_reverse_dict[ch]


helper = NormHelper()

def get_norm_helper():
	return helper
