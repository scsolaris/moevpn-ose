from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('',
  url(r'^$',kb_index),
  url(r'post/(\d+)/$',kb_post),
  url(r'category/([0-9a-zA-Z_]+)/$',kb_category),
)
