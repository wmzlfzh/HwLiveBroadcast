from django.urls import path

from LiveBroadcast.roomUtils import room_monitor_thread
from LiveBroadcast.views import *
from LiveBroadcast.callback_views import *
from LiveBroadcast.config import roomThreadPool

urlpatterns = [
    path('config/', get_user_player_config_view),
    path('login/', login_player_view),
    path('chat/', get_room_chat_content),
    path('chat/send/', send_room_chat_content),
    path('online/', get_room_online_user),
    path('room/', get_room_list_api),
    path('admin/config/', get_admin_config_view),
    path('admin/start/', start_admin_play_view),
    path('admin/stop/', stop_admin_play_api),
    path('room/callback/', zego_user_callback_api),
    path('repeat/login/', get_repeat_login_api),
    path('refresh/', close_refresh_api),

    path('room/create/', zego_login_room_api),
    path('room/close/', zego_close_room_api),
    path('room/login/', zego_create_room_api),
    path('room/logout/', zego_logout_room_api),
    path('stream/create/', zego_create_stream_api),
    path('stream/close/', zego_close_stream_api)
]

# 启动房间监控线程
roomThreadPool.submit(room_monitor_thread)

