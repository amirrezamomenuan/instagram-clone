from operator import setitem
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from . import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('activities/', include('activities.urls')),
    path('post/', include('post.urls')),
    path('profile/', include('accounts.urls')),
    path('', include('app.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()