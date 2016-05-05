#coding:utf-8

import MySQLdb as mysqldb


conn = mysqldb.connect(host='localhost',user='root',passwd='meijin',db='monitor')
conn.autocommit(True)
cur = conn.cursor()

#'IOWAIT','IDLE','LOAD'
sql = '''select iowait,idle,system,clock from web_models_cpu where host_id=%s''' %2
cur.execute(sql)
#print cur.fetchall()

sql = '''select MemTotal,MemUsage,Cached,MemFree,Buffers,SwapFree,SwapTotal,clock from web_models_memory where host_id=%s''' %2
cur.execute(sql)
data = cur.fetchall()
for item in data:
	print item
