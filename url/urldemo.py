import requests

if __name__ == '__main__':
    url = 'http://new.trunk.amazingday.cn/aws/auth/login'
    data = {'mobile': '13651200755', 'password': '123456'}

    response = requests.post(url, json=data)
    content = response.json() # type: dict
    print(content)

