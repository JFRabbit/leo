import requests

# http://requests-docs-cn.readthedocs.io/zh_CN/latest/user/quickstart.html
if __name__ == '__main__':
    url = 'http://new.trunk.amazingday.cn/aws/auth/login'
    data = {'mobile': '13651200755', 'password': '123456'}

    session = requests.session()
    response = session.post(url, json=data)

    content = response.json()  # type: dict
    print(content)
