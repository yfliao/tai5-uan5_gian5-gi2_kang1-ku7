"""
著作權所有 (C) 民國103年 意傳文化科技
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
from 臺灣言語工具.字詞組集句章.解析整理.拆文分析器 import 拆文分析器

class 斷詞結構化工具:
	__分析器 = 拆文分析器()
	def 斷詞轉章物件(self, 斷詞結果):
		章物件=self.__分析器.建立章物件('')
		for 一逝 in 斷詞結果:
			句物件=self.斷詞轉句物件(一逝)
			章物件.內底句.append(句物件)
		return 章物件
	def 斷詞轉句物件(self, 斷詞結果):
		句物件=self.__分析器.建立句物件('')
		for 半句 in 斷詞結果:
			組物件=self.斷詞轉組物件(半句)
			集物件=self.__分析器.建立集物件('')
			集物件.內底組.append(組物件)
			句物件.內底集.append(集物件)
		return 句物件
	def 斷詞轉組物件(self, 斷詞結果):
		組物件=self.__分析器.建立組物件('')
		for 詞,詞性 in 斷詞結果:
			詞物件=self.__分析器.建立詞物件(詞)
			詞物件.屬性 = {'詞性':詞性}
			組物件.內底詞.append(詞物件)
		return 組物件