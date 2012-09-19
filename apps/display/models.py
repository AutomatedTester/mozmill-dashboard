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

class SystemInfo(models.Model):

    id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=100)
    service_pack = models.CharField(max_length=40)
    system = models.CharField(max_length=40)
    version = models.CharField(max_length=40)
    bits = models.CharField(max_length=10)
    processor = models.CharField(max_length=10)
        
class Results(models.Model):

    id = models.AutoField(primary_key=True)
    report_type = models.CharField(max_length=40)
    tests_repository = models.CharField(max_length=50)
    tests_changeset = models.CharField(max_length=30)
    time_start = models.DateTimeField()
    application_changeset = models.CharField(max_length=30)
    system_info = models.ForeignKey(SystemInfo)
    platform_version = models.CharField(max_length=10)
    tests_passed = models.IntegerField()
    application_repository = models.CharField(max_length=50)
    platform_changeset = models.CharField(max_length=30)
    platform_repository = models.CharField(max_length=50)
    tests_failed = models.IntegerField()
    time_end = models.DateTimeField()
    application_locale = models.CharField(max_length=10)
    platform_buildid = models.CharField(max_length=30)
    application_version = models.CharField(max_length=10)
    tests_skipped = models.IntegerField()
    time_upload = models.DateTimeField()
    application_name = models.CharField(max_length=20)
    mozmill_version = models.CharField(max_length=10)
    report_version = models.CharField(max_length=10)
    results = models.TextField()

class DetailedResults(models.Model):
    id = models.AutoField(primary_key=True)
    passed_function = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    filename = models.CharField(max_length=255)
    failed = models.IntegerField()
    passed = models.IntegerField()
    results = models.ForeignKey(Results)

class Addons(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    is_compatible = models.BooleanField()
    version = models.CharField(max_length=10)
    addon_type = models.CharField(max_length=20, default='extension')
    addon_id = models.CharField(max_length=50)
    is_active = models.BooleanField()
    results = models.ForeignKey(Results)

