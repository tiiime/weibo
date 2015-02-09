#/usr/bin/env python
#coding=utf-8
import requests
import HTMLParser
from lxml.html.soupparser import fromstring
import lxml.etree as etree
html_parser = HTMLParser.HTMLParser()

#把cookie和ueser_uid改为你的数据
#然后就好了

_COOKIES = {
'_T_WM': '********',
'H5_INDEX': '*',
'H5_INDEX_TITLE': '********',
'gsid_CTandWM': '********',
'SUB': '********',
'SUHB': '********',
'M_WEIBOCN_PARAMS': '*********'}

USER_UID = '********'
URL_FANS = 'http://weibo.cn/{0}/fans'
URL_FOLLOW = 'http://weibo.cn/{0}/follow'

print URL_FOLLOW
print URL_FANS

#根据URL获取总页数
def get_page_num(url):
	num = 0
	req = requests.post(url, _COOKIES)
	dom = fromstring(req.content)
	pa = dom.xpath('//input')
	for item in pa:
		if item.get('name') == 'mp':
			num = item.get('value')
			break
	return long(num)

#根据头像链接获取uid
def get_uid_from_table(table):
	uid = 0
	str = table[0][0][0][0].get('src')
	uid = str.split('/')[3]
	return uid

def get_nick_from_table(table):
	str = etree.tostring(table[0][1][0])
	str = str.split('>')[1]
	str = str.split('<')[0]
	nick = html_parser.unescape(str)
	return nick


#获取单页fans uid
def get_page_fans(page,uid = USER_UID):
	page_list = {}
	request_url = URL_FANS.format(uid) + '?page={0}'.format(page)
	req = requests.post(request_url, _COOKIES)
	dom = fromstring(req.content)
	fans =  dom.xpath('//table')
	for item in fans:
		uid = get_uid_from_table(item)
		nick = get_nick_from_table(item)
		page_list[uid] = nick
		print 'fans: ' + uid + ' | ' + nick
	return page_list

def get_all_fans(uid = USER_UID):
	all_uid = {}
	pageNum = get_page_num(URL_FANS.format(uid)) + 1
	print '获取FANS UID中:'
	for x in xrange(1,pageNum):
		page_uid = get_page_fans(x,uid)
		all_uid.update(page_uid)
	return all_uid

#获取单页follows uid
def get_page_follow(page, uid = USER_UID):
	page_list = {}
	request_url = URL_FOLLOW.format(uid) + '?page={0}'.format(page)
	req = requests.post(request_url, _COOKIES)
	dom = fromstring(req.content)
	follows =  dom.xpath('//table')
	for item in follows:
			uid = get_uid_from_table(item)
			nick = get_nick_from_table(item)
			page_list[uid] = nick
			print 'follow: ' + uid + ' | ' + nick
	return page_list

def get_all_follow(uid = USER_UID):
	all_uid = {}
	pageNum = get_page_num(URL_FOLLOW.format(uid)) + 1
	print '获取FOLLOW UID中:'
	for x in xrange(1,pageNum):
		page_uid = get_page_follow(x,uid)
		all_uid.update(page_uid)
	return all_uid

dict1 = get_all_follow()
dict2 = get_all_fans()

keys = dict.fromkeys(x for x in dict1 if x in dict2)
print type(keys)
print '互粉人数:'+str( len(keys) )
for x in keys:
	print x + ' | ' + dict2[x]

for x in keys:
	del(dict2[x])
print '还没关注:'
for x in dict2:
	print x + ' | ' + dict2[x]








