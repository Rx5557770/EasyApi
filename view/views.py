import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views import View

from order.models import Project, Api, Plan, Order
from view.models import Docs
from my_auth.models import UserInfo

from util import apis


# 首页
@require_http_methods(['GET'])
def index(request):
    return render(request, 'view/index.html')

# apihub
class ApiHubView(View):
    def get(self, request, id=None):
        project_list = Project.objects.filter(is_show=True)
        # 未传入id 默认显示
        if id is None:
            api_list = Api.objects.filter(project__in=project_list).order_by('point')
            data = {
                'project_list': project_list,
                'api_list': api_list
            }
            return render(request, 'view/apihub.html', {'data': data})

        # 传入了id
        current_project = get_object_or_404(Project, id=id)
        if not current_project.is_show:
            return HttpResponse('该项目已隐藏不可访问', status=403)

        api_list = Api.objects.filter(project=current_project).filter(is_show=True).order_by('point')

        data = {
            'current_project': current_project,
            'api_list': api_list,
            'project_list': project_list
        }
        return render(request, 'view/apihub.html', {'data': data})


# 套餐
@require_http_methods(['GET'])
def plan(request):
    plan_list = Plan.objects.all()
    return render(request, 'view/plan.html', {'plan_list': plan_list})

# 帮助
@require_http_methods(['GET'])
def help(request):
    docs = Docs.objects.all()
    return render(request, 'view/help.html', {'docs': docs})

# 加入我们
@require_http_methods(['GET'])
def joinus(request):
    return render(request, 'view/joinus.html')


@login_required
def profile(request):
    order_list = Order.objects.filter(profile=request.user.user_info).order_by('-create_date')

    return render(request, 'view/profile.html', {'order_list': order_list})


@method_decorator(csrf_exempt, name='dispatch')
class TodoView(View):
    def verify(self, request):
        token = request.GET.get('token', None)
        if not token:
            return False

        # 验证token格式
        try:
            token = uuid.UUID(token)
        except ValueError:
            return False

        # 当token和接口id同时存在，获取用户信息
        user = get_object_or_404(UserInfo, token=token)
        return user

    def get(self, request, api_id):
        user = self.verify(request)
        if user is None:
            return HttpResponse('参数有误', status=400)

        # 获取接口信息
        api = get_object_or_404(Api, id=api_id)
        # 判断接口方法
        if api.method == 'POST':
            return HttpResponse('请求方法有误', status=204)

        ##### 进入业务逻辑 #####
        user.points = user.points - api.point

        # 如果余额不足
        if user.points < 0:
            return HttpResponse('套餐余额不足', status=401)

        ##### 进入脚本逻辑 #####
        res = apis.runfunc(api.id, None)
        if res.get('code') == 200:
            user.save()
        else:
            return HttpResponse('接口调试失败，不扣取点数', status=501)

        return JsonResponse(res)

    def post(self, request, api_id):
        user = self.verify(request)
        if user is None:
            return HttpResponse('参数有误', status=400)

        # 获取接口信息
        api = get_object_or_404(Api, id=api_id)
        # 判断接口方法
        if api.method == 'GET':
            return HttpResponse('请求方法有误', status=204)

        ##### 进入业务逻辑 #####
        user.points = user.points - api.point
        # 如果余额不足
        if user.points < 0:
            return HttpResponse('套餐余额不足', status=401)

        ##### 进入脚本逻辑 #####
        params:dict = request.POST.dict()
        res = apis.runfunc(api.id, **params)
        if res.get('code') == 200:
            user.save()
        else:
            return HttpResponse('接口调试失败，不扣取点数', status=501)

        return JsonResponse(res)

