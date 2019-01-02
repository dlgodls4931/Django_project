
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('UserService.urls')) ,
    path('admin/', admin.site.urls),
    path('UserService/', include('UserService.urls')), 
]
