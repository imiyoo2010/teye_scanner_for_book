#coding=utf-8

from teye_web.http.Request import Request
from teye_web.sql import sql
from teye_web.xss import xss
from teye_web.cmd import cmd
from teye_web.lfi import lfi
from teye_web.bak import bak
from teye_web.ver import ver
from teye_data.vuln import vuln
from teye_data.vulnmanager import vm


def test_sql():
	'''
	'''
	url_list = [("number","http://192.168.126.143/book/sql/1_sql.php?id=1"),
	("char_single","http://192.168.126.143/book/sql/2_sql.php?id=1"),
	("char_dobule","http://192.168.126.143/book/sql/3_sql.php?id=1"),
	("search_single","http://192.168.126.143/book/sql/4_sql.php?search=a"),
	("search_dobule","http://192.168.126.143/book/sql/5_sql.php?search=a"),
	]	
    	
	for type,url in url_list:
		req = Request(url)
    		t_scanner=sql()
    		t_scanner.check(req)
    	print vm.get_all_vuln()

def test_xss():
	'''
	'''
	url_list=['http://192.168.126.143/book/xss/1_xss.php?data=test',
	'http://192.168.126.143/book/xss/2_xss.php?data=test',
	'http://192.168.126.143/book/xss/3_xss.php?data=test'
	]
	
	for url in url_list:
		req = Request(url)
		t_scanner = xss()
		t_scanner.check(req)

	print vm.get_all_vuln()

def test_lfi():
	'''
	'''
	url_list=['http://192.168.126.145/book/lfi/1_lfi.php?data=test',
        'http://192.168.126.145/book/lfi/2_lfi.php?data=test',
        'http://192.168.126.145/book/lfi/3_lfi.php?data=test'
        ]

        for url in url_list:
                req = Request(url)
                t_scanner = lfi()
                t_scanner.check(req)

        print vm.get_all_vuln()

def test_cmd():
	'''
	'''
	url_list=['http://192.168.126.145/book/cmd/1_cmd.php?data=test',
        'http://192.168.126.145/book/cmd/2_cmd.php?data=test',
        'http://192.168.126.145/book/cmd/3_cmd.php?data=test',
	'http://192.168.126.145/book/cmd/4_cmd.php?data=test',
	'http://192.168.126.145/book/cmd/5_cmd.php?data=test'
        ]

        for url in url_list:
                req = Request(url)
                t_scanner = cmd()
                t_scanner.check(req)

        print vm.get_all_vuln()

def test_bak():
	'''
	'''
	bak_url="http://192.168.126.143/book/bak/2.php"
        req = Request(bak_url)
        t_scanner=bak()
        t_scanner.check(req)
	
	print vm.get_all_vuln()

def test_ver():
	'''
	'''
	ver_url="http://192.168.126.143/book/ver/"
        req = Request(ver_url)
        t_scanner=ver()
        t_scanner.check(req)
        print vm.get_all_vuln()
