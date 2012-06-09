from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('',
  url(r'notify/?$',notify_url_handler),
  url(r'return/?$',return_url_handler),
)
