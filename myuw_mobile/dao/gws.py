from django.conf import settings
import traceback
import logging
import sys
from restclients.gws import GWS
from myuw_mobile.user import UserService
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.util import log_resp_time, log_exception

class EffectiveMember:
    """
    The Member class encapsulates the interactions
    with the UW Affiliation Group API resource
    """

    # static class variables
    _logger = logging.getLogger('myuw_mobile.dao.gws.EffectiveMember')

    def _is_member(self, groupid):
        """
        return True if the current user netid is an effective member of the given group
        """
        timer = Timer()
        try:
            netid = UserService().get_user()
            return GWS().is_effective_member(groupid, netid)
        except Exception, message:
            traceback.print_exc()
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
        return True if the user is an UW current Seattle student
        """
        return self._is_member('uw_affiliation_seattle-student')

    def is_bothell_student(self):
        """
        return True if the user is an UW current Bothell student
        """
        return self._is_member('uw_affiliation_bothell-student')

    def is_tacoma_student(self):
        """
        return True if the user is an UW current graduate student
        """
        return self._is_member('uw_affiliation_tacoma-student')

    def is_current_grad_student(self):
        """
        return True if the user is an UW current graduate student
        """
        return self._is_member('uw_affiliation_graduate-current')

    def is_grad_student(self):
        """
        return True if the user is an UW graduate student 
        in the current, past, future quarter
        """
        return self._is_member('uw_affiliation_graduate')

    def is_undergrad_student(self):
        """
        return True if the user is an UW undergraduate student 
        in the current, past, future quarter
        """
        return self._is_member('uw_affiliation_undergraduate')

    def is_pce_student(self):
        """
        return True if the user is an UW PEC student 
        in the current, past, future quarter
        """
        return self._is_member('uw_affiliation_extension-student')

    def is_student(self):
        """
        return True if the user is an UW student 
        regardless graduate, undergraduate, or PCE 
        in the current, past, future quarter
        """
        return self.is_grad_student() or self.is_undergrad_student() or self.is_pce_student()

    def is_student_employee(self):
        """
        return True if the user is an UW student employee (valid in 15 days) 
        """
        return self._is_member('uw_affiliation_student-employee')

