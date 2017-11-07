#coding=utf-8
'''
more_pass.py
'''

import sys

pass_type_list=[
 '<name>123',
 '<name>abc',
 '<name>_123',
 '<name>!123',
 '<name>@123',
 '<name>#123',
 '<name>123456',
 '<name>abc123',
 '<name>123!@#',
 '<name>!@#123',
 '<name>123$%^',
 '<name>!@#$%^',
 '<domain>',
 '<domain>123',
 '<domain>@123',
 '<domain>@abc',
 '<domain>123!@#',
 '<domain>!@#123',
 '<domain>123$%^',
 '<domain>!@#$%^',
 '<name>@<domain>@123',
 '<domain>@<name>@123'
]

def get_pass_list(email):
	'''
	>>>email="zhangsan@baidu.com"
	>>>ext_pass_list(email)
	>>>['zhangsan@123','zhangsan@baidu@123'...]
	'''
	item   = email.split("@")
	name   = item[0]
	domain = item[1].split(".")[0]

	pass_list = []
	
	for line in pass_type_list:
		pass_item = line.strip().replace("<name>",name).replace("<domain>",domain)
		pass_list.append(pass_item)
	
	return pass_list

if __name__=="__main__":
	result=get_pass_list("zhangsan@baidu.com")
	print result
