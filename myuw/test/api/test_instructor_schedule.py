import json
from django.test.utils import override_settings
from myuw.test.api import require_url, MyuwApiTest
from restclients_core.exceptions import DataFailureException
from myuw.views.api.instructor_schedule import InstScheCurQuar, InstSect
from myuw.dao.instructor_schedule import get_instructor_schedule_by_term
from myuw.dao.term import get_current_quarter
from myuw.test import get_request_with_user, get_request_with_date


def get_current_quarter_instructor_schedule(request):
    schedule = get_instructor_schedule_by_term(
        request, get_current_quarter(request))
    return schedule


@require_url('myuw_instructor_current_schedule_api')
class TestInstructorCurrentSchedule(MyuwApiTest):

    def test_bill_current_term(self):
        now_request = get_request_with_user('bill')
        schedule = get_current_quarter_instructor_schedule(now_request)

        resp = InstScheCurQuar().get(now_request)
        data = json.loads(resp.content)

        self.assertEqual(len(data['sections']), 6)
        section1 = data['sections'][0]
        self.assertEqual(section1['lib_subj_guide'],
                         'http://guides.lib.uw.edu/research')
        self.assertEqual(section1['curriculum_abbr'], "ESS")
        self.assertEqual(section1['canvas_url'],
                         'https://canvas.uw.edu/courses/149651')
        self.assertEqual(section1['limit_estimate_enrollment'], 15)
        self.assertEqual(section1['final_exam']['latitude'], 47.656645546715)
        self.assertEqual(
            section1["email_list"]['section_list']['list_address'],
            'ess102a_sp13')

        section3 = data['sections'][2]
        self.assertEqual(section3["color_id"], "2a")
        self.assertFalse(section3["mini_card"])
        self.assertFalse(section3.get("no_2nd_registration"))
        self.assertFalse(section3.get("cc_display_dates"))
        self.assertFalse(section3.get("early_fall_start"))
        self.assertFalse(section3.get("has_early_fall_start"))

        section6 = data['sections'][5]
        self.assertTrue(section6['current_or_future'])
        self.assertEqual(section6['canvas_url'],
                         'https://canvas.uw.edu/courses/149651')
        self.assertEqual(len(section6['grade_submission_delegates']), 1)
        self.assertEqual(
            len(data['sections'][4]['grade_submission_delegates']), 1)
        self.assertGreater(len(data['related_terms']), 3)
        self.assertEqual(
            section6["email_list"]['section_list']['list_address'],
            'train101a_sp13')

        self.assertGreater(len(data['related_terms']), 2)
        self.assertEqual(data['related_terms'][
            len(data['related_terms']) - 3]['quarter'], 'Spring')
        self.assertEqual(data['related_terms'][5]['year'], 2013)

        self.assertEqual(data['sections'][1]['failure_rate'],
                         0.01790613718411552)


@require_url('myuw_instructor_schedule_api',
             kwargs={'year': 2013, 'quarter': 'summer'},
             message="Specific term instructor URLs not configured")
