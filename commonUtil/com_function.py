"""
公共函数
"""
import random
import time

from commonUtil import com_config as cc


def add_ai_user():
    """
    添加虚拟用户
    :return:
    """
    add_num = cc.ai_ratio
    for i in range(add_num):
        num = random.randint(1, 3)
        time.sleep(num)
        ai_account = str(random.randint(10100000, 10999999))
        ai_info = {
            "userId": "（观众）" + ai_account,
            "userName": ""
        }
        cc.online_user[ai_account] = ai_info


def start_add_ai_user_thread():
    """
    启动线程添加虚拟用户
    :return:
    """
    cc.threadPool.submit(add_ai_user)

