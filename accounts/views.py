from django import http
from django.shortcuts import render, HttpResponse

def signup_profile_view(request):
    return HttpResponse("signup my profile")

def signin_profile_view(request):
    return HttpResponse("signin my profile")


def change_profile_view(request):
    return HttpResponse("change my profile")


def show_profile_view(request, profile_username):
    return HttpResponse(profile_username)
