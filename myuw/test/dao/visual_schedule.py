from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from uw_sws.models import Term
from myuw.dao.term import get_term_from_quarter_string
from myuw.dao.registration import _get_schedule
from myuw.dao.visual_schedule import get_visual_schedule, get_schedule_bounds, _add_dates_to_sections
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request
import datetime



@fdao_pws_override
@fdao_sws_override
class TestVisualSchedule(TestCase):
    def setUp(self):
        get_request()

    # def test_get_vs(self):
    #     regid = "9136CCB8F66711D5BE060004AC494FFE"
    #     term = get_term_from_quarter_string("2013,summer")
    #
    #     schedule = _get_schedule(regid, term)
    #     print schedule.sections
    #
    #     # vis = get_visual_schedule(schedule)


    def test_get_bounds(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = get_term_from_quarter_string("2013,summer")

        schedule = _get_schedule(regid, term)

        schedule = _add_dates_to_sections(schedule)

        periods = get_schedule_bounds(schedule)
        self.assertEqual(periods[0], datetime.date(2013, 6, 23))
        self.assertEqual(periods[1], datetime.date(2013, 8, 24))