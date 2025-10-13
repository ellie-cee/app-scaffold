from django.shortcuts import render
from django.template import RequestContext
from .decorators import validProxy
from logging import Logger
import os

logger = Logger(__name__)

# Create your views here.
def responseContentType(request):
    proxied = request.GET.get("shop") is not None and request.GET.get("signature") is not None
    return "application/liquid" if proxied else "text/html"
    

def index(request):
    return render(
        request,
        "proxy.html",
        content_type=responseContentType()
    )
    
@validProxy
def test(request):
    return render(
        request,
        "proxy/test.html",
        content_type=responseContentType()
    )


def getProxyDetails(request):
    rc = RequestContext(request)
    rc.get('proxyDetails')