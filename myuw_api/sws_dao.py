from django.conf import settings
import datetime
from restclients.sws_client import SWSClient
from restclients.sws import SWS
import logging
import json

# This module provides the single point access to SWSClient
sws_client = SWSClient()

class Quarter:
    """ This class encapsulate the access of the term data """
    _logger = logging.getLogger('myuw_api.sws_dao.Quarter')

    def get_cur_quarter(self):
        """
        Returns calendar information for the current term.
        """
        sws = SWS()
        term = sws.get_current_term()

        return term


class Schedule:
    """
    This class encapsulates the access of the registration and section resources
    """

    _logger = logging.getLogger('myuw_api.sws_dao.Schedule')

    def __init__(self, regid):
        self.regid = regid

    def get_cur_quarter_registration(self):
        """ Return the actively enrolled sections in the current quarter """

        term = Quarter().get_cur_quarter()
        sws = SWS()

#        sections = sws.registration_for_regid_and_term(self.regid, term)

#        return sections
        return sws_client.registration_search({'year': term.year,
                                               'quarter': term.quarter,
                                               'reg_id': self.regid,
                                               'is_active': 'on'})

    def get_section(self, params={}):
        return sws_client.get_section(params)

    def get_curr_quarter_schedule(self):
        regi_rslt = self.get_cur_quarter_registration()
        if not regi_rslt:
            # not enrolled in the currrent quarter
            return None
        print regi_rslt
        #for section in regi_rslt['Section']:
        #    section_rslt = self.get_section(
        #        {'year': regi_rslt['Year'], 
        #         'quarter': regi_rslt['Quarter'],
        #         'curriculum_abbreviation': regi_rslt['CurriculumAbbreviation'],
        #         'course_number': regi_rslt['CourseNumber']})
        #    print section_rslt
        return self.mock()

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
                              }],
                },
                {'curriculum_abbr': 'CSE',
                 'course_number': '142',
                 'section_id': 'C',
                 'course_title': 'Intro to Copy Select Exhultation',
                 'course_campus': 'Seattle',
                 'class_website_url': 'http://courses.washington.edu/cse142',
                 'sln': '11004',
                 'summer_term': ' ',
                 'start_date': '', 
                 'end_date': '', 
                 'meetings': [{'index': '1',
                              'type': 'ST',
                              'days': 'TThF',
                              'start_time': '1030',
                              'end_time': '1120',
                              'building': 'MGH',
                              'room': '304',
                              'instructor': 
                               {'name': 'HALFSON, SCOTTLAND',
                                'email': 'shafso@u.washington.edu',
                                'phone': '206 543-3076'}
                              }], 
                }, 
                ]}



     


