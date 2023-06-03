"""
zego相关配置
"""

# 项目ID,作为项目的唯一标识
AppID = 1907478231

# 作为项目的鉴权密钥，在SDK中进行配置
AppSign = '07a41999a71b00a58f348481fae5c464b21467ec3f65d8b759e3a5f2531c120a'

# 用于后台服务回调接口的鉴权校验
CallbackSecret = '07a41999a71b00a58f348481fae5c464'

# 用于后台服务请求接口的鉴权校验
ServerSecret = '9fe2fa11d3d4889e11ebece68d47bd3c'

# 与服务器的WebSocket通信地址，在SDK中进行配置，适用于Web和小程序
ServerUrl = 'wss://webliveroom1907478231-api.imzego.com/ws'

# 备用的服务器WebSocket通讯地址
BackUpServerUrl = 'wss://webliveroom1907478231-api-bak.imzego.com/ws'

# token 的有效时长，单位：秒
effective_time = 86400
