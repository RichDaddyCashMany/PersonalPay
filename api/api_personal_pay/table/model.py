from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 商户
class Merchant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_no = db.Column(db.Integer)
    username = db.Column(db.String(16))
    password = db.Column(db.String(32))
    confirm_password = db.Column(db.String(32))
    phone = db.Column(db.Integer)
    email = db.Column(db.String(50))
    avatar = db.Column(db.String(200))
    parent_no = db.Column(db.Integer)
    online_from = db.Column(db.String(14))
    online_to = db.Column(db.String(14))
    is_frozen = db.Column(db.Integer)
    create_at = db.Column(db.String(14))
    create_ip = db.Column(db.String(15))
    login_at = db.Column(db.String(14))
    login_ip = db.Column(db.String(15))
    token = db.Column(db.String(32))
    alipay_name = db.Column(db.String(4))
    alipay_account = db.Column(db.String(100))
    wechat_name = db.Column(db.String(4))
    wechat_account = db.Column(db.String(100))


# 订单
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_no = db.Column(db.String(32))
    platform_order_no = db.Column(db.String(32))
    platform = db.Column(db.Integer)
    create_at = db.Column(db.String(14))
    confirm_at = db.Column(db.String(14))
    cost = db.Column(db.BigInteger)
    from_account = db.Column(db.String(20))
    from_nickname = db.Column(db.String(20))
    from_email = db.Column(db.String(100))
    message = db.Column(db.Text)
    confirm_secret_key = db.Column(db.String(32))


# 产品
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'), nullable=False)
    record_id = db.Column(db.String(32))
    name = db.Column(db.String(20))
    desc = db.Column(db.String(200))
    price = db.Column(db.BigInteger)
    is_on_sell = db.Column(db.Integer)
    create_at = db.Column(db.String(14))
    modify_at = db.Column(db.String(14))
    alipay_qrcode = db.Column(db.String(200))
    wechat_qrcode = db.Column(db.String(200))


# 库存
class ProductStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    record_id = db.Column(db.String(32))
    content = db.Column(db.Text)
    create_at = db.Column(db.String(14))
    sold_at = db.Column(db.String(14))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

