from django.shortcuts import HttpResponse, render,redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from post.models import Post,Profile,Like
from django.db.models import Q

@login_required(login_url='profile:signin')
def home_page_view(request):
    current_user = request.user
    posts = Post.objects.filter(Q(owner__in = current_user.following.all()) | Q(owner =  request.user.profile)).order_by('-date_published')
    print(posts)
    return render(request, "home.html" ,{'posts':posts, 'username':request.user.username})


def explore_page_view(request):
    posts = Post.objects.all().order_by('-date_published')
    return render(request, 'explore.html', {'posts':posts,})