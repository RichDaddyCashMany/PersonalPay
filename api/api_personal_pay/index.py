from flask import Flask
from flask_restful import Api
from config.config import Config
import os
from flask_cors import CORS
from util.db import DB
from resources.baseApi import output_json
# merchant
from resources.common import ValidImageCreate, QCloudCosSign
from resources.merchant import MerchantReg, MerchantLogin, MerchantInfo, MerchantInfoSave
from resources.product import ProductAdd, ProductList, ProductDelete, ProductStockAdd, ProductStockList, \
    ProductStockDelete, ProductStockOrderNo
from resources.client import ClientProductList, ClientOrderCreate
from resources.order import OrderList, OrderConfirm
from resources.confirm import ConfirmSend

# 设置根目录
Config.ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

# 开启cors
CORS(app)

# 初使化SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + Config.MYSQL_USER + ':' + Config.MYSQL_PASSWORD + '@' + \
                                        Config.MYSQL_HOST+ '/' + Config.MYSQL_DBNAME
# 不配置会报错提示。如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 密钥，不配置无法对session字典赋值
app.config['SECRET_KEY'] = os.urandom(24)
# 显示SQLAlchemy的sql语句日志
app.config["SQLALCHEMY_ECHO"] = True

# 缓存全局db对象，每次重新创建会导致事务不是同一个
DB.init(app)

# 自定义返回，flask_restful默认只支持json
api = Api(app, default_mediatype='application/json')
# 根据请求头的的Accept参数，返回对应的格式
api.representations = {
    'application/json': output_json,
}
#
api.add_resource(ValidImageCreate, '/common/validImage/create')  # 生成图片验证码
api.add_resource(QCloudCosSign, '/common/QCloud/sign')  # 腾讯云COS多次签名
api.add_resource(MerchantReg, '/merchant/reg')
api.add_resource(MerchantLogin, '/merchant/login')
api.add_resource(MerchantInfo, '/merchant/info')
api.add_resource(MerchantInfoSave, '/merchant/info/save')
api.add_resource(ProductAdd, '/product/add')
api.add_resource(ProductList, '/product/list')
api.add_resource(ProductDelete, '/product/delete')
api.add_resource(ProductStockAdd, '/product/stock/add')
api.add_resource(ProductStockList, '/product/stock/list')
api.add_resource(ProductStockDelete, '/product/stock/delete')
api.add_resource(ClientProductList, '/client/product/list')
api.add_resource(ProductStockOrderNo, '/product/stock/orderno')
api.add_resource(ClientOrderCreate, '/client/order/create')
api.add_resource(OrderList, '/order/list')
api.add_resource(OrderConfirm, '/order/confirm')
api.add_resource(ConfirmSend, '/confirm/send')

if __name__ == '__main__':
    # threaded=True 防止开发服务器阻塞
    app.run(host='0.0.0.0', threaded=True, debug=True)
