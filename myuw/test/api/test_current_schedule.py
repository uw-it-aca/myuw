# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.views.api.base_schedule import irregular_start_end
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
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEqual(data["term"]["year"], 2013)
        self.assertEqual(data["term"]["quarter"], 'Spring')
        self.assertEqual(len(data["sections"]), 5)
        phys = self.get_section(data, 'PHYS', '121', 'A')

        self.assertEqual(
            phys['canvas_url'],
            'https://canvas.uw.edu/courses/249652')
        self.assertEqual(
            phys['lib_subj_guide'],
            'http://guides.lib.uw.edu/friendly.php' +
            '?s=research/physics_astronomy'
        )

    def test_none_current_term(self):
        response = self.get_current_schedule_res('none')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b'Data not found')

    def test_canvas_url(self):
        response = self.get_current_schedule_res('eight')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEqual(data["term"]["year"], 2013)
        self.assertEqual(data["term"]["quarter"], 'Spring')
        self.assertEqual(len(data["sections"]), 8)

        arctic = self.get_section(data, 'ARCTIC', '200', 'A')
        self.assertEqual(arctic['lib_subj_guide'],
                         'http://guides.lib.uw.edu/tacoma/art')

        phys121a = self.get_section(data, 'PHYS', '121', 'A')
        self.assertEqual(phys121a['canvas_url'],
                         'https://test.edu/courses/249652')

        phys121ac = self.get_section(data, 'PHYS', '121', 'AC')
        self.assertEqual(phys121ac['canvas_url'],
                         'https://test.edu/courses/249652')

        response = self.get_current_schedule_res('jpce')
        data = json.loads(response.content)
        self.assertEqual(len(data["sections"]), 5)
        for sec_data in data["sections"]:
            self.assertNotIn('canvas_url', sec_data)

    def test_jbothell_current_term(self):
        response = self.get_current_schedule_res('jbothell')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEqual(data["term"]["year"], 2013)
        self.assertEqual(data["term"]["quarter"], 'Spring')

        bcwrit = self.get_section(data, 'BCWRIT', '500', 'A')
        self.assertEqual(bcwrit['lib_subj_guide'],
                         'http://guides.lib.uw.edu/bothell/')
        bisseb = self.get_section(data, 'BISSEB', '259', 'A')
        self.assertEqual(
            bisseb['lib_subj_guide'],
            'http://guides.lib.uw.edu/bothell/businternational')

    def test_missing_current_term(self):
        response = self.get_current_schedule_res('jerror')
        self.assertEqual(response.status_code, 543)

    def test_summer_terms(self):
        response = self.get_current_schedule_res('javerage',
                                                 '2013-07-06 00:00:01')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEqual(data["term"]["year"], 2013)
        self.assertEqual(data["term"]["quarter"], 'Summer')
        self.assertEqual(data["summer_term"], "a-term")

        response = self.get_current_schedule_res('javerage',
                                                 '2013-07-25 00:00:01')
        data = json.loads(response.content)
        self.assertEqual(data["summer_term"], "b-term")

    def test_javerage_efs_section(self):
        response = self.get_current_schedule_res('javerage',
                                                 '2013-09-17 00:00:01')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        efs_ok = self.get_section(data, 'EFS_OK', '101', 'AQ')
        self.assertEqual(efs_ok['start_date'],
                         '2013-08-24')
        self.assertEqual(efs_ok['end_date'],
                         '2013-09-18')
        self.assertFalse(efs_ok["is_ended"])

    def test_javerage_efs_section_ended(self):
        response = self.get_current_schedule_res('javerage',
                                                 '2013-09-19 00:00:01')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        efs_ok = self.get_section(data, 'EFS_OK', '101', 'AQ')
        self.assertEqual(efs_ok['start_date'],
                         '2013-08-24')
        self.assertEqual(efs_ok['end_date'],
                         '2013-09-18')
        self.assertTrue(efs_ok["cc_display_dates"])
        self.assertTrue(efs_ok["is_ended"])

    def test_off_term_pce_course_schedule(self):
        response = self.get_current_schedule_res('jpce',
                                                 '2013-01-17 00:00:01')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        com = self.get_section(data, 'COM', '201', 'A')
        self.assertEqual(com['start_date'], '2013-01-30')
        self.assertEqual(com['end_date'], '2013-04-29')
        self.assertFalse(com["is_ended"])
        psych = self.get_section(data, 'PSYCH', '203', 'A')
        self.assertEqual(psych['start_date'], '2013-01-29')
        self.assertEqual(psych['end_date'], '2013-07-30')
        self.assertFalse(psych["is_ended"])

        response = self.get_current_schedule_res('jpce',
                                                 '2013-06-08 00:00:01')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        section = self.get_section(data, 'AAES', '150', 'A')
        self.assertEqual(section['start_date'], '2013-04-03')
        self.assertEqual(section['end_date'], '2013-06-07')
        self.assertTrue(section["is_ended"])
        section = self.get_section(data, 'ACCTG', '508', 'A')
        self.assertEqual(section['start_date'], '2013-04-01')
        self.assertEqual(section['end_date'], '2013-06-19')
        self.assertFalse(section["is_ended"])
        section = self.get_section(data, 'CPROGRM', '712', 'A')
        self.assertEqual(section['start_date'], '2013-04-29')
        self.assertEqual(section['end_date'], '2013-06-28')
        self.assertFalse(section["is_ended"])

    def test_noncredit_cert_course_schedule(self):
        response = self.get_current_schedule_res('jeos',
                                                 '2013-01-17 00:00:01')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        section = self.get_section(data, 'BIGDATA', '220', 'A')
        self.assertEqual(section['start_date'], '2013-01-16')
        self.assertEqual(section['end_date'], '2013-03-20')
        self.assertEqual(section["section_type"], 'CLS')

        response = self.get_current_schedule_res('jeos',
                                                 '2013-04-01 00:00:01')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["has_eos_dates"])
        section = self.get_section(data, 'BIGDATA', '230', 'A')
        self.assertTrue(section["cc_display_dates"])
        self.assertFalse(section["on_standby"])
        self.assertTrue(section["has_eos_dates"])
        self.assertFalse(section["meetings"][0]["start_end_same"])
        self.assertTrue(section["meetings"][2]["start_end_same"])
        self.assertEqual(section['meetings'][0]['eos_start_date'],
                         '2013-04-03')
        self.assertEqual(section['meetings'][1]['eos_start_date'],
                         '2013-05-11')
        self.assertEqual(section['meetings'][2]['eos_start_date'],
                         '2013-05-29')

    def test_on_standby_status(self):
        response = self.get_current_schedule_res('jeos',
                                                 '2013-07-25 00:00:01')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        section = self.get_section(data, 'LIS', '498', 'C')
        self.assertTrue(section["cc_display_dates"])
        self.assertTrue(section["on_standby"])

        response = self.get_current_schedule_res('jeos',
                                                 '2013-10-25 00:00:01')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        section = self.get_section(data, 'MUSEUM', '700', 'A')
        self.assertFalse("cc_display_dates" in section)
        self.assertFalse(section["on_standby"])

    def test_non_student(self):
        response = self.get_current_schedule_res('staff',
                                                 '2013-4-25 00:00:01')
        self.assertEqual(response.status_code, 404)

    def test_invalid_user(self):
        response = self.get_response_by_reverse('myuw_current_schedule')
        self.assertEqual(response.status_code, 403)

    def test_remote_courese(self):
        # MUWM-5099
        response = self.get_current_schedule_res('eight',
                                                 '2020-10-01 00:00:01')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["term"]["year"], 2020)
        self.assertEqual(data["term"]["quarter"], 'Autumn')
        self.assertEqual(len(data["sections"]), 3)

        ee = self.get_section(data, 'E E', '233', 'A')
        self.assertTrue(ee["is_hybrid"])
        self.assertTrue(ee["meetings"][0]["is_hybrid"])

        chem = self.get_section(data, 'CHEM', '321', 'A')
        self.assertTrue(chem["is_hybrid"])
        self.assertTrue(chem["meetings"][0]["is_hybrid"])

        chem = self.get_section(data, 'CHEM', '321', 'AA')
        self.assertFalse(chem["is_hybrid"])
        self.assertFalse(chem["meetings"][0]["is_hybrid"])
