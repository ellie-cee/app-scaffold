import os
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.core import serializers
from shopify_auth.models import ShopifySite
from django.shortcuts import render,redirect
from .views import getProxyDetails
import logging

logger = logging.Logger(__name__)

def validProxy(fn):
    def wrapper(request, *args, **kwargs):
        details = getProxyDetails(request)
        if details is None or details.get("shop") is None:
            return render(
                request,
                "proxy_fail.html"
            )
        try:
            shopifySite = ShopifySite.objects.get(shopName=details.get("shop"))
            if not shopifySite.validateSignature(details.get("signature")):
                return render(
                   request,
                    "proxy_fail.html"
                )
        except:
             return render(
                   request,
                    "proxy_fail.html"
                )                             
        return fn(request, *args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper
