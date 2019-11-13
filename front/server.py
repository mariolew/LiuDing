__author__ = 'dinghanyu'
#coding=utf-8


import os
#  from utils.Initialize import initialize
from utils.Config import *
from utils.Log import *
import json



#  initialize config, logger and model
#  initialize('config/my.conf')
if not init_config('config/my.conf'):
    print('init configuration error')
    exit(1)
config = get_config()
if not init_log():
    print('init logger error')
    exit(1)
logger = get_log()
info_json = {'init': 'finish'}
info = json.dumps(info_json)
logger.info(info)

from api import server
server.debug = False

if __name__ == '__main__':
    port = int(config['server']['port'])
    host = '0.0.0.0' if 'host' not in config['server'] else config['server']['host']
    server.run(host=host, port=port)
