from django import template
register = template.Library()

@register.filter
def get_range(start, end):
    """Custom range filter for templates"""
    return range(start, end)

