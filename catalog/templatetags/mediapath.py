from django import template
from django.templatetags.static import PrefixNode

register = template.Library()


@register.simple_tag
def mediapath(image_path):
    return PrefixNode.handle_simple("MEDIA_URL") + str(image_path)
