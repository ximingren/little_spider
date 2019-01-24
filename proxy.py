import json
import random

import requests
import proxy


def get_ip1():
    # scylla
    response = requests.get('http://localhost:8899/api/v1/proxies')
    data = json.loads(response.text)
    proxies = random.choice(data['proxies'])
    proxy = {'https': 'https://' + str(proxies['ip']) + ":" + str(proxies['port']),
             'http': 'http://' + str(proxies['ip']) + ":" + str(proxies['port'])}
    return proxy


def get_ip2():
    # proxy-pool,用的是redis 6378
    response = requests.get('http://127.0.0.1:5010/get_all/')
    proxy = random.choice(list(response.json()))
    return {'https': 'https://' + proxy,
            'http': 'http://' + proxy}


def get_proxy():
    function_list = ['get_ip1', 'get_ip2']
    return getattr(proxy, random.choice(function_list))()
#构建一个docker里面有代理
#跨域