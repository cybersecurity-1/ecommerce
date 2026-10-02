from django import template
from django.templatetags.static import static

register = template.Library()


@register.filter
def image_url(image_field):
    """Use configured storage, falling back to bundled static media."""
    if not image_field:
        return ""

    try:
        url = image_field.url
    except Exception:
        url = ""

    if url:
        return url

    name = getattr(image_field, "name", "")
    return static(name) if name else ""
