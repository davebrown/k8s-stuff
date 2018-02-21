import sys
import os
from flask import Flask
import socket
import requests
import psycopg2
import logging

logfmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(stream=sys.stdout, format=logfmt, level=logging.DEBUG)
logger = logging.getLogger('counter')

DB_INFO = {
  'host': os.environ.get('DB_HOST', 'postgres'),
  'user': os.environ.get('DB_USER', 'dave'),
  'password': os.environ.get('DB_PASSWORD', ''),
  'db': os.environ.get('DB_NAME', 'counter')
}

logger.info('connecting to postgres: %s' % str(DB_INFO))
DB = psycopg2.connect("dbname='%s' password='%s' host='%s' user='%s'" % (DB_INFO['db'], DB_INFO['password'], DB_INFO['host'], DB_INFO['user']))
logger.info('connected to postgres: %s' % str(DB_INFO))

def close(obj):
  if obj is not None:
    obj.close()

def getAndIncr():
  cur = DB.cursor()
  try:
    cur.execute("SELECT counter FROM counter")
    rows = cur.fetchall()
    logger.debug('rows %s' % str(rows))
    ret = -1
    if len(rows) > 0:
      ret = rows[0][0]
    else:
      raise Exception('%d rows in counter table' % len(rows))
    cur.execute("UPDATE counter SET counter=%s", (ret + 1,))
    DB.commit()
    return ret
  except Exception as ex:
    logger.error(ex, exc_info=True)
    raise
  finally:
    close(cur)
    
app = Flask(__name__)

#@app.route('/users')
#def users():
  
@app.route('/counter')
def count():
    counter = getAndIncr()
    return '%d' % counter

@app.route("/")
def slash():
    counter = getAndIncr()

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Counter:</b> {counter}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), counter=counter)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8008)
