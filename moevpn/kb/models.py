# coding=utf-8
# Chon<chon219@gmail.com>

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=32)
    desc = models.CharField(max_length=64)
    def __unicode__(self):
      return self.name
    
class Post(models.Model):
    user = models.ForeignKey(User)
    post_id = models.AutoField(primary_key=True)
    post_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    content = models.TextField()
    category = models.ManyToManyField(Category)
