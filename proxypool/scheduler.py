# -- coding: utf-8 --
from multiprocessing import Process
from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester
import time
from proxypool.setting import *


class Scheduler(object):
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        首先声明一个 Tester 对象，然后进入死循环不断循环调用其 run() 方法，执行完一轮之后就休眠一段时间，休眠结束之后重新再执行
        """
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """定时获取代理"""
        getter = Getter()
        while True:
            print(' 开始抓取代理 ')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """开启 API"""
        app.run(host=API_HOST, port=API_PORT)

    def run(self):
        """ 3个进程就可以并行执行，互不干扰"""
        print(' 代理池开始运行 ')
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()



