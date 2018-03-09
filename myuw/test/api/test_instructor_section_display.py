from myuw.models import UserCourseDisplay
from myuw.test.api import MyuwApiTest, fdao_sws_override, fdao_pws_override
from myuw.views.api.instructor_section_display import \
    CloseMinicard, PinMinicard
from myuw.test import get_request_with_user


@fdao_sws_override
@fdao_pws_override
class TestInstSectDetails(MyuwApiTest):

    def get_schedule(self, **kwargs):
        return self.get_response_by_reverse(
            'myuw_instructor_schedule_api',
            kwargs=kwargs,)

    def test_mini_card(self):
        self.set_user('bill')
        self.get_schedule(year=2013, quarter='spring')
        records = UserCourseDisplay.objects.all()
        self.assertEquals(len(records), 6)

        req = get_request_with_user('bill')
        section_id = '2013,spring,PHYS,121/AC'
        resp = PinMinicard().get(req, section_label=section_id)
        self.assertEqual(resp.content, '{"done": true}')

        resp = CloseMinicard().get(req, section_label=section_id)
        self.assertEqual(resp.content, '{"done": true}')

        # test InvalidSectionID
        section_id = '2013,spring,PHYS,121/'
        resp = PinMinicard().get(req, section_label=section_id)
        self.assertEqual(resp.status_code, 400)

        # test DoesNotExist in DB
        section_id = '2013,spring,PHYS,121/AB'
        resp = PinMinicard().get(req, section_label=section_id)
        self.assertEqual(resp.status_code, 543)
