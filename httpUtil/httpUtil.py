import requests
from env.partial import *
from httpUtil.httpMethod import HttpMethod
from jsonCompare.jsonFormat import *


class RequestItems(object):
    def __init__(self, url: str, method: HttpMethod, data=None, json=None, **kwargs):
        self.url = url
        self.method = method
        self.data = data
        self.json = json  # type: dict
        self.kwargs = kwargs

    def __str__(self):
        return "RequestItems: [url:%s, method:%s, data:%s, json:%s, kwargs:%s]" % \
               (self.url, self.method, self.data, json_format(self.json), self.kwargs)


class ResponseItems(object):
    def __init__(self, response: requests.Response):
        self.url = response.url
        self.status = response.status_code
        try:
            self.json = response.json()
        except json.decoder.JSONDecodeError as e:
            print("json.decoder.JSONDecodeError: %s" % e)
            self.json = response.text

    def __str__(self):
        return "ResponseItems: [url:%s, status:%d, json:%s]" % \
               (self.url, self.status, json_format(self.json))


def __verify_cas():
    session = requests.session()
    session.get(CUR_ENV[CAS], verify=False)
    return session


def __ignore_urllib3_warning():
    import urllib3
    urllib3.disable_warnings()


def do_request(items: RequestItems):
    # 忽略 warning
    if http_variable[IGNORE_WARN]:
        __ignore_urllib3_warning()

    session = requests.session()

    # cas 认证
    if env_variable[CAS]:
        session = __verify_cas()

    methods = {
        HttpMethod.GET:
            session.get(items.url, **items.kwargs),
        HttpMethod.POST:
            session.post(items.url, items.data, items.json, **items.kwargs),
        HttpMethod.PUT:
            session.put(items.url, items.data, **items.kwargs),
        HttpMethod.DELETE:
            session.delete(items.url, **items.kwargs)
    }
    response = methods[items.method]
    res_items = ResponseItems(response)
    session.close()
    return res_items
