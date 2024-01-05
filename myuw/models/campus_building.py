# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models
from django.db import transaction
import json


class CampusBuilding(models.Model):
    code = models.CharField(max_length=16, db_index=True)
    # unique, but does change
    number = models.CharField(max_length=16, db_index=True)
    # unique and will never change
    latitude = models.CharField(max_length=32)
    longitude = models.CharField(max_length=32)
    name = models.CharField(max_length=96)

    def __init__(self, *args, **kwargs):
        super(CampusBuilding, self).__init__(*args, **kwargs)

    def __eq__(self, other):
        return (
            self.code == other.code and
            self.number == other.number and
            self.latitude == other.latitude and
            self.longitude == other.longitude and
            self.name == other.name)

    def __hash__(self):
        return super().__hash__()

    @staticmethod
    def exists(code):
        return CampusBuilding.objects.filter(code=code).exists()

    @staticmethod
    def exists_by_number(number):
        return CampusBuilding.objects.filter(number=number).exists()

    @staticmethod
    def get_building_by_code(code):
        return CampusBuilding.objects.get(code=code)

    @staticmethod
    def get_building_by_number(number):
        return CampusBuilding.objects.get(number=number)

    @staticmethod
    @transaction.atomic
    def upd_building(fac_obj):
        qset = CampusBuilding.objects.filter(code=fac_obj.code)
        if qset:
            if len(qset.values()) > 1:
                qset.delete()
            elif len(qset.values()) == 1:
                b_entry = CampusBuilding.objects.select_for_update().get(
                    code=fac_obj.code)
                if not b_entry.no_change(fac_obj):
                    b_entry.number = fac_obj.number
                    b_entry.latitude = fac_obj.latitude
                    b_entry.longitude = fac_obj.longitude
                    b_entry.name = fac_obj.name
                    b_entry.save()
                return b_entry

        qset = CampusBuilding.objects.filter(number=fac_obj.number)
        if qset:
            if len(qset.values()) > 1:
                qset.delete()
            elif len(qset.values()) == 1:
                b_entry = CampusBuilding.objects.select_for_update().get(
                    number=fac_obj.number)
                if not b_entry.no_change(fac_obj):
                    b_entry.code = fac_obj.code
                    b_entry.latitude = fac_obj.latitude
                    b_entry.longitude = fac_obj.longitude
                    b_entry.name = fac_obj.name
                    b_entry.save()
                return b_entry

        return CampusBuilding.objects.create(
            code=fac_obj.code,
            number=fac_obj.number,
            latitude=fac_obj.latitude,
            longitude=fac_obj.longitude,
            name=fac_obj.name)

    def no_change(self, fac_obj):
        return (
            self.code == fac_obj.code and
            self.number == fac_obj.number and
            self.latitude == fac_obj.latitude and
            self.longitude == fac_obj.longitude and
            self.name == fac_obj.name)

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
        app_label = 'myuw'
        # db_table = "myuw_campusbuilding"
        # would cause a rename of table
