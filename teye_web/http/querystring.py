#coding=utf-8
'''
querystring.py
'''
import encode_decode as enc_dec
from data import data

from encodings import DEFAULT_ENCODING

class querystring(data):
		'''
		'''
		def __init__(self, init_val=(), strict=False, encoding=DEFAULT_ENCODING):
			data.__init__(self, init_val, encoding)

		def __str__(self):
			'''
			'''
			return enc_dec.urlencode(self, encoding=self.encoding)



if __name__=="__main__":
	'''
	'''
	a = querystring([("a",[2,3])])
	print a

