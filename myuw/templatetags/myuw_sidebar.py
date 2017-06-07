from django.conf import settings
from django.template import Library
from django.core.urlresolvers import resolve


register = Library()


@register.simple_tag(takes_context=True)
def add_sidebar_context(context):
    request = context.get('request')
    if not request:
        return ''

    current_url = resolve(request.path_info).url_name

    context['is_%s' % current_url] = True

    for f in getattr(settings, "MYUW_ENABLED_FEATURES", []):
        context["%s_enabled" % f.lower()] = True

    return ''
