from django import template

from choonz.models import Tag, Playlist, Song

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
def get_playlist_list(tags_wanted=False, minimised_stars=False):
    playlist_suggestions = Playlist.objects.all()
    output = {'playlist_suggestions': playlist_suggestions, 'tags_wanted': tags_wanted,
              'minimised_stars': minimised_stars}

    return output


@register.inclusion_tag('choonz/song_search_results.html')
def get_search_results(results=None):
    search_results = results
    output = {'search_results': search_results}

    return output


@register.inclusion_tag('choonz/playlist_list_item.html')
def get_playlist_list_item(playlist, user, tags_wanted=False, minimised_stars=False):
    output = {'playlist': playlist, 'user': user, 'tags_wanted': tags_wanted,
              'tags': playlist.get_playlist_tag_descriptions, 'minimised_stars': minimised_stars,
              'average': playlist.get_average_rating}

    return output


@register.inclusion_tag('choonz/edit_playlist_list_songs.html')
def get_songs_on_playlist(playlist_slug):
    playlist = Playlist.objects.get(slug=playlist_slug)
    songs = playlist.get_song_list
    output = {'playlist_slug': playlist_slug, 'songs': songs}
    return output


@register.inclusion_tag('choonz/edit_playlist_new_song.html')
def get_song_detail_for_edit_page(playlist_slug, song):
    song = Song.objects.get(slug=song)
    song_slug = song.slug
    song_title = song.title
    song_link_spotify = song.linkToSpotify
    song_link_other = song.linkOther
    song_artist = song.artist.name
    output = {'playlist_slug': playlist_slug, 'song_slug': song_slug, 'song_title': song_title,
              'song_link_spotify': song_link_spotify, 'song_link_other': song_link_other,
              'song_artist': song_artist}

    return output
