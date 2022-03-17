#coding=utf-8
'''
teye_config.py
'''
import os
import sys
#Env Settings
#ROOT_PATH='/Users/imiyoo/workplace/tscanner'

#获取当前配置文件的绝对路径
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
LIB_PATH	= ROOT_PATH + '/thirdparty/'

#加载关键路径
sys.path.append(ROOT_PATH)
sys.path.append(LIB_PATH)

#File&Path Settings
DOMAIN_FILE 	= ROOT_PATH + '/teye_file/domain/small_domain_name.txt'
DIR_HOST_FILE   = ROOT_PATH + '/teye_file/webdir/host.lst'
DIR_WEB_FILE    = ROOT_PATH + '/teye_file/webdir/web.lst'
FINGER_FILE     = ROOT_PATH + '/teye_file/finger/app.db'

#Env Path Settings
TEYE_PY_PATH    = ROOT_PATH + '/teye.py'
NMAP_PATH       ='/usr/bin/nmap'
PYTHON_ENV      ='/usr/bin/python'

#SqlHelper Settings
class Configuration:
    SQLALCHEMY_DATABASE_URI = 'sqlite://///Users/imiyoo/workplace/tscanner_for_github/teye_files/db/scan.db'

class DevelopmentConfiguration(Configuration):
    pass

class ProductConfiguration(Configuration):
    pass


_config_table = {
        'default': DevelopmentConfiguration,
        'develope': DevelopmentConfiguration,
        'product': ProductConfiguration,
        }


#Database Settings
WAT_Host='X.X.X.X'        #database host info
WAT_Database='wat'        #database name info
WAT_User='root'           #database user info
WAT_Pass='root'           #database pass info

#Activemq Settings
ACTIVEMQ_ADDRESS="tcp://X.X.X.X:61617"
ACTIVEMQ_IP='X.X.X.X'
ACTIVEMQ_PORT='61617'
ACTIVEMQ_WATSERVER_QUEUE='/queue/WATSERVER'
ACTIVEMQ_WATCLIENT_QUEUE='/queue/WATCLIENT'
ACTIVEMQ_WATAPP_QUEUE='/queue/WATAPP'
ACTIVEMQ_USER='system'
ACTIVEMQ_PASSWORD='manager'


#Rpc Settings
RPYC_HOST="X.X.X.X"
RPYC_PORT=8888


#Dispatch Settings
MSG_INTERVAL=1
BIG_MSG_INTERVAL=1*60
RECV_MSG_TIME_IDLE =30
MAX_SCAN_TIME = 2*60*60
MAX_CONCURRENT_NUM = 2
MAX_DISPATCH_TASK = 10
MAX_RETRY_COUNT = 5
RETRY_INTERVAL = 1
SCAN_TASK_INTERVAL = 60
DISPATCH_TASK_INTERVAL= 10


#COMMON VULNS
SQL_KB="http://www.imiyoo.com/teye/index.php?c=vuln&a=detail&vid=1"
XSS_KB="http://www.imiyoo.com/teye/index.php?c=vuln&a=detail&vid=2"
LFI_KB="http://www.imiyoo.com/teye/index.php?c=vuln&a=detail&vid=3"
CMD_KB="http://www.imiyoo.com/teye/index.php?c=vuln&a=detail&vid=5"
BAK_KB="http://www.imiyoo.com/teye/index.php?c=vuln&a=detail&vid=6"
