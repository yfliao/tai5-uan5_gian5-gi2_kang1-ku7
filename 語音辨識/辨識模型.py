import os
import itertools
import shutil
import re
from 臺灣言語工具.語音合成.句物件轉合成標仔 import 句物件轉合成標仔

class 辨識模型:
	wav副檔名 = '.wav'
	音檔副檔名 = wav副檔名
	標仔副檔名 = '.lab'
	特徵 = 'mfcc'
	特徵副檔名 = '.' + 特徵
	音檔結束符號 = '.'
	_轉合成標仔 = 句物件轉合成標仔()
	恬音 = _轉合成標仔.產生主要音值標仔(_轉合成標仔.恬音)
	短恬 = _轉合成標仔.產生主要音值標仔(_轉合成標仔.短恬)
	def 訓練(self, 音檔目錄, 標仔目錄, 音節聲韻對照檔, 資料目錄, 執行檔路徑='',
			加切短恬=False, 三連音=False,
			算特徵=True,  # 開發用的
			):
		執行檔路徑 = self.執行檔路徑加尾(執行檔路徑)
		全部語料 = self.揣全部語料(音檔目錄, 標仔目錄)
		
		全部特徵檔 = os.path.join(資料目錄, '全部特徵檔.scp')
		全部標仔檔 = os.path.join(資料目錄, '全部標仔檔.scp')
		os.makedirs(資料目錄, exist_ok=True)
		# 開發用的
		if 算特徵:
			self.揣特徵而且算(執行檔路徑, 資料目錄, 全部語料, 全部特徵檔)
		原來音類檔 = os.path.join(資料目錄, '原來音類檔.list')
		原來音節檔 = os.path.join(資料目錄, '原來音節檔.mlf')
		聲韻類檔 = os.path.join(資料目錄, '聲韻類檔.list')
		聲韻檔 = os.path.join(資料目錄, '聲韻檔.mlf')
		加恬音節檔 = os.path.join(資料目錄, '加恬音節檔.mlf')
		加恬音類檔 = os.path.join(資料目錄, '加恬音類檔.list')
		加恬聲韻類檔 = os.path.join(資料目錄, '加恬聲韻類檔.list')
		加恬聲韻檔 = os.path.join(資料目錄, '加恬聲韻檔.mlf')
		
# 		if 切標仔:
		全部標仔 = []
		for 語料 in 全部語料:
			標仔所在 = 語料[2]
			全部標仔.append(標仔所在)
		self.陣列寫入檔案(全部標仔檔, 全部標仔)
		self.標仔收集起來(執行檔路徑, 全部標仔檔, 資料目錄, 原來音類檔, 原來音節檔)
		self.標仔切做聲韻(執行檔路徑, 原來音節檔, 音節聲韻對照檔, 資料目錄, 聲韻類檔, 聲韻檔)
		self.音類標仔加短恬(原來音類檔, 加恬音類檔)
		if len(self.讀檔案(原來音節檔)) > 200:
			'音節轉聲韻，漢語聲韻加起來袂超過200'
			self.音節標仔加短恬(原來音節檔, 加恬音節檔)
		else:
			'聲韻轉聲韻，漢語聲韻加起來袂超過200'
			self.音節標仔逐字中央加短恬(原來音節檔, 加恬音節檔)
		self.標仔切做聲韻(執行檔路徑, 加恬音節檔, 音節聲韻對照檔, 資料目錄, 加恬聲韻類檔, 加恬聲韻檔)
