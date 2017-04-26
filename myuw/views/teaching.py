from myuw.views.page import page
from myuw.util.page_view import page_view
from myuw.models import VisitedLink
from myuw.dao import get_netid_of_current_user


@page_view
def teaching(request,
             year=None,
             quarter=None,
             summer_term=None):
    context = {
        "year": year,
        "quarter": quarter,
        "summer_term": summer_term
    }
    _add_quicklink_context(context)
    return page(request, context, template='teaching.html')


@page_view
def teaching_section(request,
                     section,
                     year=None,
                     quarter=None,
                     summer_term=None):
    context = {
        "section": section,
        "year": year,
        "quarter": quarter,
        "summer_term": summer_term
    }
    return page(request, context, template='teaching_section.html')


@page_view
def student_photo_list(request,
                       section,
                       year=None,
                       quarter=None,
                       summer_term=None):
    context = {
        "section": section,
        "year": year,
        "quarter": quarter,
        "summer_term": summer_term
    }
    return page(request, context, template='teaching/photo_list.html')


def _add_quicklink_context(context):
    username = get_netid_of_current_user()
    context['popular_links'] = []

    recents = []
    recent_links = VisitedLink.recent_for_user(username)
    for link in recent_links:
        print "URL: ", link.url
        recents.append({'url': link.url, 'label': link.label})

    context['recent_links'] = recents
