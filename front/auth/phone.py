#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import random


class PhoneVerify:
    def __init__(self, key_id, secret):
        self.client = AcsClient(key_id, secret, "cn-hangzhou")

    def send_code(self, phone_number):
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https') # https | http
        request.set_version('2017-05-25')
        request.set_action_name('QuerySendDetails')
        verify_code = self.make_verify_code()
        welcome_str = "欢迎使用柳丁教育系统电话验证，您这次的验证码为: {}".format(verify_code)
        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('PhoneNumber', phone_number)
        request.add_query_param('SendDate', welcome_str)
        request.add_query_param('PageSize', "1")
        request.add_query_param('CurrentPage', "1")

        response = self.client.do_action(request)
        # python2:  print(response) 
        print(str(response, encoding = 'utf-8'))
        return verify_code

    def make_verify_code(self):
        return str(random.randint(0, 999999)).zfill(6)
