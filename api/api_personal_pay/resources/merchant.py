from flask_restful import reqparse, fields, marshal, request
from util.db import DB
from table.model import Merchant
from util.commonUtil import CommonUtil
from resources.baseApi import BaseApi
from util.checkUtil import CheckUtil
from util.valid import Valid
from config.config import Config


# 登录
class MerchantLogin(BaseApi):
    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        merchant = DB.session.query(Merchant).filter(Merchant.username == args.username).first()
        if merchant is None:
            return CommonUtil.json_response(-1, "用户名不存在")

        if merchant.password == CommonUtil.create_user_password(args.username, args.password):
            # 生成新token
            merchant.token = CommonUtil.create_admin_token(args.username)
            DB.session.commit()

            merchant = DB.session.query(Merchant).filter(Merchant.username == args.username).first()
            dic = {
                'token': fields.String
            }

            return CommonUtil.json_response(0, "登录成功", marshal(merchant, dic))
        else:
            print(merchant.password)
            print(CommonUtil.create_user_password(args.username, args.password))
            return CommonUtil.json_response(-1, "密码错误")


# 注册
class MerchantReg(BaseApi):
    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('password2', required=True)
        parser.add_argument('validId', required=True)
        parser.add_argument('validValue', required=True)
        args = parser.parse_args()

        # 效验验证码
        result = CheckUtil.check_valid_image(args.validId, args.validValue)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        if Valid.is_username(args.username) is None:
            return CommonUtil.json_response(-1, "用户名必须是6-16位英文或数字")

        if Valid.is_password(args.password) is None:
            return CommonUtil.json_response(-1, "密码必须是6-16位英文或数字")

        if args.password != args.password2:
            return CommonUtil.json_response(-1, "两次密码不一致")

        merchant = DB.session.query(Merchant).filter(Merchant.username == args.username).first()
        if merchant:
            return CommonUtil.json_response(-1, "用户名已存在")

        # 生成唯一的商户id
        merchant_no = None
        while merchant_no is None:
            random_id = CommonUtil.random_id()
            merchant = DB.session.query(Merchant).filter(Merchant.merchant_no == random_id).first()
            if merchant is None:
                merchant_no = random_id

        merchant = Merchant(
            merchant_no=merchant_no,
            username=args.username,
            password=CommonUtil.create_user_password(args.username, args.password),
            create_at=CommonUtil.time_format_str(),
            create_ip=request.environ['REMOTE_ADDR'],
            is_frozen=0
        )
        DB.session.add(merchant)
        DB.session.commit()
        return CommonUtil.json_response(0, "注册成功")


class MerchantInfo(BaseApi):
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

        merchant = DB.session.query(Merchant).filter(Merchant.id == result.data.id).first()

        dic = {
            'email': fields.String,
            'online_from': fields.String,
            'online_to': fields.String,
            'alipay_name': fields.String,
            'alipay_account': fields.String,
            'wechat_name': fields.String,
            'wechat_account': fields.String
        }

        result = marshal(merchant, dic)
        result['mch_url'] = Config.NOTIFY_ROOT_URL + '/buy.html?mch=' + str(merchant.merchant_no)

        return CommonUtil.json_response(0, '获取成功', result)


class MerchantInfoSave(BaseApi):
    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('online_from', required=True)
        parser.add_argument('online_to', required=True)
        parser.add_argument('alipay_name', required=True)
        parser.add_argument('alipay_account', required=True)
        parser.add_argument('wechat_name', required=True)
        parser.add_argument('wechat_account', required=True)
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_merchant_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        if Valid.is_non_empty_str(args.email) is False:
            return CommonUtil.json_response(-1, '确认邮箱不能为空')

        merchant = DB.session.query(Merchant).filter(Merchant.id == result.data.id).first()
        merchant.email = args.email
        merchant.online_from = args.online_from
        merchant.online_to = args.online_to
        merchant.alipay_name = args.alipay_name
        merchant.alipay_account = args.alipay_account
        merchant.wechat_name = args.wechat_name
        merchant.wechat_account = args.wechat_account

        DB.session.commit()

        return CommonUtil.json_response(0, '保存成功')
