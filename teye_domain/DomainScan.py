#coding=utf-8
'''
DomainScan.py
'''
import os
import sys

#加载配置文件
sys.path.append("..")
import teye_config as Settings

import re
import time
import urllib2
import dns.resolver
import dns.rdatatype
from LogManager import log

class DomainScan:
	'''
	'''
	MAX_WILD_RECORDS = 8

	def __init__(self,domain_file=None):
		'''
		'''
		self._ip_list 	= []

		self._subdomain_list = []

		self._subdomain_file = domain_file if domain_file else Settings.DOMAIN_FILE
		
		self._black_list = ['127.0.0.1']

		self._resolver = dns.resolver.Resolver()
		#百度DNS:180.76.76.76
		#阿里DNS:223.5.5.5,223.6.6.6
		self._resolver.nameservers=['180.76.76.76','223.5.5.5','223.6.6.6']

	def _load_domain(self):
		'''
		'''
		sub_list = []
		with open(self._subdomain_file) as f:
			for line in f:
				sub = line.strip()
				if sub.startswith("#"):
					continue
				sub_list.append(sub)

		return sub_list

	def domain_scan(self,root_domain):
		'''
		'''
		sublist = self._load_domain()

		for item in sublist:
			subdomain = item + "." + root_domain
			log.info("DomainScan Scanning:" + subdomain)

			try:
				resp = self._resolver.query(subdomain)
				is_wild_record = False
				if resp:
					is_local_ip = False
					for item in resp:
						wild_record = {}
						ipaddr = item.address

						if ipaddr in self._black_list:
							is_local_ip = True
							break

						if ipaddr not in self._ip_list:
							wild_record[ipaddr] = 1
							self._ip_list.append(ipaddr)
						else:
							wild_record[ipaddr] +=1
							if wild_record[ipaddr]>DomainScan.MAX_WILD_RECORDS:
								is_wild_record = True

					if is_wild_record:
						log.info("DomainScan Found Wild Record")
						break

					if subdomain not in self._subdomain_list and not is_local_ip:	
						self._subdomain_list.append(subdomain)
			
			except Exception as e:
				#print str(e)	
				continue

		return self._subdomain_list

	def get_ip_list(self):
		'''
		'''
		return self._ip_list


def get_subdomain_date(subdomain):
	'''
	'''
	api_url = "http://toolbar.netcraft.com/site_report?url=%s"

	req_url = api_url % subdomain

	res_body = ""

	try:
		res = urllib2.urlopen(req_url)	

		res_body = res.read()
	except:
		return "None"

	reg = re.compile("date\s+first\s+seen</th>(.*?)</td>",re.S|re.IGNORECASE)
	result = reg.search(res_body)

	if result is not None:
		t1 = result.group()
	else:
		return "None"

	if t1 is not None:
		if t1.find(">")>-1:
			t2 = t1.split(">")
			if len(t2)>3:
				if t2[2].find("unavailable")>-1:
					return "None"
				else:
					return t2[2].replace("</td","")
			else:
				return "None"
	else:
		return "None"
		

if __name__=="__main__":
	'''
	'''
	if len(sys.argv)<2:
		print "Plz Input Root Domain!"
		sys.exit()

	domain = sys.argv[1]

	print domain

	filename   = "domain_name.list"

	ds = DomainScan(filename)
	
	start_time = time.time()
	subdomain_list = ds.domain_scan(domain)
	end_time  = time.time()
	print "Elapsed:"+str(end_time-start_time)
	print len(subdomain_list)

	for item in subdomain_list:
		s = item.strip()
		t = get_subdomain_date(s)
		print "%s----First Seen:%s" % (s,t)

