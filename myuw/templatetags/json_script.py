import json

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

_json_script_escapes = {
    ord('>'): '\\u003E',
    ord('<'): '\\u003C',
    ord('&'): '\\u0026',
}


@register.filter(is_safe=True)
def json_script(value, element_id):
    """
    A copy of https://github.com/django/django/blob/
    d6aff369ad33457ae2355b5b210faf1c4890ff35/django/utils/html.py#L78

    Usage {{ <value>|json_script:"<element_id>" }}

    TODO: Remove this when we update to Django 2.1
    """
    from django.core.serializers.json import DjangoJSONEncoder
    json_str = json.dumps(
        value, cls=DjangoJSONEncoder
    ).translate(_json_script_escapes)
    return format_html(
        '<script id="{}" type="application/json">{}</script>',
        element_id, mark_safe(json_str)
    )