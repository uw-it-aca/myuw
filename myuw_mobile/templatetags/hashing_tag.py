from django import template
import hashlib

register = template.Library()

@register.simple_tag
def hash_netid(netid):
    if netid is not None:
        return hashlib.md5(netid).hexdigest()
    return ''