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
from lib.MysqlDB import *

logger = get_log()
config = get_config()
CourseDB = MongoDB()
CourseDB.init("mongodb://day9011:5673914@121.40.82.87:15001", "course", "signup")
db = MysqlDB()

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
            if 'account' in session:
                info = {'ip': request.remote_addr, 'url': request.url, 'interface': "CourseIndex"}
                info_str = json.dumps(info, ensure_ascii=False)
                logger.info(info_str)
                main_js = url_for('static', filename='js/main.js')
                return render_template('course.html', main=main_js)
            else:
                return redirect('/')
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
            if 'account' in session:
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
                CourseDB.insert_one(insert_dict)
                return json.dumps({'status': status, 'mes': 'OK'})
            else:
                return json.dumps({'status': status, 'mes': "not login"})
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
            if 'account' in session:
                info = {'ip': request.remote_addr, 'url': request.url, 'interface': "CourseQuery"}
                info_str = json.dumps(info, ensure_ascii=False)
                logger.info(info_str)
                sql_command = "SELECT * FROM course, teacher WHERE course.tid=teacher.id"
                courses = db.query(sql_command)
                courses = [parse_course(x) for x in courses]
                courses = sort_courses(courses)
                return json.dumps({'status': status, 'courses': courses}, ensure_ascii=False)
            else:
                return json.dumps({'status': status, 'mes': "not login"})
        except Exception as e:
            info = {'interface': "CourseQuery", 'message': str(e)}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.error(info_str)
            return json.dumps({'status': status, 'mes': str(e)})
