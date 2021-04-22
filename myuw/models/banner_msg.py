# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
import uuid


class BannerMessage(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    message_title = models.TextField()
    message_body = models.TextField()

    is_published = models.BooleanField(default=False)

    affiliation = models.CharField(max_length=80, null=True)
    pce = models.NullBooleanField()
    campus = models.CharField(max_length=8, null=True)
    group_id = models.CharField(max_length=200, null=True)

    added_by = models.CharField(max_length=50)
    added_date = models.DateTimeField(auto_now_add=True)

    preview_id = models.SlugField(null=True, db_index=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.preview_id:
            self.preview_id = str(uuid.uuid4())

        super(BannerMessage, self).save(*args, **kwargs)

    class Meta(object):
        app_label = 'myuw'
