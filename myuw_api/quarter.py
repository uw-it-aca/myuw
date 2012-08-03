from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from models import Term
from restclients.sws_client import SWSClient
import logging
import urllib
import re
import json

# quarter class definition

class Quarter:
    __logger = logging.getLogger('quartermanager')
    __sws_client = SWSClient()

    def __init__(self):
        pass

    def get_cur_quarter(self):
        # see if we have local data
        try:
            self.local = Term.objects.get(
                first_day_quarter__lte=datetime.today(),
                last_final_exam_date__gte=datetime.today()
                )
        except ObjectDoesNotExist:
            __mock()
        return self.local

    def get_next_quarter(self):
        pass

    def get_cur_quarter_from_sws(self):
        url = '...'; # mock SWS URL base
        self.sws_result = __sws_client.get_current_term(url)
        
    def get_next_quarter_from_sws(self):
        url = '...'
        self.sws_result = __sws_client.get_next_term(url)
        
    def get_prev_quarter_from_sws(self):
        url = '...'
        self.sws_result = __sws_client.get_previous_term(url)

    def refresh_sws(self):
        get_cur_quarter_from_sws()
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
        __save()

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
        __save()

    def __save(self):
        self.local.save()
     

