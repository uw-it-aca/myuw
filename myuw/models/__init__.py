import json
import logging
import hashlib
from hashlib import sha1
from datetime import datetime, timedelta
from dateutil.parser import parse
from django.utils import timezone
from django.db import models
from django.db.models import Count
from myuw.models.building import Building
from myuw.models.banner_msg import BannerMessage
from myuw.models.popular_link import PopularLink
from myuw.models.res_category_link import ResCategoryLink

logger = logging.getLogger(__name__)


##########################################
# this file has only user related tables #
##########################################


class User(models.Model):
    uwnetid = models.SlugField(max_length=16,
                               db_index=True,
                               unique=True)
    last_visit = models.DateTimeField(editable=True)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    @classmethod
    def get_user_by_netid(cls, uwnetid):
        return User.objects.get(uwnetid=uwnetid)

    @classmethod
    def get_user(cls, uwnetid, prior_netids=[]):
        obj = None
        try:
            obj = User.get_user_by_netid(uwnetid)
            obj.update_user(uwnetid)

        except User.DoesNotExist:
            # no entry for the current netid

            for prior_netid in reversed(prior_netids):
                try:
                    obj = User.get_user_by_netid(prior_netid)
                    obj.update_user(uwnetid)
                    break
                except User.DoesNotExist:
                    pass

        if obj is None:
            # no existing entry
            obj = User(uwnetid=uwnetid,
                       last_visit=timezone.now())
            obj.save()

        return obj

    def is_netid_changed(self, uwnetid):
        return uwnetid != self.uwnetid

    def update_user(self, uwnetid):
        if self.is_netid_changed(uwnetid):
            self.uwnetid = uwnetid
        self.last_visit = timezone.now()
        self.save()

    def __eq__(self, other):
        return self.uwnetid == other.uwnetid

    def json_data(self):
        return {
            "uwnetid": self.uwnetid,
            "last_visit": str(self.last_visit)
        }

    def __str__(self):
        return json.dumps(self.json_data(), default=str)

    class Meta:
        app_label = 'myuw'
        db_table = "myuw_mobile_user"


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
        notice_hash.update(notice.notice_type.encode('utf-8'))
        notice_hash.update(notice.notice_category.encode('utf-8'))
        notice_hash.update(notice.notice_content.encode('utf-8'))
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


class SeenInstructor(models.Model):
    uwnetid = models.SlugField(max_length=16,
                               db_index=True)
    year = models.PositiveSmallIntegerField(db_index=True)
    quarter = models.CharField(max_length=10, db_index=True)

    unique_together = (("uwnetid",
                        "year",
                        "quarter"
                        ),
                       )


class UserMigrationPreference(models.Model):
    username = models.CharField(max_length=20, db_index=True, unique=True)
    use_legacy_site = models.BooleanField(default=False)


class VisitedLinkNew(models.Model):
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

    user = models.ForeignKey('User', on_delete=models.PROTECT)
    visit_date = models.DateTimeField(db_index=True, auto_now_add=True)

    MAX_RECENT_HISTORY = 100
    OLDEST_RECENT_TIME_DELTA = timedelta(days=-60)
    OLDEST_POPULAR_TIME_DELTA = timedelta(days=-30)

    @classmethod
    def recent_for_user(cls, user):
        # This is more code than i want, because django doesn't support
        # distinct on fields for sqlite
        min_visit = timezone.now() + VisitedLinkNew.OLDEST_RECENT_TIME_DELTA
        objs = VisitedLinkNew.objects.filter(user=user,
                                             visit_date__gte=min_visit)
        objs = objs.order_by('-pk')[:VisitedLinkNew.MAX_RECENT_HISTORY]
        lookup = set()
        ordered = []
        for visited in objs:
            if visited.url not in lookup:
                lookup.add(visited.url)
                ordered.append(visited)

        return ordered

    @classmethod
    def get_popular(cls, **kwargs):
        min_visit = timezone.now() + VisitedLinkNew.OLDEST_POPULAR_TIME_DELTA
        objs = VisitedLinkNew.objects.filter(visit_date__gte=min_visit,
                                             **kwargs)
        objs = objs.values('url', 'label')
        objs = objs.annotate(num_users=Count('user', distinct=True),
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


class UserCourseDisplay(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT)
    year = models.PositiveSmallIntegerField()
    quarter = models.CharField(max_length=10)
    section_label = models.CharField(max_length=64)
    # year,quarter,curriculum_abbr,course_number/section_id
    color_id = models.PositiveSmallIntegerField()
    pin_on_teaching_page = models.BooleanField(default=False)

    @classmethod
    def delete_section_display(cls, user, section_label):
        obj = UserCourseDisplay.get_section_display(
            user=user, section_label=section_label)
        obj.delete()

    @classmethod
    def get_section_display(cls, user, section_label):
        return UserCourseDisplay.objects.get(user=user,
                                             section_label=section_label)

    @classmethod
    def get_course_display(cls, user, year, quarter):
        objs = UserCourseDisplay.objects.filter(user=user,
                                                year=year,
                                                quarter=quarter)
        pin_on_teaching = []  # section_labels
        color_dict = {}  # section_labels: color_id
        colors_taken = []  # a list of color_ids
        for record in objs:
            if record.pin_on_teaching_page is True:
                pin_on_teaching.append(record.section_label)
            color_dict[record.section_label] = record.color_id
            if record.color_id not in colors_taken:
                colors_taken.append(record.color_id)

        return color_dict, colors_taken, pin_on_teaching

    def save_section_color(self, color_id):
        self.color_id = color_id
        self.save()

    def json_data(self):
        return {
            "user": self.user.json_data(),
            "section_label": self.section_label,
            "color_id": self.color_id,
            "pin_on_teaching_page": self.pin_on_teaching_page
        }

    def __str__(self):
        return json.dumps(self.json_data(), default=str)

    class Meta(object):
        app_label = 'myuw'
        db_table = 'user_course_display_pref'
        unique_together = ("user", "section_label")
        index_together = [
            ["user", "year", "quarter"],
            ["user", "section_label"],
        ]
        ordering = ['section_label']


class MigrationPreference(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    display_onboard_message = models.BooleanField(default=True)
    use_legacy_site = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(MigrationPreference, self).__init__(*args, **kwargs)

    @classmethod
    def set_preference(cls, user,
                       display_onboard_message=True,
                       use_legacy_site=False):
        obj, is_new = MigrationPreference.objects.get_or_create(user=user)

        if (obj.display_onboard_message != display_onboard_message or
                obj.use_legacy_site != use_legacy_site):
            obj.display_onboard_message = display_onboard_message
            obj.use_legacy_site = use_legacy_site
            obj.save()
        return obj

    def json_data(self):
        return {
            "user": self.user.json_data(),
            "display_onboard_message": self.display_onboard_message,
            "use_legacy_site": self.use_legacy_site
        }

    def __str__(self):
        return json.dumps(self.json_data(), default=str)

    class Meta(object):
        app_label = 'myuw'
        db_table = 'migration_preference'
