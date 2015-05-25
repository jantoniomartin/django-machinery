from django import template
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter(is_safe=True)
def as_hours(text, arg):
    text = int(text)/3600.
    return floatformat(text, arg)
