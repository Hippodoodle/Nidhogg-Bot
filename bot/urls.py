from django.urls import path
from bot import views

app_name = 'bot'

urlpatterns = [
    path('', views.index, name='index'),
]
