# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from django.db import models


class ResCategoryLink(models.Model):
    ALL = "all"
    UGRAD = 'ugrad'
    GRAD = 'grad'
    PCE = 'pce'
    FYP = 'fyp'
    SEATTLE = 'seattle'
    BOTHELL = 'bothell'
    TACOMA = 'tacoma'

    url = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    affiliation = models.CharField(max_length=80, null=True)
    pce = models.NullBooleanField()
    campus = models.CharField(max_length=8, null=True)
    category_id = models.CharField(max_length=80)
    category_name = models.CharField(max_length=80)
    sub_category = models.CharField(max_length=80)
    subcategory_id = models.CharField(max_length=80, null=True)
    new_tab = models.BooleanField(default=False)

    def category_id_matched(self, acategory_id):
        return self.category_id == acategory_id

    def all_affiliation(self):
        return self.affiliation == ResCategoryLink.ALL

    def for_undergrad(self):
        return self.affiliation == ResCategoryLink.UGRAD

    def for_grad(self):
        return self.affiliation == ResCategoryLink.GRAD

    def for_pce(self):
        return self.affiliation == ResCategoryLink.PCE

    def for_fyp(self):
        return self.affiliation == ResCategoryLink.FYP

    def campus_matched(self, acampus):
        return (self.for_all_campus() or
                acampus is not None and self.campus == acampus.lower())

    def for_sea_campus(self):
        return self.campus == ResCategoryLink.SEATTLE

    def for_bot_campus(self):
        return self.campus == ResCategoryLink.BOTHELL

    def for_tac_campus(self):
        return self.campus == ResCategoryLink.TACOMA

    def for_all_campus(self):
        return self.campus is None

    def json_data(self):
        data = {
            "title": self.title,
            "url": self.url,
            "new_tab": self.new_tab
        }
        return data

    def set_category_id(self, category_name):
        self.category_id = self._concat_id(category_name)

    def set_subcategory_id(self, subcategory_name):
        self.subcategory_id = self._concat_id(subcategory_name)

    def _concat_id(self, long_name):
        concat = long_name.lower()
        concat = "".join(c for c in concat if c.isalpha())
        return concat

    def __str__(self):
        data = {"title": self.title,
                "url": self.url,
                "affiliation": self.affiliation,
                "pce": self.pce,
                "campus": self.campus,
                "category_id": self.category_id,
                "category_name": self.category_name,
                "sub_category": self.sub_category,
                "subcategory_id": self.subcategory_id,
                "new_tab": self.new_tab}
        return json.dumps(data, default=str)

    class Meta:
        db_table = "myuw_res_category_links"
