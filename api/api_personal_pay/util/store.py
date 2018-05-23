from table.model import Config
from util.db import DB


# config表的保存和读取，返回的值是字符串类型，需要自己转换
class Store:
    @classmethod
    def save(cls, key, value):
        config = DB.session.query(Config).filter(Config.key == key).first()
        if config is None:
            config = Config(
                key=key,
                value=value
            )
            DB.session.add(config)
            DB.session.commit()
        else:
            config.value = value
            DB.session.commit()

    @classmethod
    def read(cls, key):
        config = DB.session.query(Config).filter(Config.key == key).first()
        if config is None:
            return ''
        else:
            return config.value

    @classmethod
    def read_all(cls):
        configs = DB.session.query(Config).all()
        dic = dict()
        for item in configs:
            dic[item.key] = item.value
        return dic
