from django import template

register = template.Library()

@register.simple_tag
def get_range(end):
    return range(end)


@register.filter()
def to_int(value):
    return int(value)

@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})

@register.filter
def mul(value, arg):
    return value * arg