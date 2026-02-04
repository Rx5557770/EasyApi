from django import template
from decouple import config

register = template.Library()

@register.simple_tag
def get_env(key):
    """获取环境变量"""
    try:
        return config(key)
    except:
        return f'无法读取{key}的值'