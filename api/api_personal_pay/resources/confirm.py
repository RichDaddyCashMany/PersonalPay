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


class ConfirmSend(BaseApi):
    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('secret_key', required=True)
        parser.add_argument('order_no', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        order = DB.session.query(Order).filter(Order.order_no == args.order_no).first()
        if order is None:
            return CommonUtil.json_response(-1, '订单不存在')

        if order.confirm_secret_key != args.secret_key:
            return CommonUtil.json_response(-1, '订单密钥错误')

        if order.confirm_at:
            return CommonUtil.json_response(-1, '订单已确认过')

        merchant = DB.session.query(Merchant).filter(Merchant.id == order.merchant_id).first()
        # 二次密码核对
        if merchant and merchant.password == CommonUtil.create_user_password(merchant.username, args.password):
            stock = DB.session.query(ProductStock).\
                filter(order.product_id == ProductStock.product_id).\
                filter(ProductStock.sold_at == None). \
                first()
            if stock:
                stock.sold_at = CommonUtil.time_format_str()
                stock.order_id = order.id
                DB.session.commit()

                order.confirm_at = CommonUtil.time_format_str()
                DB.session.commit()

                info = '<div style="display:flex;justify-content:center"><div style="width:375px"><div><p style="color:#000;font-size:40px;font-weight:700">“</p><p style="color:#333;font-size:14px;line-height:20px;letter-spacing:2px">%s</p><p style="color:#000;font-size:40px;font-weight:700;text-align:right">”</p></div><div style="margin-top:140px;display:flex;justify-content:center"><span style="color:#999;font-size:10px">Copyright@2018 51shuaba.xyz All Rights Reseved.</span></div></div></div>' % (
                    stock.content
                )

                result = EmailUtil.send_html_email('订单' + args.order_no + '发货通知', info, order.from_email)

                if result is True:
                    return CommonUtil.json_response(0, '确认成功，已邮件通知买家')
                else:
                    return CommonUtil.json_response(0, '确认成功，但是发货邮件未能送达，请联系买家')
            else:
                return CommonUtil.json_response(-1, '库存不足')

        return CommonUtil.json_response(-1, '密码错误')
