from flask_restful import Resource
from flask import request, session, make_response
import os
import hashlib
from util.log import Logger
import json
from util.commonUtil import CommonUtil
import time

def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    # 如果是app接口，且不是支付回调，加密后返回
    Logger.log("请求id：%s 响应\n返回JSON：%s\n" % (session['requestId'], data))
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp


# 这个是Api基类，可以做统一处理
class BaseApi(Resource):
    def __init__(self):
        md5 = hashlib.md5()
        md5.update(os.urandom(24))
        session['requestId'] = md5.hexdigest()

        Logger.log(">>>>>>>>>>>>>>>>>>>>>>> 请求 请求id：%s >>>>>>>>>>>>>>>>>>>>>>>\n%s|%s|%s|%s|%s" % (session['requestId'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), request.environ['REMOTE_ADDR'], request.environ['REQUEST_METHOD'], request.url, request.get_data()))
        Resource.__init__(self)
