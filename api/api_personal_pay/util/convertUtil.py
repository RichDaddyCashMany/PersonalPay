from flask_restful import fields
from util.commonUtil import CommonUtil
import time


# 时间戳转时间，用于marshal函数，过滤返回字典
class ConvertTimeStamp(fields.Raw):
    def format(self, value):
        ret = CommonUtil.timestamp_to_time(value)
        if ret is None:
            return ''
        else:
            return ret


# 比如20170102080808转成2017-01-02 08:08:08
class ConvertFormatTime(fields.Raw):
    def format(self, value):
        t = time.strptime(value, "%Y%m%d%H%M%S")
        return time.strftime("%Y-%m-%d %H:%M:%S", t)