class TestInstructorTermSchedule(MyuwApiTest):

    def get_schedule(self, **kwargs):
        return self.get_response_by_reverse(
            'myuw_instructor_schedule_api',
            kwargs=kwargs,)

    def test_bill_future_term(self):
        self.set_user('bill')
        response = self.get_schedule(year=2013, quarter='summer')
        self.assertEquals(response.status_code, 200)

    def test_bill_past_term(self):
        self.set_user('bill')
        response = self.get_schedule(year=2013, quarter='winter')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['sections'][0]['current_or_future'])

    def test_having_secondary_sections_case(self):
        now_request = get_request_with_user(
            'billsea', get_request_with_date("2017-10-01"))
        schedule = get_current_quarter_instructor_schedule(now_request)
        resp = InstScheCurQuar().get(now_request)
        self.assertEquals(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertFalse(data["future_term"])
        self.assertEqual(len(data['sections']), 6)

        primary_section = data['sections'][0]
        self.assertEqual(primary_section["section_label"],
                         "2017_autumn_CSE_154_A")
        self.assertEqual(primary_section["color_id"], 1)
        self.assertEqual(primary_section["total_linked_secondaries"], 4)
        final = primary_section['final_exam']
        self.assertFalse(final["is_confirmed"])
        self.assertEqual(final["building"], 'ARC')
        self.assertEqual(final["room"], '147')

        secondary_section = data['sections'][1]
        self.assertEqual(secondary_section["section_label"],
                         "2017_autumn_CSE_154_AA")
        self.assertEqual(secondary_section["color_id"], "1a")
        self.assertFalse(secondary_section["mini_card"])
        self.assertEqual(secondary_section["primary_section_label"],
                         "2017_autumn_CSE_154_A")
        final = secondary_section["final_exam"]
        self.assertFalse(final["is_confirmed"])
        self.assertEqual(final["building"], 'ARC')
        self.assertEqual(final["room"], '147')

        primary_section = data['sections'][5]
        self.assertEqual(primary_section["section_label"],
                         "2017_autumn_EDC_I_552_A")


class TestInstructorSection(MyuwApiTest):
    def test_bill_section(self):
        now_request = get_request_with_user('bill')

        section_id = '2013,spring,ESS,102/A'
        resp = InstSect().get(now_request, section_id=section_id)
        data = json.loads(resp.content)

        self.assertEqual(len(data['sections']), 1)
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

    def test_non_section(self):
        now_request = get_request_with_user('bill')

        section_id = '2013,spring,ESS,102/Z'
        resp = InstSect().get(now_request, section_id=section_id)
        self.assertEqual(resp.status_code, 404)

        section_id = '2013,spring,ESS,102'
        resp = InstSect().get(now_request, section_id=section_id)
        self.assertEqual(resp.status_code, 400)

    def test_bill100_section(self):
        now_request = get_request_with_user('bill100')

        section_id = '2013,spring,ESS,102/A'
        resp = InstSect().get(now_request, section_id=section_id)

        self.assertEqual(resp.status_code, 403)

    def test_billpce_current_term(self):
        now_request = get_request_with_user('bill')
        schedule = get_current_quarter_instructor_schedule(now_request)

        resp = InstScheCurQuar().get(now_request)
        data = json.loads(resp.content)

        self.assertEqual(len(data['sections']), 6)
        section1 = data['sections'][0]
        self.assertFalse('cc_display_dates' in section1)
        self.assertFalse(section1['sln'] == 0)

        now_request = get_request_with_user('billpce')
        schedule = get_current_quarter_instructor_schedule(now_request)

        resp = InstScheCurQuar().get(now_request)
        data = json.loads(resp.content)
        self.assertEqual(len(data['sections']), 5)
        section1 = data['sections'][0]
        self.assertTrue(section1['cc_display_dates'])
        self.assertTrue(section1['sln'] == 0)
        section1 = data['sections'][1]
        self.assertTrue(section1['evaluation']["eval_not_exist"])

        request = get_request_with_user('billpce',
                                        get_request_with_date("2013-10-01"))
        resp = InstScheCurQuar().get(request)
        data = json.loads(resp.content)
        self.assertEqual(len(data['sections']), 1)
        self.assertEqual(data['sections'][0]['current_enrollment'], 1)
        self.assertEqual(data['sections'][0]['enrollment_student_name'],
                         "Student1, Jake Average")

    def test_non_instructor(self):
        now_request = get_request_with_user('staff')
        sche = get_current_quarter_instructor_schedule(now_request)
        resp = InstScheCurQuar().get(now_request)
        self.assertEquals(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(len(data['sections']), 0)

    def test_billsea_section(self):
        now_request = get_request_with_user('billsea')

        section_id = '2017,autumn,EDC&I,552/A'
        resp = InstSect().get(now_request, section_id=section_id)
        data = json.loads(resp.content)
        self.assertEqual(len(data['sections']), 1)
        self.assertEqual(data['sections'][0]['section_label'],
                         '2017_autumn_EDC_I_552_A')
        self.assertEqual(data['sections'][0]['curriculum_abbr'],
                         'EDC&I')
