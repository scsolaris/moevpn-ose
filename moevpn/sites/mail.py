# coding=utf-8
# Chon<chon219@gmail.com>

from django.core.mail import EmailMessage
from models import Notifacation,Message
from moevpn import settings
from moevpn.vpn.models import *
from datetime import datetime
import re

def send_new_reg(username):
  from_email = settings.MAIL_SENDER
  to_email = settings.MAIL_ADMIN
  notifacation = Notifacation.objects.get(name="new_register")
  subject = notifacation.title
  text_content = re.sub("{username}",username,notifacation.content)
  msg = EmailMessage(subject,text_content,from_email,[to_email])
  msg.send()
  return True

def send_new_order(username):
  from_email = settings.MAIL_SENDER
  to_email = settings.MAIL_ADMIN
  notifacation = Notifacation.objects.get(name="new_order")
  subject = notifacation.title
  text_content = re.sub("{username}",username,notifacation.content)
  msg = EmailMessage(subject,text_content,from_email,[to_email])
  msg.send()
  return True

def send_reg_mail(user):
  from_email = settings.MAIL_SENDER
  to_email = user.email
  notifacation = Notifacation.objects.get(name="register")
  subject = notifacation.title
  html_content = re.sub("{username}",user.username,notifacation.content)
  msg = EmailMessage(subject,html_content,from_email,[to_email])
  msg.content_subtype = "html"
  msg.send()
  message = Message()
  message.user = user
  message.subject = subject
  message.time = datetime.now()
  message.content = html_content
  message.sender = "SYSTEM"
  message.save()
  send_new_reg(user.username)
  return True

def send_order_mail(user,order):
  from_email = settings.MAIL_SENDER
  to_email = user.email
  notifacation = Notifacation.objects.get(name="order")
  subject = notifacation.title
  html_content = re.sub("{vpn_username}",order.username,notifacation.content)
  html_content = re.sub("{vpn_password}",order.password,html_content)
  html_content = re.sub("{vpn_plan}",order.plan.detail,html_content)
  html_content = re.sub("{vpn_cycle}",order.cycle.detail,html_content)
  html_content = re.sub("{vpn_price}",str(order.price),html_content)
  msg = EmailMessage(subject,html_content,from_email,[to_email])
  msg.content_subtype = "html"
  msg.send()
  message = Message()
  message.user = user
  message.subject = subject
  message.time = datetime.now()
  message.content = html_content
  message.sender = "SYSTEM"
  message.save()
  send_new_order(username)
  return True

def send_active_mail(user):
  from_email = settings.MAIL_SENDER
  to_email = user.email
  notifacation = Notifacation.objects.get(name="active")
  subject = notifacation.title
  html_content = notifacation.content
  msg = EmailMessage(subject,html_content,from_email,[to_email])
  msg.content_subtype = "html"
  message = Message()
  message.user = user
  message.subject = subject
  message.time = datetime.now()
  message.content = html_content
  message.sender = "SYSTEM"
  message.save()
  msg.send()
  return True
