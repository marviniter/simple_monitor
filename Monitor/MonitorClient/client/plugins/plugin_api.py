#!/usr/bin/env python
#_*_coding:utf-8_*_

import load,cpu,memory

def LinuxLoad():
    return load.monitor()

def LinuxCpu():
    return cpu.monitor()

def LinuxMemory():
    return memory.monitor()
