from django.conf import settings
import datetime
from restclients.sws import SWS
from myuw_mobile.models import CourseColor
import logging
import json


class Quarter:
    """ This class encapsulate the access of the term data """
    _logger = logging.getLogger('myuw_mobile.dao.sws.Quarter')

    def get_cur_quarter(self):
        """
        Returns calendar information for the current term.
        """
        sws = SWS()
        term = sws.get_current_term()

        return term


class Schedule:
    TOTAL_COURSE_COLORS = 8
    """
    This class encapsulates the access of the registration
    and section resources
    """

    _logger = logging.getLogger('myuw_mobile.dao.sws.Schedule')

    def __init__(self, regid):
        self.regid = regid

    def get_cur_quarter_registration(self):
        """ Return the actively enrolled sections in the current quarter """

        term = Quarter().get_cur_quarter()
        sws = SWS()

        schedule = sws.schedule_for_regid_and_term(self.regid, term)

        return schedule

    def get_curr_quarter_schedule(self):
        regi_rslt = self.get_cur_quarter_registration()

        return regi_rslt
        if not regi_rslt:
            # not enrolled in the currrent quarter
            return None

        return regi_rslt

    def get_colors_for_schedule(self, schedule):
        colors = {}

        query = CourseColor.objects.filter(
                                            regid=self.regid,
                                            year=schedule.term.year,
                                            quarter=schedule.term.quarter,
                                            )

        existing_sections = []
        color_lookup = {}
        active_colors = {}
        colors_to_deactivate = {}
        for color in query:
            existing_sections.append(color)
            if color.is_active:
                color_lookup[color.section_label()] = color
                active_colors[color.color_id] = True
                colors_to_deactivate[color.section_label()] = color

        primary_sections = []
        secondary_sections = []
        for section in schedule.sections:
            if section.is_primary_section:
                primary_sections.append(section)
            else:
                secondary_sections.append(section)

        for section in primary_sections:
            label = section.section_label()
            if section.section_label() not in color_lookup:
                color = self._get_color_for_section(
                                                    existing_sections,
                                                    active_colors,
                                                    schedule,
                                                    section,
                                                   )
                existing_sections.append(color)
                color_lookup[color.section_label()] = color
                active_colors[color.color_id] = True

            if section.section_label() in colors_to_deactivate:
                del colors_to_deactivate[section.section_label()]

            colors[label] = color_lookup[section.section_label()].color_id

        for section in secondary_sections:
            label = section.section_label()
            primary_label = section.primary_section_label()

            if colors[primary_label] == None:
                # ... uh oh
                pass

            colors[label] = "%sa" % colors[primary_label]

        for color_key in colors_to_deactivate:
            color = colors_to_deactivate[color_key]
            color.is_active = False
            color.save()

        return colors

    def _get_color_for_section(self, existing, active, schedule, section):
        color = CourseColor()
        color.regid = self.regid
        color.year = schedule.term.year
        color.quarter = schedule.term.quarter
        color.curriculum_abbr = section.curriculum_abbr
        color.course_number = section.course_number
        color.section_id = section.section_id
        color.is_active = True
        next_color = len(existing) + 1

        if next_color > self.TOTAL_COURSE_COLORS:
            for add in range(self.TOTAL_COURSE_COLORS):
                total = next_color + add
                test_color = (total % self.TOTAL_COURSE_COLORS) + 1

                if not test_color in active:
                    next_color = test_color
                    break

        if next_color > self.TOTAL_COURSE_COLORS:
            next_color = ((next_color - 1) % self.TOTAL_COURSE_COLORS) + 1

        color.color_id = next_color
        color.save()

        return color
