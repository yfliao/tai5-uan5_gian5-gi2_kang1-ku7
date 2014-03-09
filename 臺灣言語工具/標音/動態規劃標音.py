"""
著作權所有 (C) 民國102年 意傳文化科技
開發者：薛丞宏
網址：http://意傳.台灣
語料來源：請看各資料庫內說明

本程式乃自由軟體，您必須遵照SocialCalc設計的通用公共授權（Common Public Attribution License, CPAL)來修改和重新發佈這一程式，詳情請參閱條文。授權大略如下，若有歧異，以授權原文為主：
	１．得使用、修改、複製並發佈此程式碼，且必須以通用公共授權發行；
	２．任何以程式碼衍生的執行檔或網路服務，必須公開該程式碼；
	３．將此程式的原始碼當函式庫引用入商業軟體，且不需公開非關此函式庫的任何程式碼

此開放原始碼、共享軟體或說明文件之使用或散佈不負擔保責任，並拒絕負擔因使用上述軟體或說明文件所致任何及一切賠償責任或損害。

臺灣言語工具緣起於本土文化推廣與傳承，非常歡迎各界用於商業軟體，但希望在使用之餘，能夠提供建議、錯誤回報或修補，回饋給這塊土地。

感謝您的使用與推廣～～勞力！承蒙！
"""
from unittest.case import TestCase
from 臺灣言語工具.字詞組集句章.解析整理.文章粗胚 import 文章粗胚
from 臺灣言語工具.字詞組集句章.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.斷詞.型音辭典 import 型音辭典
from 臺灣言語工具.斷詞.動態規劃斷詞 import 動態規劃斷詞
from 臺灣言語工具.字詞組集句章.基本元素.字 import 字
from 臺灣言語工具.字詞組集句章.基本元素.詞 import 詞
from 臺灣言語工具.字詞組集句章.基本元素.組 import 組
from 臺灣言語工具.字詞組集句章.基本元素.集 import 集
from 臺灣言語工具.字詞組集句章.基本元素.句 import 句
from 臺灣言語工具.字詞組集句章.基本元素.章 import 章
from 臺灣言語工具.字詞組集句章.解析整理.解析錯誤 import 解析錯誤
from 臺灣言語工具.字詞組集句章.解析整理.詞物件網仔 import 詞物件網仔

class 動態規劃標音(TestCase):
	__網仔 = 詞物件網仔()
	基本 = 0.02
	權重 = [0.08, 0.2, 0.7]
	def 評分(self, 連詞, 物件):
		詞陣列 = [None] + self.__網仔.網出詞物件(物件) + [None]
		return self.評詞陣列分(連詞, 詞陣列)

	def 感覺(self, 連詞, 語句):
		條件 = 連詞.條件(語句)
		分數 = self.基本
		for 分, 權 in zip(條件, self.權重):
			分數 += 連詞.指數(分) * 權
		return 連詞.對數(分數)

	def 標音(self, 連詞, 物件):
		if isinstance(物件, 字) or isinstance(物件, 詞) or isinstance(物件, 組):
			return self.標字詞組物件音(連詞, 物件)
		if isinstance(物件, 集):
			句物件 = 句()
			句物件.內底集.append(物件)
			標好句物件, 上好分數 , 詞數 = self.標句物件音(連詞, 句物件)
			return (標好句物件.內底集[0], 上好分數, 詞數)
		if isinstance(物件, 句):
			return self.標句物件音(連詞, 物件)
		if isinstance(物件, 章):
			return self.標章物件音(連詞, 物件)
		self.__掠漏.毋是字詞組集句章的毋著(物件)

	def 標字詞組物件音(self, 連詞, 物件):
# 		return (物件, self.評分(連詞, 物件),)
		return (物件, self.評分(連詞, 物件), len(self.__網仔.網出詞物件(物件)) + 2)

	def 標章物件音(self, 連詞, 章物件):
		標好章物件 = 章()
		總分 = 0
		總詞數 = 0
		for 句物件 in 章物件.內底句:
