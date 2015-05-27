# -*- coding: utf-8 -*-
"""
著作權所有 (C) 民國103年 意傳文化科技
開發者：薛丞宏
篩址：http://意傳.台灣
語料來源：請看各資料庫內說明

本程式乃自由軟體，您必須遵照SocialCalc設計的通用公共授權（Common Public Attribution License, CPAL)來修改和重新發佈這一程式，詳情請參閱條文。授權大略如下，若有歧異，以授權原文為主：
	１．得使用、修改、複製並發佈此程式碼，且必須以通用公共授權發行；
	２．任何以程式碼衍生的執行檔或篩路服務，必須公開該程式碼；
	３．將此程式的原始碼當函式庫引用入商業軟體，且不需公開非關此函式庫的任何程式碼

此開放原始碼、共享軟體或說明文件之使用或散佈不負擔保責任，並拒絕負擔因使用上述軟體或說明文件所致任何及一切賠償責任或損害。

臺灣言語工具緣起於本土文化推廣與傳承，非常歡迎各界用於商業軟體，但希望在使用之餘，能夠提供建議、錯誤回報或修補，回饋給這塊土地。

感謝您的使用與推廣～～勞力！承蒙！
"""
import re
import sys
import time


from 臺灣言語工具.斷詞.中研院.用戶端連線 import 用戶端連線
from 臺灣言語工具.基本元素.章 import 章
from 臺灣言語工具.基本元素.句 import 句
from 臺灣言語工具.解析整理.物件譀鏡 import 物件譀鏡
from 臺灣言語工具.解析整理.字物件篩仔 import 字物件篩仔
from 臺灣言語工具.基本元素.詞 import 詞
from 臺灣言語工具.基本元素.組 import 組
from 臺灣言語工具.基本元素.集 import 集

class 斷詞用戶端(用戶端連線):
	分詞性 = re.compile('(.*)\((.*)\)')
	def __init__(self, 主機='140.109.19.104', 連接埠=1501, 編碼='UTF-8',
			帳號='ihcaoe', 密碼='aip1614'):
		self.編碼 = 編碼
		self.主機 = 主機
		self.連接埠 = 連接埠
		self.帳號 = 帳號
		self.密碼 = 密碼
		
		self.譀鏡 = 物件譀鏡()
		self.篩仔 = 字物件篩仔()
	def 斷詞(self, 物件):
		if isinstance(物件, 章):
			return self._斷章物件詞(物件)
		return self._斷句物件詞(物件)
	def _斷章物件詞(self, 章物件):
		結果章物件 = 章()
		for 句物件 in 章物件.內底句:
			結果章物件.內底句.append(self._斷句物件詞(句物件))
		return 結果章物件
	def _斷句物件詞(self, 句物件):
		語句 = self.譀鏡.看型(句物件)
		結構化結果 = self.語句斷詞後結構化(語句)
		try:
			結構 = 結構化結果[0][0]
		except:
			結構 = []
		結果詞陣列 = []
		字陣列 = self.篩仔.篩出字物件(句物件)
		字物件指標 = 字陣列.__iter__()
		for 詞文本, 詞性 in 結構:
			字物件 = 字物件指標.__next__()
			while not 詞文本.startswith(self.譀鏡.看型(字物件)):
				結果詞物件 = 詞([字物件])
				結果詞物件.屬性 = {'詞性':''}
				結果詞陣列.append(結果詞物件)
				字物件 = 字物件指標.__next__()
			結果字陣列 = [字物件]
			for _ in range(len(詞文本) - 1):
				結果字陣列.append(字物件指標.__next__())
			結果詞物件 = 詞(結果字陣列)
			結果詞物件.屬性 = {'詞性':詞性}
			結果詞陣列.append(結果詞物件)
		try:
			while True:
				字物件 = 字物件指標.__next__()
				結果詞物件 = 詞([字物件])
				結果詞物件.屬性 = {'詞性':''}
				結果詞陣列.append(結果詞物件)
		except StopIteration:
			pass
		結果組物件 = 組()
		結果組物件.內底詞 = 結果詞陣列
		結果集物件 = 集()
		結果集物件.內底組 = [結果組物件]
		結果句物件 = 句()
		結果句物件.內底集 = [結果集物件]
		return 結果句物件
	def _字陣列轉組物件(self, 結果字陣列):
		結果詞物件 = 詞(結果字陣列)
		結果組物件 = 組()
		結果組物件.內底詞 = [結果詞物件]
		return 結果組物件
	def 語句斷詞後結構化(self, 語句):
		語句結果 = self.語句斷詞做語句(語句)
		結構化結果 = []
		for 一逝字 in 語句結果:
			一逝結構化=[]
			for 一句 in 一逝字:
				逝結果 = []
				for 詞 in 一句.strip().split('　'):
					if 詞 == '':
						continue
					try:
						字, 性 = self.分詞性.split(詞)[1:3]
					except:
						字, 性 = 詞, None
					逝結果.append((字, 性))
				一逝結構化.append(逝結果)
			結構化結果.append(一逝結構化)
		return 結構化結果
	def 語句斷詞做語句(self, 語句, 等待=3, 一定愛成功=False):
		while True:
			try:
				逐逝 = self.連線(語句, 等待, self.編碼, self.主機, self.連接埠, self.帳號, self.密碼)
			except Exception as 問題:
				if 一定愛成功:
					print('連線失敗，小等閣試……。原因：{0}'.format(問題),
						file=sys.stderr)
					time.sleep(10)
				else:
					raise
			else:
				break
		return 逐逝
