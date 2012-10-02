from django.db import models
from datetime import datetime


class CourseColor(models.Model):
    regid = models.CharField(max_length=32, db_index=True)
    year = models.PositiveSmallIntegerField(db_index=True)
    quarter = models.CharField(max_length=10, db_index=True)
    curriculum_abbr = models.CharField(max_length=10)
    # 098 is a valid course number, and that leading 0 matters
    course_number = models.CharField(max_length=3)
    section_id = models.CharField(max_length=2)
    is_active = models.BooleanField()
    color_id = models.PositiveIntegerField()

    def section_label(self):
        return "%s,%s,%s,%s/%s" % (self.year,
            self.quarter, self.curriculum_abbr,
            self.course_number, self.section_id)

class User(models.Model):
    uwnetid = models.SlugField(max_length=16,
                               db_index=True,
                               unique=True)

    uwregid = models.CharField(max_length=32,
                               null=True,
                               db_index=True,
                               unique=True)

    last_visit = models.DateTimeField(default=datetime.now())


class UserMyLink(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT)
    linkid = models.PositiveSmallIntegerField()
    is_on = models.BooleanField()
    class Meta:
        unique_together = ('user',
                           'linkid')

class Link(models.Model):
    json_id = models.PositiveIntegerField()
    title = models.CharField(max_length=150)
    url = models.CharField(max_length=150)
    is_on = models.BooleanField()

    def json_data(self):
        data = {
            "title": self.title,
            "url": self.url,
            "is_on": self.is_on,
            "id": self.json_id
        }
        return data

class Building(models.Model):
    code = models.CharField(max_length=6)
    latititude = models.CharField(max_length=40)
    longitude = models.CharField(max_length=40)
    name = models.CharField(max_length=200)

