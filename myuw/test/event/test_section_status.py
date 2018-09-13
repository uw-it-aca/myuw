import json
from django.test import TestCase
from django.conf import settings
from django.utils import timezone
from myuw.event.section_status import SectionStatusProcessor


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


class TestSectionStatusProcessor(TestCase):

    def test_process_message_content(self):
        with self.settings(RESTCLIENTS_MEMCACHED_SERVERS=('localhost:11211',),
                           AWS_SQS={'SECTION_SATSUS_V1': {
                               'ACCOUNT_NUMBER': '123456789012',
                               'QUEUE': 'xxxxxxxxxx',
                               'REGION': 'xxxx',
                               'KEY_ID': 'XXXXXXXXXXXXXXXX',
                               'KEY': 'YYYYYYYYYYYYYYYYYYYYYYYY',
                               'VISIBILITY_TIMEOUT': 10,
                               'MESSAGE_GATHER_SIZE': 10,
                               'VALIDATE_SNS_SIGNATURE': False,
                               'PAYLOAD_SETTINGS': {}}}):
            event_hdlr = SectionStatusProcessor()
            # discard the event
            event_hdlr.process_inner_message(M1)

            M1["EventDate"] = str(timezone.now())
            event_hdlr.process_inner_message(M1)
