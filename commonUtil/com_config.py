"""
配置
"""
# 线程池
from concurrent.futures import ThreadPoolExecutor

threadPool = ThreadPoolExecutor(max_workers=100, thread_name_prefix='threadPool')

# 在线用户字典
online_user = {}

# 虚拟用户比例
ai_ratio = 10

# 虚拟用户列表
ai_user = {}

# 聊天信息
cha_info = []
