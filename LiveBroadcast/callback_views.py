"""
zego回调函数
"""
import json

from django.http import HttpResponse
from commonUtil.http_utils import *


def zego_login_room_api(request):
    """
    登录房间回调api
    :param request:
    :return:
    """
    json_data = json.loads(request.body)
    print('用户登录')
    print(json_data)

    return HttpResponse(json.dumps(None))


def zego_logout_room_api(request):
    """
    用户退出房间API
    :param request:
    :return:
    """

    if request.method == 'POST':
        body = json.loads(request.body)
        print("用户退出")
        print(body)
        rq_data = sp_success(None)
    else:
        rq_data = sp_error(500, '请求异常')
    return HttpResponse(json.dumps(rq_data))


def zego_create_room_api(request):
    """
    创建房间回调api
    :param request:
    :return:
    """
    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)
        rq_data = sp_success(None)
    else:
        rq_data = sp_error(500, '请求异常')
    return HttpResponse(json.dumps(rq_data))


def zego_close_room_api(request):
    """
    关闭房间API
    :param request:
    :return:
    """
    if request.method == 'POST':
        body = json.loads(request.body)
        print("关闭房间")
        print(body)
        rq_data = sp_success(None)
    else:
        rq_data = sp_error(500, '请求异常')
    return HttpResponse(json.dumps(rq_data))


def zego_create_stream_api(request):
    """
    创建流API
    :param request:
    :return:
    """
    if request.method == 'POST':
        body = json.loads(request.body)
        print("创建流")
        print(body)
        rq_data = sp_success(None)
    else:
        rq_data = sp_error(500, '请求异常')
    return HttpResponse(json.dumps(rq_data))


def zego_close_stream_api(request):
    """
    关闭流API
    :param request:
    :return:
    """
    if request.method == 'POST':
        body = json.loads(request.body)
        print("关闭流")
        print(body)
        rq_data = sp_success(None)
    else:
        rq_data = sp_error(500, '请求异常')
    return HttpResponse(json.dumps(rq_data))