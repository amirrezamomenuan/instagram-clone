from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('home/', views.chat_home_view, name= 'home'),
    path('chat/<int:chat_id>/<str:other_side_username>', views.chat_conversation_view, name='chat_page'),
]