# coding=utf-8
# Chon<chon219@gmail.com>

from django.contrib import admin
from models import *

class NotifacationAdmin(admin.ModelAdmin):
  list_display = ('name','title')

class SettingAdmin(admin.ModelAdmin):
  list_display = ('name','title')

class MessageAdmin(admin.ModelAdmin):
  list_display = ('id','user','time','subject')

admin.site.register(Notifacation,NotifacationAdmin)
admin.site.register(Setting,SettingAdmin)
admin.site.register(Message,MessageAdmin)
