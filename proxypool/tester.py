# -- coding: utf-8 --
import aiohttp
from proxypool.db import RedisClient
import asyncio
from proxypool.setting import *


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        检测单个代理的可用情况
        :param proxy: 被检测的单个代理
        :return: None
        """
        async with aiohttp.ClientSession() as session:
            try:
                # 将传入的代理参数进行类型转换，如果是bytes类型则转换为utf-8编码格式的字符串
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                # 然后在代理前面加上"http://"前缀，以构建代理的真实地址
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=10) as response:
                    if response.status in VALID_STATUS_CODES:
                        text = await response.json()
                        if proxy.split(':')[0] == text['origin']:
                            self.redis.max(proxy)
                            print('代理可用', proxy)
                        else:
                            self.redis.decrease(proxy)
                            print('返回响应和代理不符', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应码不合法', proxy)
            except (aiohttp.ClientError, aiohttp.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print('代理请求失败', proxy)

    async def test_proxy(self, test_proxies):
        tasks = []
        for proxy in test_proxies:
            tasks.append(asyncio.create_task(self.test_single_proxy(proxy)))
        await asyncio.wait(tasks)

    def run(self):
        """
        获取了所有的代理列表，使用 aiohttp 分配测试任务
        :return: None
        """
        loop = None
        try:
            count = self.redis.count()  # 获取全部代理数量
            # 弃用
            # proxies = self.redis.all()  # 获取全部代理列表

            # 只创建了一个事件循环对象，并在循环内部多次调用协程
            # loop = asyncio.get_event_loop()

            # 防止报错: RuntimeError: Event loop is closed, 现更改为下: (但实测没啥用, 在window下无法解决)
            # 使用 asyncio.new_event_loop() 函数创建了一个新的事件循环对象，通常情况下，每个线程只能有一个事件循环，如果要在不同的线程中运行协程，则需要为每个线程创建一个新的事件循环。
            loop = asyncio.new_event_loop()
            # 然后使用 asyncio.set_event_loop(loop) 将其设置为默认的事件循环对象。这样即可避免已经关闭的事件循环对象问题
            asyncio.set_event_loop(loop)

            # 批量测试代理
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print('正在测试第', start + 1, '——', stop, '个代理')
                # 弃用
                # test_proxies = proxies[i:i + BATCH_TEST_SIZE]
                # 分批测试，每次测试BATCH_TEST_SIZE个，避免代理池过大时一次性测试全部代理导致内存开销过大
                test_proxies = self.redis.batch(start, stop)
                loop.run_until_complete(self.test_proxy(test_proxies))
            # 最后要记得在程序结束时关闭事件循环，以避免资源泄漏
        except Exception as e:
            print('测试代理可用性出错:', e)
        finally:
            if loop is not None:  # 检查 loop 是否为 None
                loop.close()
