# coding=utf-8
'''
nginx.py
'''
import sys

sys.path.append("/Users/imiyoo/workplace/teye_scan/")

from misc.common import is_404
import copy
import teye_data.severity as severity
from teye_data.vuln import vuln
from teye_data.vulnmanager import vm

from LogManager import log

# wCurl
from wCurl import wcurl
from http.Request import Request


class directory:
    '''
	'''

    def __init__(self):
        '''
		'''
        self._DIR_INDEXING = (
            "<title>Index of /",
            '<a href="?C=N;O=D">Name</a>',
            '<A HREF="?M=A">Last modified</A>',
            "Last modified</a>",
            "Parent Directory</a>",
            "Directory Listing for",
            "<TITLE>Folder Listing.",
            '<table summary="Directory Listing" ',
            "- Browsing directory ",
            # IIS 6.0 and 7.0
            '">[To Parent Directory]</a><br><br>',
            # IIS 5.0
            '<A HREF=".*?">.*?</A><br></pre><hr></body></html>'
        )

        self._already_dir_urls = []

    def check(self, t_request):
        '''
		'''
        log.info(u"正在检测目标是否存在Directory目录列举漏洞...")

        http_request = copy.deepcopy(t_request)
        url_obj = http_request.get_url()
        dir_list = url_obj.get_dirs()

        for item in dir_list:
            if item in self._already_dir_urls:
                return

            self._already_dir_urls.append(item)

            req_url = item.get_uri_string()

            res = wcurl.get(req_url)

            if self._find_vuln(res):
                v = vuln()
                v.set_url(req_url)
                v.set_method("GET")
                v.set_param("")
                v.set_name("Directory List Vuln")
                v.set_rank(severity.M)
                vm.append(self, http_request.get_url().get_host(), "directory", v)

                log.info("Directory List Vuln")
                print "----------Directory List Vuln"
                break

    def _find_vuln(self, res):
        '''
		'''
        if res is None:
            return False

        res_body = res.body

        if res_body is None:
            return False

        if res.get_code() == 200 and not is_404(res_body):
            for item in self._DIR_INDEXING:
                if res_body.find(item) > -1:
                    return True
        else:
            return False

    def get_name(self):
        '''
		'''
        return "teye_directory_plugin"


if __name__ == "__main__":
    '''
	'''
    req_url = "http://bbs.wdai.com/data/attachment/forum/201507/08/"
    req = Request(req_url)
    vuln_inst = directory()
    vuln_inst.check(req)
