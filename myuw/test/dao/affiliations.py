from django.test import TestCase
from django.conf import settings
from myuw.dao.affiliation import get_all_affiliations, get_identity_log_str
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request, get_request_with_user


@fdao_pws_override
@fdao_sws_override
class TestAffilliations(TestCase):
    def setUp(self):
        get_request()

    def test_eos_enrollment(self):
        now_request = get_request_with_user('jeos')
        affiliations = get_all_affiliations(now_request)

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

    def test_is_faculty(self):
        now_request = get_request_with_user('bill')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations['faculty'])

    def test_is_clinician(self):
        now_request = get_request_with_user('eight')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations['clinician'])

    def test_is_instructor(self):
        now_request = get_request_with_user('bill')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations['instructor'])

    def test_is_grad_stud_employee(self):
        now_request = get_request_with_user('billseata')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get("grad"))
        self.assertTrue(affiliations.get("student"))
        self.assertTrue(affiliations.get("official_seattle"))
        self.assertTrue(affiliations.get("instructor"))
        self.assertTrue(affiliations.get("stud_employee"))

    def test_is_pce_stud(self):
        now_request = get_request_with_user('jpce')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get('pce'))
        self.assertTrue(affiliations.get('undergrad_c2'))
        self.assertFalse(affiliations.get('grad_c2'))
        self.assertTrue(affiliations.get("undergrad"))
        self.assertTrue(affiliations.get("student"))
        self.assertTrue(affiliations.get("official_seattle"))
        self.assertFalse(affiliations.get("official_pce"))
        self.assertTrue('PCE-student' in get_identity_log_str(now_request))

        now_request = get_request_with_user('jinter')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get('pce'))
        self.assertFalse(affiliations.get('undergrad_c2'))
        self.assertTrue(affiliations.get('grad_c2'))

        now_request = get_request_with_user('jeos')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get('undergrad_c2'))
        self.assertFalse(affiliations.get('grad_c2'))
        log_str = get_identity_log_str(now_request)
        self.assertTrue('PCE-student' in log_str)
        self.assertFalse('Campus: PCE' in log_str)

    def test_is_2fa_permitted(self):
        now_request = get_request_with_user('javerage')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations.get('2fa_permitted'))
