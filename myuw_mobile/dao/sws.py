from django.conf import settings
#import datetime
import logging
import sys
import traceback
from restclients.sws import SWS
from myuw_mobile.models import CourseColor
from myuw_mobile.dao.building import Building
from pws import Person as PersonDao

sws = SWS()
person = PersonDao()

class Quarter:
    """ 
    This class encapsulate the access of the term data 
    """

    _logger = logging.getLogger('myuw_mobile.dao.sws.Quarter')

    def get_cur_quarter(self):
        """
        Returns calendar information for the current term.
        """
        try:
            return sws.get_current_term()
        except Exception, message:
            traceback.print_exc(file=sys.stdout)
            Quarter._logger.error("Ex: get_cur_quarter --> " + message)
            return None



class Schedule:
    TOTAL_COURSE_COLORS = 8
    """
    This class encapsulates the access of the registration
    and section resources
    """

    _logger = logging.getLogger('myuw_mobile.dao.sws.Schedule')

    def __init__(self, netid):
        self.netid = netid
        self.regid = person.get_regid(netid)
        self.term = Quarter().get_cur_quarter()



    def get_cur_quarter_schedule(self):
        """ Return the actively enrolled sections in the current quarter """
        
        if not self.term:
            return None
        try:
            return sws.schedule_for_regid_and_term(self.regid, self.term)
        except Exception, message:
            print '//// get current quarter schedule from SWS: ', message
            traceback.print_exc(file=sys.stdout)
            Schedule._logger.error("Ex: get_cur_quarter_schedule for " + 
                                   netid + " --> " + message)
            return None


    def get_buildings_for_schedule(self, schedule):
        buildings = {}
        building_dao = Building()
        for section in schedule.sections:
            for meeting in section.meetings:
                if not meeting.building_to_be_arranged:
                    if not meeting.building in buildings:
                        code = meeting.building
                        building = building_dao.get_building_from_code(code)
                        buildings[code] = building

        return buildings



    def get_colors_for_schedule(self, schedule):
        if not schedule or not schedule.sections:
            return None
        colors = {}
        try:
            query = CourseColor.objects.filter(
                regid=self.regid,
                year=schedule.term.year,
                quarter=schedule.term.quarter,
                )
        except Exception, message:
            print '//// get course color from MySQL: ', message
            Schedule._logger.error("Ex: get_colors_for_schedule for " +
                                   netid + " --> " + message)
            return None

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
