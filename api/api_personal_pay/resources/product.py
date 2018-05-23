from flask_restful import reqparse, fields, marshal
from util.db import DB
from table.model import Product, ProductStock, Order
from util.commonUtil import CommonUtil
from resources.baseApi import BaseApi
from util.checkUtil import CheckUtil
from util.valid import Valid
import time
from util.convertUtil import ConvertFormatTime
import math
from sqlalchemy import func


# 商品新增
class ProductAdd(BaseApi):
    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('desc', required=True)
        parser.add_argument('price', required=True)
        parser.add_argument('alipay_qrcode', required=True)
        parser.add_argument('wechat_qrcode', required=True)
        parser.add_argument('productId', required=True)
        parser.add_argument('is_on_sell', required=True)
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_merchant_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        if Valid.is_non_empty_str(args.name) is False:
            return CommonUtil.json_response(-1, '商品名称不能为空')

        if Valid.is_non_empty_str(args.price) is False:
            return CommonUtil.json_response(-1, '商品单价不能为空')

        if len(args.productId) == 0:
            product = DB.session.query(Product).filter(Product.name == args.name).filter(
                Product.merchant_id == result.data.id).first()
            if product:
                return CommonUtil.json_response(-1, '商品名称已存在')

            product = Product(
                merchant_id=result.data.id,
                record_id=CommonUtil.md5(args.name + args.token + str(time.time())),
                name=args.name,
                desc=args.desc,
                price=args.price,
                is_on_sell='1',
                create_at=CommonUtil.time_format_str(),
                alipay_qrcode=args.alipay_qrcode,
                wechat_qrcode=args.wechat_qrcode
            )
            DB.session.add(product)
            DB.session.commit()

            return CommonUtil.json_response(0, '新增成功')
        else:
            product = DB.session.query(Product).filter(Product.record_id == args.productId).filter(
                Product.merchant_id == result.data.id).first()
            if product:
                product.price = args.price
                product.desc = args.desc
                product.alipay_qrcode= args.alipay_qrcode
                product.wechat_qrcode = args.wechat_qrcode
                product.is_on_sell = args.is_on_sell

                DB.session.commit()

                return CommonUtil.json_response(0, '修改成功')

        return CommonUtil.json_response(-1, '未知错误')


# 商品列表
class ProductList(BaseApi):
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
            if args.searchType == 'product_name':
                products = DB.session.query(Product). \
                    filter(Product.merchant_id == result.data.id). \
                    filter(Product.name.like('%' + args.searchWords + '%')). \
                    order_by(Product.create_at.desc()).limit(size).offset((page - 1) * size). \
                    all()
                count = DB.session.query(Product).\
                    filter(Product.merchant_id == result.data.id). \
                    filter(Product.name.like('%' + args.searchWords + '%')). \
                    count()
        else:
            products = DB.session.query(Product). \
                filter(Product.merchant_id == result.data.id). \
                order_by(Product.create_at.desc()).limit(size).offset((page - 1) * size). \
                all()
            count = DB.session.query(Product).filter(Product.merchant_id == result.data.id).count()

        dic = {
            'productId': fields.String(attribute='record_id'),
            'create_at': ConvertFormatTime(),
            'is_on_sell': fields.Integer,
            'name': fields.String,
            'desc': fields.String,
            'price': fields.String,
            'alipay_qrcode': fields.String,
            'wechat_qrcode': fields.String
        }

        data = {
            'list': marshal(products, dic),
            'totalCount': math.ceil(count)
        }

        return CommonUtil.json_response(0, '获取成功', data)


# 商品删除
class ProductDelete(BaseApi):
    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        parser.add_argument('productId', required=True)
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_merchant_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        DB.session.query(Product).\
            filter(Product.record_id == args.productId).\
            filter(Product.merchant_id == result.data.id).\
            delete()
        DB.session.commit()

        return CommonUtil.json_response(0, '删除成功')


# 商品库存新增
class ProductStockAdd(BaseApi):
    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        parser.add_argument('productId', required=True)
        parser.add_argument('content', required=True)
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_merchant_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        if Valid.is_non_empty_str(args.content) is False:
            return CommonUtil.json_response(-1, '内容不能为空')

        product = DB.session.query(Product).filter(Product.record_id == args.productId).filter(Product.merchant_id == result.data.id).first()
        if product is None:
            return CommonUtil.json_response(-1, '商品不存在')
        if product.is_on_sell == 0:
            return CommonUtil.json_response(-1, '商品已下架')

        contents = args.content.split('#separator#')
        create_at = CommonUtil.time_format_str()

        for index in range(len(contents)):
            content = contents[index]
            # 去首尾回车
            if len(content) > 2:
                if content[:1] == '\n':
                    content = content[1:]
            if len(content) > 2:
                if content[-1:] == '\n':
                    content = content[:-1]
            if len(content) > 0 and content != '\n':
                productStock = ProductStock(
                    product_id=product.id,
                    record_id=CommonUtil.md5(args.productId + args.token + create_at + str(index)),
                    content=content,
                    create_at=create_at
                )
                DB.session.add(productStock)
        DB.session.commit()

        return CommonUtil.json_response(0, '新增成功')


