# coding=utf-8
# Chon<chon219@gmail.com>

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

from datetime import datetime,timedelta
from moevpn.vpn.models import *
from moevpn.utils import quota_used
from mail import send_reg_mail
from models import *
from forms import *

def index(request):
  plans = []
  announcement = Setting.objects.get(name='announcement')
  news = Setting.objects.get(name='news')
  for plan in Plan.objects.all():
    plans.append({
        'class':plan.name,
        'description':plan.description})
  return render_to_response('index.html',{
      'plans':plans,
      'announcement':announcement.content,
      'news':news.content})

def reg(request):
  if request.method=='POST':
    form = RegForm(request.POST)
    if form.is_valid():
	cd = form.cleaned_data
	username = cd['username']
	email = cd['email']
	password = cd['password']
	user = User.objects.create_user(username,email,password)
	user.save()
	send_reg_mail(username,email)
	return HttpResponseRedirect('/login/')
    else:
        c = {'form':form}
        c.update(csrf(request))
	return render_to_response('reg.html',c)
  else:
    form = RegForm()
    c = {'form':form}
    c.update(csrf(request))
    return render_to_response('reg.html',c)

def log_in(request):
  if request.method == 'POST':
      form = LoginForm(request.POST)
      if form.is_valid():
	cd = form.cleaned_data
	print cd
	username = cd['username']
	password = cd['password']
	user = authenticate(username=username,password=password)
	if user is not None:
	    login(request, user)
	    return HttpResponseRedirect("/home/")
	else:
	  form.errors['password']= u"帐号验证失败！"
          c = {'form':form}
          c.update(csrf(request))
	  return render_to_response('login.html',c)
      else:
        c = {'form':form}
        c.update(csrf(request))
	return render_to_response('login.html',c)
  elif request.user.is_anonymous():
    form = LoginForm()
    c = {'form':form}
    c.update(csrf(request))
    return render_to_response('login.html',c)
  else:
    return HttpResponseRedirect("/home/")

@login_required
def log_out(request):
  logout(request)
  return HttpResponseRedirect("/login/")

@login_required
def home(request):
  vpn_accounts = []
  vpn_orders = []
  user = request.user
  accounts = Account.objects.filter(user=user)
  orders = Order.objects.filter(user=user)
  for account in accounts:
    vpn_accounts.append({
        'username':account.username,
        'password':account.password,
        'plan':account.plan.detail,
        'cycle':account.cycle.detail,
        'promotion':account.promotion,
        'quota_bytes':str("%.2f"%(float(account.quota_bytes)/1048576.00))+"MB",
        'quota_used':str("%.2f"%(float(quota_used(account))/1048576.00))+"MB",
        'expiry':account.creation+timedelta(days=account.quota_cycle),
        "status":(account.active and account.enabled)})
  for order in orders:
    vpn_orders.append({
        'order_id':order.order_id,
        'order_time':order.order_time,
        'username':order.username,
        'password':order.password,
        'cycle':order.cycle.detail,
        'plan':order.plan.detail,
        'price':order.price,
        'discount':order.discount,
        'promotion':order.promotion,
        'status':order.status})
  return render_to_response("home.html",{
      'vpn_accounts':vpn_accounts,
      'vpn_orders':vpn_orders})

def download(request):
  html = Setting.objects.get(name="download")
  return render_to_response("download.html",{"download":html.content})
