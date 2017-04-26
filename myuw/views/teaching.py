from myuw.views.page import page, try_prefetch
from myuw.util.page_view import page_view
from myuw.models import VisitedLink, PopularLink
from myuw.dao import get_netid_of_current_user
from myuw.dao.affiliation import get_all_affiliations


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

    failure = try_prefetch(request)
    if failure:
        return failure

    _add_quicklink_context(request, context)
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


def _add_quicklink_context(request, context):
    username = get_netid_of_current_user()

    recents = []
    recent_links = VisitedLink.recent_for_user(username)
    for link in recent_links:
        recents.append({'url': link.url, 'label': link.label})

    context['recent_links'] = recents

    popular = []

    # TODO - consider affiliation filtering here
    popular_links = PopularLink.objects.all()
    for link in popular_links:
        popular.append({'url': link.url, 'label': link.label})

    context['popular_links'] = popular
