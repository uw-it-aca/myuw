from django.conf import settings
import datetime
from restclients.sws import SWS
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
        counter = 1

        primary_sections = []
        secondary_sections = []
        for section in schedule.sections:
            if section.is_primary_section:
                primary_sections.append(section)
            else:
                secondary_sections.append(section)

        for section in primary_sections:
            label = section.section_label()
            colors[label] = counter
            counter += 1

        for section in secondary_sections:
            label = section.section_label()
            primary_label = section.primary_section_label()

            if colors[primary_label] == None:
                colors[primary_label] = counter
                counter += 1

            colors[label] = "%sa" % colors[primary_label]

        return colors