# 		if 做初步模型:
		做好的初步模型檔 = os.path.join(資料目錄, '初步模型檔-重估.macro')
		初步模型檔 = self.建立初步模型(執行檔路徑, 資料目錄, 全部特徵檔, 聲韻類檔, 聲韻檔)
		self.模型重估(執行檔路徑, 資料目錄, 全部特徵檔, 聲韻類檔, 聲韻檔, 初步模型檔, 估幾擺=60)
		上尾模型檔 = 做好的初步模型檔
		if 加切短恬:
			加短恬的模型 = os.path.join(資料目錄, '加短恬的模型.macro')
			self.模型加短恬(初步模型檔, 加短恬的模型)
			加短恬的重估模型 = self.模型重估(執行檔路徑, 資料目錄, 全部特徵檔,
				加恬聲韻類檔, 加恬聲韻檔, 加短恬的模型, 估幾擺=20)
			
			對齊聲韻結果檔 = self.對齊聲韻(加恬聲韻類檔, 加短恬的模型, 加恬聲韻檔,
				全部特徵檔, 資料目錄, 執行檔路徑=執行檔路徑)
			新拄好短恬全部標仔檔 = os.path.join(資料目錄, '新拄好短恬全部標仔檔.scp')
			self.陣列寫入檔案(新拄好短恬全部標仔檔, self.標仔換目錄(全部標仔檔, 對齊聲韻結果檔))
			
			新對齊短恬聲韻檔 = os.path.join(資料目錄, '新對齊短恬聲韻檔.mlf')
			用袂著的檔案 = os.path.join(資料目錄, '用袂著的檔案.garbage')
			self.標仔收集起來(執行檔路徑, 新拄好短恬全部標仔檔,
				資料目錄, 用袂著的檔案, 新對齊短恬聲韻檔)
			新拄好短恬聲韻檔 = os.path.join(資料目錄, '新拄好短恬聲韻檔.mlf')
			self.提掉傷短的短恬(新對齊短恬聲韻檔, 新拄好短恬聲韻檔)
			拄好短恬的重估模型 = self.模型重估(執行檔路徑, 資料目錄, 全部特徵檔,
				加恬聲韻類檔, 新拄好短恬聲韻檔, 加短恬的重估模型, 估幾擺=20)
			上尾模型檔 = 拄好短恬的重估模型
			聲韻類檔=加恬聲韻類檔
			聲韻檔 = 新拄好短恬聲韻檔
# 		if 加混合:
		混合數 = [1, 2, 4, 8, 12, 16, 24, 32]
		加混合了模型 = self.加混合數(執行檔路徑, 資料目錄, 全部特徵檔,
			聲韻類檔, 聲韻檔, 上尾模型檔, 混合數, 估幾擺=10)
		上尾模型檔 = self.模型重估(執行檔路徑, 資料目錄, 全部特徵檔,
			聲韻類檔, 聲韻檔, 加混合了模型, 估幾擺=50)
		return 聲韻類檔, 上尾模型檔
	def 對齊(self, 莫跳脫聲韻, 聲韻類檔, 對照檔, 模型檔,
			標仔檔, 特徵檔, 結果夾, 執行檔路徑=''):
		執行檔路徑 = self.執行檔路徑加尾(執行檔路徑)
		os.makedirs(結果夾, exist_ok=True)
		對齊指令 = '{0}HVite -A -C {1} -p -20 -t 400 -H {2} -I {3} -S {4} -o S -y lab -l "{5}" {6} {7}'\
			.format(執行檔路徑, 莫跳脫聲韻, 模型檔, 標仔檔, 特徵檔,
				結果夾, 對照檔, 聲韻類檔)
		self.走指令(對齊指令)
		return
	def 對齊聲韻(self, 聲韻類檔, 模型檔, 聲韻檔, 特徵檔, 資料目錄, 執行檔路徑=''):
		莫跳脫聲韻 = os.path.join(資料目錄, '莫跳脫聲韻.cfg')
		self.字串寫入檔案(莫跳脫聲韻, 'noNumEscapes = T')
		聲韻對照檔 = os.path.join(資料目錄, '聲韻對照檔.dict')
		self.家己對照檔(聲韻類檔, 聲韻對照檔)
		對齊結果檔 = os.path.join(資料目錄, '對齊聲韻結果')
		self.對齊(莫跳脫聲韻, 聲韻類檔, 聲韻對照檔, 模型檔, 聲韻檔, 特徵檔, 對齊結果檔, 執行檔路徑)
		return 對齊結果檔
	def 對齊音節(self, 音節聲韻對照檔, 聲韻類檔, 模型檔, 音節檔, 特徵檔, 資料目錄, 執行檔路徑=''):
		莫跳脫聲韻 = os.path.join(資料目錄, '莫跳脫聲韻.cfg')
		self.字串寫入檔案(莫跳脫聲韻, 'noNumEscapes = T')
		對齊結果檔 = os.path.join(資料目錄, '對齊音節結果')
		self.對齊(莫跳脫聲韻, 聲韻類檔, 音節聲韻對照檔, 模型檔, 音節檔, 特徵檔, 對齊結果檔, 執行檔路徑)
		return 對齊結果檔
	def 辨識(self, 設定檔, 聲韻類檔, 對照檔, 模型檔, 網路檔, 幾條網路, 特徵檔, 結果檔, 結果網路資料夾, 執行檔路徑=''):
		執行檔路徑 = self.執行檔路徑加尾(執行檔路徑)
		if 幾條網路 > 0:
			os.makedirs(結果網路資料夾, exist_ok=True)
			幾條網路設定 = '-n {0}'.format(幾條網路)
		else:
			結果網路資料夾 = '*'
			幾條網路設定 = ''
		辨識指令 = '{0}HVite -A -C {1} -p -20 -t 400 -H {2} -w {3} -S {4} -o N -y rec -z lattices -i {5} -l "{6}" {7} {8} {9}'\
			.format(執行檔路徑, 設定檔, 模型檔, 網路檔, 特徵檔,
				結果檔, 結果網路資料夾, 幾條網路設定, 對照檔, 聲韻類檔)
		self.走指令(辨識指令)
		return
	def 辨識聲韻(self, 聲韻類檔, 模型檔, 特徵檔, 資料目錄, 幾條網路, 執行檔路徑=''):
		莫跳脫聲韻 = os.path.join(資料目錄, '莫跳脫聲韻.cfg')
		self.字串寫入檔案(莫跳脫聲韻, 'noNumEscapes = T')
		網路檔 = os.path.join(資料目錄, '聲韻網路檔.lat')
		self.生辨識網路(執行檔路徑, 資料目錄, 聲韻類檔, 網路檔)
		結果檔 = os.path.join(資料目錄, '辨識聲韻結果檔.mlf')
		聲韻對照檔 = os.path.join(資料目錄, '聲韻對照檔.dict')
		self.家己對照檔(聲韻類檔, 聲韻對照檔)
		結果網路資料夾 = os.path.join(資料目錄, '辨識聲韻網路')
		self.辨識(莫跳脫聲韻, 聲韻類檔, 聲韻對照檔, 模型檔, 網路檔, 幾條網路,
			特徵檔, 結果檔, 結果網路資料夾, 執行檔路徑)
		return 結果檔, 結果網路資料夾
	def 辨識音節(self, 音節聲韻對照檔, 聲韻類檔, 模型檔,
			特徵檔, 資料目錄, 幾條網路, 執行檔路徑=''):
		莫跳脫聲韻 = os.path.join(資料目錄, '莫跳脫聲韻.cfg')
		self.字串寫入檔案(莫跳脫聲韻, 'noNumEscapes = T')
		音節類檔 = os.path.join(資料目錄, '音節類檔.list')
		self.家己類檔(音節聲韻對照檔, 聲韻類檔, 音節類檔)
		網路檔 = os.path.join(資料目錄, '音節網路檔.lat')
		self.生辨識網路(執行檔路徑, 資料目錄, 音節類檔, 網路檔)
		結果檔 = os.path.join(資料目錄, '辨識音節結果檔.mlf')
		結果網路資料夾 = os.path.join(資料目錄, '辨識音節網路')
		self.辨識(莫跳脫聲韻, 聲韻類檔, 音節聲韻對照檔, 模型檔, 網路檔, 幾條網路,
			特徵檔, 結果檔, 結果網路資料夾, 執行檔路徑)
		return 結果檔, 結果網路資料夾
	def 處理試驗語料(self, 音檔目錄, 資料目錄,
			標仔目錄=None, 音節聲韻對照檔=None, 執行檔路徑=''):
		全部語料 = self.揣全部語料(音檔目錄, 標仔目錄)
		全部特徵檔 = os.path.join(資料目錄, '資料特徵檔.scp')
		os.makedirs(資料目錄, exist_ok=True)
		self.揣特徵而且算(執行檔路徑, 資料目錄, 全部語料, 全部特徵檔)
		if 標仔目錄 == None:
			return 全部特徵檔
		全部標仔檔 = os.path.join(資料目錄, '試驗語料標仔檔.scp')
		音節檔 = os.path.join(資料目錄, '試驗語料音節檔.mlf')
		聲韻類檔 = os.path.join(資料目錄, '試驗語料聲韻類檔.list')
		聲韻檔 = os.path.join(資料目錄, '試驗語料聲韻檔.mlf')
		全部標仔 = []
		for 語料 in 全部語料:
			標仔所在 = 語料[2]
			全部標仔.append(標仔所在)
		self.陣列寫入檔案(全部標仔檔, 全部標仔)
		用袂著的檔案 = os.path.join(資料目錄, '用袂著的檔案.garbage')
		self.標仔收集起來(執行檔路徑, 全部標仔檔, 資料目錄, 用袂著的檔案, 音節檔)
		self.標仔切做聲韻(執行檔路徑, 音節檔, 音節聲韻對照檔, 資料目錄, 聲韻類檔, 聲韻檔)
