#coding=utf-8
'''
postdata.py
'''

import encode_decode as enc_dec
from data import data

from encodings import DEFAULT_ENCODING

class postdata(data):
	'''
	'''
	def __init__(self, init_val=(),encoding=DEFAULT_ENCODING):
		'''
		'''
		data.__init__(self, init_val, encoding)

		self._name 		= None
		self._method 	= None
		self._action 	= None
		self._files  	= None
		

	def get_action(self):
		'''
		'''
		return self._action

	def get_method(self):
		'''
		'''
		return self._method

	def set_method(self,method):
		'''
		'''
		self._method = method

	def set_name(self,name):
		'''
		'''
		self._name = name

	def set_action(self,action):
		'''
		'''
		self._action = action

	def set_file(self,files):
		'''
		'''
		self._files= files

	def set_data(self,key,value):
		'''
		'''
		self[key] = value

	def __str__(self):
		'''
		return enc_dec.urlencode(self, encoding=self.encoding)
		'''
		return enc_dec.urlencode(self, encoding=self.encoding)

	
if __name__=="__main__":
	'''
	'''
	postdata = postdata([('id',1),('test',2)])
	print postdata
