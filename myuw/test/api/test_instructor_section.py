import json
from django.test.utils import override_settings
from restclients_core.exceptions import DataFailureException
from myuw.test.api import MyuwApiTest, fdao_sws_override, fdao_pws_override
from myuw.views.api.instructor_section import InstSectionDetails,\
    LTIInstSectionDetails
from myuw.test.views.lti import get_lti_request, MyuwLTITest
from myuw.test import get_request, get_request_with_user, get_request_with_date


@fdao_sws_override
@fdao_pws_override
class TestInstSectDetails(MyuwApiTest):

    def test_billsea_section(self):
        now_request = get_request()
        get_request_with_user('billsea', now_request)

        section_id = '2017,autumn,CSE,154/A'
        resp = InstSectionDetails().get(now_request, section_id=section_id)
        data = json.loads(resp.content)
        self.assertEqual(len(data['sections']), 5)
        self.assertEqual(data['sections'][0]['section_type'], 'lecture')
        self.assertEqual(data['sections'][0]['section_label'],
                         '2017_autumn_CSE_154_A')

        self.assertTrue(data['sections'][0]['has_linked_sections'])
        self.assertEqual(len(data['sections'][0]['registrations']), 3)
        self.assertEqual(
            data['sections'][0]['registrations'][0]['linked_sections'],
            'AA AB')
        self.assertEqual(
            data['sections'][0]['registrations'][0]['first_name'], "June")
        self.assertEqual(
            data['sections'][0]['registrations'][0]['surname'], "Student3")
        self.assertEqual(
            data['sections'][0]['registrations'][0]['credits'], "3")
        self.assertEqual(
            data['sections'][0]['registrations'][0]['class_level'], "SENIOR")
        self.assertEqual(
            data['sections'][0]['registrations'][0]['class_code'], 4)
        self.assertEqual(
            data['sections'][0]['registrations'][0]['email'],
            'javg003@u.washington.edu')
        self.assertEqual(
            len(data['sections'][0]['registrations'][0]['majors']), 1)
        self.assertEqual(
            data['sections'][0]['registrations'][1]['linked_sections'],
            'AA AC')
        self.assertEqual(
            len(data['sections'][0]['registrations'][1]['majors']), 1)
        self.assertEqual(data['sections'][0]['total_linked_secondaries'], 4)

    def test_bill_section(self):
        request = get_request()
        get_request_with_user('bill', request)

        section_id = '2013,spring,ESS,102/A'
        resp = InstSectionDetails().get(request, section_id=section_id)
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)
        self.assertEqual(len(data['sections']), 2)
        self.assertEqual(
            data['sections'][0]['limit_estimate_enrollment'], 15)
        self.assertEqual(
            data['sections'][0]['final_exam']['latitude'],
            47.656645546715)
        self.assertEqual(data['sections'][0]['canvas_url'],
                         'https://canvas.uw.edu/courses/149651')
        self.assertEqual(
            len(data['sections'][0]['grade_submission_delegates']), 1)

        self.assertEqual(len(data['sections'][0]['registrations']), 4)

        netid_counts = {}

        for registration in data['sections'][0]['registrations']:
            if registration["netid"] in netid_counts:
                netid_counts[registration["netid"]] = netid_counts[
                    registration["netid"]] + 1
            else:
                netid_counts[registration["netid"]] = 1

        self.assertEqual(netid_counts["javg001"], 2)

        self.assertGreater(len(data['related_terms']), 3)
        self.assertEqual(data['related_terms'][
            len(data['related_terms']) - 3]['quarter'], 'Spring')
        self.assertEqual(data['related_terms'][5]['year'], 2013)

    def test_billpce_section(self):
        request = get_request()
        get_request_with_user('billpce', request)

        section_id = '2013,winter,PSYCH,203/A'
        resp = InstSectionDetails().get(request, section_id=section_id)
        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)
        self.assertEqual(data['sections'][0]['is_independent_start'], True)

        self.assertIn('start_date', data['sections'][0]['registrations'][0])
        self.assertEqual(len(data['sections'][0]['registrations']), 3)

        reg = data['sections'][0]['registrations'][0]
        self.assertEqual(reg['start_date'], '02/22/2013')
        self.assertEqual(reg['end_date'], '11/14/2013')

        reg = data['sections'][0]['registrations'][1]
        self.assertEqual(reg['start_date'], '01/01/2013')
        self.assertEqual(reg['end_date'], '12/13/2013')

        reg = data['sections'][0]['registrations'][2]
        self.assertEqual(reg['start_date'], '')
        self.assertEqual(reg['end_date'], '')

    def test_invalid_section(self):
        request = get_request()
        get_request_with_user('bill', request)

        section_id = ''
        resp = InstSectionDetails().get(request, section_id=section_id)
        self.assertEqual(resp.status_code, 400)

        section_id = '12345'
        resp = InstSectionDetails().get(request, section_id=section_id)
        self.assertEqual(resp.status_code, 400)


@override_settings(BLTI_AES_KEY=b"11111111111111111111111111111111",
                   BLTI_AES_IV=b"1111111111111111")
class TestLTIInstructorSectionDetails(MyuwLTITest):
    def test_bill_section(self):
        request = get_lti_request()

        section_id = '2013-spring-ESS-102-A'
        resp = LTIInstSectionDetails().get(request, section_id=section_id)

        self.assertEqual(resp.status_code, 200)

        data = json.loads(resp.content)
        self.assertEqual(len(data['sections']), 2)
        self.assertEqual(
            data['sections'][0]['limit_estimate_enrollment'], 15)
        self.assertEqual(
            data['sections'][0]['final_exam']['latitude'],
            47.656645546715)
        self.assertEqual(data['sections'][0]['canvas_url'],
                         'https://canvas.uw.edu/courses/149651')
        self.assertEqual(
            len(data['sections'][0]['grade_submission_delegates']), 1)

        self.assertGreater(len(data['related_terms']), 3)
        self.assertEqual(data['related_terms'][
            len(data['related_terms']) - 3]['quarter'], 'Spring')
        self.assertEqual(data['related_terms'][5]['year'], 2013)

    def test_invalid_section(self):
        request = get_lti_request()

        section_id = ''
        resp = LTIInstSectionDetails().get(request, section_id=section_id)
        self.assertEqual(resp.status_code, 403)

        section_id = '12345'
        resp = LTIInstSectionDetails().get(request, section_id=section_id)
        self.assertEqual(resp.status_code, 403)
