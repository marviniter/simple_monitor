#!/usr/bin/env python
#_*_coding:utf-8_*_

import time
import json
from plugins import plugin_api
import httplib,urllib2
import os

def requestUrl(host,port,source,params,timeout):
	headers = {'Content-type':'application/x-www-form-urlencoded','Accept':'text/plain'}
	try:	
		conn = httplib.HTTPConnection(host,port,timeout)
		conn.request('POST',source,params,headers)
		response = conn.getresponse()
		
		#读取到的返回值
		original = response.read()
		print original
	except Exception,e:
		raise e
	return original

def getHostName():
	system = os.name
	if system == 'nt':
		hostname = os.getenv('computername')
		return hostname
	elif system == 'posix':
		host = os.popen('hostname')
		try:
			hostname = host.read().strip('\n')
			return hostname
		finally:
			host.close()
	else:
		return 'Unknow hostname'

		
def getConfig(hostname):
	url = 'http://192.168.204.15:1000/api/get_config/?hostname=%s' %hostname
	print url
	response = urllib2.urlopen(url)
	result = json.load(response)

	config = result['data']
	return config

def handleData(config,hostid):
	for key,value in config.items():
		message = {}
		currenttime,interval,lasttime = time.time(),value['interval'],value['last_time']
		if (currenttime-lasttime) < interval:
			pass
		else:
			plugin_name = value['plugin_name']
			func = getattr(plugin_api,plugin_name)
			data = func()
			#更新最新执行的时间
			config[key]['last_time'] = currenttime
			#发送收集的信息
			message[key] = data
			message['hostid'] = hostid
			message = json.dumps(message)
			print '---------------------------------------------------------'
			print '监控信息: '+message
			result = requestUrl('192.168.204.15',1000,'/api/handle_data/',message,30)
			print '数据上传的状态：'+result	
			
if __name__ == '__main__':
	hostname = getHostName()
	config = getConfig(hostname)
	hostid = config['hostid']
	del config['hostid']
	while True:
		handleData(config,hostid)
