from django import template
from choonz.models import Tag

register = template.Library()

@register.inclusion_tag('choonz/tags.html')
def get_tag_list(current_tag=None):
    return {'tags': Tag.objects.all(), 'current_tag': current_tag}