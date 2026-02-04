from django.contrib import admin
from view.models import Docs


@admin.register(Docs)
class DocsAdmin(admin.ModelAdmin):
    list_display = ('id', 'qustion', 'content')


# 设置网站标题和应用标题
admin.site.site_title = "EasyApi后台管理"
admin.site.index_title = "模块管理"
admin.site.site_header = "EasyApi后台管理"