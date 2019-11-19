# Name: get_time
# Function: get current system time
# Date: 2016-06-09
# Email: day9011@gmail.com
__author__ = 'day9011'
#coding=utf-8

import datetime
import time

def get_ct():
    t_format = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return t_format

def get_date():
    t_format = datetime.datetime.now().strftime("%Y-%m-%d")
    return str(t_format)
def get_expires():
    expires = datetime.datetime.now() + datetime.timedelta(hours=1)
    return expires

if __name__ == "__main__":
    print(get_ct())
    print(get_date())
