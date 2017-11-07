#coding=utf-8
'''
banner.py
'''

version="1.0-dev for book"

website="http://www.watscan.com/teye"

banner='''
 _____                 ____                                  
|_   _|__ _   _  ___  / ___|  ___ __ _ _ __  _ __   ___ _ __ 
  | |/ _ \ | | |/ _ \ \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|\033[1;31m{%s}\033[0m
  | |  __/ |_| |  __/  ___) | (_| (_| | | | | | | |  __/ |   
  |_|\___|\__, |\___| |____/ \___\__,_|_| |_|_| |_|\___|_|   \033[4;37m%s\033[0m
          |___/     
'''% (version,website)


def scan_banner():
	print banner
