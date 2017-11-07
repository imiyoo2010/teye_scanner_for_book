#coding=utf-8
'''
dpCache.py
'''
from __future__ import with_statement

import documentParser as documentParser
from lru import LRU
import threading


class dpCache:
	'''
	This class is a document parser cache.
	'''
	def __init__(self):
		self._cache = LRU(30)
		self._LRULock = threading.RLock()

	def getDocumentParserFor(self, Response):
		'''
		'''
		res = None
		hash_string = hash(Response.body)

		with self._LRULock:
			if hash_string in self._cache:
				res = self._cache[ hash_string ]
			else:
				# Create a new instance of dp, add it to the cache
				res = documentParser.documentParser(Response)
				self._cache[ hash_string ] = res

			return res
 
dpc = dpCache()
