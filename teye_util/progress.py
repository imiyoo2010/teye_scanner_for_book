#coding=utf-8
'''
progress.py
'''

import time
from LogManager import log

class progress:
    '''
    '''    
    def __init__(self):
        
        self._max_value=0
        self._current_value=0
        self._first_amount_change_time=None
        self._eta=None
        
    def set_total_amount(self,value):
        
        self._max_value=value
        self._current_value=0.1
        self._first_amount_change_time=None
        
    
    def inc(self):
        '''
        add 1 small unit to the current value
        '''
        if self._current_value == self._max_value:
            log.error('Current value can never be greater than max value!')
        else:
            self._current_value +=0.1
            self._update_eta()
    
    def incplugin(self):
        '''
        add 1 big unit to the current value
        '''
        
        if self._current_value == self._max_value:
            log.error('Current value can never be greater than max value!')
        else:
            self._current_value +=1
            self._update_eta()
    
    def _update_eta(self):
        
        if not self._first_amount_change_time:
            self._first_amount_change_time=time.time()
        else:
            time_already_elapsed=time.time()-self._first_amount_change_time
            
            try:
                time_for_all_requests = (self._max_value * time_already_elapsed)/self._current_value
            except ZeroDivisionError:
                time_for_all_requests = time_already_elapsed * 2
            else:
                self._eta = time_for_all_requests - time_already_elapsed
    
    
    def get_progress(self):
        
        if self._max_value ==0:
            return 0
        
        return int((self._current_value / self._max_value)*100)
    
    def finish(self):
        
        self._max_value=1
        self._current_value =1
        self._first_amount_change_time = None
        self._eta = None
    
    def get_eta(self):
        
        if not self._eta:
            return 0,0,0,0
        else:
            
            self._update_eta()
            
            temp = fload()
            temp = fload(self._eta) / (60*60*24)
            d =int(temp)
            temp = (temp-d)*24
            h = int(temp)
            temp = (temp-h)*60
            m=int(temp)
            temp=(temp-m)*60
            sec = temp
            
            return d,h,m,sec
            
