from django.contrib import admin
from order.models import Plan, Project, Api, Order

class ApiInline(admin.StackedInline):
    model = Api
    extra = 2


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'points')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_show')
    inlines = [ApiInline]


# @admin.register(Api)
# class ApiAdmin(admin.ModelAdmin):
#     list_display = ('id', 'project', 'name', 'point', 'is_show')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def getuser(self, obj):
        return obj.profile.user.username
    list_display = ('id', 'order_sn', getuser, 'pay_type', 'plan', 'create_date', 'update_date', 'state', 'trade_no', 'pay_time', 'total_amount')
