import uuid

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from dashboard.models import Plan


# 扩展User表
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info', verbose_name='用户')
    # 每个用户都有套餐字段，值可为空
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_info', verbose_name='套餐名')

    points = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='点数')
    token = models.UUIDField(unique=True, default=uuid.uuid4)

    class Meta:
        db_table = 'user_info'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
