from django.shortcuts import render
from django.template import RequestContext


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
        "proxy_test.html"
    )


def getProxyDetails(request):
    rc = RequestContext(request)
    rc.get('proxyDetails')