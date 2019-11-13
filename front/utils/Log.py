#coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import logging
import logging.handlers

__all__ = ['init_log', 'get_log']


_logger_ = None

class Logger():
    def __init__(self, log_path=None):
        self.logger = self.init_logger(log_path)

    def init_logger(self, log_path=None):
        logger = logging.root
        logger.setLevel(logging.INFO)
        print('init logger at path:{}'.format(log_path))

        if log_path != None:
            handler = logging.handlers.TimedRotatingFileHandler(log_path, 'D', 1, 7, 'utf-8')
            fmt = logging.Formatter("%(asctime)s %(levelname) 8s: [%(filename)s:%(lineno)d] [%(processName)s:%(process)d %(threadName)s] - %(message)s")
            handler.setFormatter(fmt)
            logger.addHandler(handler)
            logger.handlers = [handler]
            return logger
        else:
            fmt = logging.Formatter('%(asctime)s %(levelname) 8s: [%(filename)s:%(lineno)d] [%(processName)s:%(process)d %(threadName)s] - %(message)s')
            handler = logging.StreamHandler()
            handler.setFormatter(fmt)
            logger.addHandler(handler)
            logger.handlers = [handler]
            return logger


    def get_logger(self):
        return self.logger



def init_log(log_path=None):
    global _logger_
    _logger = Logger(log_path)
    _logger_ = _logger.get_logger()
    print(_logger_)
    _logger_.info('init logger')
    if not _logger_:
        return False
    else:
        return True

def get_log():
    global _logger_
    if _logger_ is not None:
        return _logger_
    else:
        print('error get logger')
        exit(1)

