#_*_coding:utf-8_*_
__author__ = 'jieli'

import sys
basedir = '/'.join(__file__.split("/")[:-2])
sys.path.append(basedir)
from backend import main

if __name__ == '__main__':
    #sys.argv[1:]j为接收用户的参数
    main.call(sys.argv[1:])
