from 資料庫.資料庫連線 import 資料庫連線
from 資料庫.欄位資訊 import 閩南語


教育部閩南語辭典空白符號 = '\u3000 \t'
教育部閩南語辭典隔開符號 = '\u3000'
俗音記號 = '??????'
合音記號 = '------'

揣字方言差 = 資料庫連線.prepare('SELECT * ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."語音方言差" WHERE "字號"=$1 ')
揣詞方言差 = 資料庫連線.prepare('SELECT * ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."詞彙方言差" WHERE "詞彙編號"=$1 ')
偏漳優勢音腔口 = 閩南語 + '偏漳優勢音'
偏泉優勢音腔口 = 閩南語 + '偏泉優勢音'
字方言差欄位 = [閩南語 + 地區 + '腔' for 地區 in 揣字方言差.column_names[3:]]
詞方言差欄位 = [閩南語 + 地區 + '腔' for 地區 in 揣詞方言差.column_names[3:]]

教育部閩南語辭典名 = '教育部臺灣閩南語常用詞辭典'
教育部閩南語辭典地區 = '臺員'
教育部閩南語辭典年代 = 97

揣主條目 = 資料庫連線.prepare('SELECT "主編號","屬性","詞目","音讀","方言差" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."詞目總檔" WHERE "主編號">= $1  ORDER BY "主編號" ASC')
揣義倒詞的詞音 = 資料庫連線.prepare('SELECT "另注音讀" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."反義詞對應" WHERE "反義詞" = $1 ORDER BY "流水號"')
揣義近詞的詞音 = 資料庫連線.prepare('SELECT "另注音讀" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."近義詞對應" WHERE "近義詞對應" = $1 ORDER BY "流水號"')
揣詞別音 = 資料庫連線.prepare('SELECT "又音" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."又音" WHERE "主編號"=$1 AND "屬性" = \'又唸作\' ' +
	' ORDER BY "流水號"')
揣詞俗音 = 資料庫連線.prepare('SELECT "又音" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."又音" WHERE "主編號"=$1 AND "屬性" = \'俗唸作\' ' +
	' ORDER BY "流水號"')
揣詞合音 = 資料庫連線.prepare('SELECT "又音" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."又音" WHERE "主編號"=$1 AND "屬性" = \'合音唸作\' ' +
	' ORDER BY "流水號"')

設定來源指令 = 資料庫連線.prepare('INSERT INTO "言語來源"."教育部臺灣閩南語常用詞辭典來源" ' +
	'("流水號","主編號") ' + 'VALUES ($1,$2)')
揣來源指令 = 資料庫連線.prepare('SELECT "流水號","主編號" FROM "言語來源"."教育部臺灣閩南語常用詞辭典來源" ' +
	'WHERE "流水號"=$1 and "主編號"=$2')
def 設定來源(流水號, 主編號):
	if 揣來源指令.first(流水號, 主編號) == None:
		設定來源指令(流水號, 主編號)

設定合音遏袂處理 = 資料庫連線.prepare('INSERT INTO "言語來源"."教育部臺灣閩南語常用詞辭典合音遏袂處理" ' +
	'("流水號") ' + 'VALUES ($1)')

# 揣文字上大流水號資料 = 資料庫連線.prepare('SELECT MAX("流水號") ' +
# 	'FROM "言語"."文字"')
# 揣文字上大流水號 = lambda:揣文字上大流水號資料.first()


# 資料庫加文字 = 資料庫連線.prepare('INSERT INTO "言語"."文字" ' +
# 	'("來源","種類","腔口","地區","年代","型體","音標") ' +
# 	'VALUES (\'教育部臺灣閩南語常用詞辭典\',$1,$2,\'臺員\',\'97\',$3,$4) ')
#
# def 加文字(種類, 腔口, 型體, 音標):
# 	資料庫加文字(種類, 腔口, 型體, 音標)
# 	流水號 = 揣文字上大流水號()
# 	加編修狀況(流水號, '文字')

設定編修狀況 = 資料庫連線.prepare('UPDATE "言語"."編修" ' +
	'SET "版本"=$2 ' + ' WHERE "編修目標流水號"=$1')

揣義倒詞組合 = 資料庫連線.prepare('SELECT "主編號","反義詞" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."反義詞對應" ORDER BY "流水號"')
揣義近詞組合 = 資料庫連線.prepare('SELECT "主編號","近義詞對應" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."近義詞對應" ORDER BY "流水號"')
用主碼號揣流水號 = 資料庫連線.prepare('SELECT "流水號" FROM "言語來源"."教育部臺灣閩南語常用詞辭典來源" ' +
	'WHERE "主編號"=$1')
揣文白流水號 = 資料庫連線.prepare('SELECT "主編號","詞目","文白俗替" FROM "教育部臺灣閩南語常用詞辭典"."詞目總檔" ' +
	'WHERE "文白俗替" = \'文\' OR "文白俗替" = \'白\' ORDER BY "詞目" ASC, "文白俗替" ASC')

# 8016 8055 WHERE "流水號">=8055
揣釋義 = 資料庫連線.prepare('SELECT "流水號","主編號","義項順序","詞性","釋義" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."釋義" ORDER BY "流水號"')

用釋義揣例句 = 資料庫連線.prepare('SELECT "例句","標音","例句翻譯" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."例句" WHERE "釋義編號"=$1 ORDER BY "流水號" ASC ')
用流水號揣腔口 = lambda 流水號:資料庫連線.prepare('SELECT "腔口" ' +
	'FROM "言語"."文字" WHERE "流水號"=$1').first(流水號)

文字無音設定 = 資料庫連線.prepare('UPDATE "言語"."文字" ' +
	'SET "音標"=NULL WHERE "音標"=\'\'')

查詞性對照 = 資料庫連線.prepare('SELECT "詞性","詞性內容" ' +
	'FROM "教育部臺灣閩南語常用詞辭典"."詞性對照" ORDER BY "詞性" ASC ')
詞性對照表 = {詞性:詞性內容 for 詞性, 詞性內容 in 查詞性對照()}
詞性對照表[0] = '毋知'
設定詞性 = 資料庫連線.prepare('UPDATE "言語"."關係" ' +
	'SET "詞性"=$2 WHERE "流水號"=$1')
