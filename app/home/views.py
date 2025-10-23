import os
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from site_auth.decorators import requiresLogin
from django.http import HttpResponse
from shopify_sites.models import ShopifySite
import json
import logging
from django.conf import settings
from django.template import RequestContext
from django.core.mail import EmailMultiAlternatives
from .lmno import EmailStatus, jsonify,sendEmail
from appointment.models import Appointment,StaffMember,AppointmentRequest

logger = logging.Logger(__name__)


# Create your views here.




def dashboard(request):
    
    print(request.session.get("dewqdewq"))
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

def testFake(request):
    
    
    pass
def testEmail(request):
    
    result:EmailStatus = sendEmail(
        recipient="cassadyeleanor@gmail.com",
        subject="hey now",
        context={"message":"butts lol"},
        sender="ellie@elliecee.xyz",
        templatePrefix="2fa"
    )
    print(result)
    return render(
        request,
        "test.html",
        {"message":result.message}
    )

def viewed(request):
    payload = getJsonPayload(request)
    result:EmailStatus = sendEmail(
        recipient="cassadyeleanor@gmail.com",
        subject="Site View",
        context={"message":json.dumps(payload,indent=1)},
        sender="ellie@elliecee.xyz",
        templatePrefix="siteClick"
    )
    
    return jsonResponse(
        {"recieved":"true"},
        200
    )
    
                                                                                    

