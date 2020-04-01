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
id_mapping = {'Brands': 'BrandID', 'Transactions': 'TransactionID', 'Retailers': 'RetailerID',
              'Products': 'ProductID', 'ProductsForSale': 'ProductOfferingID'}


sys.path.insert(0, os.path.dirname(__file__))


def get_handler(query):
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
    curs = conn.cursor()

    try:
        table = query['table'][0]
        action = query['action'][0]
        if action == 'select':
            sql_q = f"SELECT * FROM {table}"
        elif action == 'insert':
            if 'v' not in query:
                return 'values missing'
            values = ','.join(f"\'{x}\'" for x in query['v'])
            sql_q = f"INSERT INTO {table} VALUES ({values})"
        elif action == 'delete':
            if 'id' not in query:
                return 'id missing'
            id_of_item = query['id'][0]
            sql_q = f"DELETE FROM {table} WHERE {id_mapping[table]} = {id_of_item}"
        elif action == 'update':
            if 'c' not in query or 'v' not in query or 'wc' not in query or 'wv' not in query:
                return 'parameter missing'
            columns = query['c']
            values = query['v']
            if len(columns) != len(values):
                return 'c and v in different length'
            sql_q = f"UPDATE {table} SET "
            sql_q += ', '.join([f"{c} = \'{v}\'" for c, v in zip(columns, values)])
            sql_q += f" WHERE {query['wc'][0]} = \'{query['wv'][0]}\'"
        curs.execute(sql_q)
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

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [body]
