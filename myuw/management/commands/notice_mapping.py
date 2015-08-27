import csv
import logging
from django.core.management.base import BaseCommand, CommandError


output_format = "    \"%s\": {\n        \"myuw_category\": \"%s\",\n" +\
    "        \"location_tags\": %s,\n" +\
    "        \"critical\": %s\n    },\n"


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

    args = "<spreadsheet csv path>, <outfile>"

    def handle(self, *args, **options):
        try:
            csv_path = args[0]
            outfile = args[1]
            output_string = "NOTICE_CATEGORIES = {\n"
            with open(csv_path, "rb") as f_obj:
                reader = csv.reader(f_obj)
                for row in reader:
                    myuw_id = row[2]
                    if myuw_id is None or len(myuw_id) == 0 or\
                            myuw_id.startswith("MYUW"):
                        continue

                    myuw_category = row[3]
                    critical = row[4]
                    location_tags = self._get_location_tags(row[5])
                    string = output_format % (myuw_id, myuw_category,
                                              location_tags, len(critical) > 0)
                    output_string = output_string + string
            output_string = output_string[:-2] + "\n}\n"
            f = open(outfile, 'w')
            f.write(output_string)
            f.close()

        except IndexError as e:
            raise CommandError(e)
        except Exception as ex:
            raise CommandError(ex)

    def _get_location_tags(self, tag_string):
        tags = []
        tag_pieces = tag_string.split(",")
        for piece in tag_pieces:
            piece = piece.strip()
            if piece is not "?" and len(piece) > 0:
                tags.append(piece)
        return tags