# 			標好句物件, 分數 = self.標句物件音(連詞, 句物件)
			標好句物件, 分數, 詞數 = self.標句物件音(連詞, 句物件)
			標好章物件.內底句.append(標好句物件)
			總分 += 分數
			總詞數 += 詞數
		return (標好章物件, 總分, 總詞數)

	def 標句物件音(self, 連詞, 句物件):
		全部分數佮來源 = [{(None,):(self.評詞陣列分(連詞, [None]), 1, None)}]
		if len(句物件.內底集) == 0:
			分數, 詞數, 來源 = 全部分數佮來源[-1][(None,)]
			算的分數, 算的詞數 = self.算上尾組物件分數(連詞, (None, 組()), True)
			這馬詞數 = 詞數 + 算的詞數
			這馬分數 = (分數 * 詞數 + 算的分數 * 算的詞數) / 這馬詞數
			return (句物件, 這馬分數, 這馬詞數)
		for 這馬集物件 in 句物件.內底集:
			這格分數佮來源 = {}
			for 組合, 分數佮來源 in 全部分數佮來源[-1].items():
				分數, 詞數, 來源 = 分數佮來源
				if len(這馬集物件.內底組) == 0:
					raise 解析錯誤('有空的集物件：{0}'.format(句物件))
				for 選擇組物件 in 這馬集物件.內底組:
					這馬組合 = (組合 + (選擇組物件,))[-連詞.上濟詞數:]
					算的分數, 算的詞數 = self.算上尾組物件分數(連詞, 這馬組合,
						len(全部分數佮來源) == len(句物件.內底集))
					這馬詞數 = 詞數 + 算的詞數
					這馬分數 = (分數 * 詞數 + 算的分數 * 算的詞數) / 這馬詞數
#  					print  (分數 , 詞數 , 算的分數 , 算的詞數 , 這馬詞數, '=>', 這馬分數)
					if 這馬組合 not in 這格分數佮來源:
						這格分數佮來源[這馬組合] = (這馬分數, 這馬詞數, 組合)
					elif 這馬分數 > 這格分數佮來源[這馬組合][0]:
						這格分數佮來源[這馬組合] = (這馬分數, 這馬詞數, 組合)
			全部分數佮來源.append(這格分數佮來源)
		結果集陣列 = []
		這馬組合 = None
		上好分數 = None
		結果詞數 = None
		for 組合, 分數佮來源 in 全部分數佮來源[-1].items():
			分數, 詞數, 來源 = 分數佮來源
			if 這馬組合 == None or 分數 > 上好分數:
				這馬組合 = 組合
				上好分數 = 分數
				結果詞數 = 詞數
		for 這格分數佮來源 in 全部分數佮來源[:0:-1]:
			集物件 = 集()
			# 物件內底毋是空的
# 			if 這馬組合!=None:
			集物件.內底組.append(這馬組合[-1])
			結果集陣列.append(集物件)
			分數, 詞數, 來源 = 這格分數佮來源[這馬組合]
			這馬組合 = 來源
		句物件 = 句()
		句物件.內底集 = 結果集陣列[::-1]
		return (句物件, 上好分數, 結果詞數)

	def 算上尾組物件分數(self, 連詞, 組陣列, 是毋是上尾一个):
		頭前詞陣列 = []
		for 組物件 in 組陣列[-2::-1]:
			if 組物件 == None:
				頭前詞陣列.insert(0, None)
			else:
				頭前詞陣列 = 組物件.內底詞 + 頭前詞陣列
			if len(頭前詞陣列) >= 連詞.上濟詞數:
				頭前詞陣列 = 頭前詞陣列[-連詞.上濟詞數:]
				break
		評分詞陣列 = 頭前詞陣列 + 組陣列[-1].內底詞
		if 是毋是上尾一个:
			評分詞陣列.append(None)
		return self.評詞陣列分(連詞, 評分詞陣列, len(頭前詞陣列)), len(評分詞陣列) - len(頭前詞陣列)

	def 評詞陣列分(self, 連詞, 詞陣列, 開始的所在 = 0):
		分數 = 0
		for 所在 in range(開始的所在, len(詞陣列)):
			分數 += self.感覺(連詞, 詞陣列[max(0, 所在 + 1 - 連詞.上濟詞數):所在 + 1])
		return 分數 / (len(詞陣列) - 開始的所在)
