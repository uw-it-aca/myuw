from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from uw_sws.models import Term, Section, ClassSchedule, SectionMeeting
from myuw.dao.term import get_term_from_quarter_string
from myuw.dao.registration import _get_schedule
from myuw.dao.visual_schedule import _get_visual_schedule_from_schedule, \
    get_schedule_bounds, _add_dates_to_sections, _get_weeks_from_bounds, \
    _add_sections_to_weeks, _section_lists_are_same, _sections_are_same, \
    _consolidate_weeks, _add_weekend_meeting_data, \
    get_summer_schedule_bounds, trim_summer_meetings, _get_finals_period, \
    _add_course_colors_to_schedule, _get_combined_schedule, \
    get_future_visual_schedule, get_current_visual_schedule
from myuw.test import fdao_sws_override, fdao_pws_override, \
    get_request, get_request_with_user, get_request_with_date
import datetime
import copy


@fdao_pws_override
@fdao_sws_override
class TestVisualSchedule(TestCase):
    def setUp(self):
        get_request()

    def _sections_are_same(self, sec1, sec2):
        if sec1.curriculum_abbr == sec2.curriculum_abbr \
                and sec1.course_number == sec2.course_number \
                and sec1.section_id == sec2.section_id:
            return True
        return False

    def _period_lists_are_same(self, list1, list2):
        for period1 in list1:
            match = False
            for period2 in list2:
                if period1.start_date == period2.start_date and \
                                period1.end_date == period2.end_date and \
                        _section_lists_are_same(period1.sections,
                                                period2.sections):
                    match = True
            if not match:
                return False
        return True

    def test_get_bounds(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = get_term_from_quarter_string("2013,spring")

        schedule = _get_schedule(regid, term)

        schedule = _add_dates_to_sections(schedule)

        bounds = get_schedule_bounds(schedule)
        self.assertEqual(bounds[0], datetime.date(2013, 3, 31))
        self.assertEqual(bounds[1], datetime.date(2013, 6, 8))

    def test_get_weeks(self):
        bounds = [datetime.date(2013, 3, 17), datetime.date(2013, 3, 30)]

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
        self.assertTrue(_sections_are_same(consolidated[0].sections[0],
                                           section1))

        self.assertEqual(len(consolidated[1].sections), 1)
        self.assertTrue(_sections_are_same(consolidated[1].sections[0],
                                           section2))

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
        section2.end_date = datetime.date(2017, 10, 27)
        schedule = ClassSchedule()
        schedule.sections = [section1, section2]

        bounds = get_schedule_bounds(schedule)
        weeks = _get_weeks_from_bounds(bounds)
        weeks = _add_sections_to_weeks(schedule.sections, weeks)
        consolidated = _consolidate_weeks(weeks)

        self.assertEqual(len(consolidated), 3)

        self.assertEqual(len(consolidated[0].sections), 1)
        self.assertTrue(_sections_are_same(consolidated[0].sections[0],
                                           section1))

        self.assertEqual(len(consolidated[1].sections), 2)
        self.assertTrue(_sections_are_same(consolidated[1].sections[0],
                                           section1))
        self.assertTrue(_sections_are_same(consolidated[1].sections[1],
                                           section2))

        self.assertEqual(len(consolidated[2].sections), 1)
        self.assertTrue(_sections_are_same(consolidated[2].sections[0],
                                           section2))

    def test_consolidate_weeks_jpce(self):
        regid = "10000000000000000000000000000010"
        term = get_term_from_quarter_string("2013,spring")

        schedule = _get_schedule(regid, term)
        schedule = _add_dates_to_sections(schedule)

        bounds = get_schedule_bounds(schedule)
        weeks = _get_weeks_from_bounds(bounds)
        weeks = _add_sections_to_weeks(schedule.sections, weeks)
        consolidated = _consolidate_weeks(weeks)

        self.assertEqual(len(consolidated), 4)

        w1 = [schedule.sections[1], schedule.sections[2], schedule.sections[3],
              schedule.sections[4]]
        self.assertEqual(len(consolidated[0].sections), 4)
        self.assertTrue(_section_lists_are_same(consolidated[0].sections, w1))

        w2 = [schedule.sections[0], schedule.sections[1], schedule.sections[2],
              schedule.sections[3], schedule.sections[4]]
        self.assertEqual(len(consolidated[1].sections), 5)
        self.assertTrue(_section_lists_are_same(consolidated[1].sections, w2))

        w3 = [schedule.sections[0], schedule.sections[4]]
        self.assertEqual(len(consolidated[2].sections), 2)
        self.assertTrue(_section_lists_are_same(consolidated[2].sections, w3))

        w4 = [schedule.sections[0]]
        self.assertEqual(len(consolidated[3].sections), 1)
        self.assertTrue(_section_lists_are_same(consolidated[3].sections, w4))

    def test_weekend_meetings(self):
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
        section2.start_date = datetime.date(2017, 10, 02)
        section2.end_date = datetime.date(2017, 10, 20)

        sat_mtg = SectionMeeting()
        sat_mtg.meets_saturday = True
        section1.meetings = [sat_mtg]

        sun_mtg = SectionMeeting()
        sun_mtg.meets_sunday = True
        section2.meetings = [sun_mtg]

        schedule = ClassSchedule()
        schedule.sections = [section1, section2]

        schedule = _add_dates_to_sections(schedule)

        bounds = get_schedule_bounds(schedule)
        weeks = _get_weeks_from_bounds(bounds)
        weeks = _add_sections_to_weeks(schedule.sections, weeks)
        consolidated = _consolidate_weeks(weeks)
        _add_weekend_meeting_data(consolidated)

        self.assertTrue(consolidated[0].meets_saturday)
        self.assertTrue(consolidated[0].meets_sunday)

    def test_summer_term_dates(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = get_term_from_quarter_string("2013,summer")

        schedule = _get_schedule(regid, term)
        schedule = _add_dates_to_sections(schedule)

        self.assertEqual(schedule.sections[0].start_date,
                         datetime.date(2013, 6, 24))
        self.assertEqual(schedule.sections[0].end_date,
                         datetime.date(2013, 7, 24))

        self.assertEqual(schedule.sections[1].start_date,
                         datetime.date(2013, 7, 25))
        self.assertEqual(schedule.sections[1].end_date,
                         datetime.date(2013, 8, 23))

        self.assertEqual(schedule.sections[2].start_date,
                         datetime.date(2013, 6, 24))
        self.assertEqual(schedule.sections[2].end_date,
                         datetime.date(2013, 8, 23))

    def test_summer_schedule_bounds(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = get_term_from_quarter_string("2013,summer")

        schedule = _get_schedule(regid, term)
        schedule = _add_dates_to_sections(schedule)
        a_term, b_term = get_summer_schedule_bounds(schedule)
        self.assertEqual(a_term[0], datetime.date(2013, 6, 23))
        self.assertEqual(a_term[1], datetime.date(2013, 7, 24))

        self.assertEqual(b_term[0], datetime.date(2013, 7, 25))
        self.assertEqual(b_term[1], datetime.date(2013, 8, 24))

    def test_summer_trim_meetings(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = get_term_from_quarter_string("2013,summer")
        schedule = _get_schedule(regid, term)
        schedule.sections[0].meetings[0].meets_sunday = True
        schedule.sections[0].meetings[0].meets_monday = True
        schedule.sections[0].meetings[0].meets_tuesday = True
        schedule.sections[0].meetings[0].meets_wednesday = True
        schedule.sections[0].meetings[0].meets_thursday = True
        schedule.sections[0].meetings[0].meets_friday = True
        schedule.sections[0].meetings[0].meets_saturday = True

        schedule.sections[1].meetings[0].meets_sunday = True
        schedule.sections[1].meetings[0].meets_monday = True
        schedule.sections[1].meetings[0].meets_tuesday = True
        schedule.sections[1].meetings[0].meets_wednesday = True
        schedule.sections[1].meetings[0].meets_thursday = True
        schedule.sections[1].meetings[0].meets_friday = True
        schedule.sections[1].meetings[0].meets_saturday = True

        _add_dates_to_sections(schedule)
        a_bounds, b_bounds = get_summer_schedule_bounds(schedule)
        a_weeks = _get_weeks_from_bounds(a_bounds)

        for week in a_weeks:
            week.summer_term = "A-term"
        a_weeks = _add_sections_to_weeks(schedule.sections, a_weeks)
        a_consolidated = _consolidate_weeks(a_weeks)
        a_consolidated = trim_summer_meetings(a_consolidated)
        mtg = a_consolidated[1].sections[0].meetings[0]

        self.assertTrue(mtg.meets_sunday)
        self.assertTrue(mtg.meets_monday)
        self.assertTrue(mtg.meets_tuesday)
        self.assertTrue(mtg.meets_wednesday)
        self.assertFalse(mtg.meets_thursday)
        self.assertFalse(mtg.meets_friday)
        self.assertFalse(mtg.meets_saturday)

        b_weeks = _get_weeks_from_bounds(b_bounds)
        for week in b_weeks:
            week.summer_term = "B-term"
        b_weeks = _add_sections_to_weeks(schedule.sections, b_weeks)
        b_consolidated = _consolidate_weeks(b_weeks)
        b_consolidated = trim_summer_meetings(b_consolidated)
        mtg = b_consolidated[0].sections[0].meetings[0]

        self.assertFalse(mtg.meets_sunday)
        self.assertFalse(mtg.meets_monday)
        self.assertFalse(mtg.meets_tuesday)
        self.assertFalse(mtg.meets_wednesday)
        self.assertTrue(mtg.meets_thursday)
        self.assertTrue(mtg.meets_friday)
        self.assertTrue(mtg.meets_saturday)

    def test_summer_term_schedule(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = get_term_from_quarter_string("2013,summer")
        schedule = _get_schedule(regid, term)
        get_request_with_user('javerage',
                              get_request_with_date("2013-08-01"))

        consolidated = _get_visual_schedule_from_schedule(schedule)

        self.assertEqual(len(consolidated), 5)
        self.assertEqual(consolidated[0].summer_term, "A-term")
        self.assertEqual(consolidated[2].summer_term, "B-term")

        self.assertEqual(consolidated[0].start_date,
                         datetime.date(2013, 6, 23))
        self.assertEqual(consolidated[0].end_date, datetime.date(2013, 7, 20))

        self.assertEqual(consolidated[1].start_date,
                         datetime.date(2013, 7, 21))
        self.assertEqual(consolidated[1].end_date, datetime.date(2013, 7, 24))

        self.assertEqual(consolidated[2].start_date,
                         datetime.date(2013, 7, 25))
        self.assertEqual(consolidated[2].end_date, datetime.date(2013, 7, 27))

        self.assertEqual(consolidated[3].start_date,
                         datetime.date(2013, 7, 28))
        self.assertEqual(consolidated[3].end_date, datetime.date(2013, 8, 24))

    def test_summer_term_schedule_pce_beyond_term(self):
            regid = "9136CCB8F66711D5BE060004AC494FFE"
            term = get_term_from_quarter_string("2013,summer")
            get_request_with_user('javerage',
                                  get_request_with_date("2013-08-01"))

            section1 = Section()
            section1.curriculum_abbr = 'ASD'
            section1.course_number = 123
            section1.section_id = 'A'
            section1.start_date = datetime.date(2013, 6, 2)
            section1.end_date = datetime.date(2013, 9, 4)
            section1.meetings = []
            section1.term = term

            schedule = _get_schedule(regid, term)
            schedule.sections.append(section1)

            consolidated = _get_visual_schedule_from_schedule(schedule)

            self.assertEqual(len(consolidated), 5)

            self.assertEqual(consolidated[0].start_date,
                             datetime.date(2013, 6, 23))
            self.assertEqual(consolidated[3].end_date,
                             datetime.date(2013, 8, 24))

            # ensure section exists in each week
            for week in consolidated:
                found_match = False
                for section in week.sections:
                    if _sections_are_same(section, section1):
                        found_match = True
                self.assertTrue(found_match)

    def test_summer_term_schedule_pce(self):
            regid = "9136CCB8F66711D5BE060004AC494FFE"
            term = get_term_from_quarter_string("2013,summer")
            get_request_with_user('javerage',
                                  get_request_with_date("2013-08-01"))

            section1 = Section()
            section1.curriculum_abbr = 'ASD'
            section1.course_number = 123
            section1.section_id = 'A'
            section1.start_date = datetime.date(2013, 7, 10)
            section1.end_date = datetime.date(2013, 8, 4)
            section1.meetings = []
            section1.term = term

            schedule = _get_schedule(regid, term)
            schedule.sections.append(section1)

            consolidated = _get_visual_schedule_from_schedule(schedule)

            self.assertEqual(len(consolidated), 7)

            self.assertEqual(consolidated[0].start_date,
                             datetime.date(2013, 6, 23))
            self.assertEqual(consolidated[0].end_date,
                             datetime.date(2013, 7, 6))

            self.assertEqual(consolidated[1].start_date,
                             datetime.date(2013, 7, 7))
            self.assertEqual(consolidated[1].end_date,
                             datetime.date(2013, 7, 20))

            self.assertEqual(consolidated[2].start_date,
                             datetime.date(2013, 7, 21))
            self.assertEqual(consolidated[2].end_date,
                             datetime.date(2013, 7, 24))

            self.assertEqual(consolidated[3].start_date,
                             datetime.date(2013, 7, 25))
            self.assertEqual(consolidated[3].end_date,
                             datetime.date(2013, 7, 27))

            self.assertEqual(consolidated[4].start_date,
                             datetime.date(2013, 7, 28))
            self.assertEqual(consolidated[4].end_date,
                             datetime.date(2013, 8, 10))

            self.assertEqual(consolidated[5].start_date,
                             datetime.date(2013, 8, 11))
            self.assertEqual(consolidated[5].end_date,
                             datetime.date(2013, 8, 24))

            pce_weeks = [consolidated[index] for index in [1, 2, 3, 4]]
            non_pce_weeks = [consolidated[index] for index in [0, 5]]

            # ensure section exists in each week
            for week in pce_weeks:
                found_match = False
                for section in week.sections:
                    if _sections_are_same(section, section1):
                        found_match = True
                self.assertTrue(found_match)

            # ensure section doesn't exist in each week
            for week in non_pce_weeks:
                found_match = False
                for section in week.sections:
                    if _sections_are_same(section, section1):
                        found_match = True
                self.assertFalse(found_match)

    def test_efs_schedule(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = get_term_from_quarter_string("2013,autumn")
        schedule = _get_schedule(regid, term)
        get_request_with_user('javerage',
                              get_request_with_date("2013-10-01"))
        consolidated = _get_visual_schedule_from_schedule(schedule)
        self.assertEqual(len(consolidated), 5)

        self.assertEqual(consolidated[0].start_date,
                         datetime.date(2013, 8, 25))
        self.assertEqual(consolidated[0].end_date,
                         datetime.date(2013, 9, 14))

        self.assertEqual(consolidated[1].start_date,
                         datetime.date(2013, 9, 15))
        self.assertEqual(consolidated[1].end_date,
                         datetime.date(2013, 9, 21))

        self.assertEqual(consolidated[2].start_date,
                         datetime.date(2013, 9, 22))
        self.assertEqual(consolidated[2].end_date,
                         datetime.date(2013, 9, 28))

        self.assertEqual(consolidated[3].start_date,
                         datetime.date(2013, 9, 29))
        self.assertEqual(consolidated[3].end_date,
                         datetime.date(2013, 12, 7))

        trimmed_efs_mtg = consolidated[1].sections[0].meetings[0]
        self.assertFalse(trimmed_efs_mtg.meets_sunday)
        self.assertTrue(trimmed_efs_mtg.meets_monday)
        self.assertTrue(trimmed_efs_mtg.meets_tuesday)
        self.assertTrue(trimmed_efs_mtg.meets_wednesday)
        self.assertFalse(trimmed_efs_mtg.meets_thursday)
        self.assertFalse(trimmed_efs_mtg.meets_friday)
        self.assertFalse(trimmed_efs_mtg.meets_saturday)

    def test_get_finals(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = get_term_from_quarter_string("2013,spring")
        schedule = _get_schedule(regid, term)
        finals = _get_finals_period(schedule)
        self.assertEqual(len(finals.sections), 5)

    def test_add_section_color(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = get_term_from_quarter_string("2013,spring")
        schedule = _get_schedule(regid, term)

        get_request_with_user('javerage',
                              get_request_with_date("2013-04-01"))

        _add_course_colors_to_schedule(schedule)
        self.assertEqual(schedule.sections[0].color_id, 1)
        self.assertEqual(schedule.sections[1].color_id, 2)
        self.assertEqual(schedule.sections[2].color_id, 3)
        self.assertEqual(schedule.sections[3].color_id, '3a')
        self.assertEqual(schedule.sections[4].color_id, '3a')

    def test_get_instructor_sections(self):
        request = get_request_with_user('bill',
                                        get_request_with_date("2013-04-01"))

        schedule = _get_combined_schedule(request)
        for section in schedule.sections:
            self.assertTrue(section.is_teaching)

    def test_get_mixed_sections(self):
        request = get_request_with_user('eight',
                                        get_request_with_date("2013-04-01"))

        schedule = _get_combined_schedule(request)

        for section in schedule.sections:
            # section for which user is an instructor
            if section.curriculum_abbr == "ACCTG":
                self.assertTrue(section.is_teaching)
            else:
                self.assertFalse(section.is_teaching)

    def test_sunday_schedule(self):
        request = get_request_with_user('jeos',
                                        get_request_with_date("2013-04-01"))

        schedule = _get_combined_schedule(request)
        sunday_section = schedule.sections[0]

        self.assertTrue(sunday_section.meetings[0].meets_sunday)

        visual_schedule = _get_visual_schedule_from_schedule(schedule)
        self.assertTrue(visual_schedule[1].meets_sunday)

    def test_future_term(self):
        get_request_with_user('javerage',
                              get_request_with_date("2013-03-01"))
        term = get_term_from_quarter_string("2013,summer")
        future_schedule = get_future_visual_schedule(term)

        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-08-1"))

        current_schedule = get_current_visual_schedule(request)

        # Ensure that getting summer as 'current' term returns same results
        # as getting as future
        self.assertTrue(self._period_lists_are_same(current_schedule,
                                                    future_schedule))