# 商品库存列表
class ProductStockList(BaseApi):
    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        parser.add_argument('productId', required=True)
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

        product = DB.session.query(Product).filter(Product.record_id == args.productId).filter(
                Product.merchant_id == result.data.id).first()
        if product is None:
            if Valid.is_non_empty_str(args.searchType) and Valid.is_non_empty_str(args.searchWords):
                if args.searchType == 'content':
                    stocks = DB.session.query(ProductStock.record_id, ProductStock.content, ProductStock.create_at,
                                              ProductStock.sold_at, Product.name). \
                        join(Product). \
                        filter(Product.merchant_id == result.data.id). \
                        filter(Product.id == ProductStock.product_id). \
                        filter(ProductStock.content.like('%' + args.searchWords + '%')). \
                        order_by(ProductStock.create_at.desc()).limit(size).offset((page - 1) * size). \
                        all()
                    count = DB.session.query(ProductStock). \
                        join(Product). \
                        filter(Product.merchant_id == result.data.id). \
                        filter(Product.id == ProductStock.product_id). \
                        filter(ProductStock.content.like('%' + args.searchWords + '%')). \
                        count()
                    stocks = CommonUtil.sql_result_to_json(stocks)
            else:
                stocks = DB.session.query(ProductStock.record_id, ProductStock.content, ProductStock.create_at,
                                          ProductStock.sold_at, Product.name). \
                    join(Product). \
                    filter(Product.merchant_id == result.data.id). \
                    filter(Product.id == ProductStock.product_id). \
                    order_by(ProductStock.create_at.desc()).limit(size).offset((page - 1) * size). \
                    all()
                count = DB.session.query(ProductStock). \
                    join(Product). \
                    filter(Product.merchant_id == result.data.id). \
                    filter(Product.id == ProductStock.product_id). \
                    count()
                stocks = CommonUtil.sql_result_to_json(stocks)
        else:
            if Valid.is_non_empty_str(args.searchType) and Valid.is_non_empty_str(args.searchWords):
                if args.searchType == 'content':
                    stocks = DB.session.query(ProductStock.record_id, ProductStock.content, ProductStock.create_at,
                                              ProductStock.sold_at, Product.name). \
                        join(Product). \
                        filter(Product.merchant_id == result.data.id). \
                        filter(ProductStock.product_id == product.id). \
                        filter(ProductStock.content.like('%' + args.searchWords + '%')). \
                        order_by(ProductStock.create_at.desc()).limit(size).offset((page - 1) * size). \
                        all()
                    count = DB.session.query(ProductStock). \
                        filter(Product.merchant_id == result.data.id). \
                        filter(ProductStock.product_id == product.id). \
                        filter(ProductStock.content.like('%' + args.searchWords + '%')). \
                        count()
                    stocks = CommonUtil.sql_result_to_json(stocks)
            else:
                stocks = DB.session.query(ProductStock.record_id, ProductStock.content, ProductStock.create_at,
                                          ProductStock.sold_at, Product.name). \
                    join(Product). \
                    filter(Product.merchant_id == result.data.id). \
                    filter(ProductStock.product_id == product.id). \
                    order_by(ProductStock.create_at.desc()).limit(size).offset((page - 1) * size). \
                    all()
                count = DB.session.query(ProductStock).\
                    filter(ProductStock.product_id == product.id). \
                    filter(Product.merchant_id == result.data.id). \
                    count()
                stocks = CommonUtil.sql_result_to_json(stocks)

        dic = {
            'stockId': fields.String(attribute='record_id'),
            'content': fields.String,
            'create_at': ConvertFormatTime(),
            'sold_at': ConvertFormatTime(),
            'order_no': fields.String,
            'product_name': fields.String(attribute='name')
        }

        data = {
            'list': marshal(stocks, dic),
            'totalCount': math.ceil(count)
        }

        return CommonUtil.json_response(0, '获取成功', data)


# 商品库存的订单号
class ProductStockOrderNo(BaseApi):
    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        parser.add_argument('stockId', required=True)
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_merchant_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        stock = DB.session.query(ProductStock).filter(ProductStock.record_id == args.stockId).first()
        order = DB.session.query(Order).filter(Order.id == stock.order_id).first()
        if stock and order:
            return CommonUtil.json_response(0, '获取成功', {
                'order_no': order.order_no
            })
        else:
            return CommonUtil.json_response(-1, '获取失败')


# 库存删除
class ProductStockDelete(BaseApi):
    def post(self):
        return self.handle()

    def handle(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', required=True)
        parser.add_argument('stockId', required=True)
        args = parser.parse_args()

        # 效验token
        result = CheckUtil.check_merchant_token(args.token)
        if result.code != 0:
            return CommonUtil.json_response(result.code, result.message)

        stock = DB.session.query(ProductStock).filter(ProductStock.record_id == args.stockId).first()
        if stock:
            product = DB.session.query(Product).filter(Product.id == stock.product_id).filter(Product.merchant_id == result.data.id).first()
            if product:
                DB.session.query(ProductStock).filter(ProductStock.record_id == args.stockId).delete()
                DB.session.commit()
                return CommonUtil.json_response(0, '删除成功')

        return CommonUtil.json_response(-1, '删除失败')
