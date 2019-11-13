from flask import Flask
from hashlib import sha1
import os, sys
import time
import json

create_secret = lambda: sha1(bytes('%s%s' % (os.urandom(16), time.time()), encoding='utf-8')).hexdigest()
server = Flask(__name__)
random_secret = create_secret()
server.secret_key = random_secret

from utils.Config import get_config

config = get_config()

from utils.Log import get_log
logger = get_log()

from api.index import *
from auth.login import *
from auth.register import *
from api.course import *