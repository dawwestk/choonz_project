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
def get_playlist_list(tags_wanted=False):
    playlist_suggestions = Playlist.objects.all()
    output = {'playlist_suggestions': playlist_suggestions, 'tags_wanted': tags_wanted}

    return output


@register.inclusion_tag('choonz/song_search_results.html')
def get_search_results(results=None):
    search_results = results
    output = {'search_results': search_results}

    return output


@register.inclusion_tag('choonz/playlist_list_item.html')
def get_playlist_list_item(playlist, user, tags_wanted=False):
    output = {'playlist_slug': playlist.slug, 'playlist_name': playlist.name,
              'playlist_get_average_rating': playlist.get_average_rating,
              'playlist_get_number_of_ratings': playlist.get_number_of_ratings,
              'playlist_creator': playlist.creator, 'user': user, 'tags_wanted': tags_wanted,
              'tags': playlist.get_playlist_tag_descriptions}

    return output
