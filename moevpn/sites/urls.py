from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('',
  url(r'^$',home),
  url(r'account/$',account_list),
  url(r'order/$',order_list),
#  url(r'ticket/$',ticket_list),
  url(r'message/$',message_list),
  url(r'message/(\d+)/$',message),
  url(r'profile/$',profile),
)
