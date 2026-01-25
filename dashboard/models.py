from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User

Method_TYPE = [
    ('GET', 'GET'),
    ('POST', 'POST'),
]

# 套餐
class Plan(models.Model):
    name = models.CharField(max_length=50, verbose_name='套餐名')
    # description = models.TextField(max_length=100, null=True, blank=True, verbose_name='套餐介绍')
    price = models.IntegerField(validators=[MinValueValidator(0)], default=0, verbose_name='价格')
    points = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='点数')

    class Meta:
        db_table = 'plan'
        verbose_name = '套餐信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



# 项目
class Project(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='项目名')
    # icon = models.ImageField(upload_to='projects_icon', null=True, blank=True, verbose_name='上传图标')
    is_show = models.BooleanField(default=True, verbose_name='显示')

    class Meta:
        db_table = 'project'
        verbose_name = '项目信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 项目下的api
class Api(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='apis', verbose_name='项目名')

    name = models.CharField(max_length=50, verbose_name='接口名')
    method = models.CharField(choices=Method_TYPE, max_length=10, default='GET', verbose_name='请求方法')
    req_data = models.TextField(default='', null=True, blank=True, verbose_name='请求体')
    res_data = models.TextField(verbose_name='响应体')

    description = models.TextField(max_length=100, null=True, blank=True, verbose_name='接口介绍')
    point = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='所需点数')
    is_show = models.BooleanField(default=True, verbose_name='显示')

    class Meta:
        db_table = 'api'
        verbose_name = '接口信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.project.name} - {self.name}"