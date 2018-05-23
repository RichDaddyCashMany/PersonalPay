class Response:
    code = 0
    message = ""
    data = None

    def __init__(self, code=0, message="", data=None):
        self.code = code
        self.message = message
        self.data = data
