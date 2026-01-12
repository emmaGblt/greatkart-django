from django import template
from urllib.parse import urlencode

register = template.Library()


@register.simple_tag
def urlparams(**kwargs):
    "Returns a query string by encoding one or several key-word arguments"
    safe_args = {key: value for (key, value) in kwargs.items() if value}
    if safe_args:
        return "?{}".format(urlencode(safe_args))
    return ""
