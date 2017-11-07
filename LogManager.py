#coding=utf-8
'''
LogManager.py
'''
import logging

logging.basicConfig(format='%(name)s[%(levelname)s/%(process)d]:%(asctime)s:%(module)s.%(funcName)s.%(lineno)d - %(message)s')
log = logging.getLogger("TScanner")
log.setLevel(logging.INFO)
#log.addHandler(logging.StreamHandler())
