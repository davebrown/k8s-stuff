#!/usr/bin/env python

import sys
import os
import requests
import socket
from socket import AF_INET, SOCK_STREAM
import traceback
from flask import Flask, request
import logging
import netifaces

logfmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(stream=sys.stdout, format=logfmt, level=logging.DEBUG)
log = logging.getLogger('netcheck')

# connect timeout
socket.setdefaulttimeout(5.0)

app = Flask(__name__)

def close(obj):
  if obj is not None:
    obj.close()

from netifaces import interfaces, ifaddresses

def ip4_addresses():
  ip_list = []
  for interface in interfaces():
    #print 'interface', interface
    addresses = ifaddresses(interface)
    if addresses.get(netifaces.AF_INET, None) is None:
      continue
    for link in addresses[netifaces.AF_INET]:
      #print '  link', link
      ip_list.append(link['addr'])
  return ip_list
  
def connect(host, port):
  s = socket.socket(AF_INET, SOCK_STREAM)
  try:
    s.connect((host, port))
    return True
  finally:
    close(s)
  return False

@app.route('/')
def slash():
  print 'request args', request.args
  connResult = ''
  hp = request.args.get('hostport', None)
  if hp:
    if ':' not in hp:
      connResult = '<span style="color: red;"><b>ERROR: specify connect as &lt;host&gt;:&lt;port&gt;</b></span>'
    else:
      try:
        host, port = hp.split(':')
        port = int(port)
        host = host.strip()
        log.info('connecting to "%s":%d' % (host, port))
        ret = connect(host, port)
        connResult = '<span style="color: green;"><b>connect "%s":%d SUCCESS!</b></span>' % (host, port)
      except Exception as ex:
        log.exception('exception happened: %s' % (ex))
        traceback.print_exc()
        connResult = '<pre style="color: red;"><b>ERROR:</b> connect to "%s":%d failed: %s\n-----\n%s</pre>' % (host, port, str(ex), traceback.format_exc())
        
        
  html = """
<html><head><title>netcheck</title></head><body>
<b>hostname:</b> {hostname}<br/>
<b>local addresses:</b>
<ul>
{addresses}</ul>
<hr/>
{connResult}
<form target="/">
check connect <b>&lt;host&gt;:&lt;port&gt;</b> <input name="hostport" size="20" value="{hp}"/> <input type="submit" value="Check"/>
</body></html>
"""
  addresses = ''
  ips = ip4_addresses()
  for ip in ips:
    addresses += '<li>%s</li>\n' % ip

  return html.format(hostname=socket.gethostname(), addresses=addresses, connResult=connResult, hp=hp)

def test():
  HOSTS = ['localhost', '127.0.0.1', 'google.com']
  try:
    log.info('local socket: %s', socket.gethostname())
    log.info('local IPv4 addresses: %s', str(ip4_addresses()))
    for h in HOSTS:
      log.info('socket.gethostbyname(%s)->%s' % (h, socket.gethostbyname(h)))
    ret = connect('192.168.1.1', 80)
    log.info('connect returned %s' % str(ret))
  except Exception as ex:
    log.exception('exception happened: %s' % (ex))
    traceback.print_exc()
  print '-----', slash()

    
if __name__ == '__main__':
  port = int( os.environ.get('NETCHECK_SERVICE_PORT', '8080') )
  log.info('starting netcheck service on port %d' % port)
  app.run(host='0.0.0.0', port=port)
  #test()

