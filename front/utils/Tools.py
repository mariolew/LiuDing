#coding=utf-8

import sys
import json
import os
import zipfile
import re
import pymongo

def zip_dir(dirname, zipfilename):
    file_list = []
    if os.path.isfile(dirname):
        file_list.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                file_list.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in file_list:
        arcname = tar[len(dirname):]
        zf.write(tar, arcname)
    zf.close()

def get_word_list(filename):
    ret_list = []
    for line in open(filename, 'rt'):
        items = re.split(r'\s', line.strip())
        word = items[0]
        ret_list.append(word)
    return ret_list

def get_wav_dict(filename):
    ret_dict = {}
    for line in open(filename, 'rt'):
        items = re.split(r'\s', line.strip())
        uttid = items[0]
        wav = items[1]
        ret_dict[uttid] = wav
    return ret_dict


def get_text_dict(filename):
    ret_dict = {}
    for line in open(filename, 'rt'):
        items = re.split(r'\s', line.strip())
        uttid = items[0]
        text = ' '.join(items[1:])
        ret_dict[uttid] = text
    return ret_dict

def porn_stat():
    mc = pymongo.MongoClient(os.environ['MONGO_URI'])
    db = mc.porn
    col = db.label
    uttids = {}
    print("***********************************************", file=sys.stderr)
    for i in col.find():
        uttid = i["uttid"]
        label = i['label']
        if uttid in uttids:
            if label != uttids[uttid]['label']:
                print(i, file=sys.stderr)
                print(uttids[uttid], file=sys.stderr)
                print("***********************************************", file=sys.stderr)
        else:
            uttids[uttid] = {}
            uttids[uttid].update(i)
    num_true = 0
    for k,v in uttids.items():
        if v['label'] == '1':
            num_true += 1
    num_uttids = len(uttids)
    print("true: {}, total: {}, ratio: {}".format(num_true, num_uttids, num_true / num_uttids), file=sys.stderr)
