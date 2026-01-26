import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods


from .models import Project, Api, Plan
from my_auth.models import UserInfo

from util import apis


# 首页
@require_http_methods(['GET'])
def index(request):
    return render(request, 'index.html')

# apihub
@require_http_methods(['GET'])
def apihub(request, id=None):
    project_list = Project.objects.filter(is_show=True)
    # 传入了项目id
    if id:
        current_project = get_object_or_404(Project, id=id)
        if not current_project.is_show:
            return HttpResponse('该项目已隐藏不可访问', status=403)

        api_list = Api.objects.filter(project=current_project).filter(is_show=True).order_by('point')

        data = {
            'current_project': current_project,
            'api_list': api_list,
            'project_list': project_list
        }
        return render(request, 'apihub.html', {'data': data})


    # 未传入id 默认显示
    api_list = Api.objects.filter(project__in=project_list).order_by('point')
    data = {
        'project_list': project_list,
        'api_list': api_list
    }
    return render(request, 'apihub.html', {'data': data})


# 套餐
@require_http_methods(['GET'])
def plan(request):
    plan_list = Plan.objects.all()
    return render(request, 'plan.html', {'plan_list': plan_list})

# 帮助
@require_http_methods(['GET'])
def help(request):
    return render(request, 'help.html')

# 加入我们
@require_http_methods(['GET'])
def joinus(request):
    return render(request, 'joinus.html')


@login_required
def profile(request):
    return render(request, 'profile.html')


# 获取api的id并执行脚本，再返回内容
@require_http_methods(['GET', 'POST'])
def todo(request, api_id):
    token = request.GET.get('token')
    if not token:
        return HttpResponse("缺少token参数",status=400)
    if not api_id:
        return HttpResponse("缺少接口ID参数", status=400)

    # 验证token格式
    try:
        token = uuid.UUID(token)
    except ValueError:
        return HttpResponse('token错误', status=401)

    # 当token和接口id同时存在，获取用户信息
    user = get_object_or_404(UserInfo, token=token)

    # 获取接口信息
    api = get_object_or_404(Api, id=api_id)
    user.points = user.points - api.point

    # 如果余额不足
    if user.points < 0:
        return HttpResponse('套餐余额不足', status=402)


    # 执行脚本逻辑
    res = runscript(api.id)

    if res.get('code') == 200:
        user.save()
    else:
        return HttpResponse('接口调试失败，不扣取点数', status=500)
    return JsonResponse(res)


def runscript(api_id):
    # 根据id运行脚本
    if api_id == 1:
        res = apis.dosomething()

    if api_id == 2:
        res = apis.dosomething2()
    return res