from django.core.management.base import BaseCommand, CommandError
import csv



class Command(BaseCommand):
    help = 'Builds NOTICE_MAPPING from https://docs.google.com/a/uw.edu/spreadsheet/ccc?key=0AkNIKfyuX9lwdEYtR2JfRUlqUXBRazBqNWNldk9YV2c&usp=drive_web#gid=0 (export as csv)'
    args = "<spreadsheet csv path>, <outfile>"

    def handle(self, *args, **options):
        try:
            csv_path = args[0]
            outfile = args[1]
            output_string = ""
            with open(csv_path, "rb") as f_obj:
                reader = csv.reader(f_obj)
                a = 0
                for row in reader:
                    notice_id = row[2]
                    myuw_category = row[3]
                    critical = row[4]
                    location_tags = self._get_location_tags(row[5])
                    string = "\"%s\": {\n    \"myuw_category\": \"%s\",\n    \"location_tags\": %s,\n    \"critical\": %s\n},\n" % \
                             (notice_id,
                             myuw_category,
                              location_tags,
                              len(critical) > 0
                             )
                    output_string = output_string + string

            f = open(outfile, 'w')
            f.write(output_string)
            f.close()

        except IndexError:
            raise CommandError("No path specified")
        except Exception as ex:
            raise CommandError(ex)

    def _get_location_tags(self, tag_string):
        tags = []
        tag_pieces = tag_string.split(",")
        for piece in tag_pieces:
            piece = piece.strip()
            if piece is not "?" and len(piece)>0:
                tags.append(piece)



        return tags
