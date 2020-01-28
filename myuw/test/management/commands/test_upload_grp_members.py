from django.test import TestCase
from django.conf import settings
from django.core.management import call_command


class TestClearSessions(TestCase):

    def test_run(self):
        call_command('upload_grp_members', "u_myuwgroup_fyp", "fyp_list.txt")
