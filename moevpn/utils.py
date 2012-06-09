# coding=utf-8
# Chon<chon219@gmail.com>

from moevpn.kb.models import *
from moevpn.sites.models import *
from moevpn.vpn.models import *
from moevpn.sites.mail import send_active_mail
from datetime import datetime
from datetime import timedelta

def quota_used(account):
  quota_sum = 0
  logs = Log.objects.filter(account=account,status=False)
  year = datetime.now().year
  month = datetime.now().month
  for log in logs:
      if log.start_time > datetime(year=year,month=month,day=1):
          quota_sum = quota_sum + log.bytes_sent + log.bytes_received
  return quota_sum

def make_order_paid(order_id):
  order = Order.objects.get(order_id=order_id)
  user = order.user
  username = order.username
  password = order.password
  cycle = Cycle.objects.get(name=order.cycle)
  plan = Plan.objects.get(name=order.plan)
  if order.status != "UNPAID":
    return False
  order.status = "PAID"
  order.save()
  try:
     account = Account.objects.get(user=user,username=username)
     if account.active == True:
       account.creation = account.creation + timedelta(account.quota_cycle)
     else:
       account.creation = datetime.now()
       account.active = True
       account.enabled = True
  except Account.DoesNotExist:
     account = Account()
     account.user = user
     account.username = username
     account.password = password
  account.cycle = cycle
  account.plan = plan
  account.quota_cycle = cycle.quota
  account.quota_bytes = plan.quota
  account.promotion = order.promotion
  account.save()
  send_active_mail(username,user.email)
  return True

def promotion_is_valid(user,code,plan):
    try: 
        promotion = Promotion.objects.get(code=code,plan=plan)
        if user.date_joined < promotion.register_limit and datetime.now() < promotion.order_limit:
            return True
        else:
            return False
    except Promotion.DoesNotExist:
        return False
