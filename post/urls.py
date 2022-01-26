from . import views
from django.urls import path

app_name = "post"

urlpatterns = [
    path('create/', views.create_post_view, name="create"),
    path('change/<int:post_pk>', views.change_post_view, name= 'change'),
    path('watch/<int:post_pk>', views.watch_post_view, name= 'watch'),
]