#!/usr/bin/env python
#coding:utf-8

import MySQLdb as mysqldb

def user_audit():
    conn = mysqldb.connect(host='localhost',user='root',passwd='meijin',db='monitor')    
    cur = conn.cursor()
    sql = 'select session_id from web_models_auditlog'
    cur.execute(sql)
    result = cur.fetchall()
    result = set(result)
    sessionId = [i[0] for i in result]
    msg = {'data':[]}
    for item in sessionId:
        sql = 'select id,user_id,host_id,cmd,date from web_models_auditlog where session_id={0} order by date'.format(10)
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
    print msg
user_audit()

