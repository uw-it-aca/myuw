#!/usr/bin/pyton
"""Sanity check for category/links CSV"""

from django.test import TestCase
import os
import csv


class TestCategoryCSV(TestCase):
    """
    Ensure that the CSV has no blank fields in the header, and that
    every row has the same length.
    """
    def test_csv_format(self):

        csvpath = os.path.join(
            os.path.dirname(__file__),
            '..', 'data', 'category_links_import.csv'
        )

        with open(csvpath, 'rbU') as csvfile:

            reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            # Use length of first row as the expected length for all rows
            firstrow = reader.next()

            for field in firstrow:
                if len(field) == 0:
                    self.fail('Blank field in CSV header')

            expectedlen = len(firstrow)

            for row in reader:
                rowlen = len(row)
                self.assertEquals(
                    rowlen, expectedlen,
                    'Row %s had wrong number of fields'
                    % reader.line_num
                )
