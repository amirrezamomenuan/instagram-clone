from django.urls import path
from . import views

app_name = "profile"

urlpatterns = [
    path('signup/', views.signup_profile_view, name= "signup"),
    path('signin/', views.signin_profile_view, name= "signin"),
    path('show-profile/<str:profile_username>', views.show_profile_view, name= "show"),
    path('change/', views.change_profile_view, name= "change"),
    path('forgot-password/', views.forgot_password_view, name= "forgot_password"),
    path('search/', views.search_user_view, name= "search_user"),
    path('followers/<requested>', views.followers_view, name= "followers"),
    path('following/<requested>', views.following_view, name= "following"),
    path('follow/', views.follow_manager_view, name = "follow_manager")

]