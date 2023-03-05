# -- coding: utf-8 --
import requests

PROXY_POOL_URL = 'http://localhost:8000/random'


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None
    except requests.ConnectionError:
        return None


def test():
    proxy = get_proxy()
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy,
    }
    try:
        response = requests.get('http://httpbin.org/get', proxies=proxies, timeout=6)
        print(response.text)
    except requests.exceptions.ConnectionError as e:
        print('Error', e.args)


if __name__ == '__main__':
    # 注意: 此为客户端, 在使用时必须先启动服务端主程序(scheduler.py)
    test()
