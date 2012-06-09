# Chon<chon219@gmail.com>

from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^manage/', include(admin.site.urls)),
    url(r'^kb/',include('moevpn.kb.urls')),
    url(r'^alipay/',include('moevpn.alipay.urls')),
    url(r'^vpn/',include('moevpn.vpn.urls')),
    url(r'^$','moevpn.sites.views.index'),
    url(r'^reg/$','moevpn.sites.views.reg'),
    url(r'^login/$','moevpn.sites.views.log_in'),
    url(r'^logout/$','moevpn.sites.views.log_out'),
    url(r'^home/$','moevpn.sites.views.home'),
    url(r'^download/$','moevpn.sites.views.download'),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'}),
)
