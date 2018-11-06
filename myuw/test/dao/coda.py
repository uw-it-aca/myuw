from unittest import TestCase
from myuw.dao import coda


class TestCoDaDAO(TestCase):

    def test_process_section_label(self):

        section_label = "2018_winter_T_UNIV_200_A"

        processed = coda._process_section_label(section_label)

        self.assertEquals("2018-winter-T%20UNIV-200-A", processed)

        section_label = "2018_winter_ES S_102_A"

        processed = coda._process_section_label(section_label)

        self.assertEquals("2018-winter-ES%20S-102-A", processed)
