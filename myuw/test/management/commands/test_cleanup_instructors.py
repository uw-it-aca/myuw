# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import date
from django.test import TransactionTestCase
from django.core.management import call_command
from myuw.models import Instructor, User


class TestDeleteSessions(TransactionTestCase):

    def test_run(self):
        year = date.today().year - 7
        user = User.get_user('bill')
        Instructor.add_seen_instructor(user, year, 'spring')
        user = User.get_user('billsea')
        Instructor.add_seen_instructor(user, year, 'summer')
        user = User.get_user('retirestaff')
        Instructor.add_seen_instructor(user, year, 'winter')
        user = User.get_user('billjoint')
        Instructor.add_seen_instructor(user, date.today().year - 6, 'summer')
        records = Instructor.objects.all()
        self.assertEquals(len(records), 4)
        call_command('cleanup_instructors')
        records = Instructor.objects.all()
        self.assertEquals(len(records), 3)
        self.assertEquals(records[1].year, 2013)
        self.assertEquals(records[2].year, 2013)
