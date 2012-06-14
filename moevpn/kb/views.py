# coding=utf-8
# Chon<chon219@gmail.com>

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from models import *

def kb_index(request):
  posts = Post.objects.all()
  categories = Category.objects.all()
  return render_to_response("kb_index.html",{
      'posts':posts,
      'categories':categories,
      'user':request.user})

def kb_category(request,category_name):
  try:
      category = Category.objects.get(name=category_name)
      categories = Category.objects.all()
      posts = Post.objects.filter(category=category)
      return render_to_response("kb_index.html",{
          'posts':posts,
          'category':category,
          'categories':categories,
          'user':request.user})
  except Exception:
      return HttpResponseRedirect("/kb/")

def kb_post(request,post_id):
  try:
    p = Post.objects.get(post_id=post_id)
    post = {'title':p.title,
            'content':p.content,
            'time':p.post_time,
            'author':p.user.username}
    return render_to_response('kb_post.html',{
        'post':post,
        'user':request.user})
  except Exception:
    return HttpResponseRedirect("/kb/")
