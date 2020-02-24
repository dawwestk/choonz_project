from django import template
from choonz.models import Tag

register = template.Library()

@register.inclusion_tag('choonz/tags.html')
def get_tag_list(current_tag=None, playlist=None):
    output = {}
    output['current_tag'] = current_tag
    if playlist:
        tags = playlist.get_playlist_tag_list
        output['tags'] = tags
    else:
        output['tags'] = Tag.objects.all()

    return output