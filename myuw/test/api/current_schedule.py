import json
from myuw.views.api.current_schedule import StudClasScheCurQuar
from myuw.test.api import MyuwApiTest, require_url, fdao_sws_override


@fdao_sws_override
@require_url('myuw_current_schedule')
class TestSchedule(MyuwApiTest):

    def get_current_schedule_res(self, user=None, date=None):
        if user:
            self.set_user(user)
        if date:
            self.set_date(date)
        return self.get_response_by_reverse('myuw_current_schedule')

    def test_javerage_current_term(self):

        response = self.get_current_schedule_res('javerage')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Spring')
        self.assertEquals(len(data["sections"]), 5)

        phys = self.get_section(data, 'PHYS', '121', 'A')

        self.assertEquals(phys['canvas_url'],
                          'https://canvas.uw.edu/courses/249652')
        self.assertEquals(
            phys['lib_subj_guide'],
            'http://guides.lib.uw.edu/friendly.php' +
            '?s=research/physics_astronomy'
        )

        train = self.get_section(data, 'TRAIN', '101', 'A')
        self.assertNotIn('canvas_url', train)

    def test_none_current_term(self):

        response = self.get_current_schedule_res('none')
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.content, 'Data not found')

    def test_eight_current_term(self):

        response = self.get_current_schedule_res('eight')
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Spring')
        self.assertEquals(len(data["sections"]), 8)

        arctic = self.get_section(data, 'ARCTIC', '200', 'A')
        self.assertEquals(arctic['lib_subj_guide'],
                          'http://guides.lib.uw.edu/tacoma/art')

    def test_jbothell_current_term(self):
        response = self.get_current_schedule_res('jbothell')
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Spring')

        bcwrit = self.get_section(data, 'BCWRIT', '500', 'A')
        self.assertEquals(bcwrit['lib_subj_guide'],
                          'http://guides.lib.uw.edu/bothell/')
        bisseb = self.get_section(data, 'BISSEB', '259', 'A')
        self.assertEquals(
            bisseb['lib_subj_guide'],
            'http://guides.lib.uw.edu/bothell/businternational')

    def test_missing_current_term(self):

        response = self.get_current_schedule_res('jerror')
        self.assertEquals(response.status_code, 543)

    def test_summer_terms(self):

        response = self.get_current_schedule_res('javerage',
                                                 '2013-07-06 00:00:01')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Summer')
        self.assertEquals(data["summer_term"], "a-term")

        response = self.get_current_schedule_res('javerage',
                                                 '2013-07-25 00:00:01')
        data = json.loads(response.content)
        self.assertEquals(data["summer_term"], "b-term")

    def get_section(self, data, abbr, number, section_id):
        for section in data['sections']:
            if section['curriculum_abbr'] == abbr and\
                    section['course_number'] == number and\
                    section['section_id'] == section_id:

                return section

        self.fail('Did not find course %s %s %s' % (abbr, number, section_id))

    def test_javerage_efs_section(self):
        response = self.get_current_schedule_res('javerage',
                                                 '2013-09-17 00:00:01')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)

        efs_ok = self.get_section(data, 'EFS_OK', '101', 'AQ')
        self.assertEquals(efs_ok['start_date'],
                          '2013-08-24')
        self.assertEquals(efs_ok['end_date'],
                          '2013-09-18')
        self.assertFalse(efs_ok["is_ended"])

    def test_javerage_efs_section_ended(self):
        response = self.get_current_schedule_res('javerage',
                                                 '2013-09-19 00:00:01')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        efs_ok = self.get_section(data, 'EFS_OK', '101', 'AQ')
        self.assertEquals(efs_ok['start_date'],
                          '2013-08-24')
        self.assertEquals(efs_ok['end_date'],
                          '2013-09-18')
        self.assertTrue(efs_ok["is_ended"])

    def test_jpce_schedule(self):
        response = self.get_current_schedule_res('jpce',
                                                 '2013-01-17 00:00:01')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        com = self.get_section(data, 'COM', '201', 'A')
        self.assertEquals(com['start_date'], '2013-01-30')
        self.assertEquals(com['end_date'], '2013-04-29')
        self.assertFalse(com["is_ended"])
        psych = self.get_section(data, 'PSYCH', '203', 'A')
        self.assertEquals(psych['start_date'], '2013-01-29')
        self.assertEquals(psych['end_date'], '2013-07-30')
        self.assertFalse(psych["is_ended"])

        response = self.get_current_schedule_res('jpce',
                                                 '2013-06-08 00:00:01')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        section = self.get_section(data, 'AAES', '150', 'A')
        self.assertEquals(section['start_date'], '2013-04-03')
        self.assertEquals(section['end_date'], '2013-06-07')
        self.assertTrue(section["is_ended"])
        section = self.get_section(data, 'ACCTG', '508', 'A')
        self.assertEquals(section['start_date'], '2013-04-01')
        self.assertEquals(section['end_date'], '2013-06-19')
        self.assertFalse(section["is_ended"])
        section = self.get_section(data, 'CPROGRM', '712', 'A')
        self.assertEquals(section['start_date'], '2013-04-29')
        self.assertEquals(section['end_date'], '2013-06-28')
        self.assertFalse(section["is_ended"])

    def test_noncredit_cert_student_schedule(self):
        response = self.get_current_schedule_res('jeos',
                                                 '2013-01-17 00:00:01')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        section = self.get_section(data, 'BIGDATA', '220', 'A')
        self.assertEquals(section['start_date'], '2013-01-16')
        self.assertEquals(section['end_date'], '2013-03-20')
        response = self.get_current_schedule_res('jeos',
                                                 '2013-04-01 00:00:01')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        section = self.get_section(data, 'BIGDATA', '230', 'A')
        self.assertEquals(section['start_date'], '2013-04-03')
        self.assertEquals(section['end_date'], '2013-06-12')
