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

class ProfileForm(forms.Form):
  username = forms.CharField(min_length=4,max_length=30,widget=forms.HiddenInput)
  firstname = forms.CharField(min_length=0,max_length=30,required=False)
  lastname = forms.CharField(min_length=0,max_length=30,required=False)
  email = forms.EmailField(max_length=30)
  oldpassword = forms.CharField(min_length=0,max_length=60,widget=forms.PasswordInput,required=False)
  newpassword = forms.CharField(min_length=0,max_length=60,widget=forms.PasswordInput,required=False)
  def clean(self):
      oldpassword = self.cleaned_data['oldpassword']
      newpassword = self.cleaned_data['newpassword']
      username = self.cleaned_data['username']
      if not oldpassword and not newpassword:
          return self.cleaned_data
      elif oldpassword and newpassword:
          user = User.objects.get(username=username)
          if user.check_password(oldpassword):
              return self.cleaned_data
          else:
              self._errors['oldpassword'] = ErrorList(['密码错误'])
              return self.cleaned_data
      elif not oldpassword:
          self._errors['oldpassword'] = ErrorList(['原密码不能为空'])
          return self.cleaned_data
      elif not newpassword:
          self._errors['newpassword'] = ErrorList(['新密码不能为空'])
          return self.cleaned_data
      else:
          return self.cleaned_data

class TicketForm(forms.Form):
  subject = forms.CharField(min_length=2,max_length=128,widget=forms.TextInput(attrs={"class":"input-xlarge"}))
  content = forms.CharField(min_length=2,max_length=1024,widget=forms.Textarea(attrs={"class":"input-xlarge"}),required=False)
