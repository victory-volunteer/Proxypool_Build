# -- coding: utf-8 --
from flask import Flask, g
from proxypool.db import RedisClient

# 定义了一个特殊变量 __all__，它是一个列表，用于指定模块中哪些对象可以被其他模块导入。
# 在这段代码中，__all__ 列表只包含了一个字符串 'app'，表示其他模块只能导入变量 app。
__all__ = ['app']
# 定义了一个 Flask 应用程序对象，并将它存储在变量 app 中。
# __name__ 表示当前模块的名称，通常用于初始化 Flask 应用程序对象。
# Flask 应用程序对象通常用于注册路由、配置应用程序选项、添加插件等操作，以实现一个完整的 Web 应用程序。
app = Flask(__name__)


def get_conn():
    """
    用于获取 Redis 数据库连接。函数中使用了 Flask 提供的全局变量 g，用于存储每个请求的上下文
    1.如果 g 中没有 'redis' 属性，则创建一个 Redis 数据库连接，并将它存储在 g.redis 中。
    2.如果 g 中已经存在 'redis' 属性，则直接返回它所对应的 Redis 数据库连接。
    这里没有使用全局变量或单例模式来管理 Redis 数据库连接，而是使用了 Flask 提供的上下文管理机制来处理多个请求之间的数据库连接共享。
    由于 Flask 应用程序是多线程的，因此使用全局变量来管理数据库连接可能会导致线程安全问题，使用 Flask 提供的上下文管理机制可以避免这个问题。
    """
    # 判断一个对象是否具有指定的属性
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    """首页"""
    links = ['random', 'count']
    return '<h2>Welcome to Proxy Pool System</h2>' + '<br>'.join([f'<a href={link}>{link}</a>' for link in links])


# @app.route('/random')
# def get_proxy():
#     """
#     获取随机可用代理
#     :return: 随机代理
#     """
#     conn = get_conn()
#     return conn.random()
#
#
# @app.route('/count')
# def get_counts():
#     """
#     获取代理池总量
#     :return: 代理池总量
#     """
#     conn = get_conn()
#     return str(conn.count())

# 改写为下
@app.route('/<api_path>')
def api(api_path):
    if api_path == 'random':
        conn = get_conn()
        return conn.random()

    if api_path == 'count':
        conn = get_conn()
        return str(conn.count())


# 手动运行服务端
# app.run()
# 启动(必须先cd到当前目录)
# 在cmd下输入: set FLASK_APP=api.py && set FLASK_RUN_PORT=8000 && flask run
