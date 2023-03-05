# -- coding: utf-8 --
import requests
import re
from requests.exceptions import Timeout


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # 第四个参数 attrs 中包含了类的一些属性。我们可以遍历 attrs 这个参数即可获取类的所有方法信息，就像遍历字典一样，键名对应方法的名称。
        # 然后判断方法的开头是否 crawl，如果是，则将其加入到 __CrawlFunc__属性中。
        # 这样我们就成功将所有以 crawl 开头的方法定义成了一个属性，动态获取到所有以 crawl 开头的方法列表。
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        # print(attrs)
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        """
        获取每个方法返回的代理并组合成列表形式返回
        :param callback:一个字符串参数, 表示要调用的获取代理的方法名
        :return: proxies 列表
        """
        proxies = []
        # 不使用 `eval()` 函数来动态执行代码，因为这会使代码变得不可预测和不可维护
        # 使用 `getattr()` 函数或者将类方法名作为参数直接传递进来来避免这个问题
        method = getattr(self, callback)
        for proxy in method():
            # print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_jiangxianli(self, page_count=3):
        """
        :param page_count: 页码
        :return: 代理(解析出 IP 加端口的形式的代理并返回)
        """
        for i in range(1, page_count + 1):
            print(f'获取 jiangxianli 第{i}页代理')
            url = f'https://ip.jiangxianli.com/api/proxy_ips?page={i}&order_by=speed&order_rule=DESC'
            response = None
            try:
                response = requests.get(url, timeout=(3.05, 5), verify=False)
                resp = response.json()
                for i in resp['data']['data']:
                    yield f"{i['ip']}:{i['port']}"
            except Timeout:
                print(f'获取 jiangxianli 第{i}页代理超时')
                continue
            finally:
                if response is not None:  # 检查 response 是否为 None
                    response.close()

    def crawl_ip3366(self, page_count=3):
        """
        :param page_count: 页码
        :return: 代理(解析出 IP 加端口的形式的代理并返回)
        """
        for i in range(1, page_count + 1):
            print(f'获取 ip3366 第{i}页代理')
            url = f'http://www.ip3366.net/free/?stype=1&page={i}'
            response = None
            try:
                response = requests.get(url, timeout=(3.05, 5), verify=False)
                resp = response.text
                ret = re.finditer(r'<tr>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', resp, flags=re.S)
                for i in ret:
                    yield f'{i.group(1)}:{i.group(2)}'
            except Timeout:
                print(f'获取 ip3366 第{i}页代理超时')
                continue
            finally:
                if response is not None:  # 检查 response 是否为 None
                    response.close()
