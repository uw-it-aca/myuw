from django.conf import settings
from datetime import datetime
import logging
import traceback
from restclients.sws import SWS
from restclients.models import ClassSchedule
from myuw_mobile.models import CourseColor
from building import Building
from pws import Person
from myuw_mobile.logger.timer import Timer
from restclients.exceptions import DataFailureException
from myuw_mobile.logger.logback import log_resp_time, log_exception

class Quarter:
    """ 
    This class encapsulate the access of the term data 
    """

    _logger = logging.getLogger('myuw_mobile.dao.sws.Quarter')

    def get_cur_quarter(self):
        """
        Returns calendar information for the current term.
        """
        timer = Timer()
        try:
            return SWS().get_current_term()
        except Exception as ex:
            log_exception(Quarter._logger, 
                          'sws.get_current_term', 
                          traceback.format_exc())
        finally:
            log_resp_time(Quarter._logger, 
                          'sws.get_current_term',
                          timer)
        return None

    def get_current_summer_term(self):
        term = self.get_cur_quarter()
        if datetime.now().date() > term.aterm_last_date:
            return "B-term"
        else:
            return "A-term"

    def get_next_quarter(self):
        """
        Returns calendar information for the next term.
        """
        timer = Timer()
        try:
            return SWS().get_next_term()
        except Exception as ex:
            log_exception(Quarter._logger, 
                          'sws.get_next_term', 
                          traceback.format_exc())
        finally:
            log_resp_time(Quarter._logger, 
                          'sws.get_next_term',
                          timer)
        return None

    def get_term(self, year, quarter):
        """
        Returns term object by year and quarterfor
        """
        logid = ('sws.get_term_by_year_and_quarter ' + 
                 str(year) + "," + quarter);
        timer = Timer()
        try:
            return SWS().get_term_by_year_and_quarter(year, quarter)
        except Exception as ex:
            log_exception(Quarter._logger, 
                          logid,
                          traceback.format_exc())
        finally:
            log_resp_time(Quarter._logger, 
                          logid,
                          timer)
        return None

    def get_next_autumn_quarter(self):
        """
        This function is to get the autumn quarter when in the Spring quarter
        Returns term information for the next autumn term in the same year.
        """
        return self.get_term(self.get_cur_quarter().year, 'autumn')


