# falcon_agent

## Introduction

批量部署open-falcon agent


#### 配置说明
配置文件默认为./config.json。各配置项的含义，如下

```bash
{
    "dir" : "/data/open-falcon",		#agent安装目录
    "heartbeat" : "192.168.1.1:6030",		#心跳服务器地址
    "transfer" : "192.168.1.1:8433",		#transfer服务器地址
    "servers": {				#服务器列表
        "ubuntu":{
            "host": "ubuntu",			#endpoint名字
            "net_ip": "123.120.122.111",	#外网IP
            "local_ip": "127.0.0.1",		#内网IP
	    "user": "root",			#ssh用户名
	    "passwd": "root"			#ssh密码
        },
        "centos":{
            "host": "centos",
            "net_ip": "124.123.123.122",
            "local_ip": "127.0.0.1",
	    	"user": "root",
	    	"passwd": "root"
        }
    }
}

**

