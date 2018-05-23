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


class OrderList(BaseApi):
    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        parser.add_argument('page', required=True)
        parser.add_argument('size', required=True)
        parser.add_argument('searchType')
        parser.add_argument('searchWords')
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_merchant_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        page = int(args.page)
        size = int(args.size)

        if Valid.is_non_empty_str(args.searchType) and Valid.is_non_empty_str(args.searchWords):
            if args.searchType == 'order_no':
                orders = DB.session.query(Order.order_no, Order.platform_order_no, Order.platform, Order.create_at,
                                      Order.confirm_at, Order.cost, Order.from_account, Order.from_email,
                                      Order.from_nickname, Order.message, Product.name, Product.record_id).\
                    join(Product) .\
                    filter(Product.id == Order.product_id) .\
                    filter(Order.merchant_id == result.data.id). \
                    filter(Order.order_no.like('%' + args.searchWords + '%')). \
                    order_by(Order.create_at.desc()).limit(size).offset((page - 1) * size).\
                    all()
                count = DB.session.query(Order).\
                    filter(Order.merchant_id == result.data.id). \
                    filter(Order.order_no.like('%' + args.searchWords + '%')). \
                    count()
                orders = CommonUtil.sql_result_to_json(orders)
            elif args.searchType == 'from_account':
                orders = DB.session.query(Order.order_no, Order.platform_order_no, Order.platform, Order.create_at,
                                      Order.confirm_at, Order.cost, Order.from_account, Order.from_email,
                                      Order.from_nickname, Order.message, Product.name, Product.record_id).\
                    join(Product) .\
                    filter(Product.id == Order.product_id) .\
                    filter(Order.merchant_id == result.data.id). \
                    filter(Order.from_account.like('%' + args.searchWords + '%')). \
                    order_by(Order.create_at.desc()).limit(size).offset((page - 1) * size). \
                    all()
                count = DB.session.query(Order). \
                    filter(Order.merchant_id == result.data.id). \
                    filter(Order.from_account.like('%' + args.searchWords + '%')). \
                    count()
                orders = CommonUtil.sql_result_to_json(orders)
            elif args.searchType == 'from_email':
                orders = DB.session.query(Order.order_no, Order.platform_order_no, Order.platform, Order.create_at,
                                      Order.confirm_at, Order.cost, Order.from_account, Order.from_email,
                                      Order.from_nickname, Order.message, Product.name, Product.record_id).\
                    join(Product) .\
                    filter(Product.id == Order.product_id) .\
                    filter(Order.merchant_id == result.data.id). \
                    filter(Order.from_email.like('%' + args.searchWords + '%')). \
                    order_by(Order.create_at.desc()).limit(size).offset((page - 1) * size). \
                    all()
                count = DB.session.query(Order). \
                    filter(Order.merchant_id == result.data.id). \
                    filter(Order.from_email.like('%' + args.searchWords + '%')). \
                    count()
                orders = CommonUtil.sql_result_to_json(orders)
            else:
                orders = DB.session.query(Order.order_no, Order.platform_order_no, Order.platform, Order.create_at,
                                      Order.confirm_at, Order.cost, Order.from_account, Order.from_email,
                                      Order.from_nickname, Order.message, Product.name, Product.record_id).\
                    join(Product) .\
                    filter(Product.id == Order.product_id) .\
                    filter(Order.merchant_id == result.data.id). \
                    order_by(Order.create_at.desc()).limit(size).offset((page - 1) * size).all()
                count = DB.session.query(Order). \
                    filter(Order.merchant_id == result.data.id). \
                    count()
                orders = CommonUtil.sql_result_to_json(orders)
        else:
            orders = DB.session.query(Order.order_no, Order.platform_order_no, Order.platform, Order.create_at,
                                      Order.confirm_at, Order.cost, Order.from_account, Order.from_email,
                                      Order.from_nickname, Order.message, Product.name, Product.record_id).\
                join(Product) .\
                filter(Product.id == Order.product_id) .\
                filter(Order.merchant_id == result.data.id). \
                order_by(Order.create_at.desc()).limit(size).offset((page - 1) * size).all()
            count = DB.session.query(Order).\
                filter(Order.merchant_id == result.data.id).\
                count()
            orders = CommonUtil.sql_result_to_json(orders)

        dic = {
            'order_no': fields.String,
            'platform_order_no': fields.String,
            'platform': fields.Integer,
            'create_at': ConvertFormatTime(),
            'confirm_at': ConvertFormatTime(),
            'cost': fields.String,
            'from_account': fields.String,
            'from_email': fields.String,
            'from_nickname': fields.String,
            'message': fields.String,
            'product_name': fields.String(attribute='name'),
            'productId': fields.String(attribute='record_id')
        }

        data = {
            'list': marshal(orders, dic),
            'totalCount': math.ceil(count)
        }

        return CommonUtil.json_response(0, '获取成功', data)


class OrderConfirm(BaseApi):
    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        parser.add_argument('order_no', required=True)
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_merchant_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        order = DB.session.query(Order).filter(Order.order_no == args.order_no).first()
        if order is None:
            return CommonUtil.json_response(-1, '订单不存在')

        if order.confirm_at:
            return CommonUtil.json_response(-1, '订单已确认过')

        stock = DB.session.query(ProductStock).\
            filter(order.product_id == ProductStock.product_id). \
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

        return CommonUtil.json_response(-1, '库存不足')
