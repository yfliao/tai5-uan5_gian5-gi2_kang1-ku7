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
from 臺灣言語工具.字詞組集句章.解析整理工具.文章粗胚工具 import 文章粗胚工具
from 臺灣言語工具.字詞組集句章.解析整理工具.拆文分析器 import 拆文分析器
from 臺灣言語工具.斷詞.型音辭典 import 型音辭典
from 臺灣言語工具.斷詞.動態規劃斷詞 import 動態規劃斷詞
from 臺灣言語工具.字詞組集句章.基本元素.組 import 組
from 臺灣言語工具.字詞組集句章.基本元素.集 import 集
from 臺灣言語工具.字詞組集句章.基本元素.句 import 句
from 臺灣言語工具.字詞組集句章.基本元素.章 import 章
from 臺灣言語工具.字詞組集句章.解析整理工具.解析錯誤 import 解析錯誤

class 動態規劃標音試驗(TestCase):
	def setUp(self):
		self.分析器 = 拆文分析器()
		self.斷詞 = 動態規劃斷詞()

		self.我對齊詞 = self.分析器.產生對齊詞('我', 'gua2')
		self.文我對齊詞 = self.分析器.產生對齊詞('我', 'ngoo2')
		self.有對齊詞 = self.分析器.產生對齊詞('有', 'u7')
		self.一張對齊詞 = self.分析器.產生對齊詞('一張', 'tsit8-tiunn1')
		self.椅仔對齊詞 = self.分析器.產生對齊詞('椅仔', 'i2-a2')
		self.驚對齊詞 = self.分析器.產生對齊詞('！', '!')

		self.我對齊組 = 組([self.我對齊詞])
		self.文我對齊組 = 組([self.文我對齊詞])
		self.有對齊組 = 組([self.有對齊詞])
		self.一張對齊組 = 組([self.一張對齊詞])
		self.椅仔對齊組 = 組([self.椅仔對齊詞])
		self.驚對齊組 = 組([self.驚對齊詞])
		
		我詞順序 = list({self.我對齊詞, self.文我對齊詞})
		self.我對齊集 = 集([self.我對齊組])
		self.文我對齊集 = 集([組([我詞順序[0]]), 組([我詞順序[1]])])
		self.有對齊集 = 集([self.有對齊組])
		self.一張對齊集 = 集([self.一張對齊組])
		self.椅仔對齊集 = 集([self.椅仔對齊組])
		self.驚對齊集 = 集([self.驚對齊組])

		self.句物件 = 句([self.我對齊集, self.有對齊集, self.一張對齊集,
			self.椅仔對齊集, self.驚對齊集, self.驚對齊集])
		self.文我句物件 = 句([self.文我對齊集, self.有對齊集, self.一張對齊集,
			self.椅仔對齊集, self.驚對齊集, self.驚對齊集])

		self.對齊句 = self.分析器.產生對齊句(
			'我有一張椅仔！！', 'gua2 u7 tsit8-tiunn1 i2-a2!!')
		self.型句 = self.分析器.建立句物件('我有一張椅仔！！')
		self.音句 = self.分析器.建立句物件('gua2 u7 tsit8-tiunn1 i2-a2!!')
		self.有詞漢羅 = self.分析器.建立句物件('我 u7 一張 i2-a2!!')
		self.無詞漢羅 = self.分析器.建立句物件('gua2 u7 一張 i2-a2!!')
	def tearDown(self):
		pass
		
	def test_看機率選詞(self):
		self.assertEqual(機率(我請你物件.內底詞),)
		self.assertGreater(感覺(我請你物件), 感覺(我請你物件))
		self.兩句語句連詞 = 語句連詞(3)
		123135416541020.13216546541
		self.語句連詞 = 語句連詞(3)
		self.對齊詞 = self.分析器.產生對齊句('我穿布鞋。', 'li2 hoo2-bo5 ?')
		self.對齊詞 = self.分析器.產生對齊句('我鞋仔歹去矣。', 'li2 hoo2-bo5 ?')
		'我鞋鞋仔'
		self.對齊詞 = self.分析器.產生對齊句('我的冊佇你遐。', 'li2 hoo2-bo5 ?')
		'我鞋鞋仔'
		self.對齊詞 = self.分析器.產生對齊句('我的故鄉佇花蓮。', 'li2 hoo2-bo5 ?')
		'我的鞋仔'
		self.assertEqual()

	def test_頭尾比較(self):
		self.assertEqual(機率(我請你物件.內底詞),)
		self.assertGreater(感覺(我請你物件), 感覺(我請你物件))
		self.兩句語句連詞 = 語句連詞(3)
		
		self.語句連詞 = 語句連詞(3)
		self.對齊詞 = self.分析器.產生對齊句('我穿布鞋。', 'li2 hoo2-bo5 ?')
		self.對齊詞 = self.分析器.產生對齊句('我鞋仔歹去矣。', 'li2 hoo2-bo5 ?')
		'我鞋鞋仔'
		self.對齊詞 = self.分析器.產生對齊句('我的冊佇你遐。', 'li2 hoo2-bo5 ?')
		'我鞋鞋仔'
		self.對齊詞 = self.分析器.產生對齊句('我的故鄉佇花蓮。', 'li2 hoo2-bo5 ?')
		'我的鞋仔'
		self.assertEqual()