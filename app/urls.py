from django.urls import path
from . import views

app_name = "home_and_explore"

urlpatterns = [
    path('home/', views.home_page_view, name="home"),
    path('explore/', views.explore_page_view, name='explore'),
]