"""
The interface for interacting with the MyUW HFS api
"""
import json
import logging
import re
from datetime import datetime
from restclients.exceptions import DataFailureException
from myuw_mobile.models import StudentAccountsBalances as Cache
from myuw_mobile.restclients.dao import Hfs_DAO
from myuw_mobile.logger.logback import log_info

class HfsAccounts(object):
    """
    Currently return the husky and dining balances for the user
    """
    _logger = logging.getLogger('myuw_mobile.restclients.hfs_account.HfsAccounts')

    _most_recent_update_datetime = datetime(2012,11,1,1,1)

    def set_recent_update_time(self, a_datetime):
        if a_datetime > HfsAccounts._most_recent_update_datetime:
            HfsAccounts._most_recent_update_datetime = a_datetime

    def get_balances(self, student_number):
        """
        Returns a dictionary of husky card and dining balances.
        'husky' or 'dining' are the keys, decimal number the value.
        """
        if not re.match(r'^[0-9]{7,10}$', student_number):
            raise InvalidStudentNumber(student_number)

        url = "/servlet/hfservices?sn=%s" % (student_number)

        dao = Hfs_DAO()
        response = dao.getURL(url, {"Accept": "text/html"})

        log_info(HfsAccounts._logger, 
                 'Url=%s Status=%d RespData=%s' % 
                 (url, response.status, response.data))

        if response.status == 404:
            return None

        if response.status != 200:
            raise DataFailureException(url, 
                                       response.status, 
                                       response.data)

        return self._update_cache(student_number, response.data)

    def _update_cache(self, student_number, data):
        cache = Cache()
        cache.student_number = student_number

        #"11/06/2012 at 6:40 a.m."
        timespec = re.search(
            '([0-9]{1,2})/([0-9]{1,2})/([1-9][0-9]{3}) at ([0-9]{1,2}):([0-9]{1,2}) ([ap]\.m)\.',
            data, re.I)
        if timespec:
            cache.asof_datetime = datetime(int(timespec.group(3)), #year
                                           int(timespec.group(1)), #month
                                           int(timespec.group(2)), #day
                                           int(timespec.group(4)), #hour,
                                           int(timespec.group(5))) #minute
            self.set_recent_update_time(cache.asof_datetime)
            if re.match('p\.m', timespec.group(6), re.I):
                cache.is_am = False
                # rare case
        else:
            cache.asof_datetime = HfsAccounts._most_recent_update_datetime

        husky_card_bal = re.search(
            '(?<=Husky Card Account balance was \$)([.0-9]+)',
            data)
        if husky_card_bal:
            cache.husky_card = float(husky_card_bal.group(0))

        dining_bal = re.search(
            '(?<=Residence Hall Dining Plan balance was \$)([.0-9]+)',
            data)
        if dining_bal:
            cache.residence_hall_dining = float(dining_bal.group(0))

        return cache


def test():
    accounts = HfsAccounts()
    balances = accounts.get_balances('1033334')
    print balances.json_data()
    balances = accounts.get_balances('0000000')
    print balances.json_data()

