from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like,Reply
from . forms import PostForm

@login_required(login_url='accounts:signin')
def create_post_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # image = request.POST['image']
            # caption = request.POST['caption']
            # location = request.POST['location']
            # owner = request.user

            # post = Post(image = image, caption = caption, location = location, owner = owner)
            # post.save()
            form = form.save(commit = False)
            form.owner = request.user.profile
            form.save()
            return HttpResponse("post created")

    form = PostForm()
    return render(request, "create_post.html", {'form':form})

@login_required(login_url='accounts:signin')
def change_post_view(request, post_pk):
    return HttpResponse("change post in here")


def watch_post_view(request, post_pk):
    return HttpResponse("watch post in here")