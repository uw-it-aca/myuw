from django.test import TestCase
from myuw_mobile.dao.test.course.colors import TestCourseColors

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
