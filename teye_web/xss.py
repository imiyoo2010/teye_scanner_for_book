# coding=utf-8
'''
xss.py
'''
import sys

sys.path.append("/Users/imiyoo/workplace/tscanner/")

import teye_data.severity as severity
from teye_data.vuln import vuln
from teye_data.vulnmanager import vm

from LogManager import log

import copy
from http.Request import Request

# wCurl
from wCurl import wcurl

from util.smart_fill import smart_fill


class xss:
    '''
	'''

    def __init__(self):
        '''
		'''
        self._xss_key = "<a>XSS_VULN_FOUND</a>"

        self._white_param = ["csrf_token", "captcha"]

    def check(self, t_request):
        '''
		'''
        log.info(u"正在检测目标是否存在XSS跨站漏洞...")
        http_request = copy.deepcopy(t_request)

        if http_request.get_method() == "GET":
            param_dict = http_request.get_get_param()

        if http_request.get_method() == "POST":
            param_dict = http_request.get_post_param()

        xss_payload_list = self._get_payload_list(param_dict)

        for name, poc_info in xss_payload_list:
            if name.lower() in self._white_param:
                continue

            # print "Fuzz Name:"+ name
            if http_request.get_method() == "GET":
                url_obj = http_request.get_url()
                res = wcurl.get(url_obj.get_uri_string(), params=poc_info)
                if self._find_vuln(res):
                    v = vuln()
                    url = res.get_url()
                    v.set_url(url.get_uri_string() + "?" + str(poc_info))
                    v.set_method("GET")
                    v.set_param(name)
                    v.set_name("XSS Vuln")
                    v.set_rank(severity.M)
                    vm.append(self, url.get_host(), "xss", v)

                    log.info("XSS Vuln")
                    print u"XSS Vuln 漏洞URL:%s,漏洞参数%s" % (url, name)

            if http_request.get_method() == "POST":
                url_obj = http_request.get_url()
                res = wcurl.post(url_obj.get_uri_string(), data=poc_info)
                if self._find_vuln(res):
                    v = vuln()
                    url = res.get_url()
                    v.set_url(url.get_uri_string() + ";" + str(poc_info))
                    v.set_method("POST")
                    v.set_param(name)
                    v.set_name("XSS Vuln")
                    v.set_rank(severity.M)
                    vm.append(self, url.get_host(), "xss", v)

                    log.info("XSS Vuln")
                    print u"XSS Vuln 漏洞URL:%s,漏洞参数%s" % (url, name)

    def _find_vuln(self, res):
        '''
		'''
        if res.get_code() == 404:
            return False

        if res is None:
            return False

        res_body = res.body

        if res_body is None:
            return False

        if res_body.find(self._xss_key) > -1:
            return True
        else:
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

    def _get_payload_list(self, param):
        '''
		'''
        res = []

        o_param_dict = self._fill_param(param)

        o_param_key = o_param_dict.keys()

        for name in o_param_key:
            o_v = o_param_dict.get(name)
            if type(o_v) is list:
                if len(o_v) <= 1:
                    o_v = "".join(o_v)
                else:
                    continue

            payload = "-->'''''\"\"\"\"\">>>>>;;;;;<script>" + self._xss_key + "//"

            poc_param_dict = copy.deepcopy(o_param_dict)
            poc_param_dict[name] = payload

            poc_tuple = (name, poc_param_dict)

            res.append(poc_tuple)
        return res

    def get_name(self):
        '''
		'''
        return "teye_xss_plugin"


if __name__ == "__main__":
    '''
	'''
    # sql_url = "http://nmg01-inf-ssl3.nmg01.baidu.com:8084/poc/sql-in/get_str.php?user="
    # sql_url="http://nmg01-inf-ssl3.nmg01.baidu.com:8084/poc/sql-in/get_int.php?id=1"
    # xss_url="http://nmg01-inf-ssl3.nmg01.baidu.com:8084/poc/xss/xss_sample.php?q="
    # dom_xss="http://nmg01-inf-ssl3.nmg01.baidu.com:8084/poc/fileinclude/finclude_remote_get.php?file=&id="
    un_url = "http://www.zzsmzj.gov.cn/viewCmsSite.do?gwcsCode="
    req = Request(un_url)
    vuln_inst = xss()
    vuln_inst.check(req)
    print vm.get_all_vuln()
