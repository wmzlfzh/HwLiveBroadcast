import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from LiveBroadcast.config import appID, serverUrl
from LiveBroadcast.models import LbRoom
from commonUtil import zego_config as zc, zego_token as zt
from commonUtil import com_config as cc
from LiveBroadcast import config as lc
# Create your views here.

from commonUtil import http_utils
from commonUtil.http_utils import *


def goto_room_html(request):
    app_id = 19002182
    user_id = "200012"
    token_info = zt.get_user_base_token(user_id)
    data_dic = {
        "app_id": app_id,
        "userID": user_id,
        "s_secret": zc.ServerSecret,
        "token": token_info.token,
        "server_url": zc.ServerUrl
    }
    return render(request, 'room.html', data_dic)


@login_required(login_url='/login.html')
def goto_anchor_html(request):
    """
    主播页面请求
    :param request: 请求对象
    :return:
    """
    user = request.user
    room_id = request.GET.get('roomID')
    user_id = user.username
    real_user = lc.roomDataManager[room_id].real_user
    real_user[user_id] = {
        'role': 2,
        'userID': user_id,
        'userName': ''
    }
    lc.roomDataManager[room_id].teacher = user.username

    if user.is_staff:
        return render(request, 'anchor.html')
    else:
        return redirect('/player/')


def get_online_user_view(request):
    """
    获取在线人数
    :param request:
    :return:
    """
    online = cc.online_user
    user_list = list(online.values())
    return HttpResponse(json.dumps(user_list))


def get_chat_info_view(request):
    chat_info = cc.cha_info[-14:]
    return HttpResponse(json.dumps(chat_info))


def send_chat_info_view(request):
    """
    发送聊天信息
    :param request:
    :return:
    """
    content = request.GET.get("content")
    chat_info = cc.cha_info
    user = request.user
    send_info = {
        "userId": user.username,
        "userName": user.first_name,
        "content": content
    }
    chat_info.append(send_info)
    send_data = {
        "code": 200,
        "msg": "发送成功"
    }
    return HttpResponse(json.dumps(send_data))


def get_user_token(request):
    """
    获取用户视频Token
    :param request:
    :return:
    """
    user = request.user
    token = zt.get_user_base_token(user.username)
    send_data = {
        "code": 200,
        "msg": "发送成功",
        "token": token,
        "userId": user.username
    }
    return HttpResponse(json.dumps(send_data))


"""
zego回调函数
"""


def zego_user_callback_api(request):
    """
    用户状态回调
    :param request:
    :return:
    """
    try:
        if request.method == 'POST':
            body = json.loads(request.body)
            event = body['event']
            room_id = body['room_id']
            user_id = body['user_account']
            user_name = body['user_nickname']
            room_manager = lc.roomDataManager[room_id]
            if event == 'room_login':
                room_manager.real_user[user_id] = {
                    'userID': user_id,
                    'userName': user_name
                }
            elif event == 'room_logout':
                room_manager.real_user.pop(user_id)
            elif event == 'room_create':
                pass
            elif event == 'room_close':
                room_manager.close_room()
            else:
                pass
        rq_data = sp_success(None)
    except Exception as ex:
        print(str(ex))
        rq_data = sp_error(500, '请求异常')
    return HttpResponse(json.dumps(rq_data))


"""
admin后台请求
"""


def get_admin_config_view(request):
    """
    获取参数
    :param request:
    :return:
    """
    try:
        room_id = request.GET.get('roomID')
        room = LbRoom.objects.filter(roomID=room_id)[0]
        user = request.user
        token = zt.get_user_base_token(user.username)
        config = {
            'roomID': room.roomID,
            'roomName': room.roomName,
            'audioID': room.screenID,
            'videoID': room.videoID,
            'token': token,
            'userID': user.username,
            'appID': appID,
            'server': serverUrl,
        }
        rq_data = http_utils.sp_success(config)
    except Exception as ex:
        print(str(ex))
        rq_data = http_utils.sp_error(500, '获取配置异常')
    return HttpResponse(json.dumps(rq_data))


def start_admin_play_view(request):
    """
    开播视图
    :param request:
    :return:
    """
    user = request.user
    room_id = request.GET.get('roomID')

    manager = lc.roomDataManager[room_id]

    manager.user_login(0, user.username, user.first_name)

    manager.start_play()

    if user.is_staff:
        return render(request, 'anchor.html')
    else:
        return redirect('/player/')


