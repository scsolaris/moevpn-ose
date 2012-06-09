# Chon<chon219@gmail.com>

from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('',
  url(r'order/$',order),
  url(r'change_password/([0-9a-zA-Z_]+)/$',change_password),
  url(r'order_cancel/(\d+)/$',order_cancel),
  url(r'order_payment/(\d+)/$',order_payment),
  url(r'account_renew/([0-9a-zA-Z_]+)/$',account_renew),
)
