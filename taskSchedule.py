#coding=utf-8
'''
nohup python taskSchedule.py &
'''
import os
import sys
import time
import json
import datetime
import teye_config as Settings

from LogManager import log
from Queue import Queue
from teye_worker.RDB import RDB
from teye_worker.scan import DoScanTask

WAT_MSG_INFO={"taskid":"","website":"","profile":"","message":""}

if __name__=='__main__':
    '''
    '''
    q = Queue(Settings.MAX_DISPATCH_TASK)
    while True:
	while True:
		count = 0
        	try:
        		rdb = RDB()
	        	rdb.connect()
        		tasks =rdb.getNewtasks(Settings.MAX_DISPATCH_TASK)
        		for task in tasks:
           			msg= task.get("msg")
           			taskid=task.get("taskid")
           			taskstarttime = datetime.datetime.now()
           			rdb.updateFlag(taskid)
           			rdb.updateStart(taskid,taskstarttime)
           			q.put(msg)
        		rdb.close()
			break
    		except Exception,e:
        		print str(e)
			count +=1
			if count > Settings.MAX_RETRY_COUNT:
				sys.exit(-1)
        		time.sleep(Settings.RETRY_INTERVAL)

	worker_count = q.qsize()
	wait_circle = worker_count/Settings.MAX_CONCURRENT_NUM

    	while True:
        	if q.empty()==True:
           		break

        	msg_list = []
        	for i in xrange(Settings.MAX_CONCURRENT_NUM):
           		if not q.empty():
               			msg = q.get()
        	       		msg_list.append(msg)

        	for item in msg_list:
           		try:
               			DoScanTask.delay(item)
           		except:
               			pass

    		time.sleep(wait_circle*Settings.SCAN_TASK_INTERVAL)
	time.sleep(Settings.DISPATCH_TASK_INTERVAL)
