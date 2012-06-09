# coding=utf-8
# Chon<chon219@gmail.com>

from django.contrib import admin
from models import *

class NotifacationAdmin(admin.ModelAdmin):
  list_display = ('name','title','content')

class SettingAdmin(admin.ModelAdmin):
  list_display = ('name','title','content')

admin.site.register(Notifacation,NotifacationAdmin)
admin.site.register(Setting,SettingAdmin)
