from django.conf import settings
from datetime import datetime
import restclients.sws_client
import logging
import json

class Quarter:
    """ The Quarter class encapsulate the access to the Term data """

    __logger = logging.getLogger('myuw_api.quarter')
    __sws_client = SWSClient()

    class Term:
        pass

    def __init__(self):
        self.local = Term()

    def get_cur_quarter(self):
        __mock()
#        self.sws_result = __sws_client.get_current_term()
#        __filter_data()        
        return self.local

    def get_next_quarter(self):
        self.sws_result = __sws_client.get_next_term()
        __filter_data()
        return self.local

    def get_prev_quarter(self):
        self.sws_result = __sws_client.get_previous_term()
        __filter_data()
        return self.local

    def __filter_data(self):
        self.local.year = self.sws_result.year
        self.local.quarter = self.sws_result.quarter
        self.local.first_day_quarter = self.sws_result.first_day
        self.local.last_day_instruction = self.sws_result.last_day_of_classes
        self.local.aterm_last_date = self.sws_result.a_term_last_day
        self.local.bterm_first_date = self.sws_result.b_term_first_day
        self.local.last_final_exam_date = self.sws_result.last_final_exam_day

    def __mock(self):
        self.local.year = '2012'
        self.local.quarter = 'Summer'
        self.local.first_day_quarter = datetime.date(2012, 6, 18)
        self.local.last_day_instruction = datetime.date(2012, 8, 10)
        self.local.aterm_last_date = datetime.date(2012, 7, 18)
        self.local.bterm_first_date = datetime.date(2012, 6, 19)
        self.local.last_final_exam_date = datetime.date(2012, 8, 17)


     

