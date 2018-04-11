from django.db import models


class PopularLink(models.Model):
    affiliation = models.CharField(max_length=80, null=True)
    pce = models.NullBooleanField()
    campus = models.CharField(max_length=8, null=True)
    url = models.CharField(max_length=512)
    label = models.CharField(max_length=50)
