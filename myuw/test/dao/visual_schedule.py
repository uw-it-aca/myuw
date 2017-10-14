from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from uw_sws.models import Term, Section, ClassSchedule
from myuw.dao.term import get_term_from_quarter_string
from myuw.dao.registration import _get_schedule
from myuw.dao.visual_schedule import get_visual_schedule,\
    get_schedule_bounds, _add_dates_to_sections, _get_weeks_from_bounds,\
    _add_sections_to_weeks, _section_lists_are_same, _sections_are_same, \
    _consolidate_weeks
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request
import datetime
import copy


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
        term = get_term_from_quarter_string("2013,spring")

        schedule = _get_schedule(regid, term)

        schedule = _add_dates_to_sections(schedule)

        bounds = get_schedule_bounds(schedule)
        self.assertEqual(bounds[0], datetime.date(2013, 3, 31))
        self.assertEqual(bounds[1], datetime.date(2013, 6, 8))


    def test_get_weeks(self):
        bounds = [datetime.date(2013, 3, 17), datetime.date(2013, 3, 31)]

        weeks = _get_weeks_from_bounds(bounds)

        self.assertEqual(len(weeks), 2)
        self.assertEqual(weeks[0].end_date, datetime.date(2013, 3, 23))
        self.assertEqual(weeks[1].start_date, datetime.date(2013, 3, 24))


    def test_add_schedule_to_weeks(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = get_term_from_quarter_string("2013,spring")

        schedule = _get_schedule(regid, term)
        schedule = _add_dates_to_sections(schedule)
        bounds = get_schedule_bounds(schedule)
        weeks = _get_weeks_from_bounds(bounds)
        weeks = _add_sections_to_weeks(schedule.sections, weeks)

        for week in weeks:
            self.assertEqual(len(week.sections), 5)


    def test_sections_are_same(self):
        section1 = Section()
        section1.curriculum_abbr = 'ASD'
        section1.course_number = 123
        section1.section_id = 'A'

        section2 = Section()
        section2.curriculum_abbr = 'ASD'
        section2.course_number = 123
        section2.section_id = 'A'

        self.assertTrue(_sections_are_same(section1, section2))

        section2.section_id = 'B'
        self.assertFalse(_sections_are_same(section1, section2))


    def test_section_lists_are_same(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = get_term_from_quarter_string("2013,spring")

        schedule = _get_schedule(regid, term)
        schedule = _add_dates_to_sections(schedule)

        list1 = copy.deepcopy(schedule.sections)
        list2 = copy.deepcopy(schedule.sections)
        list3 = copy.deepcopy(schedule.sections)

        self.assertTrue(_section_lists_are_same(list1,
                                                list2))

        del list1[0]
        self.assertFalse(_section_lists_are_same(list1,
                                                 list2))
        list3[0].course_number = 999
        self.assertFalse(_section_lists_are_same(list2,
                                                 list3))

    def test_consolidate_weeks_same(self):
        start = datetime.date(2017, 10, 02)
        end = datetime.date(2017, 10, 13)

        section1 = Section()
        section1.curriculum_abbr = 'ASD'
        section1.course_number = 123
        section1.section_id = 'A'
        section1.start_date = start
        section1.end_date = end

        section2 = Section()
        section2.curriculum_abbr = 'QWE'
        section2.course_number = 456
        section2.section_id = 'A'
        section2.start_date = start
        section2.end_date = end
        schedule = ClassSchedule()
        schedule.sections = [section1, section2]

        bounds = get_schedule_bounds(schedule)
        weeks = _get_weeks_from_bounds(bounds)
        weeks = _add_sections_to_weeks(schedule.sections, weeks)
        consolidated = _consolidate_weeks(weeks)
        self.assertEqual(len(consolidated), 1)

    def test_consolidate_weeks_no_overlap(self):
        section1 = Section()
        section1.curriculum_abbr = 'ASD'
        section1.course_number = 123
        section1.section_id = 'A'
        section1.start_date = datetime.date(2017, 10, 02)
        section1.end_date = datetime.date(2017, 10, 13)

        section2 = Section()
        section2.curriculum_abbr = 'QWE'
        section2.course_number = 456
        section2.section_id = 'A'
        section2.start_date = datetime.date(2017, 10, 16)
        section2.end_date = datetime.date(2017, 10, 27)
        schedule = ClassSchedule()
        schedule.sections = [section1, section2]

        bounds = get_schedule_bounds(schedule)
        weeks = _get_weeks_from_bounds(bounds)
        weeks = _add_sections_to_weeks(schedule.sections, weeks)
        consolidated = _consolidate_weeks(weeks)

        self.assertEqual(len(consolidated), 2)

        self.assertEqual(len(consolidated[0].sections), 1)
        self.assertEqual(consolidated[0].sections[0], section1)

        self.assertEqual(len(consolidated[1].sections), 1)
        self.assertEqual(consolidated[1].sections[0], section2)

    def test_consolidate_weeks_partial_overlap(self):
        section1 = Section()
        section1.curriculum_abbr = 'ASD'
        section1.course_number = 123
        section1.section_id = 'A'
        section1.start_date = datetime.date(2017, 10, 02)
        section1.end_date = datetime.date(2017, 10, 20)

        section2 = Section()
        section2.curriculum_abbr = 'QWE'
        section2.course_number = 456
        section2.section_id = 'A'
        section2.start_date = datetime.date(2017, 10, 16)
        section2.end_date = datetime.date(2017, 10, 20)
        schedule = ClassSchedule()
        schedule.sections = [section1, section2]

        bounds = get_schedule_bounds(schedule)
        weeks = _get_weeks_from_bounds(bounds)
        weeks = _add_sections_to_weeks(schedule.sections, weeks)
        consolidated = _consolidate_weeks(weeks)

        self.assertEqual(len(consolidated), 3)

        self.assertEqual(len(consolidated[0].sections), 1)
        self.assertEqual(consolidated[0].sections[0], section1)

        self.assertEqual(len(consolidated[1].sections), 2)
        self.assertEqual(consolidated[1].sections[0], section1)
        self.assertEqual(consolidated[1].sections[1], section2)

        self.assertEqual(len(consolidated[1].sections), 1)
        self.assertEqual(consolidated[1].sections[0], section2)