# 		self.標仔加恬佮切開(執行檔路徑, 全部標仔檔, 音節聲韻對照檔,
# 			資料目錄, 音節檔, 聲韻類檔, 聲韻檔)
		return 全部特徵檔, 音節檔, 聲韻檔
	def 揣全部語料(self, 音檔目錄, 標仔目錄):
		全部語料 = []
		for 音檔檔名 in os.listdir(音檔目錄):
			if 音檔檔名.endswith(self.音檔副檔名):
				語料名 = 音檔檔名[:-len(self.音檔副檔名)]
				音檔所在 = os.path.join(音檔目錄, 音檔檔名)
				if 標仔目錄 == None:
					全部語料.append((語料名, 音檔所在))
				else:
					標仔所在 = os.path.join(標仔目錄,
						語料名 + self.標仔副檔名)
					if os.path.isfile(標仔所在):
						全部語料.append((語料名, 音檔所在, 標仔所在))
		return 全部語料
	def 標仔換目錄(self, 原本全部標仔檔, 新標仔目錄):
		全部標仔 = []
		for 標仔檔名 in self.讀檔案(原本全部標仔檔):
			標仔所在 = os.path.join(新標仔目錄, os.path.basename(標仔檔名))
			if os.path.isfile(標仔所在):
				全部標仔.append(標仔所在)
		return 全部標仔
	def 揣特徵而且算(self, 執行檔路徑, 資料目錄, 全部語料, 全部特徵檔):
		算特徵參數檔 = os.path.join(資料目錄, '算特徵參數.cfg')
		self.字串寫入檔案(算特徵參數檔,
			self.特徵參數.format('WAVEFORM', 'WAV'))
		特徵目錄 = os.path.join(資料目錄, self.特徵)
		os.makedirs(特徵目錄, exist_ok=True)
		全部特徵 = []
		for 語料 in 全部語料:
			語料名, 音檔所在 = 語料[0:2]
			特徵所在 = os.path.join(特徵目錄,
				語料名 + self.特徵副檔名)
			self.算特徵(執行檔路徑, 算特徵參數檔, 音檔所在, 特徵所在)
			全部特徵.append(特徵所在)
		self.陣列寫入檔案(全部特徵檔, 全部特徵)
	def 算特徵(self, 執行檔路徑, 參數檔, 音檔所在, 特徵所在):
		執行檔路徑 = self.執行檔路徑加尾(執行檔路徑)
		特徵指令 = '{0}HCopy -A -C {1} {2} {3}'.format(
			執行檔路徑, 參數檔, 音檔所在, 特徵所在)
		self.走指令(特徵指令)
	def 標仔收集起來(self, 執行檔路徑, 全部標仔檔, 資料目錄, 原來音類檔, 原來音節檔):
		執行檔路徑 = self.執行檔路徑加尾(執行檔路徑)
		莫跳脫聲韻 = os.path.join(資料目錄, '莫跳脫聲韻.cfg')
		self.字串寫入檔案(莫跳脫聲韻, 'noNumEscapes = T')
		整理音節指令 = '{0}HLEd -A -C {1} -l "*" -n {2} -i {3} -S {4} /dev/null'\
			.format(執行檔路徑, 莫跳脫聲韻, 原來音類檔, 原來音節檔, 全部標仔檔)
		self.走指令(整理音節指令)
	def 音類標仔加短恬(self, 原來音類檔, 加恬音類檔):
		音類 = self.讀檔案(原來音類檔)
		音類.append(self.短恬)
		音類.sort()
		self.陣列寫入檔案(加恬音類檔, 音類)
	def 音節標仔加短恬(self, 原來音節檔, 加恬音節檔):
		頂一逝, *後壁資料 = self.讀檔案(原來音節檔)
		加短恬音節 = [頂一逝]
		for 一逝 in 後壁資料:
			if self.是有音標仔(頂一逝) and self.是有音標仔(一逝):
				加短恬音節.append(self.短恬)
			加短恬音節.append(一逝)
			頂一逝 = 一逝
		self.陣列寫入檔案(加恬音節檔, 加短恬音節)
	def 音節標仔逐字中央加短恬(self, 原來音節檔, 加恬音節檔):
		self.音節標仔加短恬(原來音節檔, 加恬音節檔)
		加短恬音節 = []
		目前短恬數量 = 0
		for 一逝 in self.讀檔案(加恬音節檔):
			if 一逝 == self.音檔結束符號:
				目前短恬數量 = 0
			這逝是有音標仔無 = (一逝 == self.短恬)
			if 這逝是有音標仔無:
				目前短恬數量 += 1
			if not 這逝是有音標仔無 or 目前短恬數量 % 2 == 0:
				加短恬音節.append(一逝)
		self.陣列寫入檔案(加恬音節檔, 加短恬音節)
	def 是有音標仔(self, 標仔):
		if 標仔 == '#!MLF!#' or 標仔 == self.音檔結束符號 or\
				標仔.startswith('"') or 標仔 == self.恬音:
			return False
		return True
	def 提掉傷短的短恬(self, 對齊加恬聲韻檔, 新拄好短恬聲韻檔):
		新聲韻 = []
		for 一逝 in self.讀檔案(對齊加恬聲韻檔):
			try:
				開始, 結束, 標仔 = 一逝.split()
				# 無到三个音框就提掉
				if int(結束) - int(開始) >= 300000 or 標仔 != self.短恬:
					新聲韻.append(標仔)
			except:
				新聲韻.append(一逝)
		self.陣列寫入檔案(新拄好短恬聲韻檔, 新聲韻)
	def 標仔切做聲韻(self, 執行檔路徑, 音節檔, 音節聲韻對照檔, 資料目錄, 聲韻類檔, 聲韻檔):
		執行檔路徑 = self.執行檔路徑加尾(執行檔路徑)
		莫跳脫聲韻 = os.path.join(資料目錄, '莫跳脫聲韻.cfg')
		self.字串寫入檔案(莫跳脫聲韻, 'noNumEscapes = T')
		切聲韻參數檔 = os.path.join(資料目錄, '拆聲韻參數檔.cmd')
		self.字串寫入檔案(切聲韻參數檔, 'EX')
		切聲韻指令 = '{0}HLEd -A -C {1} -l "*" -i {2} -n {3} -d {4} {5} {6}'\
			.format(執行檔路徑, 莫跳脫聲韻,
				聲韻檔, 聲韻類檔, 音節聲韻對照檔, 切聲韻參數檔, 音節檔)
		self.走指令(切聲韻指令)
	def 模型加短恬(self, 原本模型, 加短恬模型):
		恬中央狀態 = '~h \"{0}.*?\".*?<STATE> 3[ \n]*(.*?)[ \n]*<STATE> 4'\
			.format(self.恬音)
		原本資料 = self.讀檔案(原本模型)
		揣著的高斯狀態 = re.search(恬中央狀態,
			'\n'.join(原本資料), re.DOTALL)
		短恬高斯狀態 = self.短恬參數.format(self.短恬, 揣著的高斯狀態.group(1))
		原本資料.append(短恬高斯狀態)
		self.陣列寫入檔案(加短恬模型, 原本資料)
	def 建立初步模型(self, 執行檔路徑, 資料目錄, 全部特徵檔, 聲韻類檔, 聲韻檔):
		公家模型建立參數檔 = os.path.join(資料目錄, '公家模型建立參數檔.cfg')
		self.字串寫入檔案(公家模型建立參數檔,
			self.特徵參數.format('ANON', 'HTK'))
		公家模型檔 = os.path.join(資料目錄, '公家模型檔')
		模型版檔 = os.path.join(資料目錄, '模型版檔')
		self.字串寫入檔案(模型版檔, self.模型版參數)
		公家模型指令 = '{0}HCompV -A -C {1} -m -f 0.0001 -o {2} -M {3} -I {4} -S {5} {6}'\
			.format(執行檔路徑, 公家模型建立參數檔, 公家模型檔,
				資料目錄, 聲韻檔, 全部特徵檔, 模型版檔)
		self.走指令(公家模型指令)
		公家模型 = self.讀檔案(公家模型檔)
		公家變異數檔 = os.path.join(資料目錄, 'vFloors')
		公家變異數 = self.讀檔案(公家變異數檔)
		初步模型資料 = [公家模型[:3], 公家變異數]
		公家狀態 = 公家模型[4:]
		聲韻名 = '~h "{0}"'
		for 聲韻 in self.讀檔案(聲韻類檔):
			初步模型資料.append([聲韻名.format(聲韻)])
			初步模型資料.append(公家狀態)
		初步模型檔 = os.path.join(資料目錄, '初步模型檔.macro')
		self.陣列寫入檔案(初步模型檔,
			itertools.chain.from_iterable(初步模型資料))
		return 初步模型檔
	def 模型重估(self, 執行檔路徑, 資料目錄, 全部特徵檔, 聲韻類檔, 聲韻檔, 原來模型檔, 估幾擺):
		原來模型檔檔名 = os.path.basename(原來模型檔)
		這馬模型檔 = 原來模型檔
		基本路徑 = 原來模型檔.rsplit('.', 1)[0]
		資料夾 = 基本路徑 + '-重估'
		for 第幾擺 in range(估幾擺):
			這擺資料夾 = os.path.join(資料夾, '{0:02}'.format(第幾擺))
			os.makedirs(這擺資料夾, exist_ok=True)
			新統計檔 = os.path.join(這擺資料夾, '統計.sts')
			重估指令 = '{0}HERest -A -T 407 -t 450.0 150.0 1000.0 -M {1} -H {2} -s {3} -I {4} -S {5} {6}'\
				.format(執行檔路徑, 這擺資料夾, 這馬模型檔, 新統計檔,
					聲韻檔, 全部特徵檔, 聲韻類檔)
			self.走指令(重估指令)
			這馬模型檔 = os.path.join(這擺資料夾, 原來模型檔檔名)
		上尾模型檔 = '{0}-重估.macro'.format(基本路徑)
		shutil.copy(這馬模型檔, 上尾模型檔)
		return 上尾模型檔
	def 加混合數(self, 執行檔路徑, 資料目錄,
			全部特徵檔, 聲韻類檔, 聲韻檔,
			原來模型, 混合數, 估幾擺=20):
		頂一个模型 = 原來模型
		for 擺, 混合 in enumerate(混合數):
			這擺資料夾 = os.path.join(資料目錄, '加混合數', '{0:02}'.format(擺))
			os.makedirs(這擺資料夾, exist_ok=True)
			設定檔 = os.path.join(這擺資料夾, '設定檔.cmd')
			加混合模型 = os.path.join(這擺資料夾, '加混合模型.macro')
			self.陣列寫入檔案(設定檔, [
		 		"MU {0} {{*.state[2-4].mix}}".format(混合),
		 		"MU {0} {{{1}.state[2-4].mix}}".format(混合 * 2, self.恬音)])
			加混合數指令 = '{0}HHEd -A -H {1} -w {2} {3} {4}'\
				.format(執行檔路徑, 頂一个模型, 加混合模型, 設定檔, 聲韻類檔)
			self.走指令(加混合數指令)
			頂一个模型 = self.模型重估(執行檔路徑, 資料目錄, 全部特徵檔,
				聲韻類檔, 聲韻檔, 加混合模型, 估幾擺=估幾擺)
		加混合了模型 = os.path.join(資料目錄, '加混合了模型.macro')
		shutil.copy(頂一个模型, 加混合了模型)
		return 加混合了模型
	def 生辨識網路(self, 執行檔路徑, 資料目錄, 聲韻類檔, 網路檔):
		執行檔路徑 = self.執行檔路徑加尾(執行檔路徑)
		語法 = '({0} < {1} > {0})'.format(self.恬音,
			'|'.join(self.讀檔案(聲韻類檔)))
		語法檔 = os.path.join(資料目錄, '語法檔.syntax')
		self.字串寫入檔案(語法檔, 語法)
		產生網路指令 = '{0}HParse {1} {2}'\
			.format(執行檔路徑, 語法檔, 網路檔)
		self.走指令(產生網路指令)
	def 家己類檔(self, 對照檔, 聲韻類檔, 類檔):
		聲韻類 = set(self.讀檔案(聲韻類檔))
		類表 = []
		for 類 in self.讀檔案(對照檔):
			音節, *拆聲韻 = 類.split()
			for 聲韻 in 拆聲韻:
				if 聲韻 not in 聲韻類:
					break
			else:
				類表.append('{0}'.format(音節))
		self.陣列寫入檔案(類檔, 類表)
	def 家己對照檔(self, 類檔, 對照檔):
		對照表 = []
		for 類 in self.讀檔案(類檔):
			對照表.append('{0}\t{0}'.format(類))
		self.陣列寫入檔案(對照檔, 對照表)
	def 執行檔路徑加尾(self, 執行檔路徑):
		if 執行檔路徑 != '' and not 執行檔路徑.endswith('/'):
			return 執行檔路徑 + '/'
		return 執行檔路徑
	def 走指令(self, 指令):
		回傳值 = os.system(指令)
		if 回傳值 != 0:
			raise RuntimeError('指令走到一半發生問題！！指令：{0}'
				.format(指令))
	def 陣列寫入檔案(self, 檔名, 陣列):
		self.字串寫入檔案(檔名, '\n'.join(陣列))
	def 字串寫入檔案(self, 檔名, 字串):
		檔案 = open(檔名, 'w')
		print(字串, file=檔案)
		檔案.close()
	def 讀檔案(self, 檔名):
		檔案 = open(檔名, 'r')
		資料 = []
		for 一逝 in 檔案:
			一逝 = 一逝.rstrip()
			if 一逝 != '':
				資料.append(一逝)
		檔案.close()
		return 資料
	特徵參數 = \
