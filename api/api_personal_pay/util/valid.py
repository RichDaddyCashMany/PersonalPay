import re


# 验证类
class Valid:
    # 账号
    @classmethod
    def is_username(cls, value):
        return re.match("[a-zA-Z0-9_-]{6,16}", value)

    # 密码
    @classmethod
    def is_password(cls, value):
        return re.match("[a-zA-Z0-9_-]{6,16}", value)

    # 是否是非空字符
    @classmethod
    def is_non_empty_str(cls, value):
        if isinstance(value, str):
            return len(value) > 0
        else:
            return False



