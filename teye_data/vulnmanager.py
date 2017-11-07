#coding=utf-8
'''
vulnmanager.py
'''

from __future__ import with_statement

import threading
import teye_data.severity as severity

class vulnmanager:
    '''
    '''
    def __init__(self):
        '''
        '''
        self._vm ={}

        self._vuln_item =  {"site":"","vlist":[{"name":"sql","list":[]}]}

        self._vm_lock = threading.RLock()

        self._high_count    =0
        self._middle_count  =0    
        self._low_count     =0
        self._notice_count  =0


    def save(self,callingInstance,variableName,value):
        '''
        '''
        if isinstance(callingInstance,basestring):
            name = callingInstance
        else:
            name = callingInstance.get_name()
        
        with self._vm_lock:
            if name not in self._vm.keys():
                self._vm[name] = {variableName:value}
            else:
                self._vm[name][variableName]=value
    
    def append( self, callingInstance, site, variableName, value ):
        '''
        {"site":{"sql":{“"SQL注入漏洞":[]}}}
        '''
        if isinstance( callingInstance, basestring ):
            name = callingInstance
        else:
            name = callingInstance.get_name()
        
        with self._vm_lock:
            if site not in self._vm.keys():
                self._vm[ site ] = {name:{variableName:[value,]}}

            else:
                if name not in self._vm[site].keys():
                    self._vm[site][name] ={variableName:[value,]}
                else:
                    if variableName in self._vm[ site ][ name ]:
                        self._vm[ site ][ name ][ variableName ].extend( [value,] )
                    else:
                        self._vm[ site ][ name ][ variableName ] = [value,]

    def get_all_site(self):
        '''
        '''
        res = []

        with self._vm_lock:
            for item in self._vm.keys():
                res.append(item)

        return res

    def get_all_type(self,site=""):
        '''
        '''
        res = []

        with self._vm_lock:
            for item in self._vm.keys():
                for type in self._vm[site].keys():
                    res.append(type)

        return res


    def get_vuln_for_report(self):
        '''
        [{
            "site":"www.watscan.com",
            "vlist":
            [
                {
                    "sql":
                    [
                        {"url":"http://www.watscan.com/index.php?id=1","rank":"high","method":"GET"}
                    ]
                }
            ]
        }]
        '''
        res= []

        h_count = 0
        m_count = 0
        l_count = 0
        n_count = 0

        with self._vm_lock:

            for site in self._vm.keys():
                vuln_list = []
                for plugin_name in self._vm[ site ].keys():
                    for save_name in self._vm[site][plugin_name].keys():
                        if isinstance( self._vm[ site ][ plugin_name ][save_name], list ):
                            for i in self._vm[ site ][ plugin_name ][save_name]:
                                v_tuple = (save_name,i)
                                vuln_list.append( v_tuple )
                vlist = {}
                for r_name,r_vuln in vuln_list:
                    url     = r_vuln.get_url()
                    param   = r_vuln.get_param()
                    rank    = r_vuln.get_rank()
                    method  = r_vuln.get_method()
                    if rank==severity.H:
                        h_count +=1
                    if rank==severity.M:
                        m_count +=1
                    if rank==severity.L:
                        l_count +=1
                    if rank==severity.N:
                        n_count +=1
        
                    v_item ={"url":url,"param":param,"rank":rank,"method":method}
                    if r_name not in vlist.keys():
                        vlist[r_name]=[v_item,]
                    else:
                        vlist[r_name].append(v_item)

                item = {"site":site,"vlist":vlist}

                res.append(item)
        
            self._high_count  = h_count
            self._middle_count = m_count
            self._low_count    = l_count
            self._notice_count = n_count
    

        return res


    def get_count_for_report(self):
        '''
        '''
        return self._high_count,self._middle_count,self._low_count,self._notice_count

    def get_all_vuln(self):
        '''
        '''
        return self._vm

    def cleanup(self):
        '''
        Cleanup internal data.
        '''
        with self._vm_lock:
            self._vm.clear()



vm=vulnmanager()
