from django.contrib import admin
from django.utils.html import format_html

from LiveBroadcast.models import *
# Register your models here.

admin.site.site_title = '飞腾速播'
admin.site.site_header = '飞腾速播'
admin.site.index_title = '首页'


@admin.register(LbRoom)
class LbRoomAdmin(admin.ModelAdmin):
    """
    直播间admin
    """
    def buttons(self, obj):
        button_html = f'<a target="_blank"  href="/live/admin/start/?roomID={obj.roomID}">开播</a>' \
                      f'&nbsp&nbsp&nbsp&nbsp'\
                      f'<a href="/live/admin/stop?roomID={obj.roomID}">下播</a>'
        return format_html(button_html)
    buttons.short_description = "操作"

    list_display = ['roomID', 'roomName', 'screenID', 'videoID', 'status', 'buttons']
    fields = ['roomName', 'teacher', 'notice', 'remarks']


@admin.register(RoomNotice)
class RoomNoticeAdmin(admin.ModelAdmin):
    """
    公告
    """
    list_display = ['roomID', 'content']
    fields = ['roomID', 'content', 'remarks']
