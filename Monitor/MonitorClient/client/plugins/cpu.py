#!/usr/bin/env python
#_*_coding:utf-8_*_

import commands
import time

def monitor(frist_invoke=1):
    shell_command = 'sar 1 3 |grep "^Average:"'
    timestamp = int(time.time())
    status,result = commands.getstatusoutput(shell_command)
    if status !=0:
        value_dic ={'status':status}
    else:
        value_dic = {}
        user,nice,system,iowait,steal,idle = result.split()[2:]
        value_dic = {
            'user':user,
            'nice':nice,
            'system':system,
            'iowait':iowait,
            'steal':steal,
            'idle':idle,
            'status':status,
            'timestamp':timestamp,
         }
    return value_dic
        
        
        
        


