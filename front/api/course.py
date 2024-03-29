#coding=utf-8

import json
import uuid
import os
from utils.Config import get_config
from utils.Log import get_log
from utils.Tools import *
from flask import request, session, redirect, render_template, url_for, make_response
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
from lib.MysqlDB import *

logger = get_log()
config = get_config()
mongodb = MongoDB()
mongo_uri = "mongodb://{}:{}@{}:{}/resource".format(
config['mongodb']['username'],
config['mongodb']['password'],
config['mongodb']['host'],
config['mongodb']['port'])
mongodb.init(mongo_uri, "resource", "display")

mysqldb = MysqlDB(host=config['mysqldb']['host'],
                username=config['mysqldb']['username'],
                password=config['mysqldb']['password'],
                dbname=config['mysqldb']['dbname'])

course_dict = {
    0: "math",
    1: "chinese",
    2: "english"
}

time_dict = {
    0: "morning",
    1: "afternoon",
    2: "evening"
}

def parse_course(course):
    course_info = {
        'subject' : course_dict[course[1]],
        'fee'     : course[2],
        'term'    : course[3],
        'time'    : time_dict[course[4]],
        'class'   : course[5],
        'classroom': course[6],
        'grade'   : course[8],
        'date'    : course[9].strip().split(','),
        'teacher' : course[11].strip()
    }
    return course_info

def sort_courses(courses):
    courses = sorted(courses, key=lambda x: x['grade'])
    courses = sorted(courses, key=lambda x: x['term'])
    return courses


@server.route('/course', methods=['GET'])
def CourseIndex():
    if request.method == 'GET':
        status = 1
        try:
            account = request.cookies.get('account')
            if 'account' in session and session['account'] == account:
                info = {'ip': request.remote_addr, 'url': request.url, 'interface': "CourseIndex"}
                info_str = json.dumps(info, ensure_ascii=False)
                logger.info(info_str)
                main_js = url_for('static', filename='js/main.js')
                content = render_template('course.html', main=main_js)
            else:
                content = redirect('/')
            resp = make_response(content)
            if not ('account' in session and session['account'] == account):
                try:
                    resp.delete_cookie('account')
                    resp.delete_cookie('token')
                    resp.delete_cookie('name')
                except:
                    pass
            return resp
        except Exception as e:
            if status == 1:
                status = -10000
            info = {'interface': "CourseIndex", 'message': str(e)}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.error(info_str)
            return json.dumps({'status': status, 'mes': str(e)})

@server.route('/course/signup', methods=['POST'])
def CourseSignup():
    if request.method == 'POST':
        status = 1
        try:
            account = request.cookies.get('account')
            if 'account' in session and session['account'] == account:
                info = {'ip': request.remote_addr, 'url': request.url, 'interface': "CourseSignup"}
                info_str = json.dumps(info, ensure_ascii=False)
                logger.info(info_str)
                _id = request.values.get('id', None)
                subject = request.values.get('subject', None)
                term = request.values.get('term', None)
                time = request.values.get('time', None)
                grade = request.values.get('grade', None)
                insert_dict = {
                    '_id': int(_id),
                    'subject': subject,
                    'term': term,
                    'time': time,
                    'grade': int(grade),
                    'signup_time': datetime.datetime.now()
                }
                mongodb.insert_one(insert_dict)
                ret_str = json.dumps({'status': status, 'mes': 'OK'})
            else:
                ret_str = json.dumps({'status': status, 'mes': "not login"})
            
            if not ('account' in session and session['account'] == account):
                try:
                    resp.delete_cookie('account')
                    resp.delete_cookie('token')
                    resp.delete_cookie('name')
                except:
                    pass
            return ret_str
        except Exception as e:
            if status == 1:
                status = -10000
            info = {'interface': "CourseSignup", 'message': str(e)}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.error(info_str)
            return json.dumps({'status': status, 'mes': str(e)})


@server.route('/course/query', methods=['GET'])
def CourseQuery():
    if request.method == 'GET':
        status = 1
        try:
            account = request.cookies.get('account')
            if 'account' in session and session['account'] == account:
                info = {'ip': request.remote_addr, 'url': request.url, 'interface': "CourseQuery"}
                info_str = json.dumps(info, ensure_ascii=False)
                logger.info(info_str)
                sql_command = "SELECT * FROM course, teacher WHERE course.tid=teacher.id"
                courses = mysqldb.query(sql_command)
                courses = [parse_course(x) for x in courses]
                courses = sort_courses(courses)
                ret_str = json.dumps({'status': status, 'courses': courses}, ensure_ascii=False)
            else:
                ret_str = json.dumps({'status': status, 'mes': "not login"})
            
            if not ('account' in session and session['account'] == account):
                try:
                    resp.delete_cookie('account')
                    resp.delete_cookie('token')
                    resp.delete_cookie('name')
                except:
                    pass
            return ret_str
        except Exception as e:
            info = {'interface': "CourseQuery", 'message': str(e)}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.error(info_str)
            return json.dumps({'status': status, 'mes': str(e)})
