from django.conf import settings
import traceback
import logging
import sys
from restclients.gws import GWS
from myuw_mobile.dao.sws import Schedule
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception
from myuw_mobile.user import UserService

class Member:
    """
    The Member class encapsulates the interactions
    with the UW Affiliation Group API resource
    """

    # static class variables
    _logger = logging.getLogger('myuw_mobile.dao.gws.Member')

    def __init__(self):
        self.schedule = Schedule().get_cur_quarter_schedule()

    def _is_member(self, groupid):
        """
        Return True if the current user netid is 
        an effective member of the given group
        """
        timer = Timer()
        try:
            netid = UserService().get_user()
            return GWS().is_effective_member(groupid, netid)
        except Exception, message:
            traceback.print_exc(file=sys.stdout)
            log_exception(Member._logger, 
                          'gws.is_effective_member of ' + groupid,
                          message)
        finally:
            log_resp_time(Member._logger,
                          'gws.is_effective_member of ' + groupid,
                          timer)
        return None

    def is_seattle_student(self):
        """
        Return True if the user is an UW Seattle student
        in the current quarter
        Note:
        As uw_affiliation only maintains one affiliation from SDB
        we get campus information from the registered sections
        """
        if self.schedule and len(self.schedule.sections) > 0:
            for section in self.schedule.sections:
                if section.course_campus == 'Seattle':
                    return True
        return False

    def is_bothell_student(self):
        """
        Return True if the user is an UW Bothell student
        in the current quarter
        Note:
        As uw_affiliation only maintains one affiliation from SDB
        we get campus information from the registered sections
        """
        if self.schedule and len(self.schedule.sections) > 0:
            for section in self.schedule.sections:
                if section.course_campus == 'Bothell':
                    return True
        return False

    def is_tacoma_student(self):
        """
        Return True if the user is an UW Tacoma student
        in the current quarter
        Note:
        As uw_affiliation only maintains one affiliation from SDB
        we get campus information from the registered sections
        """
        if self.schedule and len(self.schedule.sections) > 0:
            for section in self.schedule.sections:
                if section.course_campus == 'Tacoma':
                    return True
        return False

    def is_current_grad_student(self):
        """
        Return True if the user is an UW graduate student
        in the current quarter
        """
        return self._is_member('uw_affiliation_graduate-current')

    def is_grad_student(self):
        """
        Return True if the user is an UW graduate student 
        in the current, previous, or future quarter
        """
        return self._is_member('uw_affiliation_graduate')

    def is_undergrad_student(self):
        """
        Return True if the user is an UW undergraduate student 
        in the current, previous, or future quarter
        """
        return self._is_member('uw_affiliation_undergraduate')

    def is_pce_student(self):
        """
        Return True if the user is an UW PEC student 
        in the current, previous, or future quarter
        """
        return self._is_member('uw_affiliation_extension-student')

    def is_student_employee(self):
        """
        Return True if the user is an UW student employee (valid in 15 days) 
        """
        return self._is_member('uw_affiliation_student-employee')

# The is_student function is in pws.py

