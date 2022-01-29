from django.shortcuts import HttpResponse, render,redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from post.models import Post,Profile,Like

@login_required(login_url='accounts:signin')
def home_page_view(request):
    current_user = request.user
    posts = Post.objects.filter(owner__in = current_user.following.all()).order_by('-date_published')
    print(posts)


def explore_page_view(request):
    posts = Post.objects.all()
    return render(request, 'explore.html', {'posts':posts,})