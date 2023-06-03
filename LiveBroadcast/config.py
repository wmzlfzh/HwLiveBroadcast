# zego项目ID
from concurrent.futures import ThreadPoolExecutor

roomThreadPool = ThreadPoolExecutor(max_workers=20, thread_name_prefix='roomPool')

appID = 1907478231
# zego项目服务器地址
serverUrl = 'wss://webliveroom1907478231-api.imzego.com/ws'

# 虚拟用户比例
ai_ratio = 20

# 在线用户
onlineUser = {}

# 房间聊天信息
imContent = {}


# 创建房间管理数据空间
roomDataManager = {}
