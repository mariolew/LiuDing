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
ResourceDB = MongoDB()
ResourceDB.init("mongodb://day9011:5673914@121.40.82.87:15001", "resource", "display")


def get_personal_info(name):
    return name

@server.route('/personal/info/<name>', methods=['GET'])
def PersonalInfo(name):
    if request.method == 'GET':
        status = 1
        try:
            info = {'ip': request.remote_addr, 'url': request.url, 'interface': "PersonalInfo"}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.info(info_str)
            info = get_personal_info(name)
            return {'status': status, 'info': info}
        # else:
        #     return "not login"
        except Exception as e:
            if status == 1:
                status = -10000
            info = {'interface': "PersonalInfo", 'message': str(e)}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.error(info_str)
            return json.dumps({'status': status, 'mes': str(e)})

@server.route('/personal/course/info/<name>', methods=['GET'])
def PersonalCourseInfo(name):
    if request.method == 'GET':
        status = 1
        try:
            info = {'ip': request.remote_addr, 'url': request.url, 'interface': "PersonalInfo"}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.info(info_str)
            info = get_personal_info(name)
            return {'status': status, 'info': info}
        # else:
        #     return "not login"
        except Exception as e:
            if status == 1:
                status = -10000
            info = {'interface': "PersonalCourseInfo", 'message': str(e)}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.error(info_str)
            return json.dumps({'status': status, 'mes': str(e)})

@server.route('/personal/course/schedule/<name>', methods=['GET'])
def PersonalCourseSchedule(name):
    if request.method == 'GET':
        status = 1
        try:
            info = {'ip': request.remote_addr, 'url': request.url, 'interface': "PersonalInfo"}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.info(info_str)
            info = get_personal_info(name)
            return {'status': status, 'info': info}
        # else:
        #     return "not login"
        except Exception as e:
            if status == 1:
                status = -10000
            info = {'interface': "PersonalCourseSchedule", 'message': str(e)}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.error(info_str)
            return json.dumps({'status': status, 'mes': str(e)})