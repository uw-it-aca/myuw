# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from django.db import models


class PopularLink(models.Model):
    affiliation = models.CharField(max_length=256, null=True)
    pce = models.NullBooleanField()
    campus = models.CharField(max_length=8, null=True)
    url = models.CharField(max_length=512)
    label = models.CharField(max_length=50)

    def json_data(self):
        return {
            "affiliation": self.affiliation,
            "pce": self.pce,
            "campus": self.campus,
            "url": self.url,
            "label": self.label,
        }

    def __str__(self):
        return json.dumps(self.json_data(), default=str)
