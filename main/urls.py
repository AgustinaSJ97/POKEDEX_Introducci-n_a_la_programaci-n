from django.contrib import admin
from django.urls import include, path
from app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', app_views.register, name='register'),
]