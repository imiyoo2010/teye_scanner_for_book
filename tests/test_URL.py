#coding=utf-8

from teye_web.http.URL import URL


def setUp():
	pass

def tearDown():
	pass


def TestURL():
	url = URL("http://www.anquanbao.com/book/index.php?id=1#top")
	assert url.get_host()=="www.anquanbao.com"
	print url.get_port()
	assert url.get_port()==80
	assert url.get_path()=="/book/index.php"
	assert url.get_filename()=="index.php"
	assert url.get_ext() =="php"
	assert url.get_fragment()=="top"
	url = URL("http://www.anquanbao.com/book")
        print url.get_filename()

	url = URL("http://www.anquanbao.com/book/")
	print url.get_filename()
