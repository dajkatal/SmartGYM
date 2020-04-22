from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('add/<profession>/<name>', views.newuser),
    path('list', views.list)
]