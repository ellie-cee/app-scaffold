from django.db import models
from encrypted_model_fields.fields import EncryptedCharField


# Create your models here.

class ShopifySite(models.Model):
    id = models.BigAutoField(primary_key=True)
    shopName = models.CharField(max_length=128)
    shopDomain = models.CharField(max_length=64)
    appKey = models.CharField(max_length=64)
    accessToken = EncryptedCharField(max_length=255)
    
    def __str__(self):
        return self.shopName
    
    class Meta:
        db_table = "shopifySite"
    def tld(self):
        return f"{self.shopDomain}.myshopify.com"
