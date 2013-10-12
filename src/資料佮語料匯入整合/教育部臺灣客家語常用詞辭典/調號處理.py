
class 調號處理:
	四縣表 = [
		('55', ''), ('24', 'ˊ'),
		('11', 'ˇ'), ('31', 'ˋ'),
		('53', '^'),#「分佢」（bun24 gi11）=>「畀」（bi53）
		('b2', 'bˋ'), ('b5', 'b'),
		('d2', 'dˋ'), ('d5', 'd'),
		('g2', 'gˋ'), ('g5', 'g'),
		]
	海陸表 = [
		('55', ''), ('24', 'ˊ'),
		('11', 'ˇ'), ('53', 'ˋ'), ('33', '+'),
		('b2', 'bˋ'), ('b5', 'b'),
		('d2', 'dˋ'), ('d5', 'd'),
		('g2', 'gˋ'), ('g5', 'g'),
		]
	大埔表 = [
		('31', '^'), 
		('113', 'ˇ'), ('53', 'ˋ'), ('33', '+'),
		('b2', 'bˋ'), ('b54', 'b'),
		('d2', 'dˋ'), ('d54', 'd'),
		('g2', 'gˋ'), ('g54', 'g'),
		]
	饒平表 = [
		('55', ''), ('24', 'ˊ'),
		('11', 'ˇ'), ('53', 'ˋ'),
		('31', '^'),#卓蘭腔
		('b2', 'bˋ'), ('b5', 'b'),
		('d2', 'dˋ'), ('d5', 'd'),
		('g2', 'gˋ'), ('g5', 'g'),
		]
	詔安表 = [
		('55', ''), ('31', '^'),
		('11', 'ˇ'), ('53', 'ˋ'),
		('b5', 'bˋ'), ('b24', 'bˊ'),
		('d5', 'dˋ'), ('d24', 'dˊ'),
		('g5', 'gˋ'), ('g24', 'gˊ'),
		]
	def 數字轉調號(self, 音, 腔):
		if 腔 == '四縣腔':
			表 = self.四縣表
		elif 腔 == '海陸腔':
			表 = self.海陸表
		elif 腔 == '大埔腔':
			表 = self.大埔表
		elif 腔 == '饒平腔':
			表 = self.饒平表
		elif 腔 == '詔安腔':
			表 = self.詔安表
		else:
			raise RuntimeError('腔口毋著：{0}'.format(腔))
		return self.查表數字轉調號(音, 表)
	def 查表數字轉調號(self, 音, 表):
		for 舊, 新 in 表:
			音 = 音.replace(舊, 新)
		return 音
