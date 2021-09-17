# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TransactionTestCase
from myuw.dao.affiliation import get_all_affiliations, get_is_hxt_viewer
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request, get_request_with_user


@fdao_pws_override
@fdao_sws_override
class TestAffilliationDao(TransactionTestCase):
    def setUp(self):
        get_request()

    """
    MUWM-4830
    def test_fyp(self):
        now_request = get_request_with_user('jnew')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations['fyp'])
        self.assertFalse(affiliations['aut_transfer'])
        self.assertFalse(affiliations['win_transfer'])

    def test_aut_transfer(self):
        now_request = get_request_with_user('javg001')
        affiliations = get_all_affiliations(now_request)
        self.assertFalse(affiliations['fyp'])
        self.assertTrue(affiliations['aut_transfer'])
        self.assertFalse(affiliations['win_transfer'])

    def test_win_transfer(self):
        now_request = get_request_with_user('javg002')
        affiliations = get_all_affiliations(now_request)
        self.assertFalse(affiliations['fyp'])
        self.assertFalse(affiliations['aut_transfer'])
        self.assertTrue(affiliations['win_transfer'])
    """

    def test_get_is_hxt_viewer(self):
        request = get_request_with_user('staff')
        self.assertTrue(get_is_hxt_viewer(request)[2])
        request = get_request_with_user('javg001')
        self.assertTrue(get_is_hxt_viewer(request)[2])
        request = get_request_with_user('jbothell')
        self.assertFalse(get_is_hxt_viewer(request)[2])
        request = get_request_with_user('seagrad')
        self.assertFalse(get_is_hxt_viewer(request)[2])

    def test_is_instructor(self):
        now_request = get_request_with_user('bill')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations['instructor'])
        self.assertTrue(affiliations['clinician'])
        self.assertTrue(affiliations['employee'])
        self.assertTrue(affiliations['all_employee'])

    def test_is_faculty(self):
        now_request = get_request_with_user('billtac')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations['faculty'])
        self.assertTrue(affiliations.get("official_tacoma"))

    def test_is_alumni(self):
        now_request = get_request_with_user('jalum')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations["alumni"])
        self.assertTrue(affiliations["no_1st_class_affi"])
        self.assertTrue(affiliations["past_stud"])
        self.assertTrue(affiliations["past_employee"])
        self.assertTrue(affiliations["alum_asso"])
        self.assertFalse(affiliations["registered_stud"])

    def test_is_retiree(self):
        now_request = get_request_with_user('retirestaff')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations["retiree"])
        self.assertTrue(affiliations["past_stud"])
        self.assertTrue(affiliations["no_1st_class_affi"])

    def test_is_pce_stud(self):
        now_request = get_request_with_user('jpce')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get('pce'))
        self.assertTrue(affiliations.get('undergrad_c2'))
        self.assertFalse(affiliations.get('grad_c2'))
        self.assertTrue(affiliations.get("undergrad"))
        self.assertTrue(affiliations.get("student"))
        self.assertTrue(affiliations.get("seattle"))
        self.assertFalse(affiliations.get("official_pce"))
        self.assertTrue(affiliations.get('J1'))
        self.assertTrue(affiliations.get("intl_stud"))

    def test_jinter(self):
        now_request = get_request_with_user('jinter')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get('F1'))
        self.assertTrue(affiliations.get("intl_stud"))
        self.assertTrue(affiliations.get('pce'))
        self.assertFalse(affiliations.get('undergrad_c2'))
        self.assertTrue(affiliations.get('grad_c2'))
        self.assertFalse(affiliations.get("hxt_viewer"))

    def test_error_case(self):
        now_request = get_request_with_user('jerror')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get('student'))
        self.assertFalse(affiliations.get('intl_stud'))
        self.assertTrue(affiliations.get('instructor'))

    def test_is_2fa_permitted(self):
        now_request = get_request_with_user('javerage')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get('2fa_permitted'))
        self.assertFalse(affiliations.get('F1'))
        self.assertFalse(affiliations.get("intl_stud"))

    def test_student_campus(self):
        now_request = get_request_with_user('javerage')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get("seattle"))
        self.assertTrue(affiliations.get("undergrad"))
        self.assertTrue(affiliations.get("registered_stud"))
        self.assertTrue(affiliations.get("hxt_viewer"))

        now_request = get_request_with_user('jbothell')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get("bothell"))
        self.assertFalse(affiliations.get("hxt_viewer"))

        now_request = get_request_with_user('eight')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get("tacoma"))
        self.assertFalse(affiliations.get("hxt_viewer"))
        self.assertFalse(affiliations.get("employee"))
        self.assertTrue(affiliations.get("all_employee"))

    def test_is_grad_stud_employee(self):
        now_request = get_request_with_user('billseata')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get("grad"))
        self.assertTrue(affiliations.get("student"))
        self.assertTrue(affiliations.get("seattle"))
        self.assertTrue(affiliations.get("instructor"))
        self.assertTrue(affiliations.get("stud_employee"))
        self.assertTrue(affiliations.get("all_employee"))
        self.assertTrue(affiliations.get("seattle"))
        self.assertTrue(affiliations.get("official_seattle"))
        self.assertFalse(affiliations.get("hxt_viewer"))

    def test_botgrad(self):
        now_request = get_request_with_user('botgrad')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get("grad"))
        self.assertTrue(affiliations.get("bothell"))
        self.assertTrue(affiliations.get("official_bothell"))
        self.assertTrue(affiliations.get('J1'))
        self.assertTrue(affiliations.get("intl_stud"))

    def test_tacgrad(self):
        now_request = get_request_with_user('tacgrad')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get("grad"))
        self.assertTrue(affiliations.get("tacoma"))
        self.assertTrue(affiliations.get("official_tacoma"))
        self.assertTrue(affiliations.get('F1'))
        self.assertTrue(affiliations.get("intl_stud"))

    def test_employee(self):
        now_request = get_request_with_user('staff')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get("official_seattle"))
        self.assertTrue(affiliations['employee'])
        self.assertTrue(affiliations['all_employee'])
        self.assertTrue(affiliations['clinician'])

    def test_eos_enrollment(self):
        now_request = get_request_with_user('jeos')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get("seattle"))
        self.assertTrue(affiliations.get("undergrad_c2"))

    def test_stud_empl_campuses(self):
        now_request = get_request_with_user('seagrad')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get("seattle"))
        self.assertTrue(affiliations.get("official_bothell"))
