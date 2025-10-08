from django.shortcuts import render
from django.template import RequestContext
from .decorators import validProxy


# Create your views here.

def index(request):
    return render(
        request,
        "proxy.html",
        {}
    )
def test(request):
    return render(
        request,
        "proxytest.html"
    )


def getProxyDetails(request):
    rc = RequestContext(request)
    rc.get('proxyDetails')