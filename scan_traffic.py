#coding=utf-8
'''
scan_traffic.py
'''
import os
import re
import sys
from teye_web.http.URL import URL
from teye_web.http.Request import Request
from teye_web.http.cookie import cookie
from teye_web.http.postdata import postdata


from BaseHTTPServer import BaseHTTPRequestHandler  
from StringIO import StringIO  
  
class HTTPRequest(BaseHTTPRequestHandler):  
	def __init__(self, request_text):
		self.rfile = StringIO(request_text)
		self.raw_requestline = self.rfile.readline()
		self.error_code = self.error_message = None
		self.parse_request()

def read_request(str):
	'''
	'''
	rlist = str.split("\n\nHTTP/1.1")
	req_str =  rlist[0].strip()

	if req_str.startswith("HTTP/1.1"):
		return None

	basereq = HTTPRequest(req_str)
	method  =basereq.command
	urlpath =basereq.path
	headers =basereq.headers
	netloc  =basereq.headers['host']
	del headers['host']

	url = URL(netloc + urlpath)
	treq = Request(url,method,headers=headers)
	return treq

def convert_traffic_to_req(http_file):
	'''
	'''
	req_list = []
	file=open(http_file,"rb")
	content = file.read()
	#[172.24.72.136:62822] -- -- --> [10.46.7.223:80]
	pattern="\[\d+\.\d+\.\d+.\d+:\d+\]\s--\s--\s-->\s\[\d+\.\d+\.\d+\.\d+:\d+\]"
	match = re.split(pattern,content)

	if len(match)>1:
        	for i in xrange(len(match)-1):
                	index = i + 1
                	data = match[index]
                	req = read_request(data)
                	if req is not None and req not in req_list:
                        	req_list.append(req)
	return req_list

pcap_file = "test.pcap"
http_file ="http_"+pcap_file.split(".")[0] + ".log"
#利用httpcap对PCAP文件进行解析和过滤
cmd = "parse_pcap -vv %s > %s" % (pcap_file,http_file)
os.system(cmd)
req_list = convert_traffic_to_req(http_file)
for item in req_list:
	print item
	from teye_core.tcore import tCore
	scan_engine = tCore()
	scan_engine.scan_request(item)

