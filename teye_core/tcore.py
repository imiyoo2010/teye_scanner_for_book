# coding=utf-8
'''
tcore.py
'''
import os
import sys
import json
import time
import base64
import thread
import datetime
import timeout_decorator

import teye_config as Settings

from teye_port.PortScan import PortScan
from teye_dir.DirScan import DirScan
from teye_finger.FingerScan import FingerScan
from teye_domain.DomainScan import DomainScan

from teye_web.http.URL import URL
from teye_web.http.Request import Request

from teye_data.config import cfg
from teye_data.info import db_info
from teye_data.vulnmanager import vm

from misc.factory import factory

from misc.common import is_ip_address, get_my_ip

from LogManager import log

from crawler import Crawler

# progress class
from teye_util.progress import progress

# mysqlmanager
from teye_util.mysqlmanager import mm

# Report
from teye_report.HtmlReport import HtmlReport

# 2个小时
MAX_SCAN_WEB_TIMEOUT = 3600


class tCore:
    '''
	'''

    def __init__(self):
        '''
		'''
        self._domain_file = Settings.DOMAIN_FILE
        self._host_dir_file = Settings.DIR_HOST_FILE
        self._web_dir_file = Settings.DIR_WEB_FILE

        self._ps = None
        # host task
        self._host_task = []
        # http task
        self._http_task = []

        self._host_info_list = []
        self._site_info_list = []
        self._common_check_list = ["sql", "xss", "cmd", "lfi", "directory"]

        self._poc_list = ["flash_crossdomain",
                          "iis_enumeration", "openssl_heartbleed"]

        self._dir_vuln = 0

        # api var
        self._api_request_list = []
        self._api_domain_list = []

        self.circle_time = 30

        self.progress = progress()

        self._progress_status = False

        self._lock = thread.allocate_lock()

    def _initial(self):
        '''
		'''
        self._ps = PortScan()

        self.progress.set_total_amount(30)

        if cfg["remote_mysql"] == True:
            mm._init()

    def update_scan_status(self):
        '''
		'''
        if self._progress_status:
            self.progress.finish()
        else:
            self.progress.incplugin()

        log.info(u"当前扫描进度为:" + str(self.progress.get_progress()) + "%")
        if cfg["remote_mysql"] == True:
            mm.t_update_percent(self.progress.get_progress())

    def update_progress(self):
        '''
		'''
        while not self._progress_status and self.progress.get_progress() < 90:
            self._lock.acquire()
            self.update_scan_status()
            if cfg["remote_mysql"] == True:
                self.store_vuln()
            self._lock.release()
            time.sleep(self.circle_time)

    def scan_site(self, target):
        '''
		'''
        # initial
        self._initial()

        site = ''
        myip = ''
        ipaddr = ''

        # config info
        target_domain = target.get_domain()
        netloc = target.get_netloc()
        myip = get_my_ip()
        ipaddr = self._ps.get_ipaddr(target_domain)

        db_info.set_entry(target_domain)
        db_info.set_myip(myip)
        db_info.set_ipaddr(ipaddr)
        db_info.set_start_time(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        pthread = thread.start_new_thread(self.update_progress, ())

        if not self._ps.is_alive(netloc):
            print "Target is not alive!"
            self._progress_status = True
            self.update_scan_status()
            self.end()

        root_domain = target.get_root_domain()

        db_info.set_domain(root_domain)

        if cfg["domain_scan"] == True:
            domain_list, ipaddr_list = self.scan_domain(root_domain)

            if target_domain not in domain_list:
                domain_list.append(target_domain)

            db_info.set_subdomain(domain_list)
            # ipaddr_list不包含当前目标的IP地址
            db_info.set_relate_ipaddr(ipaddr_list)

            self._http_task.extend(domain_list)
            self._host_task.extend(ipaddr_list)

            if ipaddr not in self._host_task:
                self._host_task.append(ipaddr)

            for item in self._host_task:
                http_target = self.scan_host(URL(item))

            for t in http_target:
                if t not in self._http_task:
                    self._http_task.append(t)

            scan_count = 0
            for task in self._http_task:
                if scan_count > cfg["max_domain_scan"]:
                    break
                url = URL(task)
                self._scan_worker(url)
                scan_count = scan_count + 1
        else:

            http_target = []
            # http_target = self.scan_host(target)
            # nmap is filter,only one target
            if len(http_target) == 0:
                target_self = target.get_host() + ":" + str(target.get_port())
                http_target.append(target_self)

            for t in http_target:
                self._http_task.append(t)

            for task in self._http_task:
                url = URL(task)
                self._scan_worker(url)

        db_info.set_end_time(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self._progress_status = True
        self.update_scan_status()

    # 应用层扫描实例函数
    def _scan_worker(self, url):
        '''
		'''
        log.info("Scaning Target:" + url.url_string)
        db_info.get("scan_target").append(url.get_netloc())

        if is_ip_address(url.get_host()):
            dir_item = self.scan_dir(url, self._host_dir_file)
            db_info.get("dir").append(dir_item)
            self.scan_web(url)
            self.scan_poc(url)
        else:
            dir_item = self.scan_dir(url,self._web_dir_file)
            db_info.get("dir").append(dir_item)

            finger_item = self.scan_finger(url)
            db_info.get("finger").append(finger_item)

            # crawl website & audit request
            self.scan_web(url)
            self.scan_poc(url)

        self.progress.incplugin()

    def scan_api(self, api_list):
        '''
		api_item:{"apiurl":"","method":"","cookie":"","data":""}
		'''
        db_info.set_start_time(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        api_report = []
        for item in api_list:
            api_report.append(item.get("apiurl"))
        db_info.set_api(api_report)

        for item in api_list:
            method = item.get("method").upper()

            if method == "GET":
                api_url = URL(item.get("apiurl"))
                cookie = item.get("cookie")

                req = Request(api_url, "GET", cookie=cookie)
                self._api_request_list.append(req)

            elif method == "POST":
                api_url = URL(item.get("apiurl"))
                cookie = item.get("cookie")
                post_data = item.get("data")

                req = Request(api_url, "POST", cookie=cookie, post_data=post_data)
                self._api_request_list.append(req)

            else:
                pass

        # Add All Domain For Poc Check
        for r in self._api_request_list:
            domain = r.get_url().get_host()
            if domain not in self._api_domain_list:
                self._api_domain_list.append(domain)
            log.info("Check URL:" + r.get_url_string())
            self.scan_request(r)

        for site in self._api_domain_list:
            urlobj = URL(site)
            self.scan_poc(urlobj)

        db_info.set_end_time(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def scan_host(self, url):
        '''
		'''
        ipaddr = ''
        ipaddr = url.get_host()
        # port  = self._ps.scan_port(ipaddr)
        port = self._ps.nmap_scan(ipaddr)
        self._host_info_list.append(port)
        db_info.set_port(self._host_info_list)

        return self._ps.get_http_target()

    @timeout_decorator.timeout(MAX_SCAN_WEB_TIMEOUT)
    def scan_web(self, url):
        '''
		'''
        w = Crawler()
        req_list = w.crawl(url)

        for item in req_list:
            print item
            self.scan_request(item)

    def scan_domain(self, root_domain):
        '''
		'''
        ds = DomainScan(self._domain_file)
        domain_list = ds.domain_scan(root_domain)

        print ds.get_ip_list()

        ipaddr_list = ds.get_ip_list()

        return domain_list, ipaddr_list

    def scan_dir(self, url, file_list=None):
        '''
		@site:http://www.watscan.com
		'''
        urlstr = url.url_string

        dir_scan = DirScan()
        dir_scan.scan_dir(urlstr, file_list)

        found_dir = dir_scan.get_dir_file()

        if len(found_dir) > 0:
            self._dir_vuln += len(found_dir)
        dir_site = {"site": url.get_host(), "found": found_dir}

        return dir_site

    def scan_finger(self, url):
        '''
		'''
        urlstr = url.url_string

        fs = FingerScan()
        # [("http://www.watscan.com","nginx")]
        finger = fs.scan_finger(urlstr)

        str_finger = ""

        if len(finger) == 0:
            str_finger = "N/A"
        else:
            finger_list = []
            for f_url, f_name in finger:
                finger_list.append(f_name)
            str_finger = ",".join(finger_list)

        finger_site = {"site": url.get_netloc(), "app": str_finger}

        return finger_site

    def scan_request(self, request):
        '''
		'''
        for vulcheck in self._common_check_list:
            vul_inst = factory("teye_web." + vulcheck)
            vul_inst.check(request)

    def scan_poc(self, url):
        '''
		'''
        for poccheck in self._poc_list:
            poc_inst = factory("teye_poc." + poccheck)
            poc_inst.check(url)

    def get_host_info(self):
        '''
		'''
        return self._host_info_list

    def store_vuln(self):
        '''
		'''
        b = vm.get_vuln_for_report()
        high, middle, low, notice = vm.get_count_for_report()
        notice = notice + self._dir_vuln
        # print high,middle,low,notice
        db_info.set_vuln(b)
        # print vm.get_all_vuln()
        # print db_info
        result = base64.b64encode(str(db_info))
        if cfg["remote_mysql"] == True:
            mm.t_report_vuln(result, high, middle, low, notice)

    def generate_report(self, filename, mode="SITE"):
        '''
		'''
        report = HtmlReport(db_info, mode)
        report.generate(filename)

    def end(self):
        '''
		'''
        if cfg["remote_mysql"] == True:
            mm.close()
        os._exit(0)


if __name__ == "__main__":
    '''
	target = URL("http://www.renrendai.com")
	scan_engine = tCore()
	scan_engine.scan_site(target)

	b = vm.get_vuln_for_report()
	print vm.get_vuln_count()
	db_info.set_vuln(b)

	report = HtmlReport(db_info)
	report.generate("site_test.html")
	'''
    # api_list=[{"apiurl":"http://vulnhost/poc/sql-in/get_int.php?id=1","method":"GET","data":None,"cookie":None}]
    api_list = []
    #filename = "api_result_mls_url_list.txt"
    filename = sys.argv[1]
    file = open(filename, "r")
    for item in file.readlines():
        api = json.loads(item.strip())
        api_list.append(api)
    scan_engine = tCore()
    scan_engine.scan_api(api_list)
    b = vm.get_vuln_for_report()
    db_info.set_vuln(b)
    report = HtmlReport(db_info, model="MAPP")
    report.generate("mobile_test.html")