from django import template
from choonz.models import Tag, Playlist

register = template.Library()

@register.inclusion_tag('choonz/tags.html')
def get_tag_list(playlist=None):
    output = {}
    if playlist:
        tags = playlist.get_playlist_tag_list
        output['tags'] = tags
    else:
        output['tags'] = Tag.objects.all()

    return output

@register.inclusion_tag('choonz/playlist_suggestion.html')
def get_playlist_list():
    output = {}
    playlist_suggestions = Playlist.objects.all()
    output['playlist_suggestions'] = playlist_suggestions

    return output
