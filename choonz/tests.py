from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from choonz.models import Playlist, Tag, Song, Artist, Rating
from django.contrib.auth.models import User

# Create your tests here.
class PlaylistModelTests(TestCase):
    def test_ensure_ratings_are_positive(self):
        '''
        Rating average value must be 0 or greater
        '''
        playlist = Playlist(name='test', averageRating=-1)
        playlist.save()

        self.assertEqual((playlist.averageRating >= 0), True)

    def test_slug_line_creation(self):
        '''
        Check that when a playlist is made, the slug is correct
        '''
        playlist = Playlist(name='Test Playlist Name')
        playlist.save()

        self.assertEqual(playlist.slug, 'test-playlist-name')

class TagModelTests(TestCase):
    def test_slug_line_creation(self):
        '''
        Check that the tag slug is correct
        '''
        tag = add_tag('Absolute Bangers')

        self.assertEqual(tag.slug, 'absolute-bangers')

    def test_slug_uniqueness(self):
        '''
        Check uniqueness criteria of Tag slug
        '''
        tag1 = add_tag('Mental Choonz')
        with self.assertRaises(IntegrityError):
            tag2 = add_tag('mentAl  choonz')

    def test_tag_get_number_of_playlists_method(self):
        tag1 = add_tag('test tag 1')
        tag2 = add_tag('test tag 2')
        playlist1 = add_playlist('test playlist 1', [tag1, tag2])
        playlist2 = add_playlist('test playlist 2', [tag1])
        playlist3 = add_playlist('test playlist 3', [tag1])
        playlist4 = add_playlist('test playlist 4', [tag1, tag2])

        self.assertEqual(tag1.getNumberOfPlaylists, 4)
        self.assertEqual(tag2.getNumberOfPlaylists, 2)


class IndexViewTests(TestCase):
    def test_index_view_with_no_playlists(self):
        """
        If no playlists exist, the appropriate message should be displayed.
        """
        response = self.client.get(reverse('choonz:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no playlists present.')
        self.assertQuerysetEqual(response.context['most_rated_playlists'], [])

    def test_index_with_playlists(self):
        '''
        With playlists we should see a list
        '''
        add_playlist('tester-1')
        add_playlist('tester-2')
        add_playlist('tester-3')

        response = self.client.get(reverse('choonz:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tester-1')
        self.assertContains(response, 'tester-2')
        self.assertContains(response, 'tester-3')

        num_playlists = len(response.context['most_rated_playlists'])
        self.assertEquals(num_playlists, 3)


def add_tag(description):
    tag = Tag.objects.get_or_create(description=description)[0]
    tag.save()

    return tag

def add_playlist(name, tags=None):
    playlist = Playlist.objects.get_or_create(name=name)[0]

    # have any tags been provided
    if tags:
        # loop through them
        for t in tags:
            # making sure they are not blank
            if t:
                tag = Tag.objects.get_or_create(description=t)[0]
                playlist.tags.add(tag)


    playlist.save()

    return playlist