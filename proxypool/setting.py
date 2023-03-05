# -- coding: utf-8 --
# Redis数据库地址
REDIS_HOST = 'localhost'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

REDIS_KEY = 'proxies'  # 有序集合的键名

# 代理分数
MAX_SCORE = 100  # 最大分数
MIN_SCORE = 0  # 最小分数
INITIAL_SCORE = 10  # 初始分数, 代理可用就设为100, 不可用就减1

# 用来存放正常的状态码，如可以定义成 [200]
# 当然某些目标网站可能会出现其他的状态码，可以自行配置
VALID_STATUS_CODES = [200]

# 用来测试的目标网站
# 注意: 有时需要将代理池检测的 URL 修改成待爬取站点，以便于把被待爬取站点封禁的代理剔除掉，留下可用代理
TEST_URL = 'https://httpbin.org/ip'

# 设置批量测试的最大值，也就是一批测试最多 100 个，这可以避免代理池过大时一次性测试全部代理导致内存开销过大的问题
BATCH_TEST_SIZE = 100

# 代理池数量界限, 最大数量
POOL_UPPER_THRESHOLD = 10000

# 代理检测周期: 每隔 60 秒进行一次代理检测
TESTER_CYCLE = 60
# 代理获取周期: 每隔 60 秒重新获取一次代理
GETTER_CYCLE = 60

# API配置
API_HOST = '127.0.0.1'
API_PORT = 8000

# 开关
# 以下3个常量分别表示测试模块、获取模块、接口模块的开关，如果都为 True，则代表模块开启
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True
