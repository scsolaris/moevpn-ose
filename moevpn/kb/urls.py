# Chon<chon219@gmail.com>

from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('',
  url(r'^$',kb_index),
  url(r'post/(\d+)/$',kb_post),
)
