import hashlib
from datetime import datetime, timedelta
from dateutil.parser import parse
from django.utils import timezone
from django.db import models
from django.db.models import Count
from myuw.models.building import Building
from myuw.models.res_category_link import ResCategoryLink
from hashlib import sha1


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

    last_visit = models.DateTimeField(default=timezone.now)

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
    user = models.OneToOneField('User', on_delete=models.PROTECT)
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


class VisitedLink(models.Model):
    url = models.CharField(max_length=512)
    label = models.CharField(max_length=50, null=True)
    is_anonymous = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_undegrad = models.BooleanField(default=False)
    is_grad_student = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_seattle = models.BooleanField(default=False)
    is_tacoma = models.BooleanField(default=False)
    is_bothell = models.BooleanField(default=False)
    is_pce = models.BooleanField(default=False)
    is_student_employee = models.BooleanField(default=False)

    username = models.CharField(max_length=20)
    visit_date = models.DateTimeField(db_index=True, auto_now_add=True)

    MAX_RECENT_HISTORY = 100
    OLDEST_RECENT_TIME_DELTA = timedelta(days=-60)
    OLDEST_POPULAR_TIME_DELTA = timedelta(days=-30)

    @classmethod
    def recent_for_user(cls, username):
        # This is more code than i want, because django doesn't support
        # distinct on fields for sqlite
        min_visit = timezone.now() + VisitedLink.OLDEST_RECENT_TIME_DELTA
        objs = VisitedLink.objects.filter(username=username,
                                          visit_date__gte=min_visit)
        objs = objs.order_by('-visit_date')[:VisitedLink.MAX_RECENT_HISTORY]
        lookup = set()
        ordered = []
        for visited in objs:
            if visited.url not in lookup:
                lookup.add(visited.url)
                ordered.append(visited)

        return ordered

    @classmethod
    def get_popular(cls, **kwargs):
        min_visit = timezone.now() + VisitedLink.OLDEST_POPULAR_TIME_DELTA
        objs = VisitedLink.objects.filter(visit_date__gte=min_visit,
                                          **kwargs)
        objs = objs.values('url', 'label')
        objs = objs.annotate(num_users=Count('username', distinct=True),
                             all=Count('*'))

        by_url = {}
        for item in objs:
            url = item['url']
            if url not in by_url:
                by_url[url] = {'labels': [],
                               'users': 0,
                               'all': 0}
            by_url[url]['users'] += item['num_users']
            by_url[url]['all'] += item['all']
            by_url[url]['labels'].append(item['label'])

        values = []
        for url in by_url:
            popularity = by_url[url]['users'] * by_url[url]['all']

            values.append({'popularity': popularity,
                           'url': url,
                           'labels': sorted(by_url[url]['labels'])})

        return sorted(values, key=lambda x: x['popularity'], reverse=True)


class PopularLink(models.Model):
    affiliation = models.CharField(max_length=80, null=True)
    pce = models.NullBooleanField()
    campus = models.CharField(max_length=8, null=True)
    url = models.CharField(max_length=512)
    label = models.CharField(max_length=50)


class CustomLink(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    url = models.CharField(max_length=512)
    label = models.CharField(max_length=50, null=True)
    url_key = models.SlugField(max_length=40)

    def save(self, *args, **kwargs):
        self.url_key = self.get_url_key(self.url)
        super(CustomLink, self).save(*args, **kwargs)

    @staticmethod
    def get_url_key(url):
        return sha1(url.encode('utf-8')).hexdigest()

    class Meta:
        unique_together = (('url_key', 'user'),)


class HiddenLink(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    url = models.CharField(max_length=512)
    url_key = models.SlugField(max_length=40)

    def save(self, *args, **kwargs):
        self.url_key = self.get_url_key(self.url)
        super(HiddenLink, self).save(*args, **kwargs)

    @staticmethod
    def get_url_key(url):
        return sha1(url.encode('utf-8')).hexdigest()

    class Meta:
        unique_together = (('url_key', 'user'),)


class BannerMessage(models.Model):
    VALID_ELIGIBILITY_TYPES = [
        'netid'
    ]
    start = models.DateField()
    end = models.DateField()
    eligibility_type = models.CharField(max_length=32)
    eligibility_data = models.CharField(max_length=255)
    message_title = models.TextField()
    message_body = models.TextField()

    @classmethod
    def from_csv(cls, csv):
        message = cls()
        message.start = parse(csv[0]).date()
        message.end = parse(csv[1]).date()
        message.eligibility_type = csv[2]
        if message.eligibility_type not in cls.VALID_ELIGIBILITY_TYPES:
            raise ValueError
        message.eligibility_data = csv[3]
        message.message_title = csv[4]
        message.message_body = csv[5]
        return message

    def json_data(self):
        data = {"title": self.message_title,
                "body": self.message_body}
        return data
