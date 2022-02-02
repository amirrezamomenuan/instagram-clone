from django.shortcuts import HttpResponse, render, redirect
from activities.models import Activity

def all_activities_view(request):
    activities = Activity.objects.filter(related_to__user = request.user)
    return render(request, 'activities.html', {'activities':activities})

def unseen_activities_view(request):
    return HttpResponse("unseen acitvities")