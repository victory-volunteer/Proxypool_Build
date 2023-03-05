# -- coding: utf-8 --
from proxypool.db import RedisClient
from proxypool.crawler import Crawler
from proxypool.setting import *


class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """判断是否达到了代理池限制(容量阈值)"""
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        if not self.is_over_threshold():
            # 调用了 Crawler 类的CrawlFunc属性，获取到所有以 crawl 开头的方法列表，
            # 依次通过 get_proxies() 方法调用，得到各个方法抓取到的代理，然后再利用 RedisClient 的 add() 方法加入数据库
            for callback_label in range(getattr(self.crawler, '__CrawlFuncCount__')):
                callback = getattr(self.crawler, '__CrawlFunc__')[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)

