import logging
import json
import os
from operator import itemgetter 
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception
from myuw_mobile.models import Link as LinkModel, UserMyLink
from myuw_mobile.dao.gws import Member

class Link:
    """ 
    This class accesses per-user quick link data 
    """
    _logger = logging.getLogger('myuw_mobile.dao.links.Link')
    
    def get_links_for_user(self, user):
        """
        Returns a list of all the links available for a user.
        If they should be active, is_on will be True; Otherwise, False
        """
        if self.customized_link(user):
            return self._get_user_links(user)
        else:
            return self._get_default_links(user)


    def save_link_preferences_for_user(self, new_selection, user):
        """
        Save the user's new selectio of links
        If they should be active, is_on will be True; Otherwise, False
        """
        self.remove_prev_selection(user)
        new_links = []
        for link_data in Link._get_all_links():
            new = UserMyLink()
            new.linkid = link_data["id"]
            new.user = user
            if new_selection[new.linkid]:
                new.is_on = True
            else:
                new.is_on = False
            new_links.append(new)
        self._save_mylink(new_links)


    def _save_mylink(self, new_links):
        timer = Timer()
        try:
            UserMyLink.objects.bulk_create(new_links)
        except Exception, message:
            traceback.print_exc(file=sys.stdout)
            log_exception(Link._logger,
                         'save UserMyLink',
                          message)
        finally:
            log_resp_time(Link._logger,
                         'save UserMyLink',
                          timer)

    def _get_mylink(self, user):
        timer = Timer()
        try:
            return UserMyLink.objects.filter(user=user)
        except Exception, message:
            traceback.print_exc(file=sys.stdout)
            log_exception(Link._logger,
                         'get UserMyLink',
                          message)
        finally:
            log_resp_time(Link._logger,
                         'get UserMyLink',
                          timer)

    def customized_link(self, user):
        """
        Return True if the user has changed her link selection 
        """
        self._user_link_subscription = self._get_mylink(user)
        return self._user_link_subscription and len(self._user_link_subscription) > 0


    def remove_prev_selection(self, user):
        """
        Remove the user's previous link selection 
        """
        if self.customized_link(user):
            self._user_link_subscription.delete()


    def _get_user_links(self, user):
        lookup = {}
        for link in self._user_link_subscription:
            lookup[link.linkid] = link.is_on

        link_list = []
        for link_data in Link._get_all_links():
            link = Link._init_link(link_data)

            if lookup[link.json_id]:
                link.is_on = True
            link_list.append(link)
        return link_list


    def _get_default_links(self, user):
        member = Member()
        link_list = []
        for link_data in Link._get_all_links():
            link = Link._init_link(link_data)

            if link_data["on_for_employees"] and member.is_student_employee() or link_data["on_for_undergrad"] and member.is_undergrad_student() or link_data["on_for_gradstudent"] and member.is_grad_student() or link_data["on_for_pce"] and member.is_pce_student():   
                if not link_data["restrict_to_campus"] or link_data["restrict_to_campus"] == "seattle" and member.is_seattle_student() or link_data["restrict_to_campus"] == "bothell" and member.is_bothell_student() or link_data["restrict_to_campus"] == "tacoma" and member.is_tacoma_student():
                    link.is_on = True
            link_list.append(link)
        return link_list


    @staticmethod
    def _get_all_links():
        """
        Return the list of all the links
        """
        path = os.path.join(os.path.dirname( __file__ ),
                            '..', 'data', 'links.json')
        f = open(path)
        return json.loads(f.read())

    @staticmethod
    def _init_link(link_data):
        link = LinkModel()
        link.title = link_data["title"]
        link.url = link_data["url"]
        link.json_id = link_data["id"]
        link.is_on = False
        return link

