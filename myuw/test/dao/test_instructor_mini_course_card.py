# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TransactionTestCase
from uw_sws.exceptions import InvalidSectionID
from myuw.models import UserCourseDisplay
from myuw.dao.exceptions import NotSectionInstructorException
from myuw.dao.term import get_current_quarter
from myuw.dao.instructor_schedule import get_instructor_schedule_by_term
from myuw.dao.instructor_mini_course_card import set_pin_on_teaching_page
from myuw.test import get_request_with_user


class TestPinMiniCard(TransactionTestCase):

    def test_set_pin_on_teaching_page(self):
        req = get_request_with_user("billsea")
        term = get_current_quarter(req)
        schedule = get_instructor_schedule_by_term(req, term)
        records = UserCourseDisplay.objects.all()
        self.assertFalse(records[0].pin_on_teaching_page)
        self.assertFalse(records[1].pin_on_teaching_page)
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
