import hashlib
from datetime import datetime
from django.utils import timezone
from django.db import models
from myuw.models.building import Building
from myuw.models.res_category_link import ResCategoryLink


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
                                   self.quarter,
                                   self.curriculum_abbr,
                                   self.course_number,
                                   self.section_id
                                   )

    class Meta:
        db_table = "myuw_mobile_coursecolor"


class User(models.Model):
    uwnetid = models.SlugField(max_length=16,
                               db_index=True,
                               unique=True)

    uwregid = models.CharField(max_length=32,
                               null=True,
                               db_index=True,
                               unique=True)

    last_visit = models.DateTimeField(default=timezone.now())

    class Meta:
        db_table = "myuw_mobile_user"


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

    class Meta:
        db_table = "myuw_mobile_studentaccountsbalances"


class TuitionDate(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT, unique=True)
    date_stored = models.DateTimeField(auto_now=True)
    date = models.DateField()

    class Meta:
        db_table = "myuw_mobile_tuitiondate"


class UserNotices(models.Model):
    notice_hash = models.CharField(max_length=32)
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    first_viewed = models.DateTimeField(auto_now_add=True)
    marked_read = models.DateTimeField(null=True)
    is_read = models.BooleanField(default=False)
    notice_cattype = models.CharField(max_length=256, null=True, blank=True)

    @staticmethod
    def generate_hash(notice):
        notice_hash = hashlib.md5()
        notice_hash.update(notice.notice_type)
        notice_hash.update(notice.notice_category)
        notice_hash.update(notice.notice_content)
        return notice_hash.hexdigest()

    @staticmethod
    def mark_notices_read(notice_hashes, user):
        notices = UserNotices.objects.filter(notice_hash__in=notice_hashes,
                                             user=user)
        for notice in notices:
            notice.is_read = True
            # notice.marked_read = datetime.now()
            notice.save()

    class Meta:
        unique_together = (("notice_hash", "user"),)
        db_table = "myuw_mobile_usernotices"


class SeenRegistration(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    year = models.PositiveSmallIntegerField(db_index=True)
    quarter = models.CharField(max_length=10, db_index=True)
    summer_term = models.CharField(max_length=1)
    first_seen_date = models.DateTimeField(auto_now_add=True)

    unique_together = (("user",
                        "year",
                        "quarter",
                        "summer_term"
                        ),
                       )

    class Meta:
        db_table = "myuw_mobile_seenregistration"


class UserMigrationPreference(models.Model):
    username = models.CharField(max_length=20, db_index=True, unique=True)
    use_legacy_site = models.BooleanField(default=False)
