#coding=utf-8
'''
factory.py
'''
import sys
import traceback

def factory(moduleName, **args):
	'''
	动态加载模块
	'''
	try:
		__import__(moduleName)
	except Exception, e:
		raise Exception('Error Import Plugin: '+ moduleName +'， Exception: ' + str(e))
	else:
		className = moduleName.split('.')[-1]

		try:
			aModule = sys.modules[moduleName]
			aClass  = getattr(aModule , className)
		except:
			raise Exception('Error Load Plugin: '+ moduleName + '.')
		else:
			try:
				inst = aClass(*args)
			except Exception, e:
				msg = 'Error Instance: ' + className + ', Exception: ' + str(e) + ', Traceback: ' + str( traceback.format_exc() )
				raise Exception(msg)
			return inst
	
