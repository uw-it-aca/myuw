""" 
This module accesses per-user quick link data 
"""

import logging
import json
import os
from myuw_mobile.models import Link as LinkModel, UserMyLink
from myuw_mobile.models import User
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception
from myuw_mobile.dao.affiliation import get_all_affiliations
from myuw_mobile.dao.pws import get_netid_of_current_user


logger = logging.getLogger(__name__)


def _customized_link():
    """
    Return True if the user has changed her link selection 
    """
    _user_link_subscription = _get_mylink()
    return _user_link_subscription and len(_user_link_subscription) > 0


def get_links_for_user():
    """
    Returns a list of all the links available for a user.
    If they should be active, is_on will be True; Otherwise, False
    """
    if _customized_link():
        return _get_user_links()
    else:
        return _get_default_links()


def _get_all_links():
    """
    Return the list of all the links
    """
    path = os.path.join(os.path.dirname( __file__ ),
                        '..', 'data', 'links.json')
    f = open(path)
    return json.loads(f.read())


def _init_link(link_data):
    link = LinkModel()
    link.title = link_data["title"]
    link.url = link_data["url"]
    link.json_id = link_data["id"]
    link.is_on = False
    return link


def _get_default_links():
    affi = get_all_affiliations()
    link_list = []
    for link_data in _get_all_links():
        link = _init_link(link_data)

        if link_data["on_for_employees"] and affi["stud_employee"] or link_data["on_for_undergrad"] and affi["undergrad"] or link_data["on_for_gradstudent"] and affi["grad"] or link_data["on_for_pce"] and affi["pce"]:   
            if not link_data["restrict_to_campus"] or link_data["restrict_to_campus"] == "seattle" and affi["seattle"] or link_data["restrict_to_campus"] == "bothell" and affi["bothell"] or link_data["restrict_to_campus"] == "tacoma" and affi["tacoma"]:
                link.is_on = True
        link_list.append(link)
    return link_list


def get_link_by_id(id):
    """
    Returns a link object for the given id, if one exists.  None otherwise.
    """
    id = int(id)
    for link_data in _get_all_links():
        link = _init_link(link_data)
        if link.json_id == id:
            return link

    return


def _get_user():
    user_netid = get_netid_of_current_user()
    in_db = User.objects.filter(uwnetid=user_netid)
    if len(in_db) > 0:
        return in_db[0]

    new = User()
    new.uwnetid = user_netid
    new.save()
    return new


def _get_mylink():
    timer = Timer()
    try:
        return UserMyLink.objects.filter(user=_get_user())
    except Exception as ex:
        log_exception(logger,
                     'get UserMyLink',
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                     'get UserMyLink',
                      timer)


def _get_user_links():
    """
    return a list of user selected links
    """
    lookup = {}
    for link in _get_mylink():
        lookup[link.linkid] = link.is_on

    link_list = []
    for link_data in _get_all_links():
        link = _init_link(link_data)

        if link.json_id in lookup and lookup[link.json_id]:
            link.is_on = True
        link_list.append(link)
    return link_list


def _remove_prev_selection():
    """
    Remove the user's previous link selection 
    """
    if _customized_link():
        _get_mylink().delete()


def _save_mylink(new_links):
    timer = Timer()
    try:
        UserMyLink.objects.bulk_create(new_links)
    except Exception as ex:
        log_exception(logger,
                     'save UserMyLink',
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                     'save UserMyLink',
                      timer)


def save_link_preferences_for_user(new_selection):
    """
    Save the user's new selectio of links
    If they should be active, is_on will be True; Otherwise, False
    """
    user = _get_user()
    _remove_prev_selection()
    new_links = []
    for link_data in _get_all_links():
        new_link = UserMyLink()
        new_link.linkid = link_data["id"]
        new_link.user = user
        if new_selection[new_link.linkid]:
            new_link.is_on = True
        else:
            new_link.is_on = False
        new_links.append(new_link)
    _save_mylink(new_links)

