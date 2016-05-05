#!/usr/bin/env python
#coding:utf-8
import commands
import time

def monitor(frist_invoke=1):
    monitor_dic = {
        'SwapUsage': 'percentage',
    }
    shell_command ="grep 'MemTotal\|MemFree\|Buffers\|^Cached\|SwapTotal\|SwapFree' /proc/meminfo"
    timestamp = int(time.time())

    status,result = commands.getstatusoutput(shell_command)
    if status != 0: #cmd exec error
        value_dic = {'status':status}
    else:
        value_dic = {'status':status}
        for i in result.split('kB\n'):
            key= i.split()[0].strip(':') # factor name
            value = i.split()[1]   # factor value
            value_dic[ key] =  value

        value_dic['SwapUsage'] = int(value_dic['SwapTotal']) - int(value_dic['SwapFree'])

        MemUsage = int(value_dic['MemTotal']) - (int(value_dic['MemFree']) + int(value_dic['Buffers']) + int(value_dic['Cached']))

        value_dic['MemUsage'] = MemUsage
    value_dic['timestamp'] = timestamp
    return value_dic

if __name__ == "__main__":
    print monitor()
