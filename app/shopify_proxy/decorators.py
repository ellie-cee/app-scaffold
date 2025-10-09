import os
import traceback
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.core import serializers
from shopify_auth.models import ShopifySite
from django.shortcuts import render,redirect
import logging

logger = logging.Logger(__name__)

def validProxy(fn):
    def wrapper(request, *args, **kwargs):
        details =  {
            "shopDomain":request.GET.get("shop"),
            "customerId":request.GET.get("logged_in_customer_id"),
            "signature":request.GET.get("signature")
        }
        print(details)
        if details is None or details.get("shopDomain") is None:
            return render(
                request,
                "proxy_fail.html",
                content_type="application/liquid"
            )
        try:
            
            if not ShopifySite.validateSignature(request):
                return render(
                   request,
                    "proxy_fail.html",
                    content_type="application/liquid"
                )
        except:
            traceback.print_exc()
            print("fayle")
            return render(
                   request,
                    "proxy_fail.html",
                    content_type="application/liquid"
                )                             
        return fn(request, *args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper
