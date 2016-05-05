#!/usr/bin/env python
#coding:utf-8
from django.shortcuts import render,HttpResponse
from web_models import models
import json
import MySQLdb as mysqldb
# Create your views here.
'''
通过url api/get_config?hostname=c1.puppet.com来访问
'''

def get_config(request):
    ret = {'status':0,'data':'','message':''}
    try:
        data = {}
        hostname = request.GET.get('hostname',None)
        if not hostname:
            return HttpResponse(json.dumps(ret))
        hostObj = models.Hosts.objects.get(hostname=hostname)
        hostname = hostObj.hostname
        host_group = hostObj.group
        
        #获取主机组对应的服务模板
        service_templates = host_group.service_template.all()
        for item in service_templates:
            temp = {}
            temp['last_time'] = 0
            temp['interval'] = item.check_interval
            temp['plugin_name'] = item.service.plugin
            temp['element'] = {}
            
            #取所有的阀值
            for cond in item.conditions.all():
                item_key = cond.item.key
                if temp['element'].has_key(item_key):
                    temp['element'][item_key].append({'formula':cond.formula.key,'operator':cond.operator.key,'threshold':cond.threshold})
                else:
                    temp['element'][item_key] = [{'formula':cond.formula.key,'operator':cond.operator.key,'threshold':cond.threshold}]
            data[item.key] = temp
            data['hostid'] = hostObj.id
            ret['data'] = data
            ret['status'] = 1
    except Exception,e:
        ret['message'] = e.message
    
    return HttpResponse(json.dumps(ret))

def handle_data(request):
	data = request.POST
	conn = mysqldb.connect(host='localhost',user='root',passwd='meijin',db='monitor')
	conn.autocommit(True)
	cur = conn.cursor()
	for tup in data.items():
		value = tup[0]
		value = json.loads(value)
		if 'cpu' in value.keys():
			cpuData = value['cpu']
			sql = '''insert into web_models_cpu (host_id,nice,system,iowait,steal,idle,clock) values (%s,%s,%s,%s,%s,%s,%s)''' %(value['hostid'],cpuData['nice'],cpuData['system'],cpuData['iowait'],cpuData['steal'],cpuData['idle'],cpuData['timestamp'])
			cur.execute(sql)
		elif 'memory' in value.keys():
			memData = value['memory']
			sql = '''insert into web_models_memory (host_id,MemTotal,MemUsage,Cached,MemFree,Buffers,SwapFree,SwapTotal,clock) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)''' %(value['hostid'],memData['MemTotal'],memData['MemUsage'],memData['Cached'],memData['MemFree'],memData['Buffers'],memData['SwapUsage'],memData['SwapTotal'],memData['timestamp'])
			cur.execute(sql)
	conn.close()
	return HttpResponse('True') 
