#!/usr/bin/env python
#coding:utf-8

"""

    批量部署open-falcon agent脚本

"""

import json
import subprocess
 
##falcon agent conf path
agent_cfg_json="./open-falcon/agent/config/cfg.json"

## 服务器列表
cfg_json="./config.json"

##get ip address
 
def get_ipaddr():
    import socket
    ##get hostname
    hostname = socket.getfqdn(socket.gethostname())
    ip_addr=socket.gethostbyname(hostname)
    return ip_addr
 
##change file
 
def change_file(config,host_info):
    ##打开文件，重新赋值
    with open(agent_cfg_json,"rb") as f:
        old_dict=json.load(f)
        old_dict["heartbeat"]["addr"] = config['heartbeat']
        old_dict["transfer"]["addrs"][0] = config['transfer']
        old_dict["hostname"] = host_info['host']
        old_dict["ip"] = host_info['net_ip']

    ##打开文件，并覆盖写入修改后内容
    with open(agent_cfg_json,"wb") as f:
        json.dump(old_dict,f,indent=4)
        
def mk_dir(dir,host_info):
        p=subprocess.Popen("sudo sshpass -p %s ssh %s@%s 'mkdir -p %s'" % (host_info['passwd'],host_info['user'],host_info['net_ip'],dir),shell=True,cwd="./",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout,stderr=p.communicate()
        return stdout,stderr
    
def scp_file(dir,host_info):
        p=subprocess.Popen("sudo sshpass -p %s scp -rp open-falcon/* %s@%s:%s/" % (host_info['passwd'],host_info['user'],host_info['net_ip'],dir),shell=True,cwd="./",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout,stderr=p.communicate()
        return stdout,stderr
 
## start open falcon agent
def start_openfalcon_agent(dir,host_info):
        p=subprocess.Popen("sshpass -p %s ssh %s@%s 'cd %s && ./open-falcon stop agent && ./open-falcon start agent'" % (host_info['passwd'],host_info['user'],host_info['net_ip'],dir),shell=True,cwd="./",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout,stderr=p.communicate()
        return stdout,stderr
    
def check_openfalcon_agent(dir,host_info):
        p=subprocess.Popen("sshpass -p %s ssh %s@%s 'cd %s && ./open-falcon check'" % (host_info['passwd'],host_info['user'],host_info['net_ip'],dir),shell=True,cwd="./",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout,stderr=p.communicate()
        return stdout,stderr
 
def main():
        ##打开配置文件
    with open(cfg_json,"rb") as f:
        config=json.load(f)
        
    for host in config['servers']:
        dir = config['dir']
        hostinfo = config['servers'][host]
        change_file(config,hostinfo)
        mk_dir(dir,hostinfo)
        scp_file(dir,hostinfo)
        start_openfalcon_agent(dir,hostinfo)
        stdoutdata,stderr = check_openfalcon_agent(dir,hostinfo)
        lines = [bat for bat in stdoutdata.splitlines() if 'falcon-agent' in bat]
        if not lines:
            ret = "FAILED"
        else:
            str_list = lines[0].split()
            if str_list[1] == "UP":
                ret = "OK"
            else:
                ret = "FAILED"
        print("%s....%s" % (hostinfo['net_ip'],ret))
    print("All Finished")
 
if __name__=="__main__":
    main()
