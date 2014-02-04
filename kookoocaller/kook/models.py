from django.db import models

class Dump(models.Model):
    type = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)    
    timestamp = models.DateTimeField(auto_now=True)    