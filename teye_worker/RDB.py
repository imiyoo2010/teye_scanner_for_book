#coding=utf-8
'''
RDB.py
'''
import sys
sys.path.append("..")
import teye_config as Settings

import rpyc
import logging
import json

import time
import hashlib
import sys
import threading

class RDB:
	
	def __init__(self):

		self.__client = None


	def connect(self):

		try:
			self.__client = rpyc.connect(Settings.RPYC_HOST,Settings.RPYC_PORT)

			self.__client.root.open()

		except Exception,e:
			
			self.close()

	def getTaskcount(self):

		result = self.__client.root.client_getTaskcount()

		count = int(result[0][0])

		return count
	
	def getNewtasks(self,num):

		data=[]

		if self.__client is None:
			self.connect()

		result = self.__client.root.client_getNewtasks(num)
		
		for task in result:

			Settings.WAT_MSG_INFO['taskid']=task[0]
			Settings.WAT_MSG_INFO['website']=task[1]
                	Settings.WAT_MSG_INFO['profile']=task[2]
			msg = json.dumps(Settings.WAT_MSG_INFO)
			
			content={"taskid":task[0],"msg":msg}

			data.append(content)
	
		return data

	def updateStart(self,taskid,starttime):
		'''
		'''
		self.__client.root.client_update_starttime(taskid,starttime)

                return True
	
	def updateFinish(self,taskid,finishtime):
		'''
		'''
		self.__client.root.client_update_finishtime(taskid,finishtime)

		return True

	def updateProgress(self,taskid,progress):
		'''
		'''
		self.__client.root.client_update_progress(taskid,progress)

		return True
	
	def updateStatus(self,taskid,status,msginfo=''):
		'''
		0----init
		1----queue
		2----scan
		3----stop
		4----erro
		5----finish
		'''
		
		self.__client.root.client_updateStatus(taskid,status,msginfo)
		
		return True
	
	def updateFlag(self,taskid):
		'''
		'''
		
		self.__client.root.client_update_flag(taskid)
		
		return True
	
	def close(self):
		if self.__client is not None:

			try:
				self.__client.root.close()
			except:
				pass

			self.__client.close()
		else:
			self.__client=None

if __name__=="__main__":
	rdb =RDB()
	rdb.connect()
	result =rdb.getNewtasks(3)
	print result
