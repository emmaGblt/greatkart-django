from django import template

register = template.Library()


@register.inclusion_tag("includes/stars.html")
def showratingstars(rating):
    return {"rating": rating}
