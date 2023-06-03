"""
URL configuration for HwLiveBroadcast project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from LiveBroadcast import views
from HwLiveBroadcast import views as c_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', c_views.test_view),

    # 公共路由
    path('login.html/', c_views.login_html_view),
    path('main/', c_views.main_views),
    path('login/', c_views.login_view),
    path('logout/', c_views.login_view),

    # 直播路由
    path('online/', views.get_online_user_view),
    path('chatInfo/', views.get_chat_info_view),
    path('sendChat/', views.send_chat_info_view),
    path('token/', views.get_user_token),
]

urlpatterns += [
    path('live/', include('LiveBroadcast.urls'))
]

