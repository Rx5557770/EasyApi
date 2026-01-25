from django.contrib import admin
from .models import Plan, Project, Api
from my_auth.models import UserInfo

class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'points')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_show')

class ApiAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'name', 'point', 'is_show')

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'points', 'token')

admin.site.register(Plan, PlanAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Api, ApiAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
