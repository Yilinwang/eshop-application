from urllib.parse import unquote

import imp
import os
import sys
import json
import pymysql


sys.path.insert(0, os.path.dirname(__file__))

def application(environ, start_response):
    body = 'Hello world!\n'
    if environ['QUERY_STRING']:
        sql_q = environ['QUERY_STRING'].strip().split('=')[1]
        db = pymysql.connect(host='localhost', user='cs411sp20team25_team25', passwd='team25team25', db='cs411sp20team25_team25db')
        curs = db.cursor()
        try:
            curs.execute(unquote(sql_q))
            response = json.dumps([str(d) for d in curs.fetchall()])
        except:
            response = 'query error'
        db.close()
        body = response.encode()

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [body]
