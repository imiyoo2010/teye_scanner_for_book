#coding=utf-8
#test_dns.py

import socket

_dnscache = {}

def _setDNSCache():
        def _getaddrinfo(*args,**kwargs):
                global _dnscache
                if args in _dnscache:
                        return _dnscache[args]
                else:
                        _dnscache[args] = socket._getaddrinfo(*args,**kwargs)
                        return _dnscache[args]

        if not hasattr(socket,'_getaddrinfo'):
                socket._getaddrinfo = socket.getaddrinfo
                socket.getaddrinfo = _getaddrinfo
def test():
        _setDNSCache()
        import requests
        r1 = requests.get('http://www.baidu.com')
        print "第一次没命中缓存的时间:"+str(r1.elapsed.microseconds)
        r2 = requests.get('http://www.baidu.com')
        print "第二次命中缓存的时间:"+str(r2.elapsed.microseconds)
test()
