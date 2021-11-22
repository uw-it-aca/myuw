# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import date
from django.test import TransactionTestCase
from django.core.management import call_command
from myuw.models import CampusBuilding


class TestDeleteSessions(TransactionTestCase):

    def test_run(self):
        records = CampusBuilding.objects.all()
        self.assertEquals(len(records), 0)
        call_command('load_buildings')
        records = CampusBuilding.objects.all()
        self.assertEquals(len(records), 1)
