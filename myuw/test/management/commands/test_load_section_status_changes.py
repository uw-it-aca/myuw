import time
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError


class TestLoadSectionStatus(TestCase):

    def test_run(self):
        with self.settings(AWS_SQS={
                'SECTION_SATSUS_V1': {
                    'ACCOUNT_NUMBER': '123456789012',
                    'QUEUE': 'xxxxxxxxxx',
                    'REGION': 'xxxx',
                    'KEY_ID': 'XXXXXXXXXXXXXXXX',
                    'KEY': 'YYYYYYYYYYYYYYYYYYYYYYYY',
                    'VISIBILITY_TIMEOUT': 10,
                    'MESSAGE_GATHER_SIZE': 10,
                    'VALIDATE_SNS_SIGNATURE': False,
                    'PAYLOAD_SETTINGS': {}}}):
            try:
                call_command('load_section_status_changes')
            except CommandError as err:
                self.assertTrue("Could not connect" in str(err))
