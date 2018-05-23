from util.redis import Redis
from util.db import DB
from model.response import Response
from table.model import Merchant
from util.commonUtil import CommonUtil
from flask import request

class CheckUtil:
    # 效验图片验证码
    @classmethod
    def check_valid_image(cls, valid_id, valid_value):
        code = Redis.get(valid_id)

        if code is None:
            return Response(-1, '验证码不存在')
        elif code != valid_value:
            return Response(-1, '验证码错误')
        else:
            Redis.delete(valid_id)
            return Response()

            # 效验token

    @classmethod
    def check_merchant_token(cls, token):
        if token is None:
            return Response(1001, '身份信息不存在')
        else:
            admin = DB.session.query(Merchant).filter(Merchant.token == token).first()
            if admin is None:
                return Response(1001, '请登录')
            elif admin.token != token:
                return Response(1001, '身份信息已过期')
            elif admin.is_frozen == 1:
                return Response(1001, '账号异常')
            else:
                admin.login_at = CommonUtil.time_format_str()
                admin.login_ip = request.environ['REMOTE_ADDR']
                DB.session.commit()
                return Response(0, '', admin)
