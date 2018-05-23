# 可以使用点语法访问
class SafeDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return None
            # raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value