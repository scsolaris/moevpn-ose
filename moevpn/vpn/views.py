# coding=utf-8
# Chon<chon219@gmail.com>

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

from models import *
from forms import *
from moevpn.sites.mail import send_order_mail
from moevpn.alipay.alipay import create_trade_by_buyer
from moevpn.utils import promotion_is_valid,message_count,ticket_count

@login_required
def order(request):
  if request.method == 'POST':
      form = OrderForm(request.POST)
      if form.is_valid():
	cd = form.cleaned_data
	order = Order()
	order.user = request.user
	order.username = cd['username']
	order.password = cd['password']
	cycle = Cycle.objects.get(name=cd['cycle'])
	plan = Plan.objects.get(name=cd['plan'])
        code = cd['promotion']
	order.cycle = cycle
	order.plan = plan
        if promotion_is_valid(request.user,code,plan):
            promotion = Promotion.objects.get(code=code,plan=plan)
            order.price = int(cycle.quota/30) * cycle.discount * plan.discount * ( plan.price - promotion.price ) * promotion.discount
            order.promotion = promotion.code
            order.discount = cycle.discount * plan.discount * promotion.discount
        else:
            order.price = int(cycle.quota/30) * cycle.discount * plan.price * plan.discount
            order.discount = cycle.discount * plan.discount
	order.save()
	send_order_mail(request.user,order.username,order.password,order.cycle,order.plan,order.price)
	return HttpResponseRedirect("/home/order/")
      else:
        c = {'form':form,
            'user':request.user,
            'message_count':message_count(request.user),
            'ticket_count':ticket_count(request.user),
            'active':'order'}
        c.update(csrf(request))
	return render_to_response("order.html",c)
  else:	
      form = OrderForm()
      c = {'form':form,
           'user':request.user,
            'message_count':message_count(request.user),
            'ticket_count':ticket_count(request.user),
           'active':'order'}
      c.update(csrf(request))
      return render_to_response("order.html",c)

@login_required
def change_password(request,username):
  if request.method == "POST":
    form = ChangePasswdForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      user = request.user
      old_password = cd['old_password']
      new_password = cd['new_password']
      try:
	account = Account.objects.get(user=user,username=username)
	if account.password == old_password:
	    account.password = new_password
	    account.save()
	    return HttpResponseRedirect("/home/account/")
	else:
	     form = ChangePasswdForm()
	     form.errors['old_password'] = u"密码错误！"
             c = {'form':form,
                  'message_count':message_count(request.user),
                  'ticket_count':ticket_count(request.user),
                  'active':'account',
                  'user':request.user}
             c.update(csrf(request))
	     return render_to_response("change_password.html",c)
      except Account.DoesNotExist:
	form = ChangePasswdForm()
	form.errors['old_password'] = u"帐号不存在！"
        c = {'form':form,
             'message_count':message_count(request.user),
             'ticket_count':ticket_count(request.user),
             'active':'account',
             'user':request.user}
        c.update(csrf(request))
	return render_to_response("change_password.html",c)
    else:
      c = {'form':form,
           'message_count':message_count(request.user),
           'ticket_count':ticket_count(request.user),
           'active':'account',
           'user':request.user}
      c.update(csrf(request))
      return render_to_response("change_password.html",c)
  else:
    form = ChangePasswdForm()
    c = {'form':form,
         'message_count':message_count(request.user),
         'ticket_count':ticket_count(request.user),
         'active':'account',
         'user':request.user}
    c.update(csrf(request))
    return render_to_response("change_password.html",c)

@login_required
def order_cancel(request,order_id):
  user = request.user
  order_id = int(order_id)
  try:
    order = Order.objects.get(user=user,order_id=order_id,status="UNPAID")
    order.status = "CANCELLED"
    order.save()
    return HttpResponseRedirect("/home/order/")
  except Order.DoesNotExist:
    return HttpResponseRedirect("/home/order/")

@login_required
def order_payment(request,order_id):
  user = request.user
  order_id = int(order_id)
  try:
    order = Order.objects.get(user=user,order_id=order_id,status="UNPAID")
    quantity = 1
    price = order.price
    subject = u"付款到MOECN.NET"
    body = order.plan.detail
    url = create_trade_by_buyer(order_id, subject, body, price, quantity)
    return HttpResponseRedirect(url)
  except Order.DoesNotExist:
    return HttpResponseRedirect("/home/order/")

@login_required
def account_renew(request,username):
  user = request.user
  try:
    account = Account.objects.get(user=user,username=username)
    order = Order()
    order.user = user
    order.username = account.username
    order.password = account.password
    order.cycle = account.cycle
    order.plan = account.plan
    if promotion_is_valid(user,account.promotion,order.plan):
        promotion = Promotion.objects.get(code=account.promotion,plan=order.plan)
        order.price = int(account.cycle.quota/30) * account.cycle.discount * account.plan.discount * ( account.plan.price - promotion.price ) * promotion.discount
        order.promotion = promotion.code
        order.discount = account.cycle.discount * account.plan.discount * promotion.discount
    else:
        order.price = int(account.cycle.quota/30) * account.cycle.discount * account.plan.discount * account.plan.price
        order.discount = account.cycle.discount * account.plan.discount
    order.save()
    send_order_mail(user,order.username,order.password,order.cycle,order.plan,order.price)
    return HttpResponseRedirect("/home/order/")
  except Exception:
    return HttpResponseRedirect("/home/account/")