def stop_admin_play_api(request):
    """
    停播操作
    :param request:
    :return:
    """
    try:
        room_id = request.GET.get('roomID')
        # 停播操作
        sp_data = lc.roomDataManager[room_id].stop_play()
    except Exception as ex:
        print(str(ex))
        sp_data = {}
    return render(request, 'stop_play.html', sp_data)


"""
下面编写的全部是前后分离直播端使用的函数
"""


def login_player_view(request):
    """
    登录接口
    :return:
    """
    if request.method == 'POST':
        rq_data = json.loads(request.body)
        username = rq_data.get('act')
        user_list = User.objects.filter(username=username)
        sp_data = http_utils.sp_error(300, '账号密或码错误')
        if user_list.count() == 1:
            password = rq_data.get('pwd')
            user = user_list[0]
            user1 = authenticate(request, username=username, password=password)
            login(request, user1)
            if user.check_password(password):
                data = {
                    "act": user.username,
                    'pwd': user.password
                }
                sp_data = http_utils.sp_success(data)
    else:
        sp_data = http_utils.sp_error(401, '请求类型错误')
    return HttpResponse(json.dumps(sp_data))


def get_room_list_api(request):
    """
    获取房间列表接口
    :param request:
    :return:
    """
    room_dict = lc.roomDataManager
    rq_data = []
    for key in room_dict:
        room = room_dict[key]
        data = {
            'url': 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
            'roomID': room.room_id,
            'roomName': room.room_name,
            'teacher': room.teacher,
            'status': room.status,
        }
        rq_data.append(data)
    return HttpResponse(json.dumps(rq_data))


def get_repeat_login_api(request):
    """
    重复登录验证,重复返回False
    :param request:
    :return:
    """
    room_id = request.GET.get('roomID')
    user_id = request.GET.get('userID')
    room = lc.roomDataManager.get(room_id)
    real_user = room.real_user
    if real_user.get(user_id) is None:
        rq_data = sp_success(True)
    else:
        rq_data = sp_success(False)
    return HttpResponse(json.dumps(rq_data))


def close_refresh_api(request):
    """
    挂载或者刷新页面
    :param request:
    :return:
    """
    try:
        room_id = request.GET.get('roomID')
        user_id = request.GET.get('userID')
        op = request.GET.get('op')
        room = lc.roomDataManager.get(room_id)
        if op == 'close':
            print(f'{user_id}: 离开直播间-{room_id}')
        if op == 'add':
            print(f'{user_id}: 进入直播间-{room_id}')
            room.user_login(2, user_id, '会员')
    except Exception as ex:
        print(str(ex))
    return HttpResponse(json.dumps(sp_success(None)))


def get_user_player_config_view(request):
    """
    获取用户直播信息
    :return:
    """
    try:
        room_id = request.GET.get('roomID')
        user_id = request.GET.get('userID')
        user = User.objects.get(username=user_id)
        room = LbRoom.objects.get(roomID=room_id)
        token = zt.get_user_base_token(user.username)
        data = {
            'appID': appID,
            'server': serverUrl,
            'userID': user_id,
            'name': user.first_name,
            'token': token,
            'roomID': room.roomID,
            'roomName': room.roomName,
            'audioID': room.screenID,
            'videoID': room.videoID,
            'notice': room.notice
        }
        config = http_utils.sp_success(data)
    except Exception as ex:
        print(str(ex))
        config = http_utils.sp_success(None)
    return HttpResponse(json.dumps(config))


def get_room_chat_content(request):
    """
    获取房间聊天数据
    :param request:
    :return:
    """
    try:
        room_id = request.GET.get('roomID')
        chat = lc.roomDataManager[room_id].chat_list
    except Exception as ex:
        print(str(ex))
        chat = []
    return HttpResponse(json.dumps(chat))


def send_room_chat_content(request):
    """
    发送房间聊天信息
    :param request:
    :return:
    """
    room_id = request.GET.get('roomID')
    user_id = request.GET.get('userID')
    content = request.GET.get('content')
    chat = lc.roomDataManager[room_id].chat_list
    data = {
        'role': 2,
        'userID': user_id,
        'content': content
    }
    chat.append(data)
    return HttpResponse(json.dumps(data))


def get_room_online_user(request):
    """
    获取房间用户
    :param request:
    :return:
    """
    try:
        room_id = request.GET.get('roomID')

        real_user = lc.roomDataManager[room_id].real_user
        virtually_user = lc.roomDataManager[room_id].virtually_user
        real_user.update(virtually_user)
        rq_data = list(real_user.values())
    except Exception as ex:
        print(str(ex))
        rq_data = []
    return HttpResponse(json.dumps(rq_data))
