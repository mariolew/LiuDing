#coding=utf-8
import os, sys
import time
from hashlib import sha1
import pymongo
import json
from utils.Log import *

if __name__ != '__main__':
    logger = get_log()
else:
    init_log()
    logger = get_log()

__all__ = ['get_token', 'get_fanti_project']

__token__ = None
c_time = time.time()

#  def get_token():
#      global token
#      return token

def get_db_token():
    uri = os.environ['TOKEN_URI']
    mc = pymongo.MongoClient(uri)
    db = mc['voice_config']
    col = db['token']
    ret_token = {}
    for item in col.find():
        ret_token[item['token']] = item['project']
    return ret_token

def get_num_token():
    uri = os.environ['TOKEN_URI']
    mc = pymongo.MongoClient(uri)
    db = mc['voice_config']
    col = db['token']
    return int(col.estimated_document_count())

def get_token():
    global __token__, c_time
    now_time = time.time()
    if __token__ is None:
        __token__ = get_db_token()
        info_json = {'token': 'init token, the number of tokens:{}'.format(len(__token__))}
        info = json.dumps(info_json)
        logger.info(info)
    if now_time - c_time > 120:
        num_db_token = get_num_token()
        if num_db_token != len(__token__):
            num_origin = len(__token__)
            __token__ = get_db_token()
            info_json = {'token': 'change token, the number of origin tokens:{}, the number of db tokens: {}'.format(num_origin, num_db_token)}
            info = json.dumps(info_json)
            logger.info(info)
        c_time = now_time
    return __token__

def gen_token():
    create_secret = lambda: sha1(bytes('%s%s' % (os.urandom(16), time.time()), encoding='utf-8')).hexdigest()
    ret_token = create_secret()
    return ret_token.lower()

def add_new_token(filepath):
    lines = open(filepath, 'rt').readlines()
    project_names = [ x.strip() for x in lines if x.strip() != '']
    print(project_names)
    tokens = get_token()
    print(dict((v,k) for k,v in tokens.items()))
    online_projects = []
    online_tokens = []
    uri = os.environ['TOKEN_URI']
    mc = pymongo.MongoClient(uri)
    db = mc['voice_config']
    col = db['token']
    for k, v in tokens.items():
        online_projects.append(v)
        online_tokens.append(k)
    #  print(online_projects)
    #  print(online_tokens)
    #  print(len(online_projects))
    #  print(len(online_tokens))
    for project in project_names:
        if project not in online_projects:
            token = gen_token()
            while token in online_tokens:
                token = gen_token()
            col.insert_one({'project': project, 'token': token})
            logger.info('add new token:{}'.format(json.dumps({'project': project, 'token': token})))
    logger.info('finish make token')


if __name__ == '__main__':
    if len(sys.argv) != 1 and len(sys.argv) != 2:
        print("Usage: python {} [<project_name_file>]".format(sys.argv[0]))
        exit(1)
    if len(sys.argv) == 1:
        create_secret = lambda: sha1(bytes('%s%s' % (os.urandom(16), time.time()), encoding='utf-8')).hexdigest()
        token = create_secret()
        print(token)
    else:
        add_new_token(sys.argv[1])

