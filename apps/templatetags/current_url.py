from django import template
from utils import url_manifest

register = template.Library()


@register.filter
def current_url(
    current: str,
    url_name: str
) -> str:
    try:
        if current == url_manifest()[url_name]:
            return "current-url"
        else:
            return ""

    except KeyError:
        return ""
