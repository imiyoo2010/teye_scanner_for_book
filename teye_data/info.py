#coding=utf-8
'''
info.py
++++++++++++++++++++++++
{
"scan_node":"",
"entry":"www.baidu.com",
"scan_target":[],
"domain":"",
"ipaddr":"",
"port":"",
"finger":[],
"nameserver":[],
"subdomain":[],
"relate_ipaddr":[],
"dir":[],
"vuln":[]
}
+++++++++++++++++++++++
'''

import json

class info(dict):
	'''
	'''
	def __init__(self):
		'''
		'''
		self["scan_node"]    = ""
		self["entry"]	     = ""
		self["start_time"]   = ""
		self["end_time"]     = ""
		self["scan_profile"] = None
		self["scan_target"]  = []
		self["domain"]	     = ""
		self["ipaddr"]	     = ""
		self["port"]         = ""
		self["finger"]	     = []
		self["nameserver"]   = []
		self["subdomain"]    = []
		self["relate_ipaddr"]= []
		self["dir"]	     = []
		self["vuln"]	     = []

		#external
		self["api"]	     = []

	def set_profile(self,profile):
		'''
		'''
		self["scan_profile"]=profile

	def set_myip(self,myip):
		'''
		'''
		self["scan_node"]=myip

	def set_entry(self,site):
		'''
		'''
		self["entry"] = site

	def set_start_time(self,starttime):
		'''
		'''
		self["start_time"] = starttime

	def set_end_time(self,endtime):
		'''
		'''
		self["end_time"] = endtime

	def set_domain(self,domain):
		'''
		'''
		self["domain"] = domain

	def set_ipaddr(self,ipaddr):
		'''
		'''
		self["ipaddr"] = ipaddr

	def set_port(self,port):
		'''
		'''
		self["port"]  = port

	def set_finger(self,finger):
		'''
		'''
		self["finger"] = finger

	def set_subdomain(self,subdomain):
		'''
		'''
		self["subdomain"] = subdomain

	def set_relate_ipaddr(self,ip_list):
		'''
		'''
		self["relate_ipaddr"] = ip_list

	def set_vuln(self,vuln):
		'''
		'''
		self["vuln"] = vuln

	def set_api(self,api):
		'''
		'''
		self["api"] = api

	def set_data(self,key,value):
		'''
		'''
		self[key] = value

	def get_data(self,key):
		'''
		'''
		return self[key]

	def __str__(self):
		'''
		'''
		msg = json.dumps(self)
	
		return msg

	def __repr__(self):
		'''
		'''
		return "<info object: site:%s ipaddr:%s>" % (self._entry,self._ipaddr)


db_info = info()
