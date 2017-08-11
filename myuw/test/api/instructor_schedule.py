from myuw.test.api import require_url, MyuwApiTest
from restclients_core.exceptions import DataFailureException
from myuw.views.api.instructor_schedule import InstScheCurQuar, InstSect
import json
from myuw.dao.instructor_schedule import\
    get_current_quarter_instructor_schedule
from myuw.test import get_request, get_request_with_user, get_request_with_date


@require_url('myuw_instructor_current_schedule_api')
class TestInstructorCurrentSchedule(MyuwApiTest):

    def test_bill_current_term(self):
        now_request = get_request()
        get_request_with_user('bill', now_request)
        schedule = get_current_quarter_instructor_schedule(now_request)

        resp = InstScheCurQuar().GET(now_request)
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

        section2 = data['sections'][5]
        self.assertEqual(section2['canvas_url'],
                         'https://canvas.uw.edu/courses/149651')
        self.assertEqual(len(section2['grade_submission_delegates']), 1)
        self.assertEqual(
            len(data['sections'][4]['grade_submission_delegates']), 1)
        self.assertGreater(len(data['related_terms']), 3)
        self.assertEqual(
            section2["email_list"]['section_list']['list_address'],
            'train101a_sp13')
        self.assertGreater(len(data['related_terms']), 2)
        self.assertEqual(data['related_terms'][
            len(data['related_terms']) - 3]['quarter'], 'Spring')
        self.assertEqual(data['related_terms'][5]['year'], 2013)


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


class TestInstructorSection(MyuwApiTest):
    def test_bill_section(self):
        now_request = get_request()
        get_request_with_user('bill', now_request)

        year = '2013'
        quarter = 'spring'
        curriculum = 'ESS'
        course_number = '102'
        course_section = 'A'
        resp = InstSect().GET(now_request, year, quarter, curriculum,
                              course_number, course_section)
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
        now_request = get_request()
        get_request_with_user('bill', now_request)

        year = '2013'
        quarter = 'spring'
        curriculum = 'ESS'
        course_number = '102'
        course_section = 'Z'
        resp = InstSect().GET(now_request, year, quarter, curriculum,
                              course_number, course_section)

        self.assertEqual(resp.status_code, 404)

    def test_bill100_section(self):
        now_request = get_request()
        get_request_with_user('bill100', now_request)

        year = '2013'
        quarter = 'spring'
        curriculum = 'ESS'
        course_number = '102'
        course_section = 'A'
        resp = InstSect().GET(now_request, year, quarter, curriculum,
                              course_number, course_section)

        self.assertEqual(resp.status_code, 403)

    def test_billpce_current_term(self):
        now_request = get_request()
        get_request_with_user('bill', now_request)
        schedule = get_current_quarter_instructor_schedule(now_request)

        resp = InstScheCurQuar().GET(now_request)
        data = json.loads(resp.content)

        self.assertEqual(len(data['sections']), 6)
        section1 = data['sections'][0]
        self.assertFalse('cc_display_dates' in section1)
        self.assertFalse(section1['sln'] == 0)

        get_request_with_user('billpce', now_request)
        schedule = get_current_quarter_instructor_schedule(now_request)

        resp = InstScheCurQuar().GET(now_request)
        data = json.loads(resp.content)
        self.assertEqual(len(data['sections']), 5)
        section1 = data['sections'][0]
        self.assertTrue(section1['cc_display_dates'])
        self.assertTrue(section1['sln'] == 0)

        request = get_request_with_user('billpce',
                                        get_request_with_date("2013-10-01"))
        resp = InstScheCurQuar().GET(request)
        data = json.loads(resp.content)
        self.assertEqual(len(data['sections']), 1)
        self.assertEqual(data['sections'][0]['current_enrollment'], 1)
        self.assertEqual(data['sections'][0]['enrollment_student_name'],
                         "Student, Jake Average")

    def test_non_instructor(self):
        now_request = get_request()
        get_request_with_user('staff', now_request)
        sche = get_current_quarter_instructor_schedule(now_request)
        resp = InstScheCurQuar().GET(now_request)
        self.assertEquals(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(len(data['sections']), 0)
