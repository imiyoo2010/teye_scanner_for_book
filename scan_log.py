#coding=utf-8
'''
scan_log.py
'''
'''
192.168.126.1 - - [17/Dec/2016:17:52:45 +0800] "GET /p.php?act=rt&callback=jQuery170013389064965628972_1481968361729&_=1481968365810 HTTP/1.1" 192.168.126.145 200 416 "http://192.168.126.145/p.php" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36" "2zA_sid=1QFL02; mycookie=you are spider" "-" "-"
'''

import re
from teye_web.http.URL import URL
from teye_web.http.Request import Request
from teye_web.http.cookie import cookie
from teye_web.http.postdata import postdata

from teye_data.vulnmanager import vm

log_pattern=re.compile(r'''
([^\s]+)\s 							#remote_ip
-\s-\s(\[[^\]]+\])\s 						#[time]
("[^"]+")\s							#request
([^\s]+)\s							#host
(\d{3})\s							#Code
(\d+)\s								#body_bytes_send
"([^"]+)"\s							#http_referer
"([^"]+)"\s							#http_user_anget
"([^"]+)"\s							#http_cookie
"([^"]+)"\s							#http_x_forward_for
"([^"]+)"							#request_body
''',re.X)

log='192.168.126.1 - - [17/Dec/2016:17:52:45 +0800] "GET /p.php?act=rt&callback=jQuery170013389064965628972_1481968361729&_=1481968365810 HTTP/1.1" 192.168.126.145 200 416 "http://192.168.126.145/p.php" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36" "2zA_sid=1QFL02; mycookie=you are spider" "-" "-"'



match = log_pattern.match(log)
if match:
	info_tuple = match.groups()
	#print info_tuple
	log_ip            = info_tuple[0]
	log_time          = info_tuple[1]
	log_request       = info_tuple[2]
	log_host          = info_tuple[3]
	log_referer       = info_tuple[6]
	log_cookie	  = info_tuple[8]
	log_x_forward_for = info_tuple[9]
	log_body          = info_tuple[10]


	temp_request = log_request.split(" ")

	method = temp_request[0][1:].upper()
	uri    = temp_request[1][0:-8]
	url    = log_host + uri

	headers={"Referer":"","Cookie":"","X-Forward-For":""}
	
	headers["Referer"]=log_referer
	headers["Cookie"]=log_cookie
	if log_x_forward_for=='-':
		del headers["X-Forward-For"]
	else:
		headers["X-Forward-For"]=log_x_forward_for

	post_data = postdata(log_body)
	urlobj = URL(url)
	if method  == "GET":
                req = Request(urlobj,method,headers=headers)
       	elif method == "POST":
      		req = Request(urlobj,method,headers=headers,post_data=post_data)
	print req
	from teye_core.tcore import tCore
    	scan_engine = tCore()
	scan_engine.scan_request(req)	

	print vm.get_all_vuln()
