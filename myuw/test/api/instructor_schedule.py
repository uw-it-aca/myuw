from myuw.test.api import require_url, MyuwApiTest
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from userservice.user import UserServiceMiddleware
from myuw.views.api.instructor_schedule import InstScheCurQuar, InstSect
import json


@require_url('myuw_instructor_current_schedule_api')
class TestInstructorCurrentSchedule(MyuwApiTest):
    def test_bill_current_term(self):
        now_request = RequestFactory().get("/")
        now_request.session = {}
        user = User.objects.create_user(username='bill',
                                        email='bill@example.com',
                                        password='')

        now_request.user = user
        UserServiceMiddleware().process_request(now_request)

        resp = InstScheCurQuar().GET(now_request)
        data = json.loads(resp.content)

        self.assertEqual(len(data['sections']), 2)
        self.assertEqual(
            data['sections'][0]['limit_estimate_enrollment'], 15)
        self.assertEqual(
            data['sections'][0]['final_exam']['latitude'],
            47.656645546715)
        self.assertEqual(data['sections'][1]['canvas_url'],
                         'https://canvas.uw.edu/courses/149651')
        self.assertEqual(
            len(data['sections'][1]['grade_submission_delegates']), 1)
        self.assertGreater(len(data['related_terms']), 3)
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
        now_request = RequestFactory().get("/")
        now_request.session = {}
        user = User.objects.create_user(username='bill',
                                        email='bill@example.com',
                                        password='')

        now_request.user = user
        UserServiceMiddleware().process_request(now_request)

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
        now_request = RequestFactory().get("/")
        now_request.session = {}
        user = User.objects.create_user(username='bill100',
                                        email='bill100@example.com',
                                        password='')

        now_request.user = user
        UserServiceMiddleware().process_request(now_request)

        year = '2013'
        quarter = 'spring'
        curriculum = 'ESS'
        course_number = '102'
        course_section = 'Z'
        resp = InstSect().GET(now_request, year, quarter, curriculum,
                              course_number, course_section)

        self.assertEqual(resp.status_code, 404)

    def test_bill100_section(self):
        now_request = RequestFactory().get("/")
        now_request.session = {}
        user = User.objects.create_user(username='bill100',
                                        email='bill100@example.com',
                                        password='')

        now_request.user = user
        UserServiceMiddleware().process_request(now_request)

        year = '2013'
        quarter = 'spring'
        curriculum = 'ESS'
        course_number = '102'
        course_section = 'A'
        resp = InstSect().GET(now_request, year, quarter, curriculum,
                              course_number, course_section)

        self.assertEqual(resp.status_code, 403)
