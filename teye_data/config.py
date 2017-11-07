#coding=utf-8
'''
config.py

'''

class config(dict):

    def save(self, variableName, value):

        self[variableName] = value

    def getData(self, variableName):

        return self.get(variableName, None)

cfg = config()
