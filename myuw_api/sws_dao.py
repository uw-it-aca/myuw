from django.conf import settings
import datetime
from restclients.sws import SWS
from myuw_api.models import CourseColor
import logging
import json

class Quarter:
    """ This class encapsulate the access of the term data """
    _logger = logging.getLogger('myuw_api.sws_dao.Quarter')

    def get_cur_quarter(self):
        """
        Returns calendar information for the current term.
        """
        sws = SWS()
        term = sws.get_current_term()

        return term


class Schedule:
    """
    This class encapsulates the access of the registration and section resources
    """

    _logger = logging.getLogger('myuw_api.sws_dao.Schedule')

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

        query = CourseColor.objects.filter(regid=self.regid,
                                            year = schedule.term.year,
                                            quarter = schedule.term.quarter
                                            )

        existing_sections = []
        color_lookup = {}
        for color in query:
            existing_sections.append(color)
            color_lookup[color.section_label()] = color

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
                color = self._get_color_for_section(existing_sections, schedule, section)
                existing_sections.append(color)
                color_lookup[color.section_label()] = color

            colors[label] = color_lookup[section.section_label()].color_id

        for section in secondary_sections:
            label = section.section_label()
            primary_label = section.primary_section_label()

            if colors[primary_label] == None:
                # ... uh oh
                pass

            colors[label] = "%sa" % colors[primary_label]

        return colors


    def _get_color_for_section(self, existing_sections, schedule, section):
        color = CourseColor()
        color.regid = self.regid
        color.year = schedule.term.year
        color.quarter = schedule.term.quarter
        color.curriculum_abbr = section.curriculum_abbr
        color.course_number = section.course_number
        color.section_id = section.section_id
        color.is_active = True
        color.color_id = len(existing_sections) + 1
        color.save()

        return color
