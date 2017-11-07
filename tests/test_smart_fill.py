#coding=utf-8
'''
smart_fill.py
'''
form_name_kb = {
"cannner":['username','user','userid','nickname','name'],
"bc123456":['password','pass','pwd'],
"est@watscan.com":['email','mail','usermail'],
"13800000000":['mobile'],
"his is just for a test":['content','text','query','search','data','comment'],
"ww.test.com":['domain','website'],
"ttp://www.test.com":['link','url']
}
def smart_fill( variable_name ):
    '''
    '''
    variable_name = variable_name.lower()
    flag = False
    for filled_value, variable_name_list in form_name_kb.items():
        for variable_name_db in variable_name_list:
		if variable_name_db == variable_name:
			flag = True
			return filled_value
    if not flag:
        msg = '[smart_fill] Failed to find a value for parameter with name "'
        msg += variable_name + '".'
        log.debug( msg )
        return 'UNKNOWN'

if __name__=="__main__":
	print smartfill("username")
	print smartfill("password")
	print smartfill("email")
	print smartfill("content")
