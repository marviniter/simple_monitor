#!/usr/bin/env python
#coding:utf-8
from django.shortcuts import render
import json
from django.shortcuts import render_to_response,HttpResponse,HttpResponseRedirect
from web_models import models
import datetime
import time
import random
from conn_helper import *  
from MonitorServer import settings
from django.contrib.auth.decorators import login_required
import MySQLdb as mysqldb

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import django.utils.timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            try:
                if django.utils.timezone.now() > user.userprofile.valid_begin_time and django.utils.timezone.now()  < user.userprofile.valid_end_time:
                    auth.login(request,user)
                    request.session.set_expiry(60*30)
                    request.session['auth'] = 'ok'
                    return render_to_response('master/layout.html',{'username':username})
                else:
                    return render(request,'login.html',{'login_err': 'User account is expired,please contact your IT guy for this!'})
            except ObjectDoesNotExist:
                    return render(request,'login.html',{'login_err': u'平台账户还未设定,请先登录后台管理界面创建平台账户!'})

        else:
            return render(request,'login.html',{'login_err': 'Wrong username or password!'})
    else:
        return render(request, 'login.html')
        

def host(request):
	if request.session.get('auth') == 'ok':
		obj_queryset = models.Hosts.objects.all()
		return render_to_response('host.html',{'data':obj_queryset,'webssh':settings.SHELLINABOX,})
	else:
		return render_to_response('login.html')
	

def user_audit(request):
    if request.session.get('auth') == 'ok':
		conn = mysqldb.connect(host='localhost',user='root',passwd='meijin',db='monitor')    
		cur = conn.cursor()
		sql = 'select session_id from web_models_auditlog'
		cur.execute(sql)
		result = cur.fetchall()
		result = set(result)
		sessionId = [i[0] for i in result]
		msg = {'data':[]}
		for item in sessionId:
			sql = 'select id,user_id,host_id,cmd,date from web_models_auditlog where session_id={0} order by date'.format(item)
			cur.execute(sql)
			result = cur.fetchall()
			for i in result:
				auditDict = {}
				sql = 'select name from web_models_userprofile where id={0}'.format(i[1])
				cur.execute(sql)
				username = cur.fetchall()
				sql = 'select hostname,ip_addr from web_models_hosts where id=%s' %i[2]
				cur.execute(sql)
				hostInfo = cur.fetchall()
				auditDict = {
					'id':i[0],
					'username':username[0][0],
					'hostname':hostInfo[0][0],
					'ip':hostInfo[0][1],
					'time':i[4],
					'cmd':i[3]
				}
				msg['data'].append(auditDict)
		return render_to_response('user_audit.html',msg)
    else:
		return render_to_response('login.html')

def user_group(request):
    if request.session.get('auth') == 'ok':
		obj_queryset = models.UserProfile.objects.all()
		conn = mysqldb.connect(host='localhost',user='root',passwd='meijin',db='monitor')    
		cur = conn.cursor()
		li = []
		for item in obj_queryset:
			sql = 'select name from web_models_department where id=%s' %item.department_id
			cur.execute(sql)
			departmentName = cur.fetchall()[0][0]
			dict = {
				'user':item.user,
				'department':departmentName,
				'create_time':item.valid_begin_time,
				'end_time':item.valid_end_time,
				'id':item.id,
			}
			li.append(dict)
		return render_to_response('user_group.html',{'data':li})
    else:
		return render_to_response('login.html')

    
#返回前端画图所用的数据
def memory(request,hostid):
    return render_to_response('memory.html',{'hostid':hostid})


def graphs_json(request,hostid):
	tmp_time = 0
	conn = mysqldb.connect(host='localhost',user='root',passwd='meijin',db='monitor')
	conn.autocommit(True)
	cur = conn.cursor()

	if tmp_time>0:
		sql = 'select clock,MemUsage from web_models_memory where clock>%s and host_id=%s' % (tmp_time,hostid)
	else:
		sql = 'select clock,MemUsage from web_models_memory where host_id=%s' %hostid
	cur.execute(sql)
	result = cur.fetchall()
	arr = []
	for i in result:
		arr.append([int(i[0])*1000,int(i[1])/1024])

	if len(arr)>0:
		tmp_time = arr[-1][0]

	return HttpResponse(json.dumps(arr))

	
def cpu(request,hostid):
	return render_to_response('cpu.html',{'hostid':hostid})
	
cpu_time = 0
def idle(request,hostid):
	conn = mysqldb.connect(host='localhost',user='root',passwd='meijin',db='monitor')
	conn.autocommit(True)
	cur = conn.cursor()
	
	global cpu_time
	if cpu_time>0:
		sql = 'select clock,idle from web_models_cpu where clock>%s and host_id=%s' % (cpu_time,hostid)
	else:
		sql = 'select clock,idle from web_models_cpu where host_id=%s' %hostid
	cur.execute(sql)
	result = cur.fetchall()
	arr = []
	for i in result:
		arr.append([int(i[0])*1000,float(i[1])])

	if len(arr)>0:
		cpu_time = arr[-1][0]
	return HttpResponse(json.dumps(arr))


class CJsonEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj,datetime):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self,obj)


