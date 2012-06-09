# coding=utf-8
# Chon<chon219@gmail.com>
from django.http import HttpResponseRedirect,HttpResponseForbidden,HttpResponse
from django.contrib.auth.decorators import login_required
from alipay import *
from moevpn.utils import make_order_paid
from django.views.decorators.csrf import csrf_exempt
import urllib

@login_required
def return_url_handler(request):
  if notify_verify(request.GET):
    tn = request.GET.get('out_trade_no')
    trade_no = request.GET.get('trade_no')
    trade_status = request.GET.get('trade_status')
    if trade_status == 'TRADE_FINISHED':
      make_order_paid(tn)
    elif trade_status == 'WAIT_SELLER_SEND_GOODS':
      make_order_paid(tn)
      url = send_goods_confirm_by_platform(trade_no)
      req = urllib.urlopen(url)
    return HttpResponseRedirect("/home/")
  else:
    return HttpResponseForbidden()

@csrf_exempt
def notify_url_handler(request):
  if request.method == 'POST':
    if notify_verify(request.POST):
      tn = request.POST.get('out_trade_no')
      trade_no = request.POST.get('trade_no')
      trade_status = request.POST.get('trade_status')
      if trade_status == 'WAIT_SELLER_SEND_GOODS':
	make_order_paid(tn)
	url = send_goods_confirm_by_platform(trade_no)
	req = urllib.urlopen(url)
	return HttpResponse("success")
      else:
	return HttpResponse("success")
    else:
      return HttpResponseForbidden()
  else:
    return HttpResponseForbidden()
