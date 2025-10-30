from django import template

register = template.Library()

@register.filter
def dictget(dictionary, key):
    """Return dictionary[key] if present, else None."""
    if dictionary and key in dictionary:
        return dictionary.get(key)
    return None

