#coding=utf-8

def test_discuz_faq_sql():
	'''
	'''
	vuln_url="http://www.baidu.com"
	
	vuln_item = (vuln_url,vuln_key)
	v = discuz_faq_sql()
	v.check(vuln_url)
