from flask_restful import reqparse
from flask import request
from util.commonUtil import CommonUtil
from resources.baseApi import BaseApi
from util.validImage import ValidImage
from util.redis import Redis
import hashlib
from util.log import Logger
from libs.qcloud_cos.cos_cred import CredInfo
from libs.qcloud_cos.cos_auth import Auth
import time
from util.checkUtil import CheckUtil


# 生成验证码图片
class ValidImageCreate(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type')
        args = parser.parse_args()

        usage = ''
        if args.type is None:
            return CommonUtil.json_response(-1, '缺少参数:type')
        elif args.type == '0':
            usage = 'regAccount'  # 注册账号
        elif args.type == '1':
            usage = 'findPassword'  # 找回密码
        elif args.type == '2':
            usage = 'adminLogin'  # 管理台登录
        else:
            return CommonUtil.json_response(-1, 'type参数格式错误')

        # 用客户端ip来作为sendId是为了使频繁请求时可以替换这个key下面原来的验证码
        md5 = hashlib.md5()
        md5.update("validimage_{}_{}".format(request.environ['REMOTE_ADDR'], usage).encode('utf-8'))
        sendId = md5.hexdigest()
        validImage = ValidImage.create()

        Redis.setex(sendId, 60, validImage['code'])

        data = {
            "img": validImage['img'],
            "sendId": sendId
        }

        Logger.log("生成图片验证码 ip:{} sendId:{} code:{}".format(request.environ['REMOTE_ADDR'], sendId, validImage['code']))

        return CommonUtil.json_response(0, "success", data)


# 生成腾讯云cos的多次签名
class QCloudCosSign(BaseApi):
    def get(self):
        return self.handle()

    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_merchant_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        cred = CredInfo(1252137158, u'密钥', u'密钥')
        auth_obj = Auth(cred)
        sign_str = auth_obj.sign_more(u'bucket', u'/文件夹/', int(time.time()) + 60)
        return CommonUtil.json_response(0, '获取成功', {
            'sign': sign_str
        })