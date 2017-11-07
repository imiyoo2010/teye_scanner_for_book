# coding=utf-8
'''
cmd.py
'''
import sys

sys.path.append("/Users/imiyoo/workplace/tscanner/")
import teye_data.severity as severity
from teye_data.vuln import vuln
from teye_data.vulnmanager import vm

from LogManager import log

import re
import copy

# wCurl
from wCurl import wcurl
from http.Request import Request

from util.smart_fill import smart_fill


class cmd:
    '''
	'''

    def __init__(self):
        '''
		'''
        # 扫描模式:0为对参数进行FUZZ,1为对路径进行FUZZ
        self._fuzz_mode = 0

        self._cmd_db = self._get_cmd_db()

    def check(self, t_request):
        '''
		'''
        log.info(u"正在检测目标是否存在命令执行漏洞...")

        http_request = copy.deepcopy(t_request)
        if http_request.get_method() == "GET":
            param_dict = http_request.get_get_param()

        if http_request.get_method() == "POST":
            param_dict = http_request.get_post_param()

        cmd_payload_list = self._get_payload_list(param_dict)

        for name, poc_info, pattern in cmd_payload_list:
            if http_request.get_method() == "GET":
                res = wcurl.get(http_request.get_url().get_uri_string(), params=poc_info)
                if self._find_vuln(res, pattern):
                    v = vuln()
                    url = res.get_url()
                    v.set_url(url.get_uri_string() + "?" + str(poc_info))
                    v.set_method("GET")
                    v.set_param(name)
                    v.set_name("CMD Vuln")
                    v.set_rank(severity.H)
                    vm.append(self, url.get_host(), "cmd", v)
                    log.info("CMD Vuln")
                    print u"CMD Vuln 漏洞URL:%s,漏洞参数:%s" % (url, name)

    def _find_vuln(self, res, pattern):
        '''
		'''
        res_body = res.body

        if res_body is None:
            return False

        result = re.search(pattern, res_body, re.I)
        if result:
            return True

        return False

    def _get_cmd_db(self):
        '''
		#"type":"linux","cmd":"id","payload":";id;","pattern":""
		'''
        cmd_db = []

        cmd_item = {}
        cmd_item["type"] = "linux"
        cmd_item["cmd"] = "id"
        # "||id;",
        cmd_item["payload"] = [";id;", "';id;'"]
        cmd_item["pattern"] = r"uid=\d+\(\w+\)\s*gid=\d+\(\w+\)\s*groups=\d+\(\w+\)"
        cmd_db.append(cmd_item)

        cmd_item = {}
        cmd_item["type"] = "php"
        cmd_item["cmd"] = "print(md5(imiyoo))"
        cmd_item["payload"] = [";${print(md5(imiyoo))}", "';${print(md5(imiyoo))};'", "\"]=1;${print(md5(imiyoo))};//"]
        cmd_item["pattern"] = r"1417a3e718a3d279aefda8711a0f5f65"
        cmd_db.append(cmd_item)

        cmd_item = {}
        cmd_item["type"] = "win"
        cmd_item["cmd"] = "set"
        cmd_item["payload"] = [";set;", "||set;"]
        cmd_item["pattern"] = r"SystemRoot=C:\Windows"
        cmd_db.append(cmd_item)

        return cmd_db

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

            for item in self._cmd_db:
                cmdtype = item["type"]
                pattern = item["pattern"]
                payload_list = item["payload"]
                for p in payload_list:
                    # payload的构造形式为:原始值+payload
                    o_param_dict[name] = o_v + p

                    # 完整的参数信息，字典类型
                    poc_param_dict = copy.deepcopy(o_param_dict)
                    poc_tuple = (name, poc_param_dict, pattern)
                    res.append(poc_tuple)
        return res

    def get_name(self):
        '''
		'''
        return "teye_cmd_plugin"


if __name__ == "__main__":
    '''
	'''
    cmd_url = "http://192.168.126.143/book/cmd/1_cmd.php?data=test"
    req = Request(cmd_url)
    t_scanner = cmd()
    t_scanner.check(req)
