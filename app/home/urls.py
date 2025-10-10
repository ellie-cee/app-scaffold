from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('install',views.install),
    path("testemail",views.testEmail)
]
