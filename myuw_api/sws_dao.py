from django.conf import settings
from datetime import datetime
from restclients.sws_client import SWSClient
import logging
import json

sws_client = SWSClient()

class Quarter:
    """ The Quarter class encapsulate the access to the Term data """
    __logger = logging.getLogger('myuw_api.quarter')

    def get_cur_quarter(self):
        assert False, __mock()
        return __mock()
#        self.sws_result = sws_client.get_current_term()
#        return __filter_data()


    def get_next_quarter(self):
        self.sws_result = sws_client.get_next_term()
        return __filter_data()

    def get_prev_quarter(self):
        self.sws_result = sws_client.get_previous_term()
        return __filter_data()

    def __filter_data(self):
        # to do: validate the data attributes
        # raise InvalidTermData exception if failed
        return {'year': self.sws_result.year,
                'quarter': self.sws_result.quarter,
                'first_day_quarter': self.sws_result.first_day,
                'last_day_instruction': self.sws_result.last_day_of_classes,
                'aterm_last_date': self.sws_result.a_term_last_day,
                'bterm_first_date': self.sws_result.b_term_first_day,
                'last_final_exam_date': self.sws_result.last_final_exam_day
                }

    def __mock(self):
        return {'year': '2012',
                'quarter': 'Summer',
                'first_day_quarter': datetime.date(2012, 6, 18),
                'last_day_instruction': datetime.date(2012, 8, 10),
                'aterm_last_date': datetime.date(2012, 7, 18),
                'bterm_first_date': datetime.date(2012, 6, 19),
                'last_final_exam_date': datetime.date(2012, 8, 17)
                }


class InvalidTermData(RuntimeError):
    def __init__(self, arg):
        self.args = arg

     
class Schedule:
    """ The Schedule class encapsulates the access to the Schedule data """

    __logger = logging.getLogger('myuw_api.schedule')
 
    def __init__(self, regid):
        self.regid = regid
        
    def get_curr_quarter_schedule(self):
        return __mock()
#        self.sws_result = sws_client.get_current_term()
#        return __filter_data()


    def get_next_quarter_schedule(self):
        self.sws_result = sws_client.get_next_term()
        return __filter_data()

    def get_prev_quarter_schedule(self):
        self.sws_result = sws_client.get_previous_term()
        return __filter_data()

    def __filter_data(self):
        return {'year': self.sws_result.year,
                'quarter': self.sws_result.quarter,
                }

    def __mock(self):
        return {'year': '2012',
                'quarter': 'Summer',
                }


     


