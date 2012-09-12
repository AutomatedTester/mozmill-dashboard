from  django.db import models

class Results(models.Model):

    id = models.AutoField(primary_key=True)
    results = models.TextField()



