from django.core.validators import MinValueValidator
from django.db import models


# 帮助文档
class Docs(models.Model):
    qustion = models.CharField(max_length=50, verbose_name='问题')
    content = models.TextField(verbose_name='内容')

    class Meta:
        db_table = 'docs'
        verbose_name = '文档管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.qustion}"
