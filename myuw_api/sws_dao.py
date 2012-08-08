from django.conf import settings
import datetime
from restclients.sws_client import SWSClient
import logging
import json

##############################
# SWS data access object layer
##############################

# meant to be private statis...
#sws_client = SWSClient()

class InvalidTermData(RuntimeError):
    def __init__(self, arg):
        self.args = arg

class Quarter:
    """ This class encapsulate the access of the term data """
    _logger = logging.getLogger('myuw_api.sws_dao.Quarter')

    def get_cur_quarter(self):
        return  self.mock()
#        self.sws_result = sws_client.get_current_term()
#        return self.flter_data()

    def mock(self):
        return {'year': '2012',
                'quarter': 'Summer',
                'first_day_quarter': datetime.date(2012, 6, 18),
                'last_day_instruction': datetime.date(2012, 8, 10),
                'aterm_last_date': datetime.date(2012, 7, 18),
                'bterm_first_date': datetime.date(2012, 6, 19),
                'last_final_exam_date': datetime.date(2012, 8, 17)
                }

    def filter_data(self):
        pass

class Schedule:
    """ The Schedule class encapsulates the access of the class schedule """

    _logger = logging.getLogger('myuw_api.sws_dao.Schedule')
 
    def __init__(self, regid):
        self.regid = regid
        
    def get_curr_quarter_schedule(self):
        return self.mock()
#        self.sws_result = sws_client.get_current_term()
#        return self.filter_data()

    def filter_data(self):
        pass

    def mock(self):
        return {'year': '2012',
                'quarter': 'Summer',
                'sections':[
                {'curriculum_abbr': 'DRAMA',
                 'course_number': '490',
                 'section_id': 'A',
                 'course_title': 'Spec Stdy Act-Direct',
                 'course_campus': 'Seattle',
                 'class_website_url': 'http://courses.washington.edu/drama490',
                 'sln': '11000',
                 'summer_term': ' ',
                 'start_date': '',
                 'end_date': '',
                 'meetings': [{'index': '1',
                              'type': 'ST',
                              'days': 'TTh',
                              'start_time': '110',
                              'end_time': '320',
                              'building': 'HUT',
                              'room': '303',
                              'instructor': 
                               {'name': 'HAFSO, SCOTT',
                                'email': 'shafso@u.washington.edu',
                                'phone': '206 543-3076'}
                              }]
                }]}


     


