#coding=utf-8
import sys
sys.path.append('/Users/imiyoo/workplace/tscanner')

import time
import requests
from wCurl import wcurl
from LogManager import log

def retry_action(retry_num=3):
    def decorator(function):
        count = {"num":0}
        def wrapper(*args,**kwargs):
            try:
                return function(*args,**kwargs)
            except Exception,e:
                if count["num"]<retry_num:
                    count["num"]+=1
                    log.info("Retry Count:%d" % count["num"])
		    time.sleep(1)
                    return wrapper(*args,**kwargs)
                else:
                    raise Exception(e)
	return wrapper
    return decorator

@retry_action(retry_num=4)
def send_http_req(id):
	#访问一个不存在的网站
	requests.get("http://www.test.com")

send_http_req(1)
