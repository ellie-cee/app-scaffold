from django.shortcuts import render
from django.template import RequestContext
from .decorators import validProxy
from logging import Logger
import os

logger = Logger(__name__)

# Create your views here.
def responseContentType():
    return "text/html" if os.environ.get("ISLOCAL")=="yes" else "application/liquid"
    

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