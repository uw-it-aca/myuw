# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from django.db import models


class MyuwNotice(models.Model):
    title = models.TextField(null=True)
    content = models.TextField(null=True)
    notice_type = models.TextField(max_length=128)
    notice_category = models.TextField(max_length=128)
    is_critical = models.BooleanField(default=False)

    start = models.DateTimeField()
    end = models.DateTimeField(null=True)
    last_edit_by = models.CharField(max_length=128)
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
    is_intl_stud = models.BooleanField(default=False)
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

    target_group = models.TextField(null=True, blank=True)

    def has_target_group(self):
        return self.target_group is not None and len(self.target_group)

    def json_data(self, include_abbr_week_month_day_format=False):
        # Returns dict in same format as SDB Notices
        notice_format = u"<span class=\"notice-title\">{}</span>" \
                        u"<span class=\"notice-body-with-title\">{}</span>"

        notice_content = notice_format.format(self.title, self.content)
        return {'notice_content': notice_content,
                'attributes': []}

    def get_notice_content(self):
        return self.title + self.content

    def __str__(self):
        data = {"title": self.title,
                "content": self.content,
                "notice_type": self.notice_type,
                "notice_category": self.notice_category,
                "is_critical": self.is_critical,
                "start": self.start.isoformat(),
                "end": self.end.isoformat(),
                "last_edit_by": self.last_edit_by,
                "last_edit_date": self.last_edit_date.isoformat(),
                "target_group": self.target_group,
                "is_bothell": self.is_bothell,
                "is_seattle": self.is_seattle,
                "is_tacoma": self.is_tacoma,
                "is_alumni": self.is_alumni,
                "is_applicant": self.is_applicant,
                "is_grad": self.is_grad,
                "is_grad_c2": self.is_grad_c2,
                "is_intl_stud": self.is_intl_stud,
                "is_pce": self.is_pce,
                "is_student": self.is_student,
                "is_undergrad": self.is_undergrad,
                "is_undergrad_c": self.is_undergrad_c2,
                "is_fyp": self.is_fyp,
                "is_past_student": self.is_past_student,
                "is_clinician": self.is_clinician,
                "is_employee": self.is_employee,
                "is_faculty": self.is_faculty,
                "is_instructor": self.is_instructor,
                "is_past_employee": self.is_past_employee,
                "is_retiree": self.is_retiree,
                "is_staff_employee": self.is_staff_employee,
                "is_stud_employee": self.is_stud_employee}
        return json.dumps(data, default=str)
