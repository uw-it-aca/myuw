from myuw.test.api import require_url, MyuwApiTest
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from userservice.user import UserServiceMiddleware
from myuw.views.api.instructor_schedule import load_schedule
from myuw.dao.instructor_schedule import\
    get_current_quarter_instructor_schedule


FDAO_SWS = 'restclients.dao_implementation.sws.File'
FDAO_PWS = 'restclients.dao_implementation.pws.File'
FDAO_Canvas = 'restclients.dao_implementation.canvas.File'


@require_url('myuw_instructor_current_schedule_api')
class TestInstructorCurrentSchedule(MyuwApiTest):
    def test_bill_current_term(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS,
                           RESTCLIENTS_CANVAS_DAO_CLASS=FDAO_Canvas):
            now_request = RequestFactory().get("/")
            now_request.session = {}
            user = User.objects.create_user(username='bill',
                                            email='bill@example.com',
                                            password='')

            now_request.user = user
            UserServiceMiddleware().process_request(now_request)
            schedule = get_current_quarter_instructor_schedule(now_request)

            data = load_schedule(now_request, schedule)
            self.assertEqual(len(data['sections']), 2)
            self.assertEqual(
                data['sections'][0]['limit_estimate_enrollment'], 15)
            self.assertEqual(
                data['sections'][0]['final_exam']['latitude'],
                47.656645546715)
            self.assertEqual(data['sections'][1]['canvas_url'],
                             'https://canvas.uw.edu/courses/149651')
            self.assertEqual(
                len(data['sections'][1]['grade_submission_delegates']),
                1)


@require_url('myuw_instructor_schedule_api',
             kwargs={'year': 2013, 'quarter': 'summer'},
             message="Specific term instructor URLs not configured")
class TestInstructorTermSchedule(MyuwApiTest):

    def get_schedule(self, **kwargs):
        return self.get_response_by_reverse(
            'myuw_instructor_schedule_api',
            kwargs=kwargs,)

    def test_bill_future_term(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS,
                           RESTCLIENTS_CANVAS_DAO_CLASS=FDAO_Canvas):
            self.set_user('bill')
            response = self.get_schedule(year=2013, quarter='summer')
            self.assertEquals(response.status_code, 200)

    def test_bill_past_term(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                           RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS,
                           RESTCLIENTS_CANVAS_DAO_CLASS=FDAO_Canvas):
            self.set_user('bill')
            response = self.get_schedule(year=2013, quarter='winter')
            self.assertEquals(response.status_code, 200)
