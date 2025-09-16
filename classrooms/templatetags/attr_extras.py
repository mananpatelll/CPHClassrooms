# classrooms/templatetags/attr_extras.py
from django import template

register = template.Library()

@register.filter
def attr(obj, field_name):
    return getattr(obj, field_name)

@register.simple_tag
def field_verbose(obj, field_name):
    return obj._meta.get_field(field_name).verbose_name

@register.simple_tag
def field_type(obj, field_name):
    return obj._meta.get_field(field_name).get_internal_type()
