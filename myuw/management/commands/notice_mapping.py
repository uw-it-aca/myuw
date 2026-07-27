# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import csv
import logging

from django.core.management.base import BaseCommand, CommandError

logger = logging.getLogger("commands")
item_format = ("        \"myuw_category\": \"{}\",\n" +
               "        \"location_tags\": {},\n" +
               "        \"critical\": {}")


class Command(BaseCommand):

    help = 'Builds NOTICE_MAPPING based on the spreadsheet from' +\
        'https://docs.google.com/a/uw.edu/spreadsheet/ccc?key=' +\
        '0AkNIKfyuX9lwdEYtR2JfRUlqUXBRazBqNWNldk9YV2c&usp=drive_web#gid=0' +\
        'Workflow: 1. download the spreadsheet as map.csv;\n' +\
        '2. transfer the file if it is not local;\n' +\
        '3. Run: python manage.py notice_mapping' +\
        'map.csv notice_categorization.py;\n' +\
        '4. Move the mapping file into myuw/dao/;\n' +\
        '5. Add and commit the notice_categorization.py'

    def add_arguments(self, parser):
        parser.add_argument('spreadsheet-csv-path')
        parser.add_argument('outfile')

    def handle(self, *args, **options):
        seen_category_keys = set()
        try:
            csv_path = options['spreadsheet-csv-path']
            seen_category_keys = set()
            categories = []

            with open(csv_path, 'r', encoding='utf8') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',')

                next(csvreader)
                for row in csvreader:
                    try:
                        myuw_id = row[2].replace(" ", "")
                        if myuw_id is None or len(myuw_id) == 0:
                            continue
                        if myuw_id in seen_category_keys:
                            continue
                        seen_category_keys.add(myuw_id)
                        # row[3]: myuw_category
                        # row[4]: critical
                        item = item_format.format(
                            row[3], self._get_location_tags(row[5]), len(row[4]) > 0)
                        categories.append(
                            "    \"{0}\": {1}\n{2}\n{3}".format(  # noqa: UP030
                                myuw_id.lower(), "{", item, "    }"))
                    except Exception as ex:
                        logger.error(f"{ex!s} in line: {row}")

            output_string = "NOTICE_CATEGORIES = {0}{1}\n{2}".format(  # noqa: UP030
                "{\n", ",\n".join(categories), "}\n")

            outfile = options['outfile']
            with open(outfile, "w") as f:
                f.write(output_string)

        except IndexError as e:
            raise CommandError(e)
        except Exception as ex:
            raise CommandError(ex)

    def _get_location_tags(self, tag_string):
        tags = []
        tag_pieces = tag_string.split(",")
        for piece in tag_pieces:
            piece = piece.strip()
            if piece != "?" and len(piece) > 0:
                tags.append(piece)
        return tags
