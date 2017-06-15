from django.template import Library


register = Library()


@register.simple_tag()
def large_number(value):
    if value < 1000:
        return value

    labels = ['K', 'M', 'B']
    for l in labels:
        value /= 1000
        if value < 1000:
            return "%s%s" % (value, l)

    return "%s%s" % (value, l)
