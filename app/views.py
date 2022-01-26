from django.shortcuts import HttpResponse, render,redirect
from django.shortcuts import render

def home_page_view(request):
    return HttpResponse("this is home page")

def explore_page_view(request):
    return HttpResponse("this is explore view")