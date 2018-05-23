from flask_restful import reqparse, fields, marshal
from util.db import DB
from table.model import Product, ProductStock, Merchant, Order
from util.commonUtil import CommonUtil
from resources.baseApi import BaseApi
from util.checkUtil import CheckUtil
from util.valid import Valid
import time
from util.convertUtil import ConvertFormatTime
import math
from util.emailUtil import EmailUtil
from config.config import Config


# 商品列表
class ClientProductList(BaseApi):
    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('mch', required=True)
        args = parser.parse_args()

        merchant = DB.session.query(Merchant).filter(Merchant.merchant_no == args.mch).first()
        if merchant is None:
            return CommonUtil.json_response(-1, '商户不存在')

        products = DB.session.query(Product).join(Merchant).filter(Product.merchant_id == merchant.id).order_by(Product.create_at.desc()).all()

        dic = {
            'productId': fields.String(attribute='record_id'),
            'is_on_sell': fields.Integer,
            'name': fields.String,
            'desc': fields.String,
            'price': fields.String,
            'alipay_qrcode': fields.String,
            'wechat_qrcode': fields.String
        }

        mch_dic = {
            'online_from': fields.String,
            'online_to': fields.String,
            'alipay_name': fields.String,
            'alipay_account': fields.String,
            'wechat_name': fields.String,
            'wechat_account': fields.String
        }

        data = {
            'list': marshal(products, dic),
            'mch': marshal(merchant, mch_dic)
        }

        return CommonUtil.json_response(0, '获取成功', data)


class ClientOrderCreate(BaseApi):
    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('productId', required=True)
        parser.add_argument('from_account', required=True)
        parser.add_argument('from_email', required=True)
        parser.add_argument('from_nickname', required=True)
        parser.add_argument('message', required=True)
        parser.add_argument('platform', required=True)
        args = parser.parse_args()

        product = DB.session.query(Product).filter(Product.record_id == args.productId).first()
        merchant = DB.session.query(Merchant).filter(Merchant.id == product.merchant_id).first()

        if product is None or merchant is None:
            return CommonUtil.json_response(-1, '商品查询失败')

        stock = DB.session.query(ProductStock).filter(ProductStock.product_id == product.id).first()
        if stock is None:
            return CommonUtil.json_response(-1, '商品库存不足')

        if product.is_on_sell == 0:
            return CommonUtil.json_response(-1, '商品已下架')

        if Valid.is_non_empty_str(args.from_account) is False:
            return CommonUtil.json_response(-1, '支付账号不能为空')

        if Valid.is_non_empty_str(args.from_email) is False:
            return CommonUtil.json_response(-1, '收货邮箱不能为空')

        secret_key = CommonUtil.md5(str(time.time()) + args.from_account + args.productId + 'secret_key')

        order_no = CommonUtil.md5(str(time.time()) + args.from_account + args.productId)

        if int(args.platform) == 0:
            payment = '支付宝'
        else:
            payment = '微信支付'

        email_head = '<div style="display:flex;justify-content:center"><div style="margin-top:40px;background-color:#fff;width:375px">'
        email_tail = '<div style="margin-top:20px;display:flex;justify-content:center"><a style="color:#fff;text-decoration:none;padding:0 10px;height:34px;background-color:#409EFF;text-align:center;line-height:34px;font-size:14px;border-radius:3px" href="%s">我已收到转账，点击确认收款</a></div><div style="margin-top:140px;display:flex;justify-content:center"><span style="color:#999;font-size:10px">Copyright@2018 51shuaba.xyz All Rights Reseved.</span></div></div></div>' % (
            Config.NOTIFY_ROOT_URL + '/confirm.html?secretkey=' + secret_key + '&orderno=' + order_no
        )
        email_order_no = '<div style="background-color:#fafaf8;border-bottom:1px solid #e6e6e6;display:flex;justify-content:space-between;padding:10px 10px"><span style="color:#333;font-size:14px">%s</span> <span style="color:#333;font-size:14px">%s</span></div>' % (
            '订单号', order_no)
        email_time = '<div style="background-color:#fafaf8;border-bottom:1px solid #e6e6e6;display:flex;justify-content:space-between;padding:10px 10px"><span style="color:#333;font-size:14px">%s</span> <span style="color:#333;font-size:14px">%s</span></div>' % (
            '提交时间', CommonUtil.timestamp_to_time(int(time.time())))
        email_payment = '<div style="background-color:#fafaf8;border-bottom:1px solid #e6e6e6;display:flex;justify-content:space-between;padding:10px 10px"><span style="color:#333;font-size:14px">%s</span> <span style="color:#333;font-size:14px">%s</span></div>' % (
            '支付方式', payment)
        email_product_name = '<div style="background-color:#fafaf8;border-bottom:1px solid #e6e6e6;display:flex;justify-content:space-between;padding:10px 10px"><span style="color:#333;font-size:14px">%s</span> <span style="color:#333;font-size:14px">%s</span></div>' % (
            '商品名称', product.name)
        email_product_price = '<div style="background-color:#fafaf8;border-bottom:1px solid #e6e6e6;display:flex;justify-content:space-between;padding:10px 10px"><span style="color:#333;font-size:14px">%s</span> <span style="color:#333;font-size:14px">%s</span></div>' % (
            '商品价格', str(product.price / 100) + '元')
        email_account = '<div style="background-color:#fafaf8;border-bottom:1px solid #e6e6e6;display:flex;justify-content:space-between;padding:10px 10px"><span style="color:#333;font-size:14px">%s</span> <span style="color:#333;font-size:14px">%s</span></div>' % (
            '支付账号', args.from_account)
        email_email = '<div style="background-color:#fafaf8;border-bottom:1px solid #e6e6e6;display:flex;justify-content:space-between;padding:10px 10px"><span style="color:#333;font-size:14px">%s</span> <span style="color:#333;font-size:14px">%s</span></div>' % (
            '收货邮箱', args.from_email)
        email_nickname = '<div style="background-color:#fafaf8;border-bottom:1px solid #e6e6e6;display:flex;justify-content:space-between;padding:10px 10px"><span style="color:#333;font-size:14px">%s</span> <span style="color:#333;font-size:14px">%s</span></div>' % (
            '支付昵称', args.from_nickname)
        email_message = '<div style="background-color:#fafaf8;border-bottom:1px solid #e6e6e6;display:flex;justify-content:space-between;padding:10px 10px"><span style="color:#333;font-size:14px">%s</span> <span style="color:#333;font-size:14px">%s</span></div>' % (
            '买家留言', args.message)

        info = '%s%s%s%s%s%s%s%s%s%s%s' % (email_head, email_order_no, email_time, email_payment, email_product_name, email_product_price, email_account, email_email, email_nickname, email_message, email_tail)

        result = EmailUtil.send_html_email('收到新的商品订单，买家正在付款中~', info, merchant.email)

        if result is True:
            order = Order(
                merchant_id=merchant.id,
                product_id=product.id,
                order_no=order_no,
                platform=args.platform,
                create_at=CommonUtil.time_format_str(),
                cost=product.price,
                from_account=args.from_account,
                from_nickname=args.from_nickname,
                from_email=args.from_email,
                message=args.message,
                confirm_secret_key=secret_key
            )

            DB.session.add(order)
            DB.session.commit()

            return CommonUtil.json_response(0, '下单成功')
        else:
            return CommonUtil.json_response(-1, '邮件通知商户失败，请重试')
