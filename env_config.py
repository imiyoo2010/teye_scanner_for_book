# coding=utf-8
'''
env_config.py
配置扫描所需要的环境
'''
import os
import platform
import teye_config as Settings

os_info = platform.platform()  # 获取操作系统名称及版本号，'Windows-7-6.1.7601-SP1'
sys_info = platform.system()  # Linux or windows or darwin
'''
def nmap_search_path():
    pass

syslist = {
    "win": ["windows"],
    "linux": ['ubuntu', 'centos', 'debian'],
    "mac": ["darwin"]
}

if os_info.lower() in syslist.get("mac"):  # Mac
    # Install brew
    cmd = 'ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2 > /dev/null'
    os.system(cmd)
    # Install Nmap
    cmd = "brew install nmap"
    os.system(cmd)
    # Install python-nmap
    cmd = "pip install python-nmap"
    os.system(cmd)

if os_info.lower() in syslist.get("linux"):  # Linux
    # python-dev,python-pip
    os.system("apt-get -y install python-dev")
    os.system("apt-get install python-pip")
    # lxml
    os.system("apt-get -y install libxml2 libxml2-dev")
    os.system("apt-get -y install python-libxml2")
    os.system("apt-get -y install python-lxml")

    # nmap
    os.system("apt-get -y install nmap")

    # python-paramiko
    os.system("apt-get -y install python-paramiko")

if os_info.lower() in syslist.get("win"):  # windows
    pass
'''
# pip install -r requirements.txt
piprequire = Settings.ROOT_PATH + "/requirements.txt"
os.system("pip install -r " + piprequire)
