from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.urlresolvers import reverse
import logging
from myuw.dao.user import get_netid_of_current_user
from myuw.views import admin_required, set_admin_wrapper_template
from myuw.models import VisitedLink, PopularLink


PAGE_SIZE = 10
MAX_PAGE = 5


@login_required
@admin_required('MYUW_ADMIN_GROUP')
def popular_links(request, page):
    logger = logging.getLogger(__name__)
    if request.POST:
        if 'url' in request.POST and 'label' in request.POST:
            PopularLink.objects.create(url=request.POST['url'],
                                       label=request.POST['label'])
            logger.info("popular link added.  user: %s, link: %s" %
                        (get_netid_of_current_user(), request.POST['url']))

        if 'remove_popular' in request.POST:
            for popular_id in request.POST.getlist('remove_popular'):
                link = PopularLink.objects.get(pk=popular_id)
                url = link.url
                link.delete()
                logger.error("popular link removed.  user: %s, link:  %s" %
                             (get_netid_of_current_user(), url))

    curated_popular = PopularLink.objects.all()
    existing_lookup = set()
    curated_links = []
    for link in curated_popular:
        curated_links.append({'url': link.url,
                              'label': link.label,
                              'id': link.pk})
        existing_lookup.add(link.url)

    kwargs = {}
    for check in dir(VisitedLink):
        if check.find('is_') == 0:
            if check in request.GET:
                kwargs[check] = True

    all_popular = VisitedLink.get_popular(**kwargs)

    # Display is 1-indexed, we're 0-indexed
    page = int(page)
    page -= 1
    if page > MAX_PAGE or page < 0:
        page = 0

    start_index = page * PAGE_SIZE
    popular = all_popular[start_index:start_index+PAGE_SIZE]

    for link in popular:
        if link['url'] in existing_lookup:
            link['exists'] = True
        else:
            link['exists'] = False

    context = {'popular': popular,
               'checked': kwargs,
               'curated_popular_links': curated_links
               }

    if page > 0:
        context['previous_page'] = reverse('myuw_popular_links_paged',
                                           kwargs={'page': page})

    if page+1 < MAX_PAGE and len(all_popular) > start_index+PAGE_SIZE:
        context['next_page'] = reverse('myuw_popular_links_paged',
                                       kwargs={'page': page+2})
    set_admin_wrapper_template(context)
    return render(request, "admin/popular_links.html", context)
