#coding=utf-8
'''
PocScan.py
'''

import sys
from teye_web.http.URL import URL

from teye_data.vuln import vuln
from teye_data.vulnmanager import vm

class PocScan:
	'''

	'''
	def __init__(self):
		'''
		'''
		self._poc_info ={

		'w_hat':{
			'author':None,
			'blog':None,
			'team':None,
			'create_time':None
		},
		'w_vul':{
			'id':None,
			'title':None,
            		'method':None,
			'tag':None,
			'rank':None,
			'info':None,
			}
		}

	def check(self,target):
		'''
		'''
		pass

	def security_hole(self,url):
		'''
		'''
		if isinstance(url,URL):
			url = url.url_string
		else:
			url = url

		name        = self._poc_info['w_vul']['title']
		method      = self._poc_info['w_vul']['method']
		link_info   = self._poc_info['w_vul']['info']
		rank        = self._poc_info['w_vul']['rank']

		v = vuln()
		v.set_url(url)
		v.set_name(name)
		v.set_rank(rank)
		v.set_method(method)
		v.set_link_info(link_info)

		site = URL(v.get_url()).get_host()

		vm.append(self,site,v.get_name(),v)

	def get_title(self):
                return self._poc_info['w_vul']['title']

	def get_name(self):
		'''
		'''
		return "teye_poc_plugin"


if __name__=="__main__":
	ps = PocScan()
	ps.security_hole("http://wwww.baidu.com")
	print vm.get_all_vuln()
