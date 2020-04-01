from urllib.parse import unquote, parse_qs

import imp
import os
import sys
import json
import pymysql

host = 'localhost'
user = 'cs411sp20team25_team25'
passwd = 'team25team25'
db = 'cs411sp20team25_team25db'
actions = ['select', 'delete', 'update', 'insert']


sys.path.insert(0, os.path.dirname(__file__))


def get_handler(query):
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
    curs = conn.cursor()

    try:
        if query['action'][0] == 'select':
            curs.execute(f"SELECT * FROM {query['table'][0]}")

        response = json.dumps([[str(v) for v in r] for r in curs.fetchall()])
        conn.commit()
    except Exception as e:
        response = f'query error {str(e)}'

    conn.close()
    return response.encode()


def application(environ, start_response):
    body = 'Hello world!'
    if environ['QUERY_STRING']:
        query = parse_qs(environ['QUERY_STRING'])
        if 'action' in query and query['action'][0] in actions:
            body = get_handler(query)
        else:
            body = 'invalid action'
        #body = json.dumps(query['action'])

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [body]
