from django import template
from django.template.defaultfilters import stringfilter
import django.utils.safestring as safestring

import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return safestring.mark_safe(md.markdown(value))