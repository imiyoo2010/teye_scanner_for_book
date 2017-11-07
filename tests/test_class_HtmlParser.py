#coding=utf-8


import sys
sys.path.append('/Users/imiyoo/workplace/tscanner')

from wCurl import wcurl
from teye_web.http.URL import URL
from teye_web.parser.HtmlParser import HtmlParser


def test_HtmlParser():
	'''
	'''
	req_url="http://192.168.126.147"
	real_contain_urls=['http://www.w3.org/1999/xhtml',
	'http://192.168.126.147/lnmp.gif',
	'http://lnmp.org',
	'http://192.168.126.147/p.php',
	'http://192.168.126.147/phpinfo.php',
	'http://192.168.126.147/phpmyadmin/',
	'http://lnmp.org',
	'http://bbs.vpser.net/forum-25-1.html',
	'http://www.vpser.net/vps-howto/',
	'http://www.vpser.net/usa-vps/',
	'http://lnmp.org',
	'http://blog.licess.com/',
	'http://www.vpser.net']
	r = wcurl.get(req_url)

	parser = HtmlParser(r)
	re_urls,tag_urls = parser.urls

	print "Regex URL:"
	for item in re_urls:
		print item

	print "Tag URL:"	
	for item in tag_urls:
		print item

	page_urls = []
	page_urls.extend(re_urls)
	page_urls.extend(tag_urls)	
	
	true_num = 0
	for item in real_contain_urls:
		real_url = URL(item)
		if real_url in page_urls:
			true_num +=1
		else:
			print real_url
	
	assert len(real_contain_urls)==true_num	
