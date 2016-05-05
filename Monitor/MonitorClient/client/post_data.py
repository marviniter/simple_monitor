#coding:utf-8
import urllib
import httplib
import time
import json

#agent获取服务器相关的信息，并且定期发送给某一个URL进行处理。

def RequestUrl(host,port,source,params,timeout):
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

#如果自己写数据通过http发送给后台，使用json.dumps序列化或反序列化时，如果有单引号可能会产生错误	
server_info = {
	"hostname":'c1.puppet.com',
	"sn":"6cu345234Rs",
	"modify":1,
	"manufactory":"HP",
	"model":"ProLinat Gen8",
	"cpu_model":"Intel(R)CPU E5-2660",

	"ram":{
		"modify":1,
		"data":{
			"#1":{"manufactory":"HP","sn":"Test","capacity":17,"model":"DDR3"},
			"#2":{"manufactory":"HP","sn":"Test","capacity":17,"model":"DDR3"},
			"#3":{"manufactory":"HP","sn":"Test","capacity":17,"model":"DDR3"},
		}
		},
	"nic":{
		"modify":1,
		"data":{
			"eth1":{"macaddress":"38:EA:A7:CC:FF:89","ipaddress":"0.0.0.0","hardware":1,"netmask":"","model":"","network":""},
			"eth2":{"macaddress":"38:EA:A7:CC:FF:89","ipaddress":"0.0.0.0","hardware":1,"netmask":"","model":"","network":""},
			"eth3":{"macaddress":"38:EA:A7:CC:FF:89","ipaddress":"0.0.0.0","hardware":1,"netmask":"","model":"","network":""},	
		}
		},
	"physical_disk_driver":{
		"modify":1,
		"data":[
			{"iface_type":"SAS",},
			{"iface_type":"SAS",},
			{"iface_type":"SAS",},
			{"iface_type":"SAS",},
		]
		},

}


if __name__ == '__main__':
	while True:
		#RequestData = {'data':server_info}
		#RequestData = json.dumps(RequestData)
		#通过plugin获取硬件信息
		#将nic，disk组合成大字典
		#把大字典发送到api（api保存数据到数据库中）
		RequestData = urllib.urlencode({'data':server_info})
		
		#result为Agent发送数据之后，api返回的结果
		result = RequestUrl('192.168.204.130','8000','/api/handle_data/',RequestData,30,)
		print '=======The reuslt is %s========'%(result,)
		time.sleep(30)
