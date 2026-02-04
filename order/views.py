from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from order.models import Plan, Order
from my_auth.models import UserInfo
from util import pay

class AliPayView(View):
    def get(self, request, plan_id):
        # 获取套餐信息
        plan = get_object_or_404(Plan, pk=plan_id)
        # 初始化支付
        alipay = pay.AliPay()

        # 获取时间
        current_time = timezone.now()
        formatted_time = current_time.strftime("%y%m%d%H%M%S")

        # 支付订单号
        out_trade_no = f"pay{formatted_time}"
        # 总金额
        total_amount = float(plan.price)

        ##### 创建订单 #####
        try:
            Order.objects.create(order_sn=out_trade_no, profile=UserInfo.objects.get(user=request.user), pay_type='alipay', plan=plan, trade_no=out_trade_no, total_amount=total_amount)
        except Exception:
            return JsonResponse({
                'code':500,
                'msg': '订单创建失败'
            })
        # 调用支付
        res = alipay.TradePagePay(out_trade_no=out_trade_no, total_amount=total_amount, subject=plan.name, product_code='FAST_INSTANT_TRADE_PAY')
        # print('调用支付结束，等待通知')
        return redirect(res)

@method_decorator(csrf_exempt, name='dispatch')
class AliPayCallBackView(View):
    def post(self, request):
        # 初始化支付
        alipay = pay.AliPay()
        params:dict = request.POST.dict()
        try:
            # 去除sign 和 sign_type
            sign = params.pop('sign')
            del params['sign_type']
            unsigned_string = alipay.get_sign(params)
        except KeyError:
            return HttpResponse('fail', status=400)

        ###### 进行校验 ######
        if not alipay.verify_sign(unsigned_string, sign):
            return HttpResponse('fail', status=400)

        try:
            order = Order.objects.get(order_sn=params.get('out_trade_no'))
        except:
            return HttpResponse('fail', status=400)
        if str(params.get('total_amount')) != str(order.total_amount):
            return HttpResponse('fail', status=400)

        if params.get('seller_id') != alipay.alipay_client_config.seller_id:
            return HttpResponse('fail', status=400)
        if params.get('app_id') != alipay.alipay_client_config.app_id:
            return HttpResponse('fail', status=400)

        ###### 校验结束 ######
        # 更改订单状态
        out_trade_no = params.get('out_trade_no')
        order = Order.objects.get(trade_no=out_trade_no)
        order.state = True
        order.pay_time = timezone.now()
        order.save()

        # 更改用户point
        userinfo = order.profile
        userinfo.points += order.plan.points
        userinfo.save()
        return HttpResponse('success')