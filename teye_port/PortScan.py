#coding=utf-8

import os
import sys

from thirdparty.libnmap.process import NmapProcess
from thirdparty.libnmap.parser import NmapParser,NmapParserException

import re
import time
import socket

import brute_ftp
#import brute_ssh
#import brute_smtp
#import brute_mysql

class PortScan:
	'''
	'''
	NORMAL= 0

	NMAP_STATE=["open"]#open,filtered,closed,unfiltered

	NMAP_OPTIONS = "-sV -p 21-25,80-89,110,111,443,513,873,1080,1433,1521,2375,3306,3389,3690,5900,6379,7001,8000-8090,9000,9418,11211,27017-27019,50060"

	def __init__(self):
		'''
		'''
		self._check_port = [21,22,80,110,111,873,1433,3306,3389,6379,27017]
		
		self._timeout = 5

		self._http_target = []

		self._s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

		self._s.settimeout(float(self._timeout))	

	def is_ipaddr(self,target):
		'''
		'''
		ip_re = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.")
		if ip_re.search(target):
			return True
		else:
			return False

	def get_ipaddr(self,domain):
		'''
		'''
		ipaddr = None

		if self.is_ipaddr(domain):
			ipaddr = domain
		else:
			ipaddr = socket.gethostbyname(domain)

		return ipaddr
		
	def is_alive(self,netloc):
		'''
		'''
		if netloc.find(":")>-1:
			ipaddr = self.get_ipaddr(netloc.split(":")[0])
			port = int(netloc.split(":")[1])
		else:
			ipaddr = self.get_ipaddr(netloc)
			port = 80

		try:
			s = socket.socket()
			status = s.connect_ex((ipaddr,port))
			s.close()
			if status == PortScan.NORMAL:
				return True
			else:
				return False
		except Exception,e:
			
			return False

	def nmap_scan(self,target,option=NMAP_OPTIONS):
		'''
		'''
		#初始化self._http_target
		if len(self._http_target)>0:
			self._http_target = []

		#Nmap param should str or list
		if isinstance(target,unicode):
			str_target = target.encode("utf-8")
		nmap_proc = NmapProcess(targets=str_target,options=option)
		nmap_proc.run_background()

		run_time = 0

		while nmap_proc.is_running():
			#print '%s' % (nmap_proc.command)
			time.sleep(5)

		if nmap_proc.is_successful():
			result = dict()
			nmap_report = NmapParser.parse(nmap_proc.stdout)

			for host in nmap_report.hosts:

				ipaddr = host.address
				if not ipaddr:
					continue

				port_open = []
				for item in host.services:
					if item.state.lower() in PortScan.NMAP_STATE:
						info 	= item.service_dict
						port	= item.port
						name 	= info.get("name")
						product = info.get("product")

						if name.find("http")>-1:
							if self.is_ipaddr(target):
								http_item = ipaddr +":"+str(port)
								self._http_target.append(http_item)
							else:
								http_item = target + ":" + str(port)
								self._http_target.append(http_item)

						port_open.append(port)	
						#print host.address
						#print port
						#print name
						#print product
				result[ipaddr] = port_open

			return result

	def get_http_target(self):
		'''
		'''
		return self._http_target
				
	def scan_port(self,target):
		'''
		'''
		port_open = []

		result = dict()

		if self.is_alive(target):
			port_open.append(80)

		ipaddr = self.get_ipaddr(target)

		for port in self._check_port:
			try:
				status=self._s.connect_ex((ipaddr,port))
				
				if status == PortScan.NORMAL:
					if port not in port_open:
						port_open.append(port)		
						
				else:
					print str(port) + ": no open"
			except Exception,e:
				
				continue

			time.sleep(0.1)

		self._s.close()
		
		result[ipaddr]=port_open

		return result

if __name__=="__main__":
	'''
	'''
	target = "31.193.196.16"

	ps   = PortScan()

	print "Port Scanning Host:" + ps.get_ipaddr(target)

	open_ports = ps.nmap_scan(target)

	print open_ports

	if 21 in open_ports:
		brute_ftp.brute(target_ipaddr,"username.lst","password.lst")

	if 22 in open_ports:
		brute_ssh.brute(target_ipaddr,"username.lst","password.lst")
		
	if 25 in open_ports:
		brute_smtp.brute(target_ipaddr,"username.lst","password.lst")

	if 3306 in open_ports:
		brute_mysql.brute(target_ipaddr,"username.lst","password.lst")
