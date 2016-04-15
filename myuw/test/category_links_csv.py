#!/usr/bin/pyton

from django.test import TestCase
import os
import csv

# Fields which should be validated as URLs
urlfields = [3, 5, 7, 9]


def check_ascii(s):
    '''
    Ensure entire string is ASCII
    '''
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return False

    return True


def validate_URL(s):
    '''
    Sanity check to make sure something looks like a URL
    '''
    return s.startswith('http')


class TestCategoryCSV(TestCase):
    '''
    Test the resource links/categories CSV for:
        * Lack of trailing commas
        * Same number of fields in each record
        * No Unicode characters
        * Fields that should be URLs actually look like URLs
    '''
    def test_csv_format(self):

        csvpath = os.path.join(
            os.path.dirname(__file__),
            '..', 'data', 'category_links_import.csv'
        )

        with open(csvpath, 'rbU') as csvfile:

            reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            # Use length of first row as the expected length for all rows
            firstrow = reader.next()
            expectedlen = len(firstrow)

            for row in reader:
                # Ensure there are no trailing blanks
                lastnonblank = 0
                rownum = reader.line_num
                rowlen = len(row)
                # Using the first row, set this value
                # Otherwise, check against the expected value
                self.assertEquals(
                    expectedlen,
                    rowlen,
                    'Row %s had %s fields, expected %s'
                    % (rownum, rowlen, expectedlen)
                )

                for fieldindex in range(rowlen):
                    fieldvalue = row[fieldindex]
                    # Keep track of last non-empty field
                    if len(fieldvalue) > 0:
                        lastnonblank = fieldindex

                        # Check for non-ascii
                        if not(check_ascii(fieldvalue)):
                            self.fail(
                                'Row %s field %s contained non-ASCII character'
                                % (rownum, fieldindex)
                            )

                        # URL sanity check
                        if fieldindex in urlfields:
                            if not(validate_URL(fieldvalue)):
                                self.fail(
                                    'Row %s field %s doesn\'t look like a URL'
                                    % (rownum, fieldindex)
                                )

                # Fail if there are trailing empty fields
                if lastnonblank < rowlen - 1:
                    self.fail(
                        'CSV had trailing blank fields on line %s'
                        % reader.line_num
                    )
