from django.db import models

class Locale(models.Model):
    def __init__(self,locale):
        self.locale = locale
        self.save()
        
    locale = models.CharField(max_length=15)
    
    def __unicode__(self):
        return self.locale
    
class OS(models.Model):
    def __init__(self,OS):
        self.OS = OS
        #self.save()
        
    OS = models.CharField(max_length=15)
    
    def __unicode__(self):
        return self.OS
        
class Results(models.Model):

    id = models.AutoField(primary_key=True)
    report_type = models.CharField(max_length=40)
    time_upload = models.DateTimeField()
    results = models.TextField()

