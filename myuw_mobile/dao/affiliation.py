import logging
from myuw_mobile.logger.logback import log_info
from myuw_mobile.dao.sws import Schedule
from myuw_mobile.dao.gws import Member

class Affiliation:
    """
    This class encapsulate the access of the term data
    """
    _logger = logging.getLogger('myuw_mobile.dao.affiliation.Affiliation')

    def __init__(self):
        self.enrolled_campuses = Schedule().get_cur_quarter_campuses()
        self.member = Member()

    def get_all(self):
        """
        return a dictionary of affiliations
        """
        data = {"grad": self.member.is_grad_student(),
                "undergrad": self.member.is_undergrad_student(),
                "pce": self.member.is_pce_student(),
                "stud_employee": self.member.is_student_employee(),
                "seattle": self._is_seattle_student(),
                "bothell": self._is_bothell_student(), 
                "tacoma": self._is_tacoma_student()
                }
        log_info(Affiliation._logger, data)
        return data

    def _is_seattle_student(self):
        """
        Return True if the user is an UW Seattle student
        in the current quarter
        Note:
        As the UW Affiliation group only knows about one campus,
        we also use registered sections in the current quarter
        to determine the campuses.
        """
        return self.member.is_seattle_student() or self.enrolled_campuses["seattle"]

    def _is_bothell_student(self):
        """
        Return True if the user is an UW Bothell student
        in the current quarter
        Note:
        As the UW Affiliation group only knows about one campus,
        we also use registered sections in the current quarter
        to determine the campuses.
        """
        return self.member.is_bothell_student() or self.enrolled_campuses["bothell"]

    def _is_tacoma_student(self):
        """
        Return True if the user is an UW Tacoma student
        in the current quarter
        Note:
        As the UW Affiliation group only knows about one campus,
        we also use registered sections in the current quarter
        to determine the campuses.
        """
        return self.member.is_tacoma_student() or self.enrolled_campuses["tacoma"]
