import random
import time

from LiveBroadcast.models import LbRoom
from LiveBroadcast.config import roomDataManager, roomThreadPool


class RoomManager:
    """
    房间管理器
    """

    def __init__(self, room: LbRoom):
        # 房间ID
        self.room_id = room.roomID
        # 直播名字
        self.room_name = room.roomName
        # 讲师名字
        self.teacher = room.teacher
        # 视频流ID
        self.video_id = room.videoID
        # 音频流ID
        self.audio_id = room.screenID
        # 真实用户字典(不重复)
        self.real_user = {}
        # 虚拟用户字典(不重复)
        self.virtually_user = {}
        # 虚实用户比例, 默认1:2
        self.rv_ratio = 10
        # 聊天信息列表
        self.chat_list = []
        # 公告列表
        self.notice_list = [room.notice]
        # 直播状态
        self.status = room.status
        # 开播时间
        self.start_time = None
        # 停播时间
        self.stop_time = None

    def user_login(self, role, user_id, user_name):
        """
        用户登录
        :return:
        """
        try:
            if self.real_user.get(user_id) is None:
                self.real_user[user_id] = {
                    'role': role,
                    'userID': user_id,
                    'userName': user_name
                }
                # 添加虚拟用户
                roomThreadPool.submit(add_virtually_user, self.room_id, self.rv_ratio)
        except Exception as ex:
            print(str(ex))

    def user_logout(self, user_id):
        """
        用户退出
        :param user_id:
        :return:
        """
        try:
            self.real_user.pop(user_id)
        except Exception as ex:
            print(str(ex))

    def send_chat(self, user_id, content):
        """
        发送聊天信息
        :param user_id:
        :param content:
        :return:
        """
        self.chat_list.append({
            'userID': user_id,
            'content': content
        })

    def close_room(self):
        """
        房间关闭
        :return:
        """
        self.real_user.clear()
        self.virtually_user.clear()
        self.chat_list = []
        self.notice_list = []
        self.status = False

    def change_status(self):
        """
        状态变更
        :return:
        """
        if self.teacher not in self.real_user:
            self.status = False
            self.close_room()
        else:
            self.status = True

    def start_play(self):
        """
        开播操作
        :return:
        """
        self.status = True
        self.start_time = time.time()
        room = LbRoom.objects.get(roomID=self.room_id)
        room.status = True
        room.save()

    def stop_play(self):
        """
        停播操作
        :return:
        """
        self.status = False
        self.stop_time = time.time()
        self.real_user.clear()
        self.chat_list.clear()
        room = LbRoom.objects.get(roomID=self.room_id)
        room.status = False
        room.save()

        return {
            "startTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start_time)),
            "stopTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.stop_time)),
            "duration": round(int(self.stop_time - self.start_time)/60, 0),
            "realNum": len(self.real_user),
            "realUser": list(self.real_user.values()),
            "vUserNum": len(self.virtually_user)
        }

    def add_virtually_user(self):
        """
        添加虚拟用户
        :return:
        """
        real_num = len(self.real_user)
        v_num = len(self.virtually_user)
        print(real_num)
        print(v_num)
        add_num = real_num * self.rv_ratio - v_num
        print(add_num)
        # if add_num > 0:
        #     roomThreadPool.submit()


def room_monitor_thread():
    """
    房间监控线程
    :return:
    """
    while True:
        rooms = LbRoom.objects.all()
        for room in rooms:
            if roomDataManager.get(room.roomID) is None:
                roomDataManager[room.roomID] = RoomManager(room)

        for room_id in roomDataManager:
            rooms = LbRoom.objects.filter(roomID=room_id)
            if rooms.count() == 0:
                roomDataManager.pop(room_id)
        time.sleep(30)


# def virtually_user_change(room_id, ly):
#     """
#     虚拟人数变更
#     :param room_id:
#     :param ly: 1是加，0是减
#     :return:
#     """
#     virtually_user = roomDataManager[room_id].virtually_user
#     rv_ratio = roomDataManager[room_id].rv_ratio
#     if ly == 1:
#         for i in range(rv_ratio):
#             sleep_num = random.randint(1, 2)
#             time.sleep(sleep_num)
#             v_account = str(random.randint(104000, 109999))
#             v_user = {
#                 'role': 2,
#                 'userID': v_account,
#                 'userName': ''
#             }
#             virtually_user[v_account] = v_user
#     if ly == 0:
#         for i in range(int(rv_ratio)):
#             sleep_num = random.randint(1, 3)
#             time.sleep(sleep_num)
#             virtually_user.popitem()


def add_virtually_user(room_id, add_num):
    """
    :param room_id:
    :param add_num:
    :return:
    """
    virtually_user = roomDataManager[room_id].virtually_user
    for i in range(add_num):
        sleep_num = random.randint(1, 2)
        time.sleep(sleep_num)
        v_account = str(random.randint(104000, 109999))
        v_user = {
            'role': 2,
            'userID': v_account,
            'userName': ''
        }
        virtually_user[v_account] = v_user
