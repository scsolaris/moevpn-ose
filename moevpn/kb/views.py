# coding=utf-8
# Chon<chon219@gmail.com>

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from models import *

def kb_index(request):
  posts = []
  post_all = Post.objects.all()
  for post in post_all:
    posts.append({'post_id':post.post_id,'author':post.user.username,'time':post.post_time,'title':post.title})
  return render_to_response("kb_index.html",{'posts':posts})

def kb_post(request,post_id):
  try:
    p = Post.objects.get(post_id=post_id)
    post = {'title':p.title,'content':p.content,'time':p.post_time,'author':p.user.username}
    return render_to_response('kb_post.html',{'post':post})
  except Exception:
    return HttpResponseRedirect("/kb/")
