# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError

ARN = "arn:aws:sqs:us-xxxx-1:123456789012:uw-eval-myuw"


class TestLoadSectionStatus(TestCase):

    def test_run(self):
        with self.settings(AWS_SQS={
                'SECTION_STATUS_V1': {
                    'QUEUE_ARN': ARN,
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
