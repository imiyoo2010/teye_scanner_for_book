#coding=utf-8
import copy
from teye_web.http.function import is_similar_url

def test_filter_similar():
	'''
	'''
	url_list=['http://www.anquanbao.com/',
	'http://www.anquanbao.com/index.php',
	'http://www.anquanbao.com/index.php?a=1',
	'http://www.anquanbao.com/index.php?a=6',
	'http://www.anquanbao.com/index.php?a=102',
	'http://www.anquanba.com/index.php?b=1',
	'http://www.anquanbao.com/index.php?b=5',
	'http://www.anquanbao.com/index.php?a=1&b=1']

	result = []

	temp_list = copy.deepcopy(url_list)
	if len(temp_list)>1:
		result.append(temp_list[0])
		del temp_list[0]
	
		for item in temp_list:
			flag = False
			for a in result:
				if is_similar_url(item,a):
					flag = True
			if not flag:
				result.append(item)	
	print "去似去含前的数据:"
	print url_list
	print "去似去含后的数据:"
	print result

	
