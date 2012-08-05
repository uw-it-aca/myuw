from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from models import Term
from restclients.sws_client import SWSClient
import logging
import urllib
import re
import json

class Quarter:
    __logger = logging.getLogger('quartermanager')
    __sws_client = SWSClient()
    __sws_url_base = ''

    def __init__(self):
        expiration = datetime.nowtimedelta(1)

    def get_cur_quarter(self):
        # see if we have local data
        try:
            self.local = Term.objects.get(
                first_day_quarter__lte=datetime.today(),
                last_final_exam_date__gte=datetime.today()
                )
        except ObjectDoesNotExist:
#            __mock()
            __refresh_cur_quarter()
        else:
            # if the cached date is older than a day, refresh it
            if (self.local.last_verified__lte=datetime.today()) :
                __refresh_cur_quarter()
        return self.local

    def get_next_quarter(self):
        pass

    def get_prev_quarter(self):
        pass

    def __refresh_cur_quarter(self):
        self.sws_result = __sws_client.get_current_term(__sws_url_base)
        __refresh_cache()

    def __refresh_next_quarter(self):
        self.sws_result = __sws_client.get_next_term(__sws_url_base)
        __refresh_cache()

    def __refresh_prev_quarter(self):
        self.sws_result = __sws_client.get_previous_term(__sws_url_base)
        __refresh_cache()

    def __refresh_cache(self):
        self.local = Term (
            year = self.sws_result.year,
            quarter = self.sws_result.quarter,
            first_day_quarter = self.sws_result.first_day,
            last_day_instruction = self.sws_result.last_day_of_classes, 
            aterm_last_date = self.sws_result.last_add_day_a_term,
            bterm_first_date = self.sws_result.b_term_first_day,
            last_final_exam_date = self.sws_result.last_final_exam_day,
            last_verified =  datetime.now()
            )
        self.local.save()

    def __mock(self):
        # mock data
        self.local = Term (
            year = '2012',
            quarter = '3',
            first_day_quarter = datetime.date(2012, 6, 18),
            last_day_instruction = datetime.date(2012, 8, 10),
            aterm_last_date = datetime.date(2012, 7, 18),
            bterm_first_date = datetime.date(2012, 6, 19),
            last_final_exam_date = datetime.date(2012, 8, 17),
            last_verified =  datetime.now()
            )
        self.local.save()

     

