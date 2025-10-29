import uuid
from django.db import models


# Create your models here.

class IdAware:
    def getId(self):
        return str(self.id)

class BaseModel(models.Model):
    def getId(self):
        return str(self.id)


class SiteNav(models.Model,IdAware):
    id = models.BigAutoField(primary_key=True)
    #permission = models.CharField(max_length=64)
    url = models.CharField(max_length=255,default="/")
    label = models.CharField(max_length=255)
    displayOrder = models.IntegerField(default=99999999 )
    
    def __str__(self):
        return self.url
    
    
    
    class Meta:
        db_table="sitenav"
        
class ApplicationVariant(models.Model):
    id = models.BigAutoField(primary_key=True)
    identifier = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=255)
    purged = models.BooleanField(default=False)
    fileName = models.CharField(max_length=255,default="")
    
    