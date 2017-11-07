#coding=utf-8
'''
smart_fill.py
'''
import sys
sys.path.append("/Users/imiyoo/workplace/tscanner/")

from LogManager import log

parameter_name_knowledge = {
    'tscanner': ['username','user','uname','userid','nickname', 'logname','name','lastname','firstname'],
    
    'abc123456': ['pass','word','pswd','pwd','auth','password'],

    'test@watscan.com':['mail','email','e-mail'],
    
    'www.test.com':['domain'],

    'http://www.test.com/':['link','target', 'url', 'website', 'website'],
    
    'Just For A Test!':['content','text', 'words', 'query', 'search', 'keyword', 'title', 'desc', 'data',
                             'payload', 'answer', 'description', 'descripcion', 
                             'message', 'excerpt', 'comment'],

    'www.watscan.com':['domain']
    
    }

def smart_fill( variable_name ):
    '''
    '''
    variable_name = variable_name.lower()

    flag = False

    for filled_value, variable_name_list in parameter_name_knowledge.items():
        
        for variable_name_db in variable_name_list:

            if variable_name_db == variable_name:
		
		flag = True

                return filled_value
            
    if not flag:

        msg = '[smart_fill] Failed to find a value for parameter with name "' + variable_name + '".'
        log.debug( msg )
        
        return 'UNKNOWN'

if __name__=="__main__":
	print "usrname=%s" % smart_fill("username")
	print "password=%s" % smart_fill("password")
	print "domain=%s" % smart_fill("domain")
	print "email=%s" % smart_fill("email")
	print "content=%s" % smart_fill("content")
