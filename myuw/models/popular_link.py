import json
from django.db import models


class PopularLink(models.Model):
    affiliation = models.CharField(max_length=80, null=True)
    pce = models.NullBooleanField()
    intl_stud = models.BooleanField(default=False)
    campus = models.CharField(max_length=8, null=True)
    url = models.CharField(max_length=512)
    label = models.CharField(max_length=50)

    def json_data(self):
        return {
            "affiliation": self.affiliation,
            "pce": self.pce,
            "intl_stud": self.intl_stud,
            "campus": self.campus,
            "url": self.url,
            "label": self.label,
        }

    def __str__(self):
        return json.dumps(self.json_data(), default=str)
