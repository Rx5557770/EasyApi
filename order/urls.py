from django.urls import path
from .views import AliPayView, AliPayCallBackView

app_name = 'order'
urlpatterns = [
    path('<int:plan_id>/alipay/', AliPayView.as_view(), name='alipay'),
    path('alipay/callback/', AliPayCallBackView.as_view(), name='alipay_callback'),
]