import os
import sys
import pymysql

sys.path.insert(0, os.path.dirname(__file__))


hostname = "localhost"
username = "cs411sp20team25_team25"
password = "team25team25"
database = "cs411sp20team25_team25db"

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    message = 'It works! Team25!!!\n'
    version = 'Python %s\n' % sys.version.split()[0]
    #response = '\n'.join([message, version])

    db = pymysql.connect(host='localhost', user='cs411sp20team25_team25', passwd='team25team25', db='cs411sp20team25_team25db')
    curs = db.cursor()
    query = 'SELECT * FROM Brands'
    curs.execute(query)
    response = '\n'.join([str(d) for d in curs.fetchall()])
    print(response)
    db.close()
    #db_version = "Database version : %s " % data
    #db.close()

    #response = '\n'.join([message, version, db_version])

    return [response.encode()]
