# coding=utf-8
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
      'news':news.content,
      'user':request.user})

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
	send_reg_mail(user)
	return HttpResponseRedirect('/login/')
    else:
        c = {'form':form,'user':request.user}
        c.update(csrf(request))
	return render_to_response('reg.html',c)
  else:
    form = RegForm()
    c = {'form':form,'user':request.user}
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
	    return HttpResponseRedirect("/home/account/")
	else:
	  form.errors['password']= u"帐号验证失败！"
          c = {'form':form,'user':request.user}
          c.update(csrf(request))
	  return render_to_response('login.html',c)
      else:
        c = {'form':form,'user':request.user}
        c.update(csrf(request))
	return render_to_response('login.html',c)
  elif request.user.is_anonymous():
    form = LoginForm()
    c = {'form':form,'user':request.user}
    c.update(csrf(request))
    return render_to_response('login.html',c)
  else:
    return HttpResponseRedirect("/home/account/")

@login_required
def log_out(request):
  logout(request)
  return HttpResponseRedirect("/")

@login_required
def home(request):
    return HttpResponseRedirect("/home/account/")

@login_required
def account_list(request):
  vpn_accounts = []
  user = request.user
  accounts = Account.objects.filter(user=user)
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
  return render_to_response("account_list.html",{
      'vpn_accounts':vpn_accounts,
      'user':request.user,
      'active':'account'})

@login_required
def order_list(request):
  vpn_orders = []
  user = request.user
  orders = Order.objects.filter(user=user)
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
  return render_to_response("order_list.html",{
      'vpn_orders':vpn_orders,
      'user':request.user,
      'active':'order'})

def download(request):
  html = Setting.objects.get(name="download")
  return render_to_response("download.html",{"download":html.content,'user':request.user})

@login_required
def profile(request):
  user = request.user
  if request.method == 'POST':
      form = ProfileForm(request.POST)
      if form.is_valid():
	cd = form.cleaned_data
	firstname = cd['firstname']
	lastname = cd['lastname']
        email = cd['email']
        password = cd['newpassword']
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        if password:
            user.set_password(password)
        user.save()
        c = {'form':form,
            'user':request.user,
            'active':'profile'}
        c.update(csrf(request))
        return render_to_response('profile.html',c)
      else:
        c = {'form':form,
            'user':request.user,
            'active':'profile'}
        c.update(csrf(request))
        return render_to_response('profile.html',c)
  else:
      data = {'firstname':user.first_name,
              'lastname':user.last_name,
              'username':user.username,
              'email':user.email}
      form = ProfileForm(data)
      c = {'form':form,
           'user':request.user,
           'active':'profile'}
      c.update(csrf(request))
      return render_to_response('profile.html',c)

@login_required
def message_list(request):
    user = request.user
    messages = Message.objects.filter(user=user)
    return render_to_response("message_list.html",{
        "messages":messages,
        "user":request.user,
        "active":"message"})

@login_required
def message(request,message_id):
    user = request.user
    message_id = int(message_id)
    try:
        message = Message.objects.get(user=user,id=message_id)
        message.active = False
        message.save()
        return render_to_response("message.html",{
            "message":message,
            "user":user,
            "active":"message"})
    except Message.DoesNotExist:
        return HttpResponseRedirect("/home/message/")
