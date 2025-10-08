import os
from django.db import models
import hashlib, base64, hmac

# Create your models here.

class ShopifySite(models.Model):
    id = models.BigAutoField(primary_key=True)
    shopName = models.CharField(max_length=128)
    shopDomain = models.CharField(max_length=64)
    appKey = models.CharField(max_length=64)
    accessToken = models.CharField(max_length=255)
    
    def __str__(self):
        return self.shopName
    
    def validateSignature(self,request):
        params = request.GET.dict()
        hmac = params.pop('signature')
        if hmac is None:
            return False
        secret = os.environ.get("SHOPIFY_APP_SECRET")
        line = '&'.join([
            '%s=%s' % (key, value)
            for key, value in sorted(params.items())
        ])
        h = hmac.new(secret.encode('utf-8'), line.encode('utf-8'), hashlib.sha256)
        if hmac.compare_digest(h.hexdigest(), hhmac) == False:
            return False
        return True
    
    class Meta:
        db_table = "shopifySite"
    def tld(self):
        return f"{self.shopDomain}.myshopify.com"
