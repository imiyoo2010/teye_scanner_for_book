#coding=utf-8
'''
HtmlReport.py
'''
import sys
import teye_config as Settings

import json
import time

class HtmlReport:
	'''
	'''
	def __init__(self,db_info=None,model="SITE"):
		'''
		'''
		if model=="SITE":
			self._report_template = Settings.ROOT_PATH + "/teye_report/template/WAT_SITE_Report_For_Test_V1.html"
		elif model=="MAPP":
			self._report_template = Settings.ROOT_PATH + "/teye_report/template/WAT_MAPP_Report_For_Test_V1.html"


		print Settings.ROOT_PATH
		self._report_dir = Settings.ROOT_PATH + "/teye_report/template/"

		self._db_info = db_info

		self._apiinfos	= []
		self._vulntypes = []
		self._vulninfos = []
		self._infos	= {}

		self._vulnids = []
	
	def set_report_info(self,target,date_string=""):
		'''
		'''
		if date_string=="":
			self._infos["date"]=time.strftime('%a %b %d %X %Y',time.localtime(time.time()))
		self._infos["target"] = target

	def generate(self,filename):
		'''
		report_data = {"entry":"www.watscan.com",
		"scan_target":["10.10.10.10","app.watscan.com","test.watscan.com"],
		"ipaddr":"10.10.10.10",
		"port":[],
		"domain":"baidu.com",
		"relate_ipaddr":[],
		"finger":"",
		"nameserver":[],
		"subdomain":[],
		"dir":[],
		"vuln":[{
				"site":"www.watscan.com",
				"vlist":
				[
					{
						"name":"SQL注入漏洞",
					 	"list":
						[
							{"url":"http://www.watscan.com/index.php?id=1","risk":"高危","method":"GET"}
						]
					}
				]
			}]
		};
		'''
		report_dict = json.loads(str(self._db_info))

		json_data = json.dumps(report_dict)

		fd = open(self._report_template,"r+")
		html_data = fd.read()
		html_data = html_data.replace("#___JSON_DATA___#",json_data)
		fd.close()
		
		filepath = self._report_dir+time.strftime('%Y-%m-%d',time.localtime(time.time()))+"_"+filename
		fd_new = open(filepath,"w+")
		fd_new.write(html_data)
		fd_new.close()
