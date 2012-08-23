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
