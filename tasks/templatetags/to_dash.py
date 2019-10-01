from django import template

register = template.Library()

@register.filter
def to_dash(value):
    print(value)
    return value.__str__().replace(".","-")
