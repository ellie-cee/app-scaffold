from django.shortcuts import render
from django.template import RequestContext
from .decorators import validProxy
from logging import Logger

logger = Logger(__name__)

# Create your views here.

def index(request):
    return render(
        request,
        "proxy.html",
        content_type="application/liquid"
    )
    
@validProxy
def test(request):
    return render(
        request,
        "proxy/test.html",
        content_type="application/liquid"
    )


def getProxyDetails(request):
    rc = RequestContext(request)
    rc.get('proxyDetails')