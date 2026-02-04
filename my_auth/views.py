import uuid

from django import views
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .forms import LoginForm, RegisterForm
from .models import UserInfo


class LoginView(views.View):
    def get(self,request):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self,request):
        form = LoginForm(request.POST)

        # 表单通过
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # 认证
            user = authenticate(username=email, password=password)
            if user is None:
                form.add_error(None, '邮箱或密码错误')
                return render(request, 'auth/login.html', {'form': form})


            # 认证通过，进行登录并跳转
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'auth/login.html', {'form': form})

class RegisterView(views.View):
    def get(self,request):
        form = RegisterForm()
        return render(request, 'auth/register.html', {'form': form})
    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # 创建用户
            user = User.objects.create_user(username=username, password=password)
            # 关联info表的信息
            userinfo = UserInfo.objects.create(user=user)
            userinfo.save()

            # 跳转到登录页面
            return redirect('auth:login')
        else:
            return render(request, 'auth/register.html', {'form': form})

@login_required
@require_http_methods(['POST'])
def loggout(request):
    logout(request)
    return redirect('/')

@login_required
@require_http_methods(['POST'])
def change_token(request):
    user = request.user
    user.user_info.token = uuid.uuid4()
    user.user_info.save()
    return render(request, 'profile.html')

