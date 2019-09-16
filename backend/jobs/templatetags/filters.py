from django import template
from django.utils.crypto import get_random_string

register = template.Library()


@register.filter
def multiply(arg, value):
    return arg * value


@register.filter
def subtract(arg, value):
    return arg - value


@register.filter
def rnd(arg):
    return str(arg) + get_random_string(8, allowed_chars='1234567890abcdef')
