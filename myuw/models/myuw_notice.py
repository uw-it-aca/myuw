from django.db import models


class MyuwNotice(models.Model):
    title = models.TextField(null=True)
    content = models.TextField(null=True)
    notice_type = models.TextField(max_length=128)
    notice_category = models.TextField(max_length=128)

    start = models.DateTimeField()
    end = models.DateTimeField(null=True)
    last_edit_by = models.CharField(max_length=16)
    last_edit_date = models.DateTimeField(auto_now=True)

    # Affiliation Targeting
    # campus affil
    is_seattle = models.BooleanField(default=False)
    is_tacoma = models.BooleanField(default=False)
    is_bothell = models.BooleanField(default=False)

    # academic affil
    is_alumni = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)
    is_grad = models.BooleanField(default=False)
    is_grad_c2 = models.BooleanField(default=False)
    is_pce = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_undergrad = models.BooleanField(default=False)
    is_undergrad_c2 = models.BooleanField(default=False)
    is_fyp = models.BooleanField(default=False)
    is_past_student = models.BooleanField(default=False)

    # employee affil
    is_clinician = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_past_employee = models.BooleanField(default=False)
    is_retiree = models.BooleanField(default=False)
    is_staff_employee = models.BooleanField(default=False)
    is_stud_employee = models.BooleanField(default=False)

    def json_data(self, include_abbr_week_month_day_format=False):
        # Returns dict in same format as SDB Notices
        notice_format = u"<span class=\"notice-title\">{}</span>" \
                        u"<span class=\"notice-body-with-title\">{}</span>"

        notice_content = notice_format.format(unicode(self.title, 'utf-8'),
                                              unicode(self.content, 'utf-8'))
        return {'notice_content': notice_content,
                'attributes': []}

    def get_notice_content(self):
        return self.title + self.content
