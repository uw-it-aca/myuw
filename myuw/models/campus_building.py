# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from django.db import transaction
import json


class Buildings(models.Model):
    code = models.CharField(max_length=10, db_index=True)
    number = models.CharField(max_length=10, db_index=True)
    latititude = models.CharField(max_length=40)
    longitude = models.CharField(max_length=40)
    name = models.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(Buildings, self).__init__(*args, **kwargs)

    def __eq__(self, other):
        return (
            self.code == other.code and
            self.number == other.number and
            self.latititude == other.latitude and
            self.longitude == other.longitude and
            self.name == other.name)

    def __hash__(self):
        return super().__hash__()

    @classmethod
    def exists(cls, code):
        return Buildings.objects.filter(code=code).exists()

    @classmethod
    def exists_by_number(cls, number):
        return Buildings.objects.filter(number=number).exists()

    @classmethod
    def get_building_by_code(cls, code):
        return Buildings.objects.get(code=code)

    @classmethod
    def get_building_by_number(cls, number):
        return Buildings.objects.get(number=number)

    @staticmethod
    @transaction.atomic
    def upd_building(fac_obj):
        if Buildings.exists_by_number(fac_obj.number):
            b_entry = Buildings.objects.select_for_update().get(
                number=fac_obj.number)
            b_entry.code = fac_obj.code.code
            b_entry.latititude = fac_obj.latitude,
            b_entry.longitude = fac_obj.longitude
            b_entry.name = fac_obj.name
            if b_entry != Buildings.get_building_by_number(fac_obj.number):
                b_entry.save()
            return b_entry

        if Buildings.exists(fac_obj.code):
            b_entry = Buildings.objects.select_for_update().get(
                code=fac_obj.code)
            b_entry.number = fac_obj.number
            b_entry.latititude = fac_obj.latitude,
            b_entry.longitude = fac_obj.longitude
            b_entry.name = fac_obj.name
            if b_entry != Buildings.get_building_by_code(fac_obj.code):
                b_entry.save()
            return b_entry

        return Buildings.objects.update_or_create(
            code=fac_obj.code,
            number=fac_obj.number,
            latititude=fac_obj.latitude,
            longitude=fac_obj.longitude,
            name=fac_obj.name
            )

    def json_data(self):
        return {
            "code": self.code,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "name": self.name,
            "number": self.number,
        }

    def __str__(self):
        return json.dumps(self.json_data(), default=str)

    class Meta:
        db_table = "myuw_campus_buildings"
        app_label = "myuw"
