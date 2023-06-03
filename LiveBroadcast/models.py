import random

from django.db import models

# Create your models here.


class CommonField(models.Model):
    """
    公共字段
    """
    createTime = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    remarks = models.TextField(verbose_name='描述')

    class Meta:
        abstract = True


def random_screen_id():
    """
    随机screenID
    :return:
    """
    return str(random.randint(10000000, 10999999))


def random_room_id():
    """
    随机直播间ID
    :return:
    """
    return f'room' + str(random.randint(104000, 109999))


def random_video_id():
    """
    随机screenID
    :return:
    """
    return str(random.randint(10000000, 10999999))


class LbRoom(CommonField):
    """
    直播间
    """
    roomID = models.CharField(max_length=50, default=random_room_id, verbose_name='直播间ID')
    roomName = models.CharField(max_length=250, default='', verbose_name='直播间名字')
    teacher = models.CharField(max_length=50, verbose_name='直播老师')
    screenID = models.CharField(max_length=100, default=random_screen_id, verbose_name='远程桌面流ID')
    videoID = models.CharField(max_length=100, default=random_video_id, verbose_name='视频流ID')
    status = models.BooleanField(default=False, verbose_name='开播状态')
    notice = models.TextField(default='', verbose_name='公告')

    def __str__(self):
        return self.roomID

    class Meta:
        verbose_name = '直播间'
        verbose_name_plural = verbose_name


def get_range():
    return str(random.randint(104000, 109999))


class RoomNotice(CommonField):
    """
    直播公告
    """
    roomID = models.CharField(max_length=50, verbose_name='直播间ID')
    content = models.TextField(default='', verbose_name='内容')

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = verbose_name
