# coding=utf-8
# Chon<chon219@gmail.com>

from django.core.mail import EmailMessage
from models import Notifacation
from moevpn import settings
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

def send_reg_mail(username,email):
  from_email = settings.MAIL_SENDER
  to_email = email
  notifacation = Notifacation.objects.get(name="register")
  subject = notifacation.title
  html_content = re.sub("{username}",username,notifacation.content)
  msg = EmailMessage(subject,html_content,from_email,[to_email])
  msg.content_subtype = "html"
  msg.send()
  send_new_reg(username)
  return True

def send_order_mail(username,email,password,cycle,plan,price):
  from_email = settings.MAIL_SENDER
  to_email = email
  notifacation = Notifacation.objects.get(name="order")
  subject = notifacation.title
  html_content = re.sub("{vpn_username}",username,notifacation.content)
  html_content = re.sub("{vpn_password}",password,html_content)
  html_content = re.sub("{vpn_plan}",plan.detail,html_content)
  html_content = re.sub("{vpn_cycle}",cycle.detail,html_content)
  html_content = re.sub("{vpn_price}",str(price),html_content)
  msg = EmailMessage(subject,html_content,from_email,[to_email])
  msg.content_subtype = "html"
  msg.send()
  send_new_order(username)
  return True

def send_active_mail(username,email):
  from_email = settings.MAIL_SENDER
  to_email = email
  notifacation = Notifacation.objects.get(name="active")
  subject = notifacation.title
  html_content = notifacation.content
  msg = EmailMessage(subject,html_content,from_email,[to_email])
  msg.content_subtype = "html"
  msg.send()
  return True

def send_renew_mail(username,email):
  from_email = settings.MAIL_SENDER
  to_email = email
  notifacation = Notifacation.objects.get(name="renew")
  subject = notifacation.title
  html_content = re.sub("{username}",username,notifacation.content)
  msg = EmailMessage(subject,html_content,from_email,[to_email])
  msg.content_subtype = "html"
  msg.send()
  return True
