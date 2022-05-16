from django import template
from django.template.defaultfilters import stringfilter
import bleach
from bleach_whitelist import markdown_tags, markdown_attrs
import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return bleach.clean(md.markdown(value, safe_mode=True,
    extensions=['markdown.extensions.fenced_code']),markdown_tags, markdown_attrs)
    # return md.markdown(value, safe_mode=True,
    # extensions=['markdown.extensions.fenced_code'])
