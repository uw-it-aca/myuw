from django.db import models
from datetime import datetime
import hashlib


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
    json_id = models.PositiveIntegerField(db_index=True,
                                          unique=True)
    title = models.CharField(max_length=150)
    url = models.CharField(max_length=150)
    is_on = models.BooleanField()

    def json_data(self):
        data = {
            "id": self.json_id,
            "title": self.title,
            "url": self.url,
            "is_on": self.is_on
        }
        return data

class Building(models.Model):
    code = models.CharField(max_length=6, db_index=True)
    latititude = models.CharField(max_length=40)
    longitude = models.CharField(max_length=40)
    name = models.CharField(max_length=200)

class StudentAccountsBalances(models.Model):
    student_number = models.CharField(max_length=10,
                                      db_index=True,
                                      unique=True)
    employee_id = models.CharField(max_length=10,
                                   db_index=True,
                                   null=True,
                                   blank=True)
    asof_datetime = models.DateTimeField()
    is_am = models.BooleanField(default=True)
    husky_card = models.DecimalField(max_digits=6,
                                     decimal_places=2,
                                     default=0.00)
    residence_hall_dining = models.DecimalField(max_digits=7,
                                                decimal_places=2,
                                                null=True,
                                                blank=True)

    def json_data(self):
        data = {
            "asof_date": self.asof_datetime.date().strftime("%m/%d/%Y"),
            "asof_time": self.asof_datetime.time().strftime("%H:%M"),
            "husky_card": self.husky_card,
            "residence_hall_dining": self.residence_hall_dining
            }
        return data


class UserNotices(models.Model):
    notice_hash = models.CharField(max_length=32, unique=True)
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    first_viewed = models.DateTimeField(auto_now_add=True)
    marked_read = models.DateTimeField(null=True)
    is_read = models.BooleanField(default=False)

    @staticmethod
    def generate_hash(notice):
        notice_hash = hashlib.md5()
        notice_hash.update(notice.notice_type)
        notice_hash.update(notice.notice_category)
        notice_hash.update(notice.notice_content)
        return notice_hash.hexdigest()

    @staticmethod
    def mark_notices_read(notice_hashes, user):
        notices = UserNotices.objects.filter(notice_hash__in=notice_hashes, user=user)
        for notice in notices:
            notice.is_read = True
            notice.marked_read = datetime.now()
            notice.save()


class CategoryLinks(models.Model):
    url = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    campus = models.CharField(max_length=8, null=True)
    category_id = models.CharField(max_length=80)
    category_name = models.CharField(max_length=80)
    sub_category = models.CharField(max_length=80)

    def json_data(self):
        data = {
            "title": self.title,
            "url": self.url
        }
        return data

    def set_category_id(self, category_name):
        category_id = category_name.lower()
        category_id = "".join(c for c in category_id if c.isalpha())
        self.category_id = category_id

class TuitionDate(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT, unique=True)
    date_stored = models.DateTimeField(auto_now=True)
    date = models.DateTimeField()
