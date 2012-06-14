# coding=utf-8
# Chon<chon219@gmail.com>

from django.db import models
from django.contrib.auth.models import User

class Notifacation(models.Model):
    name = models.CharField(primary_key=True,max_length=128)
    title = models.CharField(max_length=128)
    content = models.TextField()

class Setting(models.Model):
    name = models.CharField(primary_key=True,max_length=128)
    title = models.CharField(max_length=128)
    content = models.TextField()

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    subject = models.CharField(max_length=128)
    time = models.DateTimeField()
    sender = models.CharField(max_length=30)
    content = models.TextField()
    active = models.BooleanField(default=True)

class TicketThread(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    subject = models.CharField(max_length=128)
    time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    def __unicode__(self):
        return self.user.username + ": " + self.subject

class Ticket(models.Model):
    thread = models.ForeignKey(TicketThread)
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    sender = models.CharField(max_length=30)
