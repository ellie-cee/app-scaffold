import uuid
from django.db import models
import os
import random
import pymupdf
from xyz import settings
import datetime


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
class ResumeVariant(models.Model):
    type = models.CharField(max_length=255,default="")       
    label = models.CharField(max_length=255,default="")

    class Meta:
        db_table = "resumeVariants"

class ApplicationVariant(models.Model):
    id = models.BigAutoField(primary_key=True)
    identifier = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=255)
    purged = models.BooleanField(default=False)
    filePath = models.CharField(max_length=255,default="")
    
    def process(self,variant):

        outputFileSuffix = f"{datetime.datetime.now().strftime("%Y-%m-%d")}-{random.randint(69,696969)}"
        outputFileName = f"eleanor-cassady-{outputFileSuffix}.pdf"
        
        
        outputFile = inputFile = os.path.join(
            settings.FILES_ROOT,
            "ephemeral",
            outputFileName
        )
        self.filePath = outputFile
        self.save()
        logger.error(
            os.path.join(
                settings.FILES_ROOT,
                "docs",
                f"resume-template-{variant}.pdf"
            )
        )
        logger.error(variant)
        document = pymupdf.open(
            os.path.join(
                settings.FILES_ROOT,
                "docs",
                f"resume-template-{variant}.pdf"
            )
        )
        for page in document:
            for link in page.get_links():
                
                if os.environ.get("SHOPIFY_DOMAIN") in link.get("uri"):
                    link["uri"] = f"https://{os.environ.get('SHOPIFY_DOMAIN')}/?srcId={self.identifier}"
                    page.update_link(link)
        document.save(outputFile)
        return outputFile,outputFileName
    
    