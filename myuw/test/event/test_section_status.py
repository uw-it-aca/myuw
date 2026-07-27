# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import mock

from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from myuw.event.section_status import (
    CachedHTTPResponse,
    MyUWMemcachedCache,
    SectionStatusProcessor,
    SectionStatusProcessorException,
)

M1 = {
    "Header": {},
    "EventID": "...",
    "Href": "/student/v5/course/2018,autumn,HCDE,210/A/status.json",
    "EventDate": "2018-08-12T16:39:08.2704415-07:00",
    "Previous": {
        "CurrentEnrollment": 137,
        "CurrentRegistrationPeriod": "2",
        "AddCodeRequired":  False,
        "FacultyCodeRequired":  False,
        "LimitEstimateEnrollment": 150,
        "LimitEstimateEnrollmentIndicator": "limit",
        "RoomCapacity": 250,
        "Section": {
            "Href": "/student/v5/course/2018,autumn,HCDE,210/A.json",
            "Year": 2018,
            "Quarter": "autumn",
            "CurriculumAbbreviation": "HCDE",
            "CourseNumber": "210",
            "SectionID": "A",
            "SLN": "15753"},
        "SLN": "15753",
        "SpaceAvailable": 13,
        "Status": "open"},
    "Current": {
        "CurrentEnrollment": 138,
        "CurrentRegistrationPeriod": "2",
        "AddCodeRequired":  False,
        "FacultyCodeRequired":  False,
        "LimitEstimateEnrollment": 150,
        "LimitEstimateEnrollmentIndicator": "limit",
        "RoomCapacity": 250,
        "Section": {
            "Href": "/student/v5/course/2018,autumn,HCDE,210/A.json",
            "Year": 2018,
            "Quarter": "autumn",
            "CurriculumAbbreviation": "HCDE",
            "CourseNumber": "210",
            "SectionID": "A",
            "SLN": "15753"},
        "SLN": "15753",
        "SpaceAvailable": 12,
        "Status": "open"}
}
override = override_settings(
    AWS_SQS={'SECTION_STATUS_V1': {
        'QUEUE_ARN': "arn:aws:sqs:us-xxxx-1:123456789012:xxxx_xxxx",
        'KEY_ID': 'XXXXXXXXXXXXXXXX',
        'KEY': 'YYYYYYYYYYYYYYYYYYYYYYYY',
        'VISIBILITY_TIMEOUT': 10,
        'MESSAGE_GATHER_SIZE': 10,
        'VALIDATE_SNS_SIGNATURE': False,
        'PAYLOAD_SETTINGS': {}}},
    MEMCACHED_SERVERS="")


class TestSectionStatusProcessor(TestCase):
    def test_message_validation(self):
        processor = SectionStatusProcessor()
        self.assertTrue(processor.validate_message_body({}))
        self.assertTrue(processor.validate_message_body(M1))
        self.assertTrue(processor.validate_message_body(
            {'EventDate': str(timezone.now())}))
        self.assertTrue(processor.validate_message_body(
            {'EventDate': str(timezone.now()),
             'Current': None}))

    @mock.patch.object(MyUWMemcachedCache, 'updateCache')
    def test_process_message_content(self, mock_updateCache):
        processor = SectionStatusProcessor()

        # Tests for missing data
        self.assertRaises(SectionStatusProcessorException,
                          processor.process_message_body, {})
        self.assertRaises(SectionStatusProcessorException,
                          processor.process_message_body,
                          {'Current': None, 'Href': '/'})
        self.assertRaises(SectionStatusProcessorException,
                          processor.process_message_body,
                          {'Current': {}, 'Href': ''})

        # Test for updateCache args
        processor.process_message_body(M1)
        args, _kwargs = mock_updateCache.call_args

        self.assertEqual(args[0], 'sws')
        self.assertEqual(args[1],
                         '/student/v5/course/2018,autumn,HCDE,210/A/status.json')
        self.assertIsInstance(args[2], CachedHTTPResponse)
