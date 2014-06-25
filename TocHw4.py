# -*- coding: UTF-8 -*-

#	HW4
#	Name:潘柏豪
#	ID:F74006276
#	Description:
#		自網址讀入讀入jsonn檔後,依"路","大道","街","巷"
#		作第一層分類,再依年月份作第二次分類,最後將相同
#		的地址存入Dict,連帶比較所有相同地址的年月份及最
#		及最小總金額,將這些資訊一起存進Dict,最後再將這筆
#		Dict存入List,最後將擁有最多不同年月份的地址及其
#		最大和最小交易金額印出
#
#	How-to-use:
#		命令列格式必須要與以下相符:
#			python TocHW4.py 網址

from datetime import datetime, timedelta
import urllib2, logging, csv, re, json, sys

if len(sys.argv) != 2:
	print 'Input Error!!'
	sys.exit(1)

url = sys.argv[1]
logging.info(url)
cc = urllib2.urlopen(url)
csv_read = csv.reader(cc)
ss = json.load(cc)

lis = [{1:1}]

ansstr = ''
anscnt = 0

chk = 0
for i in ss:
	chk = i[u'土地區段位置或建物區門牌'].find(u'巷')
	if chk != -1:
		cnt = chk + 1
		strin = i[u'土地區段位置或建物區門牌'][0:cnt]
	chk = i[u'土地區段位置或建物區門牌'].find(u'大道')
	if chk != -1:
		cnt = chk + 2
		strin = i[u'土地區段位置或建物區門牌'][0:cnt]
	chk = i[u'土地區段位置或建物區門牌'].find(u'街')
	if chk != -1:
		cnt = chk + 1
		strin = i[u'土地區段位置或建物區門牌'][0:cnt]
	chk = i[u'土地區段位置或建物區門牌'].find(u'路')
	if chk != -1:
		cnt = chk + 1
		strin = i[u'土地區段位置或建物區門牌'][0:cnt]
	if chk == -1:
		continue

	chk = 0
	ym = i[u'交易年月']
	for inin in lis:
		if inin.has_key(strin) == True:
			if inin.has_key(ym) == False:
				tmp = inin['num']
				inin['num'] = tmp + 1
				inin[ym] = 1
				chk = 1
			else:
				chk = 1
			if i[u'總價元'] > inin['high']:
				inin['high'] = i[u'總價元']
			if i[u'總價元'] < inin['low']:
				inin['low'] = i[u'總價元']
	if chk == 0:
		dic = {}
		dic['name'] = strin
		dic['num'] = 1
		dic[strin] = 1
		dic[ym] = 1
		dic['high'] = i[u'總價元']
		dic['low'] = i[u'總價元']
		lis.append(dic)

lis.pop(0)
for ii in lis:
	if ii['num'] >= anscnt:
		anscnt = ii['num']
for ii in lis:
	if ii['num'] == anscnt:
		print ii['name'],', 最高成交價:',ii['high'],', 最低成交價:',ii['low']
