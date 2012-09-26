import json
import os
from myuw_mobile.models import Link as LinkModel

class Link:
    """ This class gives access to per-user link data """

    def get_links_for_user(self, user):
        """
        Returns a list of all links available for a user.
        If they should be active, is_on will be True.
        """
        path = os.path.join(
                            os.path.dirname( __file__ ),
                            '..', 'data', 'links.json')

        f = open(path)
        link_config = json.loads(f.read())

        links = []

        for link_data in link_config:
            link = LinkModel()
            link.title = link_data["title"]
            link.url = link_data["url"]

            if link_data["on_for_employees"]:
                link.is_on = True

            links.append(link)

        return links
