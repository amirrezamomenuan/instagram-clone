from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('activities/', include('activities.urls')),
    path('post/', include('post.urls')),
    path('profile/', include('accounts.urls')),
    path('', include('app.urls')),

]
