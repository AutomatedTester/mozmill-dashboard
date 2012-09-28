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

class Endurance(models.Model):
    id = models.AutoField(primary_key=True)
    delay = models.CharField(max_length=20)
    entities = models.IntegerField()
    iterations = models.IntegerField()
    restart = models.BooleanField()


class StatsInfo(models.Model):
    id = models.AutoField(primary_key=True)
    max_mem = models.IntegerField()
    ave_mem = models.IntegerField()
    min_mem = models.IntegerField()

class Stats(models.Model):
    id = models.AutoField(primary_key=True)
    resident = models.ForeignKey(StatsInfo, related_name='stats_resident')
    explicit = models.ForeignKey(StatsInfo, related_name='stats_explicit')

class Iterations(models.Model):
    id = models.AutoField(primary_key=True)
    stats = models.ForeignKey(Stats)

class CheckPoints(models.Model):
    id = models.AutoField(primary_key=True)
    resident = models.IntegerField()
    timestamp = models.DateTimeField()
    explicit = models.IntegerField()
    label = models.CharField(max_length=255, null=True)
    iterations = models.ForeignKey(Iterations)

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
    tests_repository = models.CharField(max_length=50, null=True)
    tests_changeset = models.CharField(max_length=30, null=True)
    time_start = models.DateTimeField()
    application_changeset = models.CharField(max_length=30, null=True)
    system_info = models.ForeignKey(SystemInfo)
    platform_version = models.CharField(max_length=30, null=True)
    tests_passed = models.IntegerField()
    application_repository = models.CharField(max_length=50, null=True)
    platform_changeset = models.CharField(max_length=30, null=True)
    platform_repository = models.CharField(max_length=50, null=True)
    tests_failed = models.IntegerField()
    time_end = models.DateTimeField()
    application_locale = models.CharField(max_length=10, null=True)
    platform_buildid = models.CharField(max_length=30, null=True)
    application_version = models.CharField(max_length=30, null=True)
    tests_skipped = models.IntegerField()
    time_upload = models.DateTimeField()
    application_name = models.CharField(max_length=20, null=True)
    mozmill_version = models.CharField(max_length=10, null=True)
    report_version = models.CharField(max_length=10, null=True)
    results = models.TextField()
    endurance = models.ForeignKey(Endurance, null=True)

class DetailedResults(models.Model):
    id = models.AutoField(primary_key=True)
    function = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    filename = models.CharField(max_length=255)
    failed = models.IntegerField()
    passed = models.IntegerField()
    results = models.ForeignKey(Results)

class Addons(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    is_compatible = models.BooleanField()
    version = models.CharField(max_length=30)
    addon_type = models.CharField(max_length=20, default='extension')
    addon_id = models.CharField(max_length=255)
    is_active = models.BooleanField()
    results = models.ForeignKey(Results)

class Patch(models.Model):
    id = models.AutoField(primary_key=True)
    url_mirror = models.TextField()
    build_id = models.CharField(max_length=100)
    download_duration = models.IntegerField()
    patch_type = models.CharField(max_length=30)
    is_complete = models.BooleanField()
    channel = models.CharField(max_length=100)
    size = models.IntegerField()

class BuildInfo(models.Model):
    id = models.AutoField(primary_key=True)
    build_id = models.CharField(max_length=100)
    locale = models.CharField(max_length=30)
    disabled_addons = models.TextField()
    version = models.CharField(max_length=100)
    useragent = models.TextField()
    url_aus = models.TextField()

class Updates(models.Model):
    id = models.AutoField(primary_key=True)
    build_pre = models.ForeignKey(BuildInfo, related_name='update_build_pre')
    build_post = models.ForeignKey(BuildInfo, related_name='update_build_post')
    result = models.ForeignKey(Results)
    success = models.BooleanField()
    fallback = models.BooleanField()
    patch = models.ForeignKey(Patch)
    target_buildid = models.CharField(max_length=100)
