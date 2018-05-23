"""
这里封装了一些常用的方法
"""
import hashlib
import time
import base64
from Crypto.Cipher import AES
from config.config import Config
import json
from util.safedict import SafeDict
from flask_restful import reqparse
from util.log import Logger
from flask import session
import random


class CommonUtil:
    # 返回json数据
    @classmethod
    def json_response(cls, code, msg, data={}):
        res = {
            "code": code,
            "message": msg,
            "data": data
        }
        return res

    # python3.6比如md5经常提示参数类型不对
    @classmethod
    def utf8str(cls, arg):
        ret = "{}".format(arg).encode('utf-8').decode()
        if ret != "{}":
            return ret
        else:
            raise AssertionError('convert {} to utf-8 error'.format(arg))

    # md5
    @classmethod
    def md5(cls, arg):
        obj = hashlib.md5()
        obj.update(cls.utf8str(arg).encode('utf-8'))
        return obj.hexdigest()

    @classmethod
    def random_id(cls):
        return random.randint(1000000000, 1999999999)

    # 创建管理员token
    @classmethod
    def create_admin_token(cls, value):
        return cls.md5('admin_'+ value + str(time.time()))

    # 创建用户token
    @classmethod
    def create_user_token(cls, value):
        return cls.md5('user_' + value + str(time.time()))

    # 用户密码
    @classmethod
    def create_user_password(cls, username, password):
        return cls.md5(username + password + '_pwd')

    # 时间戳转时间
    @classmethod
    def timestamp_to_time(cls, value):
        time_local = time.localtime(value)
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        if time_str:
            return time_str
        else:
            return ''

    # 时间转时间戳
    @classmethod
    def time_to_timestamp(cls, value, formatter="%Y-%m-%d %H:%M:%S"):
        time_local = time.strptime(value, formatter)
        return int(time.mktime(time_local))

    # 14位格式化无符号时间
    @classmethod
    def time_format_str(cls):
        return time.strftime('%Y%m%d%H%M%S', time.localtime())

    @classmethod
    def sql_result_to_json(cls, result):
        if type(result) is dict:
            return result._asdict()
        else:
            arr = []
            for item in result:
                arr.append(item._asdict())
            return arr

