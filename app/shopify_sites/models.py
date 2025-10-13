import os
from django.db import models
import hashlib, base64, hmac
from .graphql import GraphQL
import shopify
import sys
import hmac,hashlib
# Create your models here.

class ShopifySite(models.Model):
    id = models.BigAutoField(primary_key=True)
    shopName = models.CharField(max_length=128)
    shopDomain = models.CharField(max_length=64,default="",db_index=True)
    appKey = models.CharField(max_length=64)
    accessToken = models.CharField(max_length=255)
    shopifyUrl = models.CharField(max_length=255,default="")
    contactName = models.CharField(max_length=255,default="")
    contactEmail = models.CharField(max_length=255,default="")
    
    def __str__(self):
        return self.shopName
    
    @staticmethod
    def validateSignature(request):
        params = request.GET.dict()
        signature = params.pop('signature')
        print(params)
        if signature is None:
            return False
        secret = os.environ.get("SHOPIFY_API_SECRET")
        print(secret)
        print(signature)
        line = ''.join([
            '%s=%s' % (key, value)
            for key, value in sorted(params.items())
        ])
        print(line)
        h = hmac.new(secret.encode('utf-8'), line.encode('utf-8'), hashlib.sha256)
        print(h.hexdigest())
        if hmac.compare_digest(h.hexdigest(), signature) == False:
            return False
        return True
    
    @staticmethod
    def load(domain):
        try:
            profile = ShopifySite.objects.get(shopifyDomain=domain)
            profile.startSession()
        except:
            print(f"Unable to load profile {domain}",file=sys.stderr)
            return None
        
    def startSession(self):
        shopify.ShopifyResource.activate_session(
            shopify.Session(
                f"{self.shopDomain}.myshopify.com/admin",
                os.environ.get("API_VERSION"),
                self.accessToken
            )
        )
    def shopDetails(self):
        self.startSession()
        shop = GraphQL().run(
            """
            query {
                shop {
                    contactEmail
                    url
                    shopOwnerName
                    name
                }
                
            }
            """,
            {}
        
        )
        if shop.isUnauthorized():
            return False
        self.contactEmail = shop.search("data.shop.contactEmail")
        self.contactName = shop.search("data.shop.shopOwnerName")
        self.shopName = shop.search("data.shop.name ")
        self.shopUrl = shop.search("data.shop.url")
        return True
        
    
    class Meta:
        db_table = "shopifySite"
    def tld(self):
        return f"{self.shopDomain}.myshopify.com"
