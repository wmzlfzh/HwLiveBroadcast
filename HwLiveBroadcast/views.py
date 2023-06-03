import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect


def login_html_view(request):
    """
    登录页
    :param request:
    :return:
    """
    next_url = request.GET.get('next')

    return_data = {
        "next": next_url
    }
    user_agent = request.headers.get('User-Agent')
    if "Android" in user_agent or "iPhone" in user_agent:
        return render(request, 'login/login-mobile.html', return_data)
    else:
        return render(request, 'login/login.html', return_data)


def login_view(request):
    """
    登录请求
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next_url = request.POST.get('next', '')
        # 与数据库中的用户名和密码比对，django默认保存密码是以哈希形式存储，并不是明文密码，这里的password验证默认调用的是User类的check_password方法，以哈希值比较。
        user = authenticate(request, username=username, password=password)
        # 验证如果用户不为空
        if user is not None:
            # login方法登录
            login(request, user)
            rq_url = next_url if len(next_url) > 5 else '/main.html/'
            return redirect(rq_url)
        else:
            return redirect('/login.html/')
    return render(request, 'login/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'login/login.html')


@login_required(login_url='/login.html')
def main_views(request):
    """
    主页
    :param request:
    :return:
    """
    return render(request, 'main.html')


def test_view(request):
    user_agent = request.headers.get('User-Agent')
    if "Android" in user_agent or "iPhone" in user_agent:
        print("安卓手机")
    else:
        print("PC")
    print(user_agent)
    data = {
        "code": 200,
        "msg": "PC"
    }
    return HttpResponse(json.dumps(data))
