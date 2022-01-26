from django.shortcuts import render
from django.shortcuts import HttpResponse, render, redirect

def all_activities_view(request):
    return HttpResponse("all activities")

def unseen_activities_view(request):
    return HttpResponse("unseen acitvities")