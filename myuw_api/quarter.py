from django.conf import settings
from datetime import datetime
from restclients.sws_client import SWSClient
import logging
import json

class Quarter:
    """ The Quarter class encapsulate the access to the Term data """

    __logger = logging.getLogger('myuw_api.quarter')
    __sws_client = SWSClient()

    def get_cur_quarter(self):
        return __mock()
#        self.sws_result = __sws_client.get_current_term()
#        return __filter_data()


    def get_next_quarter(self):
        self.sws_result = __sws_client.get_next_term()
        return __filter_data()

    def get_prev_quarter(self):
        self.sws_result = __sws_client.get_previous_term()
        return __filter_data()

    def __filter_data(self):
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


     

