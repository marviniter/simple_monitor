#!/usr/bin/env python
#_*_coding:utf-8_*_

import commands
import time

def monitor():
    shell_command = 'uptime'
    timestamp = int(time.time())
    status,result = commands.getstatusoutput(shell_command)
    if status != 0:
        value_dic = {'status':status}
    else:
        value_dic = {}
        uptime = result.split(',')[:1][0]
        load1,load5,load15 = result.split('load average:')[1].split(',')
        value_dic ={
            'uptime':uptime,
            'load1':load1,
            'load5':load5,
            'load15':load15,
            'status':status,
            'timestamp':timestamp,
        }
    return value_dic
