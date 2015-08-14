from django.db import models


class Building(models.Model):
    code = models.CharField(max_length=6, db_index=True)
    latititude = models.CharField(max_length=40)
    longitude = models.CharField(max_length=40)
    name = models.CharField(max_length=200)

    class Meta:
        db_table = "myuw_mobile_building"
