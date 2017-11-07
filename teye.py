#!/usr/bin/env python
#coding=utf-8

import os
import sys
from teye_util.banner import scan_banner
import teye_config as Settings

import optparse
import json
import datetime
from teye_web.http.URL import URL
from teye_web.http.cookie import cookie
from teye_data.config import cfg
from teye_data.info import db_info

from teye_data.vulnmanager import vm


def parseargs():
    '''
    '''
    parser = optparse.OptionParser(usage="%prog [OPTIONS]\n\n"  \
                                                "example:%prog -s \"http://testphp.vulnweb.com/\" -p '{\"useragent\":\"TScanner/1.0\",\"type\":2,\"cookie\":\"\"}' -t 100000")

    parser.add_option("-s","--URL",action="store",dest="url",   \
                      help="scan target,scan the url", \
                      default="http://www.gudwine.com")

    parser.add_option("-p","--Profile",action="store",dest="profile",   \
                      help="scan profile,config the task")

    parser.add_option("-t","--Taskid",action="store",dest="taskid", \
                      help="scan taskid,remote database index", \
		      default="100000")

    parser.add_option("-m","--Mode",action="store",dest="mode", \
                      help="scan mode,teye or tweb",	\
                      default="tweb")

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(-1)

    options,args = parser.parse_args()


    return options


def scan_config():
    '''
    '''
    scan_banner()
    options = parseargs()

    cfg.save("target",URL(options.url))
    cfg.save("profile",options.profile)
    cfg.save("taskid",int(options.taskid))
    cfg.save("mode",options.mode)

    #rpc server configure
    cfg.save("RPC_SERVER_IP","123.57.242.231")
    if cfg["mode"].lower()=="tweb":
        cfg.save("RPC_SERVER_PORT",9999)
    else:
        cfg.save("RPC_SERVER_PORT",8888)

    if cfg["taskid"]>100000:
        cfg["remote_mysql"]=True
    else:
        cfg["remote_mysql"]=False

    #profile config
    cfg["domain_scan"]=False
    t_profile = cfg.get("profile")

    if t_profile is not None:
        #type,rate,useragent,proxy,cookie
        set_profile = json.loads(t_profile)
        if int(set_profile.get("type"))==2:
            cfg["domain_scan"]=True
            cfg["max_domain_scan"]=20

        if set_profile.get("useragent"):
            cfg["scan_signature"]   = set_profile.get("useragent")
        else:
            cfg["scan_signature"]   = "TScanner/1.0"
        
        cfg["scan_cookies"]     = cookie(set_profile.get("cookie"))
        cfg["scan_proxies"]     = {'http':set_profile.get("pxory")}

    else:
        cfg["scan_signature"] 	= "TScanner/1.0"
        cfg["scan_cookies"]	= {}
        cfg["scan_proxies"]	= {}

    l_profile={}
    l_profile["useragent"]	=cfg["scan_signature"]
    l_profile["cookie"]		=cfg["scan_cookies"]
    l_profile["proxies"]	=cfg["scan_proxies"] 

    db_info.set_profile(l_profile)


if __name__=="__main__":
    '''
    '''
    scan_config()

    from teye_core.tcore import tCore
    scan_engine = tCore()
    
    try:
        scan_engine.scan_site(cfg.get("target"))

    except Exception,e:
        print str(e)
        db_info.set_end_time(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    finally:
        scan_engine.store_vuln()
        filename = cfg.get("target").get_host()+".html"
        scan_engine.generate_report(filename)
        scan_engine.end()