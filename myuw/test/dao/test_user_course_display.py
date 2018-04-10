from django.test import TransactionTestCase
from django.conf import settings
from userservice.user import UserServiceMiddleware
from uw_sws.exceptions import InvalidSectionID
from myuw.models import UserCourseDisplay
from myuw.dao.exceptions import NotSectionInstructorException
from myuw.dao.instructor_schedule import get_instructor_schedule_by_term
from myuw.dao.registration import get_schedule_by_term
from myuw.dao.term import get_current_quarter
from myuw.dao.user import get_user_model
from myuw.dao.user_course_display import set_course_display_pref,\
    _get_next_color, set_pin_on_teaching_page, _save_section_color
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
        self.assertEqual(len(sections), 5)
        self.assertEqual(sections[0].color_id, 1)
        self.assertEqual(sections[1].color_id, 2)
        self.assertEqual(sections[2].color_id, 3)

        self.assertEqual(sections[3].primary_section_label(),
                         sections[2].section_label())
        self.assertEqual(sections[3].color_id, '3a')

        self.assertEqual(sections[4].primary_section_label(),
                         sections[2].section_label())
        self.assertEqual(sections[4].color_id, '3a')
        records = UserCourseDisplay.objects.all()
        self.assertEqual(len(records), 5)

    def test_single_section_multiple_enrollments(self):
        # multiple enrollments of a single section
        req = get_request_with_user("seagrad",
                                    get_request_with_date("2017-04-10"))
        term = get_current_quarter(req)
        schedule = get_schedule_by_term(req, term)
        set_course_display_pref(req, schedule)
        sections = schedule.sections
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0].color_id, 1)
        self.assertEqual(sections[1].color_id, 1)
        records = UserCourseDisplay.objects.all()
        self.assertEqual(len(records), 1)

    def test_instructor_schedule(self):
        req = get_request_with_user("billsea")
        term = get_current_quarter(req)
        schedule = get_instructor_schedule_by_term(req, term)
        set_course_display_pref(req, schedule)

        sections = schedule.sections
        self.assertEqual(len(sections), 8)
        self.assertEqual(sections[0].color_id, 1)

        self.assertEqual(sections[1].section_label(),
                         '2013,spring,PHYS,122/B')
        self.assertEqual(sections[1].color_id, 2)

        # secondaries has its primary's color id plus 'a'
        self.assertEqual(sections[2].section_label(),
                         '2013,spring,PHYS,122/BA')
        self.assertEqual(sections[2].primary_section_label(),
                         sections[1].section_label())
        self.assertEqual(sections[2].color_id, '2a')
        self.assertFalse(sections[2].pin_on_teaching)

        self.assertEqual(sections[3].section_label(),
                         '2013,spring,PHYS,122/BS')
        self.assertEqual(sections[3].primary_section_label(),
                         sections[1].section_label())
        self.assertEqual(sections[3].color_id, '2a')

        self.assertEqual(sections[4].color_id, 3)
        self.assertEqual(sections[5].color_id, 4)

        self.assertEqual(sections[6].primary_section_label(),
                         sections[5].section_label())
        self.assertEqual(sections[6].color_id, '4a')

        self.assertEqual(sections[7].color_id, '5a')
        records = UserCourseDisplay.objects.all()
        self.assertEqual(len(records), 8)

        # test .pin_on_teaching is True
        secondary_obj = records[2]
        secondary_obj.pin_on_teaching_page = True
        secondary_obj.save()
        schedule = get_instructor_schedule_by_term(req, term)
        set_course_display_pref(req, schedule)
        self.assertTrue(schedule.sections[2].pin_on_teaching)

    def test_all_secondary_schedule(self):
        req = get_request_with_user("billseata")
        term = get_current_quarter(req)
        schedule = get_instructor_schedule_by_term(req, term)
        set_course_display_pref(req, schedule)
        sections = schedule.sections
        self.assertEqual(len(sections), 7)
        self.assertEqual(sections[0].color_id, '1a')
        self.assertEqual(sections[1].color_id, '1a')
        self.assertEqual(sections[2].color_id, '2a')
        self.assertEqual(sections[3].color_id, '2a')
        self.assertEqual(sections[4].color_id, '3a')
        self.assertEqual(sections[5].color_id, '4a')
        self.assertEqual(sections[6].color_id, '4a')

        records = UserCourseDisplay.objects.all()
        self.assertEqual(len(records), 7)

        #  test drop sections
        schedule.sections.remove(sections[6])
        schedule.sections.remove(sections[0])
        schedule.sections.remove(sections[0])
        set_course_display_pref(req, schedule)
        records = UserCourseDisplay.objects.all()
        self.assertEqual(len(records), 4)

        # add them back
        schedule = get_instructor_schedule_by_term(req, term)
        set_course_display_pref(req, schedule)
        sections = schedule.sections
        self.assertEqual(len(sections), 7)
        self.assertEqual(sections[0].color_id, '1a')
        self.assertEqual(sections[1].color_id, '1a')
        self.assertEqual(sections[2].color_id, '2a')
        self.assertEqual(sections[3].color_id, '2a')
        self.assertEqual(sections[4].color_id, '3a')
        self.assertEqual(sections[5].color_id, '4a')
        self.assertEqual(sections[6].color_id, '4a')
        records = UserCourseDisplay.objects.all()
        self.assertEqual(len(records), 7)

    def test_set_pin_on_teaching_page(self):
        req = get_request_with_user("billsea")
        term = get_current_quarter(req)
        schedule = get_instructor_schedule_by_term(req, term)
        set_course_display_pref(req, schedule)
        records = UserCourseDisplay.objects.all()
        self.assertFalse(records[2].pin_on_teaching_page)
        self.assertFalse(records[3].pin_on_teaching_page)

        section_label = schedule.sections[2].section_label()
        # test pin mini card
        self.assertTrue(set_pin_on_teaching_page(req,
                                                 section_label))
        records = UserCourseDisplay.objects.all()
        self.assertTrue(records[2].pin_on_teaching_page)

        # close pin mini card
        self.assertTrue(set_pin_on_teaching_page(req,
                                                 section_label,
                                                 pin=False))
        records = UserCourseDisplay.objects.all()
        self.assertFalse(records[2].pin_on_teaching_page)

        # test if not in DB
        records[2].delete()
        with self.assertRaises(UserCourseDisplay.DoesNotExist):
            set_pin_on_teaching_page(req, section_label, pin=True)

        # not pin primary section
        section_label = '2013,spring,PHYS,122/A'
        self.assertFalse(set_pin_on_teaching_page(req, section_label))

        # test InvalidSectionID
        section_label = '2013,spring,PHYS,122/'
        with self.assertRaises(InvalidSectionID):
            set_pin_on_teaching_page(req, section_label)

        # test NotSectionInstructorException
        section_label = '2013,spring,PHYS,121/AC'
        with self.assertRaises(NotSectionInstructorException):
            set_pin_on_teaching_page(req, section_label)
