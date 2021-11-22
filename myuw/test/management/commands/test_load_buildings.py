# Copyright 2021 UW-IT, University of Washington
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

    def test_run(self):
        records = CampusBuilding.objects.all()
        self.assertEquals(len(records), 0)
        call_command('load_buildings', '-l')
        records = CampusBuilding.objects.all()
        self.assertEquals(len(records), 1)
        self.assertEquals(records[0].code, 'MEB')

        with patch.object(Facilities, 'search_by_number', spec=True) as mock:
            mock.return_value = Facility(
                code='NMEB',
                last_updated=datetime.now(),
                latitude='47.653693',
                longitude='-122.304747',
                name='Mechanical Engineering Building',
                number='1347',
                site='Seattle Main Campus',
                type='Building')
            call_command('load_buildings')
            records = CampusBuilding.objects.all()
            self.assertEquals(len(records), 1)
            self.assertEquals(records[0].code, 'NMEB')

    @patch.object(Facilities, 'search_by_number', spec=True)
    def test_error(self, mock):
        mock.side_effect = DataFailureException(
            'facility/1347.json', 404, '')
        call_command('load_buildings')
