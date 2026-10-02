from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static
from pathlib import Path

register = template.Library()


@register.filter
def image_url(image_field):
    """Prefer bundled image files, falling back to configured media storage."""
    if not image_field:
        return ""

    name = getattr(image_field, "name", "")
    if name:
        bundled_path = Path(settings.BASE_DIR) / "media" / name
        if bundled_path.is_file():
            try:
                return staticfiles_storage.url(name)
            except ValueError:
                return static(name)

    try:
        return image_field.url
    except Exception:
        return static(name) if name else ""
