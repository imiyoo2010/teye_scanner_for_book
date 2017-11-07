#coding=utf-8
'''
mysqlmanager.py
'''
import rpyc
import hashlib
import datetime

from LogManager import log
from teye_data.config import cfg

class mysqlmanager:
    
    '''
    a class to manager the action between the program and the mysql
    
    according to rpyc report the information to the database
    
    '''
    
    def __init__(self):
            
        self._client = None
        
        self._host    =None
        
        self._port    =None

    def _init(self):
        
        self._taskid    =int(cfg.getData('taskid'))
        self._website   =cfg.getData("target").get_host()

	self._host    =cfg.getData('RPC_SERVER_IP')
        self._port    =int(cfg.getData('RPC_SERVER_PORT'))
        
        try:
            self._client=rpyc.connect(self._host,self._port)
            self._client.root.open()
            
        except Exception,e:
            log.error(str(e))
        
    def md5hex(self,str):
        '''
        '''
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    #exposed_client_update_percent(self,taskid,progress):
    def t_update_percent(self,progress):
        '''
        '''
        try:
            self._client.root.client_update_progress(self._taskid,progress)
        except Exception,e:
            log.error(str(e))
    
    #exposed_client_update_starttime(self,taskid,starttime):
    def wat_update_starttime(self,starttime):
        '''
        '''
        try:
           self._client.root.client_update_starttime(self._taskid,starttime)
        except Exception,e:
            log.error(str(e))

    #exposed_client_update_finishtime(self,taskid,finishtime):
    def wat_update_finishtime(self,finishtime):
        '''
        '''
        try:
           self._client.root.client_update_finishtime(self._taskid,finishtime)
        except Exception,e:
            log.error(str(e))
    
    #exposed_client_insert_brute
    def wat_report_bruteurl(self,bruteurl):
        '''
        '''
        try:
            self._client.root.client_insert_bruteurl(self._taskid,self._domain,bruteurl)
        except Exception,e:
            om.out.error(str(e))

    def t_task_exist(self):
	'''
	'''
	result = None
	try:
	    result = self._client.root.client_task_exist(self._taskid)
	except Exception,e:
	    log.error(str(e))

	return result

    #exposed_client_insert_reports(self,taskid,website,high,middle,low,notice)
    def t_report_vuln(self,result,high_count,middle_count,low_count,notice_count):
	'''
	'''
	if self.t_task_exist():
	    try:
	        self._client.root.client_update_reports(self._taskid,result,high_count,middle_count,low_count,notice_count)
	    except Exception,e:
		log.error(str(e))
	else:

	    try:
                self._client.root.client_insert_reports(self._taskid,self._website,result,high_count,middle_count,low_count,notice_count)
            except Exception,e:
                log.error(str(e))
    
    
    def close(self):
      
        if self._client:
                self._client.close()
        else:
                return True
        

mm = mysqlmanager()
