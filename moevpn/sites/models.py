# coding=utf-8
# Chon<chon219@gmail.com>

from django.db import models

class Notifacation(models.Model):
    name = models.CharField(primary_key=True,max_length=128)
    title = models.CharField(max_length=128)
    content = models.TextField()

class Setting(models.Model):
    name = models.CharField(primary_key=True,max_length=128)
    title = models.CharField(max_length=128)
    content = models.TextField()
