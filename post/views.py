from django.shortcuts import get_object_or_404, redirect, render,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like,Reply
from . forms import PostForm, CommentForm

@login_required(login_url='accounts:signin')
def create_post_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit = False)
            form.owner = request.user.profile
            form.save()
            return redirect("home_and_explore:home")

    form = PostForm()
    return render(request, "create_post.html", {'form':form})


@login_required(login_url='accounts:signin')
def change_post_view(request, post_pk):
    post = get_object_or_404(Post, id = post_pk)
    if request.user != post.owner.user:
        return HttpResponse('invalid access', status = 400)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post:watch", post_pk = post_pk)
    
    form = PostForm(instance=post)
    return render(request, "change_post.html", {'form':form, 'post_pk':post_pk})


def watch_post_view(request, post_pk):
    post = get_object_or_404(Post, id = post_pk)
    has_liked = request.user.username in post.like_set.values_list("owner__user__username", flat = True)
    print(has_liked)
    return render(request, 'watch.html', {'post':post, 'has_liked':has_liked,})


@login_required(login_url='accounts:signin')
def like_view(request, pk):
    if request.method == 'POST':
        post= get_object_or_404(Post, id= pk)
        like = Like.objects.filter(on_post = post, owner= request.user.profile).exists()
        if like:
            like = Like.objects.get(on_post = post, owner= request.user.profile)
            like.delete()
        else:
            Like.objects.create(on_post = post, owner= request.user.profile)
        if request.POST.get('next'):
            return redirect("post:watch",post_pk = pk)
        return redirect('home_and_explore:home')

@login_required(login_url='accounts:signin')
def comment_view(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.writer = request.user.profile
            form.on_post = Post.objects.get(id = pk)
            form.save()
    
    form = CommentForm()
    comments = Comment.objects.filter(on_post__id = pk)
    return render(request, 'comments.html', {'comments':comments, 'pk':pk, 'form':form ,'username':request.user.username})