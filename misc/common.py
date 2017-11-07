# coding=utf-8
'''
common.py
'''

import json
import string
import hashlib
import urllib2

from random import choice, randint


def rand_letters(length=0):
    '''
	'''
    t_list = []
    for i in xrange(length or randint(6, 10)):
        t_list.append(choice(string.letters))
    return ''.join(t_list)


def rand_numbers(length=0):
    '''
	'''
    t_list = []
    for i in xrange(length or randint(6, 10)):
        if i == 0:
            t_list.append(choice(string.digits[1:]))
        else:
            t_list.append(choice(string.digits))
    return ''.join(t_list)


def md5(str):
    '''
    '''
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


def get_my_ip():
    '''
	'''
    api = "http://ip.taobao.com/service/getIpInfo.php"
    ipaddr = ""
    try:
        req = urllib2.Request(api, data="ip=myip")
        res = urllib2.urlopen(req)
        data = json.loads(res.read())
        ipaddr = data["data"]["ip"]
    except:
        pass

    return ipaddr


def is_404(res_body):
    '''
    '''
    T_404_key = [u"抱歉，您访问的页面", u"404-页面不存在", u"很抱歉，您要访问的页面不存在！", u"error404"]

    if isinstance(res_body, unicode):
        str_res_body = res_body.encode("utf-8")
    else:
        str_res_body = res_body

    for pattern in T_404_key:
        try:
            if str_res_body.find(pattern) > -1:
                return True
        except:
            return False

    return False


def is_ip_address(address):
    '''
	'''
    parts = address.split(".")
    if len(parts) != 4:
        return False

    for item in parts:
        try:
            if not 0 <= int(item) <= 255:
                return False
        except:
            return False

    return True


def is_equal_list(s_list, o_list):
    '''
        '''
    if not isinstance(s_list, list) or not isinstance(o_list, list):
        return False

    s_len = len(s_list)
    o_len = len(o_list)

    if s_len != o_len:
        return False

    count = 0
    for item in s_list:
        if item in o_list:
            count += 1

    if count == s_len:
        return True


if __name__ == "__main__":
    ip = get_my_ip()
    print ip
