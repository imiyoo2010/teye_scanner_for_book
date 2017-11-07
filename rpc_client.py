#coding=utf-8
'''
rpc_client.py
'''
import rpyc
c=rpyc.connect('192.168.126.167',9999)
print c.root.test()
c.close()

