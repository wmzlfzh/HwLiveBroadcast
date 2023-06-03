"""
工具函数
"""
import random
import time

from commonUtil import com_config as cc
from LiveBroadcast import config


def online_user(room_id, user_id, role=2):
    """
    用户上线
    :param room_id: 房间ID
    :param user_id: 用户ID
    :param role: 组别(默认2) 0、讲师 1、管理员 2、普通用户
    :return:
    """
    room = config.onlineUser.get(room_id)
    if room is None:
        room = config.onlineUser[room_id] = {
            'real': {},
            'ai': {}
        }
    room['real'][user_id] = {
        'role': role,
        'userID': user_id,
        'userName': ''
    }
    # 多线程随机间隔添加用户
    cc.threadPool.submit(thread_add_user, room_id)


def thread_add_user(room_id, role=2):
    """
    线程间隔添加指定比例用户
    :param room_id: 房间ID
    :param role: 组别(默认2) 0、讲师 1、管理员 2、普通用户
    :return:
    """
    ai_ratio = config.ai_ratio
    real_dict = config.onlineUser[room_id]['real']
    ai_dict = config.onlineUser[room_id]['ai']
    add_num = len(real_dict) * ai_ratio - len(ai_dict)
    for i in range(add_num):
        sleep_num = random.randint(1, 3)
        time.sleep(sleep_num)
        ai_account = str(random.randint(101000, 199999))
        ai_info = {
            'role': role,
            'userID': ai_account,
            'userName': ''
        }
        config.onlineUser[room_id]['ai'][ai_account] = ai_info


def online_user_monitor():
    """
    在线用户监控
    :return:
    """
    while True:
        time.sleep(2)
        add_del = random.randint(0, 1)
        # 判断是添加还是删除
        if add_del == 0:
            for room_id in config.onlineUser.keys():
                config.onlineUser[room_id].popitem()
        else:
            for room_id in config.onlineUser.keys():
                ai_account = str(random.randint(101000, 199999))
                ai_info = {
                    'role': 2,
                    'userID': ai_account,
                    'userName': ''
                }
                config.onlineUser[room_id]['ai'][ai_account] = ai_info

