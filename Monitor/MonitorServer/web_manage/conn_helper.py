#!/usr/bin/env python
#coding:utf-8

import MySQLdb as mysql

def conn_db(dbname,sql):
    conn = mysql.connect(host='localhost',db=dbname,user='root',passwd='meijin')
    conn.autocommit(True)
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    return result






