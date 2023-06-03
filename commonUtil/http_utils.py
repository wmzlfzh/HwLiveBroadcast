"""
http相关工具
"""


def sp_success(data):
    return {
        'code': 200,
        'msg': 'success',
        'data': data
    }


def sp_error(code, msg):
    return {
        'code': code,
        'msg': msg,
        'data': None
    }
