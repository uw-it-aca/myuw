from django.test import TransactionTestCase
from django.conf import settings
from userservice.user import UserServiceMiddleware
from myuw.models import UserCourseDisplay
from myuw.dao.instructor_schedule import get_instructor_schedule_by_term
from myuw.dao.registration import get_schedule_by_term
from myuw.dao.term import get_current_quarter
from myuw.dao.user_course_display import set_course_display_pref,\
    _get_next_color, set_pin_on_teaching_page
from myuw.test import get_request_with_user, get_request_with_date


class TestUserCourseDisplayDao(TransactionTestCase):

    def test_get_next_color(self):
        colors_taken = []
        self.assertEqual(_get_next_color(colors_taken), 1)
        self.assertEqual(_get_next_color(colors_taken), 2)
        self.assertEqual(_get_next_color(colors_taken), 3)
        self.assertEqual(_get_next_color(colors_taken), 4)
        self.assertEqual(_get_next_color(colors_taken), 5)
        self.assertEqual(_get_next_color(colors_taken), 6)
        self.assertEqual(_get_next_color(colors_taken), 7)
        self.assertEqual(_get_next_color(colors_taken), 8)
        self.assertEqual(_get_next_color(colors_taken), 1)

        colors_taken = [1, 3, 4]
        self.assertEqual(_get_next_color(colors_taken), 2)
        self.assertEqual(_get_next_color(colors_taken), 5)

    def test_student_schedule(self):
        req = get_request_with_user("javerage")
        term = get_current_quarter(req)
        schedule = get_schedule_by_term(req, term)
        set_course_display_pref(req, schedule)
        sections = schedule.sections
        self.assertEquals(len(sections), 5)
        self.assertEquals(sections[0].color_id, 1)
        self.assertEquals(sections[1].color_id, 2)
        self.assertEquals(sections[2].color_id, 3)

        self.assertEquals(sections[3].primary_section_label(),
                          sections[2].section_label())
        self.assertEquals(sections[3].color_id, '3a')

        self.assertEquals(sections[4].primary_section_label(),
                          sections[2].section_label())
        self.assertEquals(sections[4].color_id, '3a')
        records = UserCourseDisplay.objects.all()
        self.assertEquals(len(records), 5)

    def test_instructor_schedule(self):
        req = get_request_with_user("billsea")
        term = get_current_quarter(req)
        schedule = get_instructor_schedule_by_term(req, term)
        set_course_display_pref(req, schedule)
        sections = schedule.sections
        self.assertEquals(len(sections), 8)
        self.assertEquals(sections[0].color_id, 1)
        self.assertEquals(sections[1].color_id, 2)
        self.assertEquals(sections[2].primary_section_label(),
                          sections[1].section_label())
        self.assertEquals(sections[2].color_id, '2a')

        self.assertEquals(sections[3].primary_section_label(),
                          sections[1].section_label())
        self.assertEquals(sections[3].color_id, '2a')

        self.assertEquals(sections[4].color_id, 3)
        self.assertEquals(sections[5].color_id, 4)

        self.assertEquals(sections[6].primary_section_label(),
                          sections[5].section_label())
        self.assertEquals(sections[6].color_id, '4a')

        self.assertEquals(sections[7].color_id, '5a')
        records = UserCourseDisplay.objects.all()
        self.assertEquals(len(records), 8)

    def test_all_secondary_schedule(self):
        req = get_request_with_user("billseata")
        term = get_current_quarter(req)
        schedule = get_instructor_schedule_by_term(req, term)
        set_course_display_pref(req, schedule)
        sections = schedule.sections
        self.assertEquals(len(sections), 7)
        self.assertEquals(sections[0].color_id, '1a')
        self.assertEquals(sections[1].color_id, '1a')
        self.assertEquals(sections[2].color_id, '2a')
        self.assertEquals(sections[3].color_id, '2a')
        self.assertEquals(sections[4].color_id, '3a')
        self.assertEquals(sections[5].color_id, '4a')
        self.assertEquals(sections[6].color_id, '4a')

        records = UserCourseDisplay.objects.all()
        self.assertEquals(len(records), 7)

        #  test drop sections
        schedule.sections.remove(sections[6])
        schedule.sections.remove(sections[0])
        schedule.sections.remove(sections[0])
        set_course_display_pref(req, schedule)
        records = UserCourseDisplay.objects.all()
        self.assertEquals(len(records), 4)

        # add them back
        schedule = get_instructor_schedule_by_term(req, term)
        set_course_display_pref(req, schedule)
        sections = schedule.sections
        self.assertEquals(len(sections), 7)
        self.assertEquals(sections[0].color_id, '1a')
        self.assertEquals(sections[1].color_id, '1a')
        self.assertEquals(sections[2].color_id, '2a')
        self.assertEquals(sections[3].color_id, '2a')
        self.assertEquals(sections[4].color_id, '3a')
        self.assertEquals(sections[5].color_id, '4a')
        self.assertEquals(sections[6].color_id, '4a')
        records = UserCourseDisplay.objects.all()
        self.assertEquals(len(records), 7)

    def test_set_pin_on_teaching_page(self):
        req = get_request_with_user("billsea")
        term = get_current_quarter(req)
        schedule = get_instructor_schedule_by_term(req, term)
        set_course_display_pref(req, schedule)
        records = UserCourseDisplay.objects.all()
        self.assertFalse(records[2].pin_on_teaching_page)
        self.assertFalse(records[3].pin_on_teaching_page)

        section_label = schedule.sections[2].section_label()
        set_pin_on_teaching_page(req,
                                 schedule.term.year,
                                 schedule.term.quarter,
                                 section_label)
        records = UserCourseDisplay.objects.all()
        self.assertTrue(records[2].pin_on_teaching_page)

        set_pin_on_teaching_page(req,
                                 schedule.term.year,
                                 schedule.term.quarter,
                                 section_label,
                                 pin=False)
        records = UserCourseDisplay.objects.all()
        self.assertFalse(records[2].pin_on_teaching_page)
