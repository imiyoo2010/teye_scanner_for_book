#coding=utf-8
'''
scan.py
'''
import sys
sys.path.append("..")
import teye_config as Settings

from celery import Celery
from celery import platforms

import os
import uuid
import platform
import hashlib
import time
import datetime
import json

#import subprocess
from LogManager import log
from RDB import RDB

#ROOT启动
#platforms.C_FORCE_ROOT = True
#每个worker执行了多少任务就会死掉
#CELERYD_MAX_TASKS_PER_CHILD = 40

BROKER_URL='redis://127.0.0.1:6379/0'
app = Celery('scan',broker=BROKER_URL)
#app.config_from_object('scan.config')

'''
class CountTask(celery.Task):
    count = 0

    def on_success(self, retval, task_id, args, kwargs):
        self.count += 1
        return self.count
'''

@app.task(ignore_result=True)
def DoScanTask(msg_info):
    log.info("TScanner Get the Msg From the Task Queue")
    msg_json = json.loads(msg_info)
    website= msg_json.get("website")
    taskid= int(msg_json.get("taskid"))
    profile = msg_json.get("profile")
    taskstarttime = datetime.datetime.now()
    if platform.system().lower()=="linux":
        cmd="timeout %s %s %s -t %d -s '%s' -p '%s' -m 'teye'" % (Settings.MAX_SCAN_TIME,Settings.PYTHON_ENV,Settings.TEYE_PY_PATH,taskid,website,profile)
    else:
        cmd="%s %s -t %d -s '%s' -p '%s' -m 'teye'" % (Settings.PYTHON_ENV,Settings.TEYE_PY_PATH,taskid,website,profile)

    print cmd
    log.info(cmd)
    #ret = subprocess.call(cmd)
    ret= os.system(cmd)
    #ret=0 success
    if ret!=0:
        log.error("Error DoScanTask:%s" % cmd)
        rdb = RDB()
        rdb.connect()
        taskendtime = datetime.datetime.now()
        rdb.updateProgress(taskid,100)
        rdb.updateFinish(taskid,taskendtime)
        rdb.close()
        return False

    rdb = RDB()
    rdb.connect()
    taskendtime = datetime.datetime.now()
    rdb.updateFinish(taskid,taskendtime)
    rdb.close()
    log.info("Scan Website:"+website + " Spend Time:"+str(taskendtime-taskstarttime))
    return True
