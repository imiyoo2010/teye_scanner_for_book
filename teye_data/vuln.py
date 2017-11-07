#coding=utf-8
'''
vuln.py
'''

import uuid
import json

class vuln(dict):
	'''
	'''
	def __init__( self ):
		#设置默认值
		self["url"] 		= None
		self["method"]		= None
		self["param"]		= None
		self["name"] 		= None
		self["title"]		= None
		self["rank"]		= None
		self["desc"]		= None
		self["link_info"] 	= None


	def set_url(self,url):
		'''
		'''
		self["url"] = url

	def set_method(self,method):
		'''
		'''
		self["method"] = method

	def set_param(self,param):
		'''
		'''
		self["param"] = param

	def set_name(self,name):
		'''
		'''
		self["name"] = name

	def set_rank(self,rank):
		'''
		'''
		self["rank"] = rank

	def set_link_info(self,link_info):
		'''
		'''
		self["link_info"] = link_info

	def get_url(self):
		'''
		'''
		return self["url"]

	def get_name(self):
		'''
		'''
		return self["name"]

	def get_rank(self):
		'''
		'''
		return self["rank"]

	def get_method(self):
		'''
		'''
		return self["method"]

	def get_param(self):
		'''
		'''
		return self["param"]

	def __str__(self):
		'''
		'''
		return json.dumps(self)
 
	def __repr__(self):
		'''
		'''
		if isinstance(self["name"],unicode):
			name = self["name"].encode("utf-8")
		elif isinstance(self["name"],basestring):
			name = self["name"]

		return '<vuln object: "'+name+'">'
