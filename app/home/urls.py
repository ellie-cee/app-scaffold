from django.contrib import admin
from django.urls import path
import shopify_proxy.views as pviews
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('install',views.install),
    path("testemail",views.testEmail),
    path("contact/send",pviews.sendContact),
    path("contact",pviews.contactForm)
]
