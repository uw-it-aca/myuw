from django.test import TestCase
from uw_sws.models import Section, ClassSchedule, SectionMeeting
from myuw.dao.term import get_term_from_quarter_string
from myuw.dao.registration import get_schedule_by_term
from myuw.dao.visual_schedule import (
    _get_visual_schedule_from_schedule, get_future_visual_schedule,
    get_schedule_bounds, _add_dates_to_sections, _get_weeks_from_bounds,
    _add_sections_to_weeks, _section_lists_are_same, _sections_are_same,
    _consolidate_weeks, _add_weekend_meeting_data, _get_combined_schedule,
    get_summer_schedule_bounds, trim_summer_meetings, _get_finals_period,
    get_current_visual_schedule, _trim_summer_term,
    _get_disabled_days, _get_earliest_meeting_day, get_schedule_json,
    _get_latest_meeting_day, _get_earliest_start_from_period,
    _get_latest_end_from_period, trim_section_meetings,
    trim_weeks_no_meetings, _get_off_term_trimmed, _adjust_off_term_dates,
    _add_qtr_start_data_to_weeks, _remove_empty_periods,
    _adjust_period_dates, get_visual_schedule_from_schedule)
from myuw.dao.term import get_current_quarter
from myuw.test import (
    fdao_sws_override, fdao_pws_override,
    get_request, get_request_with_user, get_request_with_date)
