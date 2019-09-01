from django import template
register = template.Library()


@register.filter
def multiply(arg, value):
    return arg * value
