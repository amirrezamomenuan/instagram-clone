from django.shortcuts import render,HttpResponse

def create_post_view(request):
    return HttpResponse("create post in here")


def change_post_view(request, post_pk):
    return HttpResponse("change post in here")


def watch_post_view(request, post_pk):
    return HttpResponse("watch post in here")