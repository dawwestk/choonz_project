from django import template
from choonz.models import Playlist

register = template.Library()

@register.inclusion_tag('choonz/playlists.html')
def get_playlist_list(current_playlist=None):
    return {'categories': Playlist.objects.all(), 'current_playlist': current_playlist}