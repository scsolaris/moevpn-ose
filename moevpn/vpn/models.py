# coding=utf-8
# Chon<chon219@gmail.com>

from django.db import models
from django.contrib.auth.models import User

class Cycle(models.Model):
    name = models.CharField(primary_key=True,max_length=128)
    detail = models.CharField(max_length=128)
    quota = models.IntegerField()
    discount = models.FloatField()
    def __unicode__(self):
      return self.name

class Plan(models.Model):
    name = models.CharField(primary_key=True,max_length=128)
    detail = models.CharField(max_length=128)
    quota = models.DecimalField(max_digits=13,decimal_places=0,default=32212254720)
    price = models.FloatField()
    discount = models.FloatField()
    description = models.TextField()
    def __unicode__(self):
      return self.name

class Account(models.Model):
    user = models.ForeignKey(User)
    username = models.CharField(max_length=30,primary_key=True)
    password = models.CharField(max_length=60)
    creation = models.DateTimeField(auto_now_add=True)
    quota_cycle = models.IntegerField(default=31)
    quota_bytes = models.DecimalField(max_digits=13,decimal_places=0,default=32212254720)
    cycle = models.ForeignKey(Cycle)
    plan = models.ForeignKey(Plan)
    promotion = models.CharField(max_length=16,null=True,blank=True) 
    active = models.BooleanField(default=True)
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
      return self.username
    class Meta:
      ordering = ['username']

class Log(models.Model):
    account = models.ForeignKey(Account)
    log_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True)
    bytes_received = models.DecimalField(default=0,max_digits=13,decimal_places=0)
    bytes_sent = models.DecimalField(default=0,max_digits=13,decimal_places=0)
    local_ip = models.CharField(max_length=64)
    remote_ip = models.CharField(max_length=64)
    proto = models.CharField(max_length=24)
    status = models.BooleanField(default=False)
    def __unicode__(self):
      return unicode(self.start_time)
    class Meta:
      ordering = ['start_time']

class Order(models.Model):
    STATUS_CHOICES = (
      ('PAID','paid'),
      ('UNPAID','unpaid'),
      ('CANCELLED','cancelled'),
      )
    user = models.ForeignKey(User)
    order_id = models.AutoField(primary_key=True)
    order_time = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=30) 
    password = models.CharField(max_length=60)
    cycle = models.ForeignKey(Cycle)
    plan = models.ForeignKey(Plan)
    status = models.CharField(max_length=16,default="UNPAID",choices=STATUS_CHOICES)
    price = models.FloatField()
    discount = models.FloatField()
    promotion = models.CharField(max_length=16,blank=True,null=True) 
    def __unicode__(self):
      return unicode(self.order_id)
    class Meta:
      ordering = ['order_time']

class Promotion(models.Model):
    code = models.CharField(max_length=16) 
    plan = models.ForeignKey(Plan)
    price = models.FloatField()
    discount = models.FloatField()
    register_limit = models.DateTimeField()
    order_limit = models.DateTimeField()
