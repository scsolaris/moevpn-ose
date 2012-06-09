# coding=utf-8
# Chon<chon219@gmail.com>

from django.contrib import admin
from models import *
from moevpn.utils import make_order_paid

class AccountAdmin(admin.ModelAdmin):
  list_display = ('user','username','creation','quota_cycle','plan','cycle','promotion','active','enabled')
  list_filter = ('quota_cycle','plan','cycle','active','enabled',)
  raw_id_fields = ('user',)

class LogAdmin(admin.ModelAdmin):
  list_display = ('account','log_id','username','start_time','end_time','bytes_received','bytes_sent','local_ip','remote_ip','proto','status')
  list_filter = ('status','start_time','proto')
  ordering = ('-start_time',)

class OrderAdmin(admin.ModelAdmin):
  list_display = ('user','order_id','order_time','username','plan','cycle','price','discount','promotion','status')
  list_filter = ('plan','cycle','status','order_time',)
  ordering = ('-order_time',)
  def make_paid(self,request,queryset):
    for order in queryset:
	make_order_paid(order.order_id)
    self.message_user(request,"Successful!")
  make_paid.short_description = "Make selected orders as paid"
  actions = [make_paid]

class CycleAdmin(admin.ModelAdmin):
  list_display = ('name','detail','quota','discount')

class PlanAdmin(admin.ModelAdmin):
  list_display = ('name','detail','quota','price','discount')

class PromotionAdmin(admin.ModelAdmin):
  list_display = ('code','price','plan','discount','register_limit','order_limit')

admin.site.register(Account,AccountAdmin)
admin.site.register(Log,LogAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Cycle,CycleAdmin)
admin.site.register(Plan,PlanAdmin)
admin.site.register(Promotion,PromotionAdmin)
