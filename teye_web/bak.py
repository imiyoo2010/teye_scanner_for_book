# coding=utf-8
'''
bak.py
'''
import sys

sys.path.append("/Users/imiyoo/workplace/tscanner/")
import re
import os
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


class bak:
    '''
	'''

    def __init__(self):
        '''
		vim的临时文件:~
		vim的备份文件:swp
		管理员的备份文件:bak
		'''
        self._bak_ext = ["~", ".bak", ".swp"]

        self._zip_ext = ["zip", "rar", "7z", "gzip"]

        self._res_zip_type = ["application/zip", "application/x-rar-compressed", "application/x-7z-compressed",
                              "application/gzip"]

        self._key_ext = {"asp": "<\s*%", "aspx": "<\s*%", "php": "<?\s*php", "jsp": "<\s*%"}

        self._report_num = 0

        self._bak_max_num = 10

    def check(self, t_request):
        '''
		压缩文件，www.baidu.com,www.zip,wwwroot,w,
		'''
        if self._report_num > self._bak_max_num:
            return

        log.info(u"正在检测目标是否存在文件备份漏洞...")

        http_request = copy.deepcopy(t_request)
        url_obj = http_request.get_url()

        scheme = url_obj.get_scheme()
        domain = url_obj.get_domain()
        uri_string = url_obj.get_uri_string()
        zip_file_list = gen_zip_name(domain)

        for fname in zip_file_list:
            for item in self._zip_ext:
                zip_file = fname + "." + item
                zip_url = URL(uri_string).urljoin(zip_file)
                res = requests.head(zip_url)
                ct = res.headers["content-type"].lower()
                if ct in self._res_zip_type:
                    v = vuln()
                    v.set_url(zip_url)
                    v.set_method("GET")
                    v.set_param("")
                    v.set_name("Bak Vuln")
                    v.set_rank(severity.H)
                    vm.append(self, http_request.get_url().get_host(), "bak", v)
                    log.info("Bak Vuln")
                    print "Bak Vuln 漏洞URL:%s" % (zip_url)
                    self._report_num += 1

        url_ext = url_obj.get_ext()
        url_file = url_obj.get_filename()

        if url_file == "":
            return
        if url_ext not in self._key_ext.keys():
            return

        for bak_ext in self._bak_ext:
            if bak_ext == ".swp":
                bak_file = "." + url_file + bak_ext
                bak_url = URL(uri_string).urljoin(bak_file)
                res = requests.head(bak_url)
                bak_ct = res.headers["content-type"]
                # (".swp","application/octet-stream")
                if bak_ct == "application/octet-stream":
                    v = vuln()
                    v.set_url(bak_url)
                    v.set_method("GET")
                    v.set_param("")
                    v.set_name("Bak Vuln")
                    v.set_rank(severity.H)
                    vm.append(self, http_request.get_url().get_host(), "bak", v)
                    log.info("Bak Vuln")
                    print "Bak Vuln 漏洞URL:%s" % (bak_url)
                    self._report_num += 1
            else:
                bak_url = uri_string + bak_ext
                res = wcurl.get(bak_url)
                if self._find_vuln(res, url_ext):
                    v = vuln()
                    v.set_url(bak_url)
                    v.set_method("GET")
                    v.set_param("")
                    v.set_name("Bak Vuln")
                    v.set_rank(severity.H)
                    vm.append(self, http_request.get_url().get_host(), "bak", v)
                    log.info("Bak Vuln")
                    print u"Bak Vuln 漏洞URL:%s" % (bak_url)
                    self._report_num += 1

    def _find_vuln(self, res, url_ext):
        '''
		'''
        res_body = res.body

        if res_body is None:
            return False

        if res.get_code() == 200:
            if not is_404(res_body) and self._find_key(res_body, url_ext):
                return True
        else:
            return False

    def _find_key(self, res_body, url_ext):
        '''
		'''
        pattern = self._key_ext.get(url_ext)
        result = re.search(pattern, res_body, re.I)
        if result:
            return True
        return False

    def get_name(self):
        '''
		'''
        return "teye_bak_plugin"


if __name__ == "__main__":
    '''
	'''
    bak_url = "http://192.168.126.142/book/bak/2.php"
    req = Request(bak_url)
    t_scanner = bak()
    t_scanner.check(req)
    print vm.get_all_vuln()
