from django.urls import path
from . import views

app_name = "activities"

urlpatterns = [
    path('all-activities/', views.all_activities_view, name="all"),
    path('unseen-activities/', views.unseen_activities_view, name='unseen'),
]