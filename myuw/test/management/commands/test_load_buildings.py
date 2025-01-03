# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from django.test import TransactionTestCase
from unittest.mock import patch
from django.core.management import call_command
from restclients_core.exceptions import DataFailureException
from uw_space.models import Facility
from myuw.models import CampusBuilding
from myuw.management.commands.load_buildings import Facilities


class TestDeleteSessions(TransactionTestCase):

    def test_init_load(self):
        records = CampusBuilding.objects.all()
        self.assertEqual(len(records), 0)
        call_command('load_buildings', '-l')
        records = CampusBuilding.objects.all()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].code, 'MEB')

    def test_update(self):
        obj = CampusBuilding.objects.create(
            code='NMEB',
            number='1347',
            latitude='47.653693',
            longitude='',
            name='Mechanical Engineering Building',
        )
        obj.save()
        obj = CampusBuilding.objects.create(
            code='NMEB',
            number='1347',
            latitude='',
            longitude='-122.304747',
            name='Mechanical Engineering Building',
        )
        obj.save()
        records = CampusBuilding.objects.all()
        self.assertEqual(len(records), 2)

        with patch.object(Facilities, 'search_by_code', spec=True) as mock:
            mock.return_value = [Facility(
                code='NMEB',
                last_updated=datetime.now(),
                latitude='47.653693',
                longitude='-122.304747',
                name='Mechanical Engineering Building',
                number='1347',
                site='Seattle Main Campus',
                status='A',
                type='Building')]
            call_command('load_buildings')
            records = CampusBuilding.objects.all()
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].code, 'NMEB')

    @patch.object(Facilities, 'search_by_code', spec=True)
    def test_error(self, mock):
        fac_obj = Facility(
            code='MEB',
            last_updated=datetime.now(),
            latitude='47.653693',
            longitude='-122.304747',
            name='Mechanical Engineering Building',
            number='1347',
            site='Seattle Main Campus',
            type='Building')
        CampusBuilding.upd_building(fac_obj)
        mock.side_effect = DataFailureException(
            'facility.json?facility_code=MEB', 404, '')
        call_command('load_buildings')
        records = CampusBuilding.objects.all()
        self.assertEqual(len(records), 1)
