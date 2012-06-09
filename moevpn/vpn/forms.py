# coding: utf-8
# Chon<chon219@gmail.com>

from django import forms
from models import *
import re

class OrderForm(forms.Form):
  VPN_PLAN_CHOICES = []
  VPN_CYCLE_CHOICES = []
  for plan in Plan.objects.all():
    VPN_PLAN_CHOICES.append((plan.name,plan.detail))
  for cycle in Cycle.objects.all():
    VPN_CYCLE_CHOICES.append((cycle.name,cycle.detail))
  username = forms.CharField(min_length=4,max_length=30,label=u"VPN帐号")
  password = forms.CharField(min_length=4,max_length=60,label=u"VPN密码")
  plan = forms.ChoiceField(choices=VPN_PLAN_CHOICES)
  cycle = forms.ChoiceField(choices=VPN_CYCLE_CHOICES)
  promotion = forms.CharField(min_length=2,max_length=16,label=u"优惠代码",required=False)
  def clean_username(self):
    username = self.cleaned_data['username']
    pattern = re.compile("^[0-9a-zA-Z_]+$")
    if not re.match(pattern,username):
      raise forms.ValidationError('帐号只能包含字符/数字/下划线')
    try:
      account = Account.objects.get(username=username)
      if account is not None:
	raise forms.ValidationError('帐号已存在')
    except Account.DoesNotExist:
      pass
    return username


class ChangePasswdForm(forms.Form):
  old_password = forms.CharField(min_length=4,max_length=60,label=u"原密码")
  new_password = forms.CharField(min_length=4,max_length=60,label=u"新密码")
