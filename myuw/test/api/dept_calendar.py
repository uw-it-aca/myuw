from myuw.test.api import require_url, MyuwApiTest
import json


@require_url('myuw_deptcal_events')
class TestDeptCalAPI(MyuwApiTest):
    '''Test Department Calendar API'''

    def get_deptcal(self):
        rev = 'myuw_deptcal_events'
        return self.get_response_by_reverse(rev)

    def test_javerage_cal_apr15(self):
        '''Test javerage's deptcal on default date'''

        self.set_user('javerage')
        self.set_date('2013-4-15')
        response = self.get_deptcal()
        data = json.loads(response.content)

        self.assertEqual(len(data['future_active_cals']), 0)
        self.assertEqual(len(data['active_cals']), 2)
        events = data['events']
        self.assertEqual(len(events), 7)

        sorted_events = sorted(events, key=lambda x: x.get('summary'))

        event_two = sorted_events[2]
        self.assertEqual(event_two['event_location'], u'')
        self.assertEqual(
            event_two['summary'],
            'Organic Chemistry Seminar: Prof. Matthew Becker3')
        self.assertEqual(
            event_two['event_url'],
            'http://art.washington.edu/calendar/?trumbaEmbed=eventid%3D11074'
            '21160%26view%3Devent'
        )
        self.assertTrue(event_two['is_all_day'])
        self.assertEqual(event_two['start'], '2013-04-18T00:00:00-07:53')
        self.assertEqual(event_two['end'], '2013-04-18T00:00:00-07:53')

    def test_javerage_cal_feb15(self):
        '''Test javerage's deptcal on date with no events'''

        self.set_user('javerage')
        self.set_date('2013-2-15')
        response = self.get_deptcal()
        data = json.loads(response.content)

        self.assertEqual(
            data,
            {'future_active_cals': [], 'active_cals': [], 'events': []})

    def test_nonexistant_user(self):
        '''Test user with no deptcals'''

        self.set_user('nonexist')
        self.set_date('2013-4-15')
        response = self.get_deptcal()
        data = json.loads(response.content)

        self.assertEqual(
            data,
            {'future_active_cals': [], 'active_cals': [], 'events': []})
