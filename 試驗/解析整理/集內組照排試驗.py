# -*- coding: utf-8 -*-
from unittest.case import TestCase
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.基本元素.集 import 集
from 臺灣言語工具.基本元素.句 import 句
from 臺灣言語工具.基本元素.章 import 章
from 臺灣言語工具.解析整理.集內組照排 import 集內組照排
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from timeit import itertools

class 集內組照排試驗(TestCase):
	def setUp(self):
		self.分析器 = 拆文分析器()
		self.組照排 = 集內組照排()

	def tearDown(self):
		pass

	def test_型照排(self):
		一 = self.分析器.建立組物件('1一')
		一.內底詞[0].屬性 = '我是一'
		空 = self.分析器.建立組物件('0零')
		空.屬性 = '⿰厓係零'
		顛倒集 = 集()
		顛倒集.內底組 = [一, 空]
		顛倒集.資料 = '9'
		答案集 = 集()
		答案集.內底組 = [空, 一]
		顛倒集.物件 = '6'
		譀鏡 = 物件譀鏡()
		排法 = lambda 組物件:譀鏡.看型(組物件)
		self.assertEqual(self.組照排.排好(排法, 顛倒集), 答案集)
		self.assertEqual(self.組照排.排好(排法, 答案集), 答案集)
		self.assertEqual(self.組照排.排好(排法, 顛倒集).內底組[0].屬性, 空.屬性)
		self.assertEqual(self.組照排.排好(排法, 答案集).內底組[0].屬性, 空.屬性)
		self.assertEqual(self.組照排.排好(排法, 顛倒集).內底組[1].內底詞[0].屬性, 一.內底詞[0].屬性)
		self.assertEqual(self.組照排.排好(排法, 答案集).內底組[1].內底詞[0].屬性, 一.內底詞[0].屬性)
		self.assertEqual(hasattr(self.組照排.排好(排法, 顛倒集), '資料'), False)
		self.assertEqual(hasattr(self.組照排.排好(排法, 答案集), '物件'), False)
		句物件 = 句()
		句物件.內底集 = [答案集, 顛倒集, 顛倒集]
		self.assertEqual(self.組照排.排好(排法, 句物件), 句([答案集, 答案集, 答案集]))
		self.assertEqual(self.組照排.排好(排法, 句物件).內底集[0].內底組[0].屬性, 空.屬性)
		self.assertEqual(self.組照排.排好(排法, 句物件).內底集[0].內底組[1].內底詞[0].屬性, 一.內底詞[0].屬性)
		self.assertEqual(self.組照排.排好(排法, 句物件).內底集[1].內底組[0].屬性, 空.屬性)
		self.assertEqual(self.組照排.排好(排法, 句物件).內底集[1].內底組[1].內底詞[0].屬性, 一.內底詞[0].屬性)
		self.assertEqual(self.組照排.排好(排法, 句物件).內底集[2].內底組[0].屬性, 空.屬性)
		self.assertEqual(self.組照排.排好(排法, 句物件).內底集[2].內底組[1].內底詞[0].屬性, 一.內底詞[0].屬性)
		章物件 = 章()
		章物件.內底句 = [句物件, 句物件]
		self.assertEqual(self.組照排.排好(排法, 章物件),
			章([句([答案集, 答案集, 答案集]), 句([答案集, 答案集, 答案集])]))
		self.assertEqual(self.組照排.排好(排法, 章物件).內底句[0].內底集[0].內底組[0].屬性, 空.屬性)
		self.assertEqual(self.組照排.排好(排法, 章物件).內底句[0].內底集[0].內底組[1].內底詞[0].屬性, 一.內底詞[0].屬性)
		self.assertEqual(self.組照排.排好(排法, 章物件).內底句[0].內底集[1].內底組[0].屬性, 空.屬性)
		self.assertEqual(self.組照排.排好(排法, 章物件).內底句[0].內底集[1].內底組[1].內底詞[0].屬性, 一.內底詞[0].屬性)
		self.assertEqual(self.組照排.排好(排法, 章物件).內底句[0].內底集[2].內底組[0].屬性, 空.屬性)
		self.assertEqual(self.組照排.排好(排法, 章物件).內底句[0].內底集[2].內底組[1].內底詞[0].屬性, 一.內底詞[0].屬性)
		self.assertEqual(self.組照排.排好(排法, 章物件).內底句[1].內底集[0].內底組[0].屬性, 空.屬性)
		self.assertEqual(self.組照排.排好(排法, 章物件).內底句[1].內底集[0].內底組[1].內底詞[0].屬性, 一.內底詞[0].屬性)
		self.assertEqual(self.組照排.排好(排法, 章物件).內底句[1].內底集[1].內底組[0].屬性, 空.屬性)
		self.assertEqual(self.組照排.排好(排法, 章物件).內底句[1].內底集[1].內底組[1].內底詞[0].屬性, 一.內底詞[0].屬性)
		self.assertEqual(self.組照排.排好(排法, 章物件).內底句[1].內底集[2].內底組[0].屬性, 空.屬性)
		self.assertEqual(self.組照排.排好(排法, 章物件).內底句[1].內底集[2].內底組[1].內底詞[0].屬性, 一.內底詞[0].屬性)
		
	def test_排序試驗(self):
		毋著四 = self.分析器.產生對齊組('我有一張椅仔', 'ngoo2 iu2 it4 tiong1 i2 a2')
		毋著三 = self.分析器.產生對齊組('我有一張椅仔', 'ngoo2 u7 it4 tiong1 i2 a2')
		毋著二 = self.分析器.產生對齊組('我有一張椅仔', 'ngoo2 u7 tsit8 tiong1 i2 a2')
		毋著一 = self.分析器.產生對齊組('我有一張椅仔', 'ngoo2 u7 tsit8 tiunn1 i2 a2')
		無毋著 = self.分析器.產生對齊組('我有一張椅仔', 'gua2 u7 tsit8 tiunn1 i2 a2')
		無毋著.分數 = 90
		毋著一.分數 = 80
		毋著二.分數 = 70
		毋著三.分數 = 60
		毋著四.分數 = 50
		答案集 = 集()
		答案集.內底組 = [無毋著, 毋著一, 毋著二, 毋著三, 毋著四, ]
		for 組陣列 in itertools.permutations([毋著四, 毋著三, 毋著二, 毋著一, 無毋著]):
			集物件 = 集()
			集物件.內底組 = 組陣列
			self.assertEqual(self.組照排.排好(lambda 組物件:-組物件.分數, 集物件), 答案集)