import datetime
import copy
from myuw.dao.term import get_current_summer_term


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

    def _get_weekend_meeting_schedule(self):
        section1 = Section()
        section1.curriculum_abbr = 'ASD'
        section1.course_number = 123
        section1.section_id = 'A'
        section1.start_date = datetime.date(2017, 10, 2)
        section1.end_date = datetime.date(2017, 10, 20)

        section2 = Section()
        section2.curriculum_abbr = 'QWE'
        section2.course_number = 456
        section2.section_id = 'A'
        section2.start_date = datetime.date(2017, 10, 2)
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
        return consolidated

    def _get_schedule_with_meetings(self):
        section1 = Section()
        section1.curriculum_abbr = 'ASD'
        section1.course_number = 123
        section1.section_id = 'A'
        section1.start_date = datetime.date(2017, 10, 2)
        section1.end_date = datetime.date(2017, 10, 20)

        section2 = Section()
        section2.curriculum_abbr = 'QWE'
        section2.course_number = 456
        section2.section_id = 'A'
        section2.start_date = datetime.date(2017, 10, 2)
        section2.end_date = datetime.date(2017, 10, 20)

        s1_meetings = SectionMeeting()
        s1_meetings.meets_saturday = True
        s1_meetings.meets_tuesday = True
        section1.meetings = [s1_meetings]

        s2_meetings = SectionMeeting()
        s2_meetings.meets_wednesday = True
        s2_meetings.meets_friday = True
        section2.meetings = [s2_meetings]

        schedule = ClassSchedule()
        schedule.sections = [section1, section2]

        schedule = _add_dates_to_sections(schedule)

        bounds = get_schedule_bounds(schedule)
        weeks = _get_weeks_from_bounds(bounds)
        weeks = _add_sections_to_weeks(schedule.sections, weeks)
        weeks = trim_section_meetings(weeks)
        weeks = trim_weeks_no_meetings(weeks)
        consolidated = _consolidate_weeks(weeks)
        _add_weekend_meeting_data(consolidated)
        return consolidated

    def _get_schedule_no_meetings(self):
        section1 = Section()
        section1.curriculum_abbr = 'ASD'
        section1.course_number = 123
        section1.section_id = 'A'
        section1.start_date = datetime.date(2017, 10, 2)
        section1.end_date = datetime.date(2017, 10, 20)

        section2 = Section()
        section2.curriculum_abbr = 'QWE'
        section2.course_number = 456
        section2.section_id = 'A'
        section2.start_date = datetime.date(2017, 10, 2)
        section2.end_date = datetime.date(2017, 10, 20)

        s1_meetings = SectionMeeting()
        s1_meetings.meeting_type = "NON"
        section1.meetings = [s1_meetings]

        s2_meetings = SectionMeeting()
        s2_meetings.meeting_type = "NON"
        section2.meetings = [s2_meetings]

        schedule = ClassSchedule()
        schedule.sections = [section1, section2]

        schedule = _add_dates_to_sections(schedule)

        bounds = get_schedule_bounds(schedule)
        weeks = _get_weeks_from_bounds(bounds)
        weeks = _add_sections_to_weeks(schedule.sections, weeks)
        weeks = trim_section_meetings(weeks)
        weeks = trim_weeks_no_meetings(weeks)
        consolidated = _consolidate_weeks(weeks)
        _add_weekend_meeting_data(consolidated)
        return consolidated

    def test_get_bounds(self):
        term = get_term_from_quarter_string("2013,spring")
        request = get_request_with_user('javerage')
        schedule = get_schedule_by_term(request, term)

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
        term = get_term_from_quarter_string("2013,spring")

        request = get_request_with_user('javerage')
        schedule = get_schedule_by_term(request, term)
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
        term = get_term_from_quarter_string("2013,spring")

        request = get_request_with_user('javerage')
        schedule = get_schedule_by_term(request, term)
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
        start = datetime.date(2017, 10, 2)
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
        section1.start_date = datetime.date(2017, 10, 2)
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
        section1.start_date = datetime.date(2017, 10, 2)
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
        term = get_term_from_quarter_string("2013,spring")

        request = get_request_with_user('jpce')
        schedule = get_schedule_by_term(request, term)
        schedule = _add_dates_to_sections(schedule)
        self.assertEqual(len(schedule.sections), 5)

        bounds = get_schedule_bounds(schedule)
        weeks = _get_weeks_from_bounds(bounds)
        weeks = _add_sections_to_weeks(schedule.sections, weeks)
        consolidated = _consolidate_weeks(weeks)

        self.assertEqual(len(consolidated), 5)

        w1 = [schedule.sections[2], schedule.sections[3], schedule.sections[4]]
        self.assertEqual(len(consolidated[0].sections), 3)
        self.assertTrue(_section_lists_are_same(consolidated[0].sections, w1))

        w2 = [schedule.sections[1], schedule.sections[2],
              schedule.sections[3], schedule.sections[4]]
        self.assertEqual(len(consolidated[1].sections), 4)
        self.assertTrue(_section_lists_are_same(consolidated[1].sections, w2))

        w3 = [schedule.sections[0], schedule.sections[1], schedule.sections[2],
              schedule.sections[3], schedule.sections[4]]
        self.assertEqual(len(consolidated[2].sections), 5)
        self.assertTrue(_section_lists_are_same(consolidated[2].sections, w3))

        w4 = [schedule.sections[0], schedule.sections[1], schedule.sections[3]]
        self.assertEqual(len(consolidated[3].sections), 3)
        self.assertTrue(_section_lists_are_same(consolidated[3].sections, w4))

        w5 = [schedule.sections[0], schedule.sections[1]]
        self.assertEqual(len(consolidated[4].sections), 2)
        self.assertTrue(_section_lists_are_same(consolidated[4].sections, w5))

    def test_weekend_meetings(self):
        consolidated = self._get_weekend_meeting_schedule()

        self.assertTrue(consolidated[0].meets_saturday)
        self.assertTrue(consolidated[0].meets_sunday)

    def test_summer_term_dates(self):
        term = get_term_from_quarter_string("2013,summer")

        request = get_request_with_user('javerage')
        schedule = get_schedule_by_term(request, term, summer_term='full-term')
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
        term = get_term_from_quarter_string("2013,summer")

        request = get_request_with_user('javerage')
        schedule = get_schedule_by_term(request, term, 'b-term')
        schedule = _add_dates_to_sections(schedule)
        a_term, b_term = get_summer_schedule_bounds(schedule)
        self.assertEqual(a_term[0], datetime.date(2013, 6, 23))
        self.assertEqual(a_term[1], datetime.date(2013, 7, 24))

        self.assertEqual(b_term[0], datetime.date(2013, 7, 25))
        self.assertEqual(b_term[1], datetime.date(2013, 8, 24))

    def test_summer_trim_meetings(self):
        term = get_term_from_quarter_string("2013,summer")
        request = get_request_with_user('javerage')
        schedule = get_schedule_by_term(request, term)
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
        term = get_term_from_quarter_string("2013,summer")
        request = get_request_with_user('javerage')
        schedule = get_schedule_by_term(request, term)
        get_request_with_user('javerage',
                              get_request_with_date("2013-08-01"))

        consolidated = _get_visual_schedule_from_schedule(
            schedule, request, schedule.summer_term)

        self.assertEqual(len(consolidated), 5)
        self.assertEqual(consolidated[0].summer_term, "A-term")
        self.assertEqual(consolidated[2].summer_term, "B-term")

        self.assertEqual(consolidated[0].start_date,
                         datetime.date(2013, 6, 24))
        self.assertEqual(consolidated[0].end_date, datetime.date(2013, 7, 19))

        self.assertEqual(consolidated[1].start_date,
                         datetime.date(2013, 7, 22))
        self.assertEqual(consolidated[1].end_date, datetime.date(2013, 7, 24))

        self.assertEqual(consolidated[2].start_date,
                         datetime.date(2013, 7, 25))
        self.assertEqual(consolidated[2].end_date, datetime.date(2013, 7, 26))

        self.assertEqual(consolidated[3].start_date,
                         datetime.date(2013, 7, 29))
        self.assertEqual(consolidated[3].end_date, datetime.date(2013, 8, 23))

    def test_summer_term_schedule_pce_beyond_term(self):
        term = get_term_from_quarter_string("2013,summer")
        get_request_with_user('javerage',
                              get_request_with_date("2013-08-01"))

        section1 = Section()
        section1.curriculum_abbr = 'ASD'
        section1.course_number = 123
        section1.section_id = 'A'
        section1.start_date = datetime.date(2013, 6, 2)
        section1.end_date = datetime.date(2013, 9, 4)
        section1.term = term

        s1_meetings = SectionMeeting()
        s1_meetings.meets_monday = True
        s1_meetings.meets_friday = True
        section1.meetings = [s1_meetings]

        request = get_request_with_user('javerage')
        schedule = get_schedule_by_term(request, term)
        schedule.sections.append(section1)

        consolidated = _get_visual_schedule_from_schedule(
            schedule, request, schedule.summer_term)

        self.assertEqual(len(consolidated), 5)

        self.assertEqual(consolidated[0].start_date,
                         datetime.date(2013, 6, 24))
        self.assertEqual(consolidated[3].end_date,
                         datetime.date(2013, 8, 23))

        # ensure section exists in each week
        for week in consolidated:
            found_match = False
            for section in week.sections:
                if _sections_are_same(section, section1):
                    found_match = True
            self.assertTrue(found_match)

    def test_summer_term_schedule_pce(self):
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

        request = get_request_with_user('javerage')
        schedule = get_schedule_by_term(request, term)
        schedule.sections.append(section1)

        consolidated = _get_visual_schedule_from_schedule(
            schedule, request, schedule.summer_term)

        self.assertEqual(len(consolidated), 7)

        self.assertEqual(consolidated[0].start_date,
                         datetime.date(2013, 6, 24))
        self.assertEqual(consolidated[0].end_date,
                         datetime.date(2013, 7, 5))

        self.assertEqual(consolidated[1].start_date,
                         datetime.date(2013, 7, 8))
        self.assertEqual(consolidated[1].end_date,
                         datetime.date(2013, 7, 19))

        self.assertEqual(consolidated[2].start_date,
                         datetime.date(2013, 7, 22))
        self.assertEqual(consolidated[2].end_date,
                         datetime.date(2013, 7, 24))

        self.assertEqual(consolidated[3].start_date,
                         datetime.date(2013, 7, 25))
        self.assertEqual(consolidated[3].end_date,
                         datetime.date(2013, 7, 26))

        self.assertEqual(consolidated[4].start_date,
                         datetime.date(2013, 7, 29))
        self.assertEqual(consolidated[4].end_date,
                         datetime.date(2013, 8, 9))

        self.assertEqual(consolidated[5].start_date,
                         datetime.date(2013, 8, 12))
        self.assertEqual(consolidated[5].end_date,
                         datetime.date(2013, 8, 23))

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
        term = get_term_from_quarter_string("2013,autumn")
        request = get_request_with_user('javerage')
        schedule = get_schedule_by_term(request, term)
        get_request_with_user('javerage',
                              get_request_with_date("2013-10-01"))
        consolidated = _get_visual_schedule_from_schedule(
            schedule, request, None)
        self.assertEqual(len(consolidated), 5)

        self.assertEqual(consolidated[0].start_date,
                         datetime.date(2013, 8, 26))
        self.assertEqual(consolidated[0].end_date,
                         datetime.date(2013, 9, 13))

        self.assertEqual(consolidated[1].start_date,
                         datetime.date(2013, 9, 16))
        self.assertEqual(consolidated[1].end_date,
                         datetime.date(2013, 9, 18))

        self.assertEqual(consolidated[2].start_date,
                         datetime.date(2013, 9, 25))
        self.assertEqual(consolidated[2].end_date,
                         datetime.date(2013, 9, 27))

        self.assertEqual(consolidated[3].start_date,
                         datetime.date(2013, 9, 30))
        self.assertEqual(consolidated[3].end_date,
                         datetime.date(2013, 12, 6))

        trimmed_efs_mtg = consolidated[1].sections[0].meetings[0]
        self.assertFalse(trimmed_efs_mtg.meets_sunday)
        self.assertTrue(trimmed_efs_mtg.meets_monday)
        self.assertTrue(trimmed_efs_mtg.meets_tuesday)
        self.assertTrue(trimmed_efs_mtg.meets_wednesday)
        self.assertFalse(trimmed_efs_mtg.meets_thursday)
        self.assertFalse(trimmed_efs_mtg.meets_friday)
        self.assertFalse(trimmed_efs_mtg.meets_saturday)

    def test_get_finals(self):
        term = get_term_from_quarter_string("2013,spring")
        request = get_request_with_user('javerage')
        schedule = get_schedule_by_term(request, term)
        finals = _get_finals_period(schedule)
        self.assertEqual(len(finals.sections), 5)

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

        visual_schedule = _get_visual_schedule_from_schedule(
            schedule, request, None)
        self.assertTrue(visual_schedule[1].meets_sunday)

    def test_future_term(self):
        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-03-01"))
        term = get_term_from_quarter_string("2013,summer")
        future_schedule = get_future_visual_schedule(
            request, term, summer_term='b-term')

        now_req = get_request_with_date("2013-08-01")
        second_request = get_request_with_user('javerage', now_req)
        current_schedule, term, summer_term = get_current_visual_schedule(
            second_request)
        self.assertTrue(summer_term, 'b-term')
        # Ensure that getting summer as 'current' term returns same results
        # as getting as future
        self.assertTrue(self._period_lists_are_same(current_schedule,
                                                    future_schedule))

    def test_trim_summer_schedule(self):
        term = get_term_from_quarter_string("2013,summer")
        request = get_request_with_user('javerage')
        schedule = get_schedule_by_term(request, term)
        get_request_with_user('javerage',
                              get_request_with_date("2013-08-01"))

        consolidated = _get_visual_schedule_from_schedule(
            schedule, request, schedule.summer_term)

        a_trimmed = _trim_summer_term(consolidated, 'a-term')
        b_trimmed = _trim_summer_term(consolidated, 'b-term')
        self.assertEqual(len(a_trimmed), 2)
        self.assertEqual(len(b_trimmed), 2)

    def test_future_summer(self):
        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-03-01"))
        term = get_term_from_quarter_string("2013,summer")
        future_schedule = get_future_visual_schedule(request, term, "a-term")
        self.assertEqual(len(future_schedule), 2)

    def test_future_regular(self):
        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-03-01"))
        term = get_term_from_quarter_string("2013,autumn")
        future_schedule = get_future_visual_schedule(request, term)
        self.assertEqual(len(future_schedule), 5)

    def test_get_earliest_start_from_period(self):
        periods = self._get_schedule_with_meetings()
        earliest_start = _get_earliest_start_from_period(periods[0])
        self.assertEqual(earliest_start, datetime.date(2017, 10, 3))

        no_mtg_periods = self._get_schedule_no_meetings()
        earliest_start = _get_earliest_start_from_period(no_mtg_periods[0])
        self.assertEqual(earliest_start, datetime.date(2017, 10, 2))

    def test_get_latest_end_from_period(self):
        periods = self._get_schedule_with_meetings()
        latest_end = _get_latest_end_from_period(periods[0])
        self.assertEqual(latest_end, datetime.date(2017, 10, 14))
        latest_end = _get_latest_end_from_period(periods[1])
        self.assertEqual(latest_end, datetime.date(2017, 10, 20))

        no_mtg_periods = self._get_schedule_no_meetings()
        latest_end = _get_latest_end_from_period(no_mtg_periods[0])
        self.assertEqual(latest_end, datetime.date(2017, 10, 20))

    def test_get_earliest_meeting(self):
        # first is sat + tues, 2nd is wed + fri
        periods = self._get_schedule_with_meetings()
        meeting = periods[0].sections[0].meetings[0]
        self.assertEqual(_get_earliest_meeting_day(meeting), 1)
        meeting = periods[0].sections[1].meetings[0]
        self.assertEqual(_get_earliest_meeting_day(meeting), 2)

    def test_get_latest_meeting(self):
        periods = self._get_schedule_with_meetings()
        meeting = periods[0].sections[0].meetings[0]
        self.assertEqual(_get_latest_meeting_day(meeting), 5)
        meeting = periods[0].sections[1].meetings[0]
        self.assertEqual(_get_latest_meeting_day(meeting), 4)

    def test_get_disabled_days(self):
        days = _get_disabled_days(datetime.date(2013, 7, 25), True)
        disabled_days = {'sunday': True,
                         'monday': True,
                         'tuesday': True,
                         'wednesday': True,
                         'thursday': False,
                         'friday': False,
                         'saturday': False}

        self.assertDictEqual(days, disabled_days)

        days = _get_disabled_days(datetime.date(2013, 7, 25), False)
        disabled_days = {'sunday': False,
                         'monday': False,
                         'tuesday': False,
                         'wednesday': False,
                         'thursday': False,
                         'friday': True,
                         'saturday': True}

        self.assertDictEqual(days, disabled_days)

    def test_get_off_term_trimmed(self):
        request = get_request_with_user('jeos',
                                        get_request_with_date("2013-07-25"))
        schedule = _get_combined_schedule(request)
        visual_schedule = _get_visual_schedule_from_schedule(
            schedule, request, schedule.summer_term)
        trimmed = _get_off_term_trimmed(visual_schedule)
        self.assertEqual(trimmed[0]['section'], 'LIS 498 C')

    def test_pce_schedule(self):
        mon_mtg = SectionMeeting()
        mon_mtg.meets_monday = True
        sat_mtg = SectionMeeting()
        sat_mtg.meets_saturday = True
        thu_mtg = SectionMeeting()
        thu_mtg.meets_thursday = True

        section1 = Section()
        section1.curriculum_abbr = 'CLDAWS'
        section1.course_number = 220
        section1.section_id = 'A'
        section1.start_date = datetime.date(2018, 1, 8)
        section1.end_date = datetime.date(2018, 3, 26)
        section1.meetings = [mon_mtg]

        section2 = Section()
        section2.curriculum_abbr = 'SOF DEV'
        section2.course_number = 105
        section2.section_id = 'A'
        section2.start_date = datetime.date(2018, 1, 6)
        section2.end_date = datetime.date(2018, 2, 24)
        section2.meetings = [sat_mtg, thu_mtg, sat_mtg]

        section3 = Section()
        section3.curriculum_abbr = 'SOF DEV'
        section3.course_number = 115
        section3.section_id = 'A'
        section3.start_date = datetime.date(2018, 3, 10)
        section3.end_date = datetime.date(2018, 4, 24)
        section3.meetings = [sat_mtg, thu_mtg, sat_mtg]

        term = get_term_from_quarter_string("2018,winter")
        schedule = ClassSchedule()
        schedule.term = term
        schedule.sections = [section1, section2, section3]

        schedule = _add_dates_to_sections(schedule)

        bounds = get_schedule_bounds(schedule)
        weeks = _get_weeks_from_bounds(bounds)
        weeks = _add_qtr_start_data_to_weeks(weeks, schedule)
        weeks = _add_sections_to_weeks(schedule.sections, weeks)
        weeks = trim_section_meetings(weeks)
        weeks = trim_weeks_no_meetings(weeks)
        consolidated = _consolidate_weeks(weeks)
        _add_weekend_meeting_data(consolidated)
        _adjust_period_dates(consolidated)

        self.assertEqual(len(consolidated), 6)
        self.assertEqual(consolidated[0].start_date, datetime.date(2018, 1, 3))
        self.assertEqual(consolidated[0].end_date, datetime.date(2018, 1, 6))
        self.assertEqual(consolidated[1].start_date, datetime.date(2018, 1, 8))
        self.assertEqual(consolidated[1].end_date, datetime.date(2018, 2, 24))
        self.assertEqual(consolidated[2].start_date,
                         datetime.date(2018, 2, 26))
        self.assertEqual(consolidated[2].end_date, datetime.date(2018, 3, 2))
        self.assertEqual(consolidated[3].start_date, datetime.date(2018, 3, 5))
        self.assertEqual(consolidated[3].end_date, datetime.date(2018, 3, 10))
        self.assertEqual(consolidated[4].start_date,
                         datetime.date(2018, 3, 12))
        self.assertEqual(consolidated[4].end_date, datetime.date(2018, 3, 31))
        self.assertEqual(consolidated[5].start_date,
                         datetime.date(2018, 4, 2))
        self.assertEqual(consolidated[5].end_date, datetime.date(2018, 4, 21))

    def test_midweek_start(self):
        mwf_mtg = SectionMeeting()
        mwf_mtg.meets_monday = True
        mwf_mtg.meets_wednesday = True
        mwf_mtg.meets_friday = True

        tth_mtg = SectionMeeting()
        tth_mtg.meets_tuesday = True
        tth_mtg.meets_thursday = True

        th_mtg = SectionMeeting()
        th_mtg.meets_thursday = True

        mw_mtg = SectionMeeting()
        mw_mtg.meets_monday = True
        mw_mtg.meets_wednesday = True

        f_mtg = SectionMeeting()
        f_mtg.meets_friday = True

        section1 = Section()
        section1.curriculum_abbr = 'CSE'
        section1.course_number = 143
        section1.section_id = 'A'
        section1.meetings = [mwf_mtg]

        section2 = Section()
        section2.curriculum_abbr = 'CSE'
        section2.course_number = 143
        section2.section_id = 'AQ'
        section2.meetings = [tth_mtg]

        section3 = Section()
        section3.curriculum_abbr = 'MATH'
        section3.course_number = 126
        section3.section_id = 'F'
        section3.meetings = [th_mtg]

        section4 = Section()
        section4.curriculum_abbr = 'PSYCH'
        section4.course_number = 210
        section4.section_id = 'A'
        section4.meetings = [mw_mtg, f_mtg]

        term = get_term_from_quarter_string("2018,winter")
        schedule = ClassSchedule()
        schedule.term = term
        schedule.sections = [section1, section2, section3, section4]

        _add_dates_to_sections(schedule)

        bounds = get_schedule_bounds(schedule)
        weeks = _get_weeks_from_bounds(bounds)
        weeks = _add_qtr_start_data_to_weeks(weeks, schedule)
        weeks = _add_sections_to_weeks(schedule.sections, weeks)
        weeks = trim_section_meetings(weeks)
        weeks = trim_weeks_no_meetings(weeks)
        consolidated = _consolidate_weeks(weeks)
        _add_weekend_meeting_data(consolidated)
        _adjust_period_dates(consolidated)
        self.assertEqual(len(consolidated), 2)

    def test_summer_full_only(self):
        mwf_mtg = SectionMeeting()
        mwf_mtg.meets_monday = True
        mwf_mtg.meets_wednesday = True
        mwf_mtg.meets_friday = True

        section1 = Section()
        section1.curriculum_abbr = 'SOF DEV'
        section1.course_number = 115
        section1.section_id = 'A'
        section1.meetings = [mwf_mtg]
        section1.summer_term = "Full-term"

        section2 = Section()
        section2.curriculum_abbr = 'ASD'
        section2.course_number = 115
        section2.section_id = 'A'
        section2.meetings = [mwf_mtg]
        section2.summer_term = "Full-term"

        term = get_term_from_quarter_string("2013,summer")
        schedule = ClassSchedule()
        schedule.term = term
        schedule.sections = [section1, section2]

        request = get_request_with_user('javerage',
                                        get_request_with_date("2013-07-01"))
        summer_term = get_current_summer_term(request)
        vs = get_visual_schedule_from_schedule(request, schedule, summer_term)
        self.assertEqual(len(vs), 2)
        self.assertEqual(len(vs[0].sections), 2)

    def test_summer_full_and_a(self):
        mwf_mtg = SectionMeeting()
        mwf_mtg.meets_monday = True
        mwf_mtg.meets_wednesday = True
        mwf_mtg.meets_friday = True

        section1 = Section()
        section1.curriculum_abbr = 'SOF DEV'
        section1.course_number = 115
        section1.section_id = 'A'
        section1.meetings = [mwf_mtg]
        section1.summer_term = "a-term"

        section2 = Section()
        section2.curriculum_abbr = 'ASD'
        section2.course_number = 115
        section2.section_id = 'A'
        section2.meetings = [mwf_mtg]
        section2.summer_term = "Full-term"

        term = get_term_from_quarter_string("2013,summer")
        schedule = ClassSchedule()
        schedule.term = term
        schedule.sections = [section1, section2]

        request = get_request_with_user('javerage',
                                        get_request_with_date(
                                            "2013-07-01"))

        summer_term = get_current_summer_term(request)
        vs = get_visual_schedule_from_schedule(request, schedule,
                                               summer_term)
        self.assertEqual(len(vs), 2)
        self.assertEqual(len(vs[0].sections), 2)
        self.assertEqual(vs[0].end_date, datetime.date(2013, 7, 19))

    def test_add_dates_to_sections(self):
        section1 = Section()
        section1.curriculum_abbr = 'ASD'
        section1.course_number = 123
        section1.section_id = 'A'
        section1.start_date = datetime.date(2017, 10, 2)
        section1.end_date = datetime.date(2017, 10, 20)

        section2 = Section()
        section2.curriculum_abbr = 'QWE'
        section2.course_number = 456
        section2.section_id = 'A'
        section2.start_date = datetime.date(2017, 10, 2)
        section2.end_date = None

        schedule = ClassSchedule()
        schedule.sections = [section1, section2]

        schedules = []
        schedules.append(schedule)

        end_schedule = ClassSchedule()

        term = get_term_from_quarter_string("2013,summer")
        schedule.term = term

        end_section1 = Section()
        end_section1.curriculum_abbr = 'ASD'
        end_section1.course_number = 123
        end_section1.section_id = 'A'
        end_section1.start_date = datetime.date(2017, 10, 2)
        end_section1.end_date = term.last_day_instruction

        end_section2 = Section()
        end_section2.curriculum_abbr = 'QWE'
        end_section2.course_number = 456
        end_section2.section_id = 'A'
        end_section2.start_date = datetime.date(2017, 10, 2)
        end_section2.end_date = term.last_day_instruction

        end_schedule = ClassSchedule()
        end_schedule.sections = [section1, section2]

        end_schedules = []

        end_schedules.append(end_schedule)

        _add_dates_to_sections(schedule)

        for x in range(0, len(schedules)):
            for y in range(0, len(schedules[x].sections)):
                self.assertEqual(
                    schedules[x].sections[y].end_date,
                    end_schedules[x].sections[y].end_date)

    def test_remote_instructor_sections(self):
        request = get_request_with_user('billsea',
                                        get_request_with_date("2020-10-01"))
        term = get_current_quarter(request)
        schedule, term, summer_term = get_current_visual_schedule(request)
        self.assertEqual(len(schedule), 3)
        schedule_json = get_schedule_json(schedule, term)
        self.assertEqual(len(schedule_json['periods']), 3)

    def test_remote_student_sections(self):
        request = get_request_with_user('eight',
                                        get_request_with_date("2020-10-01"))
        term = get_current_quarter(request)
        schedule, term, summer_term = get_current_visual_schedule(request)
        self.assertEqual(len(schedule), 3)
        schedule_json = get_schedule_json(schedule, term)
        self.assertEqual(len(schedule_json['periods']), 3)
        self.assertTrue(
            schedule_json['periods'][2]['sections'][0]['is_remote'])
        self.assertTrue(
            schedule_json['periods'][2]['sections'][1]['is_remote'])
        self.assertTrue(
            schedule_json['periods'][2]['sections'][2]['is_remote'])


    def test_MUWM_4800(self):
        request = get_request_with_user(
            'jeos', get_request_with_date("2013-05-12"))
        term = get_current_quarter(request)
        schedule, term, summer_term = get_current_visual_schedule(request)
        self.assertEqual(len(schedule), 5)
        schedule_json = get_schedule_json(schedule, term)
        self.assertEqual(len(schedule_json['periods']), 5)
        self.assertEqual(str(schedule_json['periods'][2]['end_date']),
                         '2013-06-15')
        self.assertEqual(len(schedule_json['periods'][2]['sections']), 2)
        self.assertEqual(
            schedule_json['periods'][2]['sections'][0]['curriculum_abbr'],
            'BIGDATA')
        self.assertEqual(
            schedule_json['periods'][2]['sections'][0]['course_number'],
            '230')
        # BIGDATA 230 A ends 2013/6/12
        self.assertEqual(str(schedule_json['periods'][3]['start_date']),
                         '2013-06-17')
        self.assertEqual(len(schedule_json['periods'][3]['sections']), 1)
        self.assertEqual(
            schedule_json['periods'][3]['sections'][0]['curriculum_abbr'],
            'BIGDATA')
        self.assertEqual(
            schedule_json['periods'][3]['sections'][0]['course_number'],
            '233')
