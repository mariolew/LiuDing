#coding=utf-8

import json
import uuid
import os
from utils.Config import get_config
from utils.Log import get_log
from utils.Tools import *
from flask import request, session, redirect, render_template, url_for
from utils.GetTime import *
from api import server
import random

import time
from multiprocessing import Process
import requests
import urllib
from lib.MongoDB import MongoDB
import base64
import numpy as np
import subprocess

logger = get_log()
config = get_config()
mongodb = MongoDB()
mongo_uri = "mongodb://{}:{}@{}:{}/resource".format(
config['mongodb']['username'],
config['mongodb']['password'],
config['mongodb']['host'],
config['mongodb']['port'])
mongodb.init(mongo_uri, "resource", "display")

@server.route('/index/display', methods=['POST'])
def IndexDisplay():
    if request.method == 'POST':
        status = 1
        try:
            account = request.cookies.get('account')
            info = {'ip': request.remote_addr, 'url': request.url, 'interface': "IndexDisplay", 'method': 'POST', 'account': account}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.info(info_str)
            num = int(request.values.get('num', 0))
            if num < 1:
                status = -10
                raise Exception('the num param error')
            col = mongodb.get_col()
            base64_imgs = []
            for i in col.find({'page': 'index',
                    'time': {"$gte": datetime.datetime(2019, 10, 22, 0, 0, 0)}},
                    sort=[('time', -1)]).limit(num):
                img = i['img']
                base64_imgs.append(base64.b64encode(img).decode('ascii'))
            return json.dumps({'status': status, 'imgs':base64_imgs}, ensure_ascii=False)
        except Exception as e:
            if status == 1:
                status = -10000
            info = {'interface': "IndexDisplay", 'message': str(e)}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.error(info_str)
            return json.dumps({'status': status, 'mes': str(e)})


@server.route('/', methods=['GET'])
@server.route('/index', methods=['GET'])
def Index():
    if request.method == 'GET':
        info = {'ip': request.remote_addr, 'url': request.url, 'interface': "Index", 'method': 'GET'}
        info_str = json.dumps(info, ensure_ascii=False)
        logger.info(info_str)
        main_js = url_for('static', filename='js/main.js')
        return render_template('index.html', main=main_js)
