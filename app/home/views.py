import os
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from site_auth.decorators import requiresLogin
from django.http import HttpResponse
from shopify_auth.models import ShopifySite
import json
import logging
from django.conf import settings
from django.template import RequestContext
from django.core.mail import EmailMultiAlternatives
from xyz import settings


logger = logging.Logger(__name__)


# Create your views here.




def dashboard(request):
    logger.error(__debug__)
    logger.error(settings.DEBUG)
    logger.error(settings.STATIC_ROOT)
    return render(
        request,
        "index.html",
        {}
    )
def logJson(payload):
    logger.error(
        json.dumps(payload,indent=1)
    )
def jsonResponse(payload,status=200):
    payload["status"] = status
    return HttpResponse(
        json.dumps(payload),
        content_type="application/json",
        status=status
    )
def getJsonPayload(request):
    return json.loads(request.body.decode("utf-8"))

def install(request):
    shopifySite,created = ShopifySite.objects.get_or_create(shopDomain=request.session["shopify"].get("shop_url"))
    shopifySite.accessToken = request.session["shopify"].get("access_token")
    details = shopifySite.shopDetails()
    shopifySite.save()
    return redirect("/")

def testEmail(request):
    print(settings.EMAIL_HOST_USER,settings.EMAIL_PORT,settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
    msg = EmailMultiAlternatives(
        "Your YWM Login Code",
        render_to_string(
            "email.txt",
            {
                "text":"ewqfefeq"
            }
        ),
        os.environ.get("DEFAULT_EMAIL"),
        ["cassadyeleanor@gmail.com"],
    )
    msg.attach_alternative(
        render_to_string(
            "email.html",
            {
                "text":"ewqfefeq"
            }
        ),
        "text/html"
    )
    msg.send()
    return render(
        request,
        "test.html"
    )
                                                                                    

