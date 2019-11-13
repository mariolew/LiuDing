import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os
import multiprocessing

# worker config
workers = 10
#  workers= multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
worker_connections = 1000
threads = 2

bind = '0.0.0.0:9700'
daemon = 'false'
#pidfile = '/tmp/gunicorn.pid.ver'
#  access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
#  accesslog = '/tmp/gunicorn_access.log'
#  errorlog = '/tmp/gunicorn_error.log'
#  loglevel = 'info'

keepalive = 2
timeout = 60
max_requests = 1024
backlog = 65535
#  chdir = os.path.dirname(os.path.abspath(__file__))
