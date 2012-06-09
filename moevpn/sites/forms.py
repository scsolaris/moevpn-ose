# coding: utf-8
# Chon<chon219@gmail.com>

from django import forms
from django.forms.util import ErrorList
from django.contrib.auth.models import User
from moevpn.captcha.fields import ReCaptchaField
from models import *
import re

class RegForm(forms.Form):
  username = forms.CharField(min_length=4,max_length=30,label=u"用户名")
  email = forms.EmailField(max_length=30,label="Email")
  password = forms.CharField(min_length=4,max_length=60,label="密码",widget=forms.PasswordInput)
  captcha = ReCaptchaField()
  def clean_username(self):
    username = self.cleaned_data['username']
    pattern = re.compile("^[0-9a-zA-Z_]+$")
    if not re.match(pattern,username):
      raise forms.ValidationError('用户名只能包含字符/数字/下划线')
    try:
      user = User.objects.get(username=username)
      if user is not None:
	raise forms.ValidationError('帐号已存在')
    except User.DoesNotExist:
      pass
    return username

class LoginForm(forms.Form):
  username = forms.CharField(min_length=4,max_length=30,label=u"用户名")
  password = forms.CharField(min_length=4,max_length=60,label=u"密码",widget=forms.PasswordInput)
  def clean(self):
    username = self.cleaned_data['username']
    password = self.cleaned_data['password']
    try:
	user = User.objects.get(username=username)
	if not user.is_active:
	   self._errors['username'] = ErrorList(['帐号已被禁用'])
	if not user.check_password(password):
	   self._errors['password'] = ErrorList(['密码错误'])
    except User.DoesNotExist:
	self._errors['username'] = ErrorList(['帐号不存在'])
    return self.cleaned_data
