import json
import os
from myuw_mobile.models import Link as LinkModel, UserMyLink

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
            link.json_id = link_data["id"]

            if link_data["on_for_employees"]:
                link.is_on = True

            links.append(link)


        saved = UserMyLink.objects.filter(user = user)

        if len(saved) > 0:
            use_user_preference = True
            lookup = {}
            for pref in saved:
                lookup[pref.linkid] = pref.is_on

            for link in links:
                if lookup[link.json_id]:
                    link.is_on = True
                else:
                    link.is_on = False

        return links

    def save_link_preferences_for_user(self, link_preferences, user):
        all_links = self.get_links_for_user(user)

        saved = UserMyLink.objects.filter(user = user)
        saved.delete()

        new_links = []
        for link in all_links:
            new = UserMyLink()
            new.linkid = link.json_id
            new.user = user

            if link_preferences[link.json_id]:
                new.is_on = True
            else:
                new.is_on = False

            new_links.append(new)

        UserMyLink.objects.bulk_create(new_links)
