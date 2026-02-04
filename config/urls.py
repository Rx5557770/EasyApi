"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from view import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 认证
    path('auth/', include('my_auth.urls')),
    # 订单与支付
    path('order/', include('order.urls')),

    # 主页面内容
    path('', views.index, name='index'),
    path('apihub/', views.ApiHubView.as_view(), name='apihub'),
    path('apihub/item/<int:id>', views.ApiHubView.as_view(), name='apihub_oneProject'),
    path('plan/', views.plan, name='plan'),
    path('help/', views.help, name='help'),
    path('joinus/', views.joinus, name='joinus'),
    path('profile/', views.profile, name='profile'),

    # 本地脚本
    path('apis/<int:api_id>', views.TodoView.as_view())
]