'''
SOURCEKIND = {0}
SOURCEFORMAT = {1}
TARGETKIND = MFCC_E_D_A_Z
TARGETRATE = 100000.0
WINDOWSIZE = 200000.0
PREEMCOEF = 0.975
NUMCHANS = 26
CEPLIFTER = 22
NUMCEPS = 12
USEHAMMING = T
DELTAWINDOW = 2	
ACCWINDOW= 2
'''
	模型版參數 = \
'''
~o <VecSize> 39 <MFCC_E_D_A_Z> <DiagC> <StreamInfo> 1 39
<BeginHMM>
<NUMSTATES> 5
<STATE> 2
<NUMMIXES> 1 
<SWeights> 1 1 
<STREAM> 1
<MIXTURE> 1 1.000000e+000
<MEAN> 39
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 \
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
<VARIANCE> 39
1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 \
1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0

<STATE> 3
<NUMMIXES> 1 
<SWeights> 1 1 
<STREAM> 1
<MIXTURE> 1 1.000000e+000
<MEAN> 39
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 \
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
<VARIANCE> 39
1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 \
1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0

<STATE> 4
<NUMMIXES> 1 
<SWeights> 1 1 
<STREAM> 1
<MIXTURE> 1 1.000000e+000
<MEAN> 39
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 \
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
<VARIANCE> 39
1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 \
1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0 1.0

<TRANSP> 5
0.000000e+000 1.000000e+000 0.000000e+000 0.000000e+000 0.000000e+000 
0.000000e+000 6.000000e-001 4.000000e-001 0.000000e+000 0.000000e+000 
0.000000e+000 0.000000e+000 6.000000e-001 4.000000e-001 0.000000e+000 
0.000000e+000 0.000000e+000 0.000000e+000 6.000000e-001 4.000000e-001 
0.000000e+000 0.000000e+000 0.000000e+000 0.000000e+000 0.000000e+000 
<ENDHMM>
'''
	短恬參數 = \
'''
~h "{0}"
<BEGINHMM>
<NUMSTATES> 3
<STATE> 2
{1}
<TRANSP> 3
0.000000e+00 1.000000e+00 0.000000e+00
0.000000e+00 5.000000e-01 5.000000e-01
0.000000e+00 0.000000e+00 0.000000e+00
<ENDHMM>
'''
