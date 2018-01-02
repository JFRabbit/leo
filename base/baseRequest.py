from httpUtil.httpMethod import *


class BaseRequest(object):
    def __init__(self, url: str, method: HttpMethod):
        self.url = url
        self.method = method
