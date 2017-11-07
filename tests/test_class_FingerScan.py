#coding=utf-8

import sys
sys.path.append('/Users/imiyoo/workplace/tscanner')

from teye_finger.FingerScan import FingerScan


def test_scan_finger():
	'''
	'''
	lnmp_body     = "http://192.168.126.143/"

	nginx_headers = "http://192.168.1.143/"

	thinkphp_md5  = "http://192.168.126.143/thinkphp/"

	fs = FingerScan()
	fs.set_mode(1)
	res = fs.scan_finger(lnmp_body)
	print "%s 的应用指纹有:" % lnmp_body
	print res

	res1 = fs.scan_finger(thinkphp_md5)
	print "%s 的应用指纹有:" % thinkphp_md5
	print res1

