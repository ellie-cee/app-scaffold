
import logging
import os

logger = logging.getLogger(__name__)
def app_urls(request):
    if request.GET.get("shop") is not None and request.GET.get("signature") is not None:
        return {
            "create_appointment":f"/apps/xyz/appointment/request-submit/",
            "client_info":"/apps/xyz/appointment/client-info/",
            "reschedule":"/apps/xyz/appointment-reschedule-submit/"
        }
    else:
        return {
            "create_appointment":f"/shopify-proxy/appointment/request-submit/",
            "client_info":"/shopify-proxy/appointment/client-info/",
            "reschedule":"/shopify-proxy/appointment-reschedule-submit/"
        }
