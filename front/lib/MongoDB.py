#coding=utf-8

from utils.Log import get_log
import pymongo
import os
import datetime

__all__ = ['init_db', 'get_db', 'get_label_db', 'MongoDB']

__DB__ = None

logger = get_log()

class MongoDB(object):
    def init(self, mongohost, dbname, collection):
        try:
            self.__mongohost = mongohost
            self.__dbname = dbname
            self.__collection = collection
            self._time_format = '%Y-%m-%d %H:%M:%S'
            return self.__connect()
        except Exception as e:
            print(str(e))
            return False

    def __connect(self):
        self.__conn = pymongo.MongoClient(self.__mongohost)
        self.__db = self.__conn[self.__dbname]
        self.__col = self.__db[self.__collection]
        return self.__check_connected()


    def __check_connected(self):
        try:
            if self.__conn:
                col_list = self.__db.list_collection_names()
                if len(col_list) > 0:
                    return True
                else:
                    self.__connect()
            else:
                self.__connect()
            return True
        except Exception as e:
            logger.error(str(e))
            return False

    def get_col(self):
        try:
            if not self.__check_connected():
                raise Exception("connect mongo db error")
            return self.__col
        except Exception as e:
            return False, str(e)

    def insert_one(self, data):
        try:
            if not self.__check_connected():
                raise Exception("connect mongo db error")
            ret_id = self.__col.insert_one(data).inserted_id
            if ret_id:
                return True, ret_id
        except Exception as e:
            return False, str(e)

    def find_one(self, data):
        try:
            if not self.__check_connected():
                raise Exception("connect mongo db error")
            ret_dict = self.__col.find_one(data)
            if ret_dict:
                return True, ret_dict
            else:
                raise Exception("get record error")
        except Exception as e:
            return False, str(e)

    def datetime2str(d_time):
        return datetime.datetime.strftime(d_time, self._time_format)

    def str2datetime(string):
        if string == '':
            return datetime.datetime(2019, 1, 1, 1, 1)
        return datetime.datetime.strptime(string, self._time_format)

    def find_latest(self):
        try:
            if not self.__check_connected():
                raise Exception("connect mongo db error")
            results = list(self.__col.find().sort('time', -1).limit(1))
            if len(results) > 0:
                return True, results
            else:
                raise Exception("get record error")
        except Exception as e:
            return False, str(e)

    def find_n_data(self, num_data, project, exclude=None):
        try:
            if not self.__check_connected():
                raise Exception("connect mongo db error")
            if project:
                results = [x for x in self.__col.find({'error': False, 'service_name': project}).sort('_id', -1).limit(num_data)]
            else:
                results = [x for x in self.__col.find({'error': False, 'service_name': {'$nin': [exclude, 'test']}, 'time': {'$gte': datetime.datetime.now() - datetime.timedelta(seconds=30)}}).sort('_id', -1).limit(num_data)]
            if len(results) > 0:
                return True, results
            else:
                raise Exception("get record error")
        except Exception as e:
            return False, str(e)

    def count_by_data(self, data):
        try:
            if not self.__check_connected():
                raise Exception("connect mongo db error")
            num_data = self.__col.find(data).count()
            if num_data > 0:
                return True, num_data
            else:
                raise Exception("cant find data")
        except Exception as e:
            return False, str(e)

def init_db(config):
    global __DB__
    if isinstance(__DB__, MongoDB):
        return True
    logger.info('its in init database')
    mongo_client = os.environ['MONGO_URI']
    dbname = config['db']['dbname']
    collection = config['db']['collection']
    __DB__ = MongoDB()
    SYN = __DB__.init(mongo_client, dbname, collection)
    if SYN:
        return True
    else:
        __DB__ = None
        return False

#  def get_db(config):
#      mongo_client = os.environ['MONGO_URI']
#      dbname = config['db']['dbname']
#      collection = config['db']['collection']
#      db = MongoDB()
#      SYN = db.init(mongo_client, dbname, collection)
#      if SYN:
#          return db
#      else:
        #  return False


def get_db():
    global __DB__
    if isinstance(__DB__, MongoDB):
        return __DB__
    else:
        return False


def get_label_db():
    mc_str = os.environ['AUDIO_DATA_FILTER_URI']
    mc = pymongo.MongoClient(mc_str)
    db = mc.audio_data_filter
    if len(db.list_collection_names()) > 0:
        col = db.label
        return col
    else:
        return False


