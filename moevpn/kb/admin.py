# coding=utf-8
# Chon<chon219@gmail.com>

from django.contrib import admin
from moevpn.kb.models import *

class PostAdmin(admin.ModelAdmin):
  list_display = ('post_id','user','title','post_time')

class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name','desc')

admin.site.register(Post,PostAdmin)
admin.site.register(Category,CategoryAdmin)
