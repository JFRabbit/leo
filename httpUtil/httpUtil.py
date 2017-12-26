import requests
from env.partial import *
from httpUtil.httpMethod import HttpMethod


def __verify_cas():
    session = requests.session()
    session.get(CUR_ENV[CAS], verify=False)
    return session

def __ignore_urllib3_warning():
    import urllib3
    urllib3.disable_warnings()

def do_request(url:str, method: HttpMethod, data=None, json=None, **kwargs):
    # 忽略 warning
    if http_variable[IGNORE_WARN]:
        __ignore_urllib3_warning()

    session = requests.session()

    # cas 认证
    if env_variable[CAS]:
        session = __verify_cas()

    methods = {
        HttpMethod.GET : session.get(url, **kwargs),
        HttpMethod.POST: session.post(url, data, json, **kwargs),
        HttpMethod.PUT: session.put(url, data, **kwargs),
        HttpMethod.DELETE: session.delete(url, **kwargs)
    }
    return methods[method]