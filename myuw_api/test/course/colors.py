from django.test import TestCase
from django.conf import settings

from myuw_api.sws_dao import Schedule as ScheduleDAO
from restclients.models import ClassSchedule, Term, Section, Person

class TestCourseColors(TestCase):
    def test_single_course(self):
        term = Term()
        term.year = 2012
        term.quarter = "autumn"

        person = Person()
        person.uwnetid = "javerage"
        person.regid = "00000000000000000000000000000001"
        schedule = ClassSchedule()

        schedule.term = term
        schedule.user = person
        schedule.sections = []

        section = Section()
        section.term = term
        section.curriculum_abbr = "MATH"
        section.course_number = 124
        section.section_id = "A"
        section.is_primary_section = True

        schedule.sections.append(section)

        sched_dao = ScheduleDAO(person.regid)
        colors = sched_dao.get_colors_for_schedule(schedule)

        self.assertEquals(colors[section.section_label()], 1, "Single course section gets the first color")

    def test_2_courses(self):
        term = Term()
        term.year = 2012
        term.quarter = "autumn"

        person = Person()
        person.uwnetid = "javerage"
        person.regid = "00000000000000000000000000000002"
        schedule = ClassSchedule()

        schedule.term = term
        schedule.user = person
        schedule.sections = []

        section = Section()
        section.term = term
        section.curriculum_abbr = "MATH"
        section.course_number = 124
        section.section_id = "A"
        section.is_primary_section = True

        schedule.sections.append(section)

        section2 = Section()
        section2.term = term
        section2.curriculum_abbr = "MATH"
        section2.course_number = 300
        section2.section_id = "A"
        section2.is_primary_section = True

        schedule.sections.append(section2)



        sched_dao = ScheduleDAO(person.regid)
        colors = sched_dao.get_colors_for_schedule(schedule)

        self.assertEquals(colors[section.section_label()], 1, "First course section gets the first color")
        self.assertEquals(colors[section2.section_label()], 2, "Second section gets the second color")


    def test_primary_secondary(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            schedule_dao = ScheduleDAO("00000000000000000000000000000003")
            schedule = schedule_dao.get_curr_quarter_schedule()

            colors = schedule_dao.get_colors_for_schedule(schedule)

            self.assertEquals(colors["2012,summer,PHYS,121/A"], 1, "Primary gets the 1st color")
            self.assertEquals(colors["2012,summer,PHYS,121/AC"], "1a", "Secondary gets the 1st color, secondary version")
            self.assertEquals(colors["2012,summer,PHYS,121/AQ"], "1a", "Second secondary gets the 1st color, secondary version")


    def test_drop_then_new_add(self):
        term = Term()
        term.year = 2012
        term.quarter = "autumn"

        person = Person()
        person.uwnetid = "javerage"
        person.regid = "00000000000000000000000000000004"
        schedule = ClassSchedule()

        schedule.term = term
        schedule.user = person
        schedule.sections = []

        section = Section()
        section.term = term
        section.curriculum_abbr = "MATH"
        section.course_number = 124
        section.section_id = "A"
        section.is_primary_section = True

        schedule.sections.append(section)

        section2 = Section()
        section2.term = term
        section2.curriculum_abbr = "MATH"
        section2.course_number = 300
        section2.section_id = "A"
        section2.is_primary_section = True

        schedule.sections.append(section2)

        sched_dao = ScheduleDAO(person.regid)

        # Get the colors for the first round - doesn't matter what they are though
        colors = sched_dao.get_colors_for_schedule(schedule)

        schedule.sections = []
        schedule.sections.append(section)

        section3 = Section()
        section3.term = term
        section3.curriculum_abbr = "MATH"
        section3.course_number = 309
        section3.section_id = "A"
        section3.is_primary_section = True

        schedule.sections.append(section3)

        colors = sched_dao.get_colors_for_schedule(schedule)

        self.assertEquals(colors[section.section_label()], 1, "First course section gets the first color")

        try:
            c2 = colors[section2.section_label()]
            self.fail("There shouldn't be a color for section 2")
        except KeyError as ex:
            pass

        self.assertEquals(colors[section3.section_label()], 3, "3rd section gets the 3rd color")




