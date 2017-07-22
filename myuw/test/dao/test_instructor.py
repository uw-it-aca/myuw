from django.test import TestCase
from myuw.dao.instructor import add_seen_instructor, is_seen_instructor,\
    remove_seen_instructors_for_term, remove_seen_instructors_for_prior_terms,\
    remove_seen_instructors_for_prior_years
from myuw.dao.term import get_specific_term


class TestSeenInstructor(TestCase):
    def test_non_instructorness(self):
        self.assertEqual(is_seen_instructor('bill'), False)

    def test_add_seen_instructor(self):
        term = get_specific_term(2013, "summer")
        add_seen_instructor('bill', term)
        self.assertEqual(is_seen_instructor('bill'), True)

    def test_remove_instructors_for_term(self):
        term = get_specific_term(2013, "summer")
        add_seen_instructor('bill', term)
        remove_seen_instructors_for_term(term)
        self.assertEqual(is_seen_instructor('bill'), False)

    def test_remove_instructors_prior_terms(self):
        term = get_specific_term(2012, "summer")
        add_seen_instructor('bill', term)
        term2 = get_specific_term(2013, "autumn")
        remove_seen_instructors_for_prior_terms(term2)
        self.assertEqual(is_seen_instructor('bill'), False)

    def test_remove_instructors_prior_years(self):
        term = get_specific_term(2012, "summer")
        add_seen_instructor('bill', term)
        remove_seen_instructors_for_prior_years(2013)
        self.assertEqual(is_seen_instructor('bill'), False)
