#coding=utf-8

from wCurl import wcurl
from teye_util.page_404 import is_404

def test_is_404():
	'''
	'''
	url_200 = "http://www.anquanbao.com/"
	url_404 = "http://www.anquanbao.com/noexist.html"
	
	resp_200 =wcurl.get(url_200)
	resp_404 =wcurl.get(url_404)

	assert is_404(resp_200)==False
	assert is_404(resp_404)==True


	url_200 = "http://www.baidu.com/"
        url_404 = "http://www.baidu.com/noexist.html"

        resp_200 =wcurl.get(url_200)
        resp_404 =wcurl.get(url_404)

        assert is_404(resp_200)==False
        assert is_404(resp_404)==True	
