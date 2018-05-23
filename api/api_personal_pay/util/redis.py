import redis


class Redis:
    @classmethod
    def setex(cls, name, time, value):
        r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        r.setex(name, time, value)

    @classmethod
    def get(cls, name):
        r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        value = r.get(name)
        if value is None:
            return None
        else:
            # pytyhon3 redis默认返回的是bytes
            return bytes.decode(value)

    @classmethod
    def delete(cls, name):
        r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        r.delete(name)  # 看源码明明可以支持多参数的，但是之前把参数封装成*names会删除失败
