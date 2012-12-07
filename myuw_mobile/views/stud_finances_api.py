from django.http import HttpResponse
from django.utils import simplejson as json
import logging
from rest_dispatch import RESTDispatch, data_not_found
from myuw_mobile.dao.student_finances import Accounts
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response, log_success_response

class AccountBalances(RESTDispatch):
    """
    Performs actions on resource at /api/v1/finabala/.
    """

    def GET(self, request):
        """ 
        GET returns 200 with the student account balances 
        of the current user
        """

        timer = Timer()
        logger = logging.getLogger('myuw_mobile.views.stud_finances_api.AccountBalances.GET')

        balances = Accounts().get_balances()
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(balances.json_data()))

