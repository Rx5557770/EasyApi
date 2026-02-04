from django.core.validators import MinValueValidator
from django.db import models


# 套餐
class Plan(models.Model):
    name = models.CharField(max_length=50, verbose_name='套餐名')
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)], default=0, verbose_name='价格')
    points = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='点数')

    class Meta:
        db_table = 'plan'
        verbose_name = '套餐管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 项目
class Project(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='项目名')
    # icon = models.ImageField(upload_to='projects_icon', null=True, blank=True, verbose_name='上传图标')
    is_show = models.BooleanField(default=True, verbose_name='显示状态')

    class Meta:
        db_table = 'project'
        verbose_name = '项目管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 项目下的api
class Api(models.Model):
    Method_TYPE = [
        ('GET', 'GET'),
        ('POST', 'POST'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='apis', verbose_name='项目名')

    name = models.CharField(max_length=50, verbose_name='接口名')
    method = models.CharField(choices=Method_TYPE, max_length=10, default='GET', verbose_name='请求方法')
    req_data = models.TextField(default='', null=True, blank=True, verbose_name='请求体')
    res_data = models.TextField(verbose_name='响应体')

    description = models.TextField(max_length=100, null=True, blank=True, verbose_name='接口介绍')
    point = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='所需点数')
    is_show = models.BooleanField(default=True, verbose_name='显示状态')

    class Meta:
        db_table = 'api'
        verbose_name = '接口管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.project.name} - {self.name}"


# 订单表
class Order(models.Model):
    Pay_TYPE = [
        ('alipay', '支付宝'),
        ('wxpay', '微信')
    ]

    order_state = [
        (False, '未支付'),
        (True, '已支付'),
    ]

    order_sn = models.CharField(max_length=100, unique=True, verbose_name='系统订单编号')
    profile = models.ForeignKey('my_auth.UserInfo', on_delete=models.CASCADE, verbose_name='下单用户')
    pay_type = models.CharField(max_length=10, choices=Pay_TYPE, verbose_name='支付方式')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, verbose_name='套餐')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    state = models.BooleanField(choices=order_state, default=False, verbose_name='支付状态')

    # 支付宝订单号
    trade_no = models.CharField(max_length=100, verbose_name='支付订单编号')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    total_amount = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name='支付金额')

    class Meta:
        db_table = 'order'
        verbose_name = '订单管理'
        verbose_name_plural = verbose_name