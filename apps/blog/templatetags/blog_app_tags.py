from django.template import Library

register = Library()


@register.filter(name='split')
def split(value, arg):
    return value.split(arg)
