"""nidhogg_bot URL Configuration"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from bot import views


urlpatterns = [
    path('', views.index, name='index'),
    path('bot/', include('bot.urls')),
    path('admin/', admin.site.urls),
]
