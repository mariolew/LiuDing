#coding=utf-8


import json
import uuid
import os
from utils.Config import get_config
from utils.Log import get_log
from api import server
from hashlib import md5
import datetime
from urllib import parse
import json
import requests
from flask import request, session, redirect, render_template, url_for
from lib.MysqlDB import *


logger = get_log()
config = get_config()
db = MysqlDB()

@server.route('/register', methods=['GET', 'POST'])
def Register():
    status = 1
    try:
        if request.method == 'GET':
            info = {'ip': request.remote_addr, 'url': request.url, 'interface': "Register", 'method': 'GET'}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.info(info_str)
            auth_js = url_for('static', filename='js/auth.js')
            main_js = url_for('static', filename='js/main.js')
            return render_template('register.html', main=main_js, auth=auth_js)
        elif request.method == 'POST':
            info = {'ip': request.remote_addr, 'url': request.url, 'interface': "Register", 'method': 'POST'}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.info(info_str)
            name = request.values.get('name', None)
            account = request.values.get('account', None)
            password = request.values.get('password', None)
            sex = request.values.get('sex', None) # 1 for male, 2 for female
            age = request.values.get('age', None)
            school = request.values.get('school', None)
            email = request.values.get('email', None)
            parent = request.values.get('parent', None)
            relation = request.values.get('relation', None)
            tel = request.values.get('tel', None)
            parent_tel = request.values.get('parent_tel', None)
            params = {
                'name': name,
                'account': account,
                'password': password,
                'sex': sex,
                'age': age,
                'school': school,
                'email': email,
                'parent': parent,
                'relation': relation,
                'tel': tel,
                'parent_tel': parent_tel
            }
            info = {'interface': "Register", 'params': params}
            info_str = json.dumps(info, ensure_ascii=False)
            logger.info(info_str)
            if db.verify_student_account(account) > 0:
                status = -201
                raise Exception('account {} is exist'.format(account))

            # insert information
            sql_command = """INSERT INTO student (name,tel,sex,age,school,email,parent_name,relation,parent_tel) \
                VALUES ('{}', '{}', '{}', '{}', {}, {}, '{}', '{}', '{}')""".format(
                    name, tel, int(sex), int(age), school, email, parent, int(relation), parent_tel)
            db.execute(sql_command)

            # get the id of the student
            sql_command = """SELECT id FROM student WHERE student.parent_tel='{}'""".format(parent_tel)
            results = db.query(sql_command)
            _id = int(results[0][0])

            # insert account into table
            sql_command = """INSERT INTO account (id, account, password) VALUES({}, '{}', '{}')""".format(_id, account, password)
            db.execute(sql_command)
            return json.dumps({'status': status, 'mes': "{} register successfully".format(name)}, ensure_ascii=False)
    except Exception as e:
        if status == 1:
            status = -10000
        info = {'interface': "Register", 'message': str(e)}
        info_str = json.dumps(info, ensure_ascii=False)
        logger.error(info_str)
        return json.dumps({'status': status, 'mes': str(e)})