class Schedule:
    TOTAL_COURSE_COLORS = 8
    """
    This class encapsulates the access of the registration
    and section resources
    """

    _logger = logging.getLogger('myuw_mobile.dao.sws.Schedule')

    def get_regid(self):
        return Person().get_regid()

    def get_schedule(self, term):
        """ 
        Return the actively enrolled sections in the given term/quarter 
        """
        regid = self.get_regid()
        if regid is None or term is None:
            return None
        logid = ('sws.schedule_for_regid_and_term ' + 
                 str(regid) + ',' + str(term.year) + ',' + term.quarter)

        timer = Timer()
        try:
            return SWS().schedule_for_regid_and_term(regid, term)
        except DataFailureException as ex:
            log_exception(Schedule._logger,
                          logid,
                          traceback.format_exc())
            empty = ClassSchedule()
            empty.term = term
            empty.sections = []
            return empty
        except Exception as ex:
            log_exception(Schedule._logger,
                          logid,
                          traceback.format_exc())
        finally:
            log_resp_time(Schedule._logger,
                          logid,
                          timer)
        return None


    def get_cur_quarter_schedule(self):
        """
        Return the actively enrolled sections in the current quarter 
        """
        return self.get_schedule(Quarter().get_cur_quarter())

    def get_next_quarter_schedule(self):
        """ 
        Return the actively enrolled sections in the next quarter 
        """
        return self.get_schedule(Quarter().get_next_quarter())

    def get_next_autumn_quarter_schedule(self):
        """
        Return the actively enrolled sections in the next autumn quarter 
        """
        return self.get_schedule(Quarter().get_next_autumn_quarter())

    def get_registered_summer_terms(self, registered_summer_sections):
        """
        Return summer registered terms
        """
        data = {
            "full_term" : None,
            "A_term" : None,
            "B_term" : None,
            }
        for section in registered_summer_sections:
            if section.summer_term == "Full-term":
                data["Full_term"] = True
            elif section.summer_term == "A-term":
                data["A_term"] = True
            elif section.summer_term == "B-term":
                data["B_term"] = True
            else:
                pass
        return data

    def _get_future_term_json(self, term, summer_term):
        res_json = term.json_data()
        res_json["summer_term"] = summer_term
        url = "/" + str(term.year) + "," + term.quarter
        if summer_term:
            url = url + "," + summer_term.lower()
        res_json["url"] = url
        return res_json


    def get_registered_future_quarters(self):
        """ 
        Return the list of future quarters that 
        has actively enrolled sections
        """
        terms = []
        next_quar_sche = self.get_next_quarter_schedule()
        next_quarter = next_quar_sche.term
        if next_quar_sche is not None and len(next_quar_sche.sections) > 0:

            if next_quarter.quarter == "summer":
                sumr_tms = self.get_registered_summer_terms(next_quar_sche.sections)

                if sumr_tms["A_term"] and sumr_tms["B_term"] and sumr_tms["Full_term"] or sumr_tms["A_term"] and sumr_tms["Full_term"] or sumr_tms["B_term"] and sumr_tms["Full_term"] or sumr_tms["A_term"] and sumr_tms["B_term"]:

                    if sumr_tms["A_term"]:
                        terms.append(self._get_future_term_json(next_quarter,
                                                                "A-Term"))

                    if sumr_tms["Full_term"] and not sumr_tms["A_term"]:
                        terms.append(self._get_future_term_json(next_quarter,
                                                                "A-Term"))

                    if sumr_tms["B_term"]:
                        terms.append(self._get_future_term_json(next_quarter,
                                                                "B-Term"))

                    if sumr_tms["Full_term"] and not sumr_tms["B_term"]:
                        terms.append(self._get_future_term_json(next_quarter,
                                                                "B-Term"))
            else:
                terms.append(self._get_future_term_json(next_quarter,""))

        if next_quarter.quarter == 'summer':
            next_autumn_quar_sche = self.get_next_autumn_quarter_schedule()
            if next_autumn_quar_sche is not None and len(next_autumn_quar_sche.sections) > 0:
                terms.append(self._get_future_term_json(next_autumn_quar_sche.term,
                                                        ""))
        return terms

    def get_cur_quarter_campuses(self):
        """
        Returns a dictionary indicating the campuses that the student
        has enrolled in the current quarter:
         { seattle: false|true, 
           bothell: false|true,
           tacoma: false|true } 
        True if the user is registered on that campus in the current quarter
        """
        campuses = {"seattle": False,
                    "bothell": False,
                    "tacoma": False}

        schedule = self.get_cur_quarter_schedule()
        if schedule is not None and len(schedule.sections) > 0:
            for section in schedule.sections:
                if section.course_campus == "Seattle":
                    campuses["seattle"]=True
                elif section.course_campus == "Bothell":
                    campuses["bothell"]=True
                elif section.course_campus == "Tacoma":
                    campuses["tacoma"]=True
                else:
                    pass
        return campuses


    def get_buildings_for_schedule(self, schedule):
        if schedule is None or len(schedule.sections) == 0:
            return None
        buildings = {}
        building_dao = Building()
        for section in schedule.sections:
            if section.final_exam and section.final_exam.building:
                code = section.final_exam.building
                if not code in buildings:
                    building = building_dao.get_building_from_code(code)
                    buildings[code] = building
            for meeting in section.meetings:
                if not meeting.building_to_be_arranged:
                    if not meeting.building in buildings:
                        code = meeting.building
                        building = building_dao.get_building_from_code(code)
                        buildings[code] = building

        return buildings


    def get_colors_for_schedule(self, schedule):
        if schedule is None or len(schedule.sections) == 0:
            return None
        colors = {}
        regid = Person().get_regid()
        timer = Timer()
        try:
            query = CourseColor.objects.filter(
                regid=regid,
                year=schedule.term.year,
                quarter=schedule.term.quarter,
                )
        except Exception as ex:
            log_exception(Schedule._logger, 
                          'query CourseColor',
                          traceback.format_exc())
            return None
        finally:
            log_resp_time(Schedule._logger, 
                          'query CourseColor',
                          timer)

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
                                                    regid,
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

    def _get_color_for_section(self, existing, active, schedule, section, regid):
        color = CourseColor()
        color.regid = regid
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


