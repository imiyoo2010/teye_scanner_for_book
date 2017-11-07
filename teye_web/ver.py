# coding=utf-8
'''
ver.py
'''
import re
import os
import sys
import copy
import teye_data.severity as severity
from teye_data.vuln import vuln
from teye_data.vulnmanager import vm

from LogManager import log

# wCurl
from wCurl import wcurl
from http.URL import URL
from http.Request import Request

import requests

from util.gen_zip_name import gen_zip_name

from misc.common import is_404


class ver:
    '''
	'''

    def __init__(self):
        '''
		'''
        self._already_flag = False

        self._already_check_domain = []

        self._ver_file = [".svn/wc.db", ".svn/entries", ".git/index"]

        self._ver_content_type = "application/octet-stream"

    def check(self, t_request):
        '''
		'''
        http_request = copy.deepcopy(t_request)
        url_obj = http_request.get_url()
        domain = url_obj.get_domain()

        if self._already_flag:
            return

        if domain not in self._already_check_domain:
            self._already_check_domain.append(domain)
            self._already_flag = True

        log.info(u"正在检测目标是否存在版本文件漏洞...")
        uri_string = url_obj.get_uri_string()

        for item in self._ver_file:
            ver_url = URL(uri_string).urljoin(item)
            res = requests.head(ver_url)
            ver_ct = res.headers["content-type"].lower()
            # ("wc.db|entries|index","application/octet-stream")
            if ver_ct == self._ver_content_type:
                v = vuln()
                v.set_url(ver_url)
                v.set_method("GET")
                v.set_param("")
                v.set_name("Ver Vuln")
                v.set_rank(severity.H)
                vm.append(self, http_request.get_url().get_host(), "ver", v)
                log.info("Ver Vuln")
                print "Ver Vuln 漏洞URL:%s" % (ver_url)

    def get_name(self):
        '''
		'''
        return "teye_ver_plugin"


if __name__ == "__main__":
    '''
	'''
    ver_url = "http://192.168.126.142/book/ver/"
    req = Request(ver_url)
    t_scanner = ver()
    t_scanner.check(req)
    print vm.get_all_vuln()
