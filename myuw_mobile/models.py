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


class UserId(models.Model):
    uwregid = models.CharField(max_length=32,
                               db_index=True,
                               unique=True)
    class Meta:
        abstract = True


class User(UserId):
    uwnetid = models.SlugField(max_length=16,
                               db_index=True,
                               unique=True)
    use_default_mylink = models.BooleanField()
    last_visit = models.DateTimeField(default=datetime.now())


class UserMyLink(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT)
    linkid = models.PositiveSmallIntegerField()
    class Meta:
        unique_together = ('user',
                           'linkid')


