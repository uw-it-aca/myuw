import os
import json
from copy import deepcopy
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone
from myuw.event.section_status import (
    SectionStatusProcessor, SectionStatusProcessorException)


M1 = {
    "EventID": "...",
    "Href": "/v5/course/2018,autumn,HCDE,210/A/status.json",
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
            "Href": "/v5/course/2018,autumn,HCDE,210/A.json",
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
            "Href": "/v5/course/2018,autumn,HCDE,210/A.json",
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
        'PAYLOAD_SETTINGS': {}}})


@override
class TestSectionStatusProcessor(TestCase):
    def test_message_validation(self):
        event_hdlr = SectionStatusProcessor()
        self.assertFalse(event_hdlr.validate_message_body(None))
        self.assertFalse(event_hdlr.validate_message_body({}))
        self.assertFalse(event_hdlr.validate_message_body({"EventDate": None}))
        self.assertFalse(event_hdlr.validate_message_body(M1))
        self.assertFalse(event_hdlr.validate_message_body(
            {"EventDate": str(timezone.now())}))
        self.assertFalse(event_hdlr.validate_message_body(
            {"EventDate": str(timezone.now()),
             "Current": {}}))
        self.assertFalse(event_hdlr.validate_message_body(
            {"EventDate": str(timezone.now()),
             "Current": None}))
        m1 = deepcopy(M1)
        m1.pop('Href')
        self.assertFalse(event_hdlr.validate_message_body(m1))

        m2 = deepcopy(M1)
        m2.pop("Current")
        self.assertFalse(event_hdlr.validate_message_body(m2))

    def test_process_message_content(self):
        event_hdlr = SectionStatusProcessor()
        M1["EventDate"] = str(timezone.now())
        self.assertRaises(SectionStatusProcessorException,
                          event_hdlr.process_message_body, M1)

        self.assertTrue(event_hdlr.validate_message_body(M1))
        event_hdlr.process_message_body(M1)
