from datetime import datetime

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from choonz.models import Playlist, Tag, Song, Artist, Rating
from choonz.forms import PlaylistForm
from django.contrib.auth.models import User

'''
    Model related tests
'''


class PlaylistModelTests(TestCase):

    def playlist_test_setup(self, playlist_name, n_tags=10, n_songs=10, n_ratings=10):
        # create generic tags
        tags = []
        for i in range(0, n_tags):
            tags.append(add_tag('test tag ' + str(i)))

        # assign them to a playlist
        playlist = add_playlist(playlist_name, tags)

        # create an artist
        artist1 = add_artist('test artist 1')

        # generate songs by artist and add to the playlist
        for i in range(0, n_songs):
            playlist.songs.add(add_song(title='song ' + str(i), artist=artist1))

        # create users to rate playlist
        for i in range(0, n_ratings):
            user = add_user('test user ' + str(i))
            rating = add_rating(playlist, user, 1.0, "test comment " + str(i))

        return playlist


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

    def test_playlist_song_count(self):
        '''
        Check that the playlist.get_song_list method lists all songs on a playlist
        '''
        playlist = self.playlist_test_setup(playlist_name='test song count', n_songs=10)

        playlist_songs = playlist.get_song_list
        self.assertEqual(len(playlist_songs), 10)

    def test_playlist_get_number_of_ratings(self):
        '''
        Check that the playlist.get_number_of_ratings method lists all ratings on a playlist
        '''
        playlist = self.playlist_test_setup(playlist_name='rating count playlist', n_ratings=10)

        playlist_ratings = playlist.get_number_of_ratings
        self.assertEqual(playlist_ratings, 10)

    def test_playlist_get_tag_list(self):
        '''
        Check that the playlist.get_playlist_tag_list method lists all tags on a playlist
        '''
        playlist = self.playlist_test_setup(playlist_name='tag list playlist', n_tags=10)

        playlist_tags = playlist.get_playlist_tag_list

        for i in range(0, 10):
            self.assertTrue(Tag.objects.get(description='test tag ' + str(i)) in playlist_tags)

    def test_playlist_get_playlist_tag_descriptions(self):
        '''
        Check that the playlist.get_playlist_tag_descriptions method returns all tag descriptions
        '''
        playlist = self.playlist_test_setup(playlist_name='tag description playlist', n_tags=10)

        playlist_tags = playlist.get_playlist_tag_descriptions

        for i in range(0, 10):
            self.assertTrue(('test tag ' + str(i)) in playlist_tags)

    def test_playlist_get_playlist_tag_descriptions_as_string(self):
        '''
        Check that the playlist.get_playlist_tag_descriptions_as_string method returns all tag descriptions as a string
        '''
        playlist = self.playlist_test_setup(playlist_name='tag description playlist', n_tags=10)

        playlist_tags = playlist.get_playlist_tag_descriptions_as_string

        for i in range(0, 10):
            self.assertTrue(('test tag ' + str(i)) in playlist_tags)

    def test_playlist_get_average_rating(self):
        '''
        Check that the playlist.get_average_rating method returns the correct result
        '''
        playlist = self.playlist_test_setup(playlist_name='average rating playlist', n_ratings=0)

        user1 = User.objects.get_or_create(username='test user 1')[0]
        user2 = User.objects.get_or_create(username='test user 2')[0]
        rating1 = add_rating(playlist=playlist, user=user1, stars=5.0)
        rating2 = add_rating(playlist=playlist, user=user2, stars=3.0)

        self.assertEqual(playlist.get_average_rating, 4.0)


class TagModelTests(TestCase):
    def test_slug_line_creation(self):
        '''
        Check that the tag slug is correct
        '''
        tag = add_tag('Absolute Bangers')

        self.assertEqual(tag.slug, 'absolute-bangers')

    def test_slug_uniqueness(self):
        '''
        Check uniqueness criteria of tag slug
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


class ArtistModelTests(TestCase):
    def test_slug_line_creation(self):
        '''
        Check that the artist slug is correct
        '''
        artist = add_artist('Test Band')

        self.assertEqual(artist.slug, 'test-band')


class SongModelTests(TestCase):
    def test_slug_line_creation(self):
        '''
        Check that the song slug is correct
        '''
        artist = add_artist('test artist')
        song = add_song('Test Song', artist)

        self.assertEqual(song.slug, 'test-song-test-artist')


class RatingModelTests(TestCase):
    def test_rating_get_rated_playlist_creator(self):
        '''
        Check that the rating.get_rated_playlist_creator method returns a playlist creator
        '''
        playlist = add_playlist('test rating playlist')
        playlist_creator = add_user('test creator')
        playlist.creator = playlist_creator
        playlist.save()

        rating_provider = add_user('rating provider')
        rating = add_rating(playlist, rating_provider)

        self.assertEqual(rating.get_rated_playlist_creator, playlist_creator)

    def test_rating_star_boundaries(self):
        user = add_user('test user')
        playlist = add_playlist('rating test playlist')
        rating = add_rating(playlist, user, stars=-3)
        rating.save()

        self.assertEqual((rating.stars >= 0), True)
        self.assertEqual((rating.stars <= 5), True)


'''
    View related tests
'''
class IndexViewTests(TestCase):
    def test_index_view_with_no_playlists(self):
        """
        If no playlists exist, the appropriate message should be displayed.
        """
        response = self.client.get(reverse('choonz:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no playlists present.')
        self.assertQuerysetEqual(response.context['most_rated_playlists'], [])

    def test_index_with_most_rated_playlists(self):
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

    def test_index_with_highest_rated_playlists(self):
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

        num_playlists = len(response.context['highest_rated_playlists'])
        self.assertEquals(num_playlists, 3)

    def test_index_user_not_logged_in(self):
        '''
        Making sure that a non-logged-in user sees a link to login
        '''

        response = self.client.get(reverse('choonz:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/accounts/login')
        self.assertContains(response, '/accounts/register')
        self.assertNotContains(response, '/choonz/add_playlist')

    def test_index_user_logged_in(self):
        '''
        Making sure that a logged-in user can logout
        '''
        user, owner = create_user_and_log_in('test', 'test_password')
        response = self.client.login(username='test', password='test_password')
        self.assertTrue(response)

        # User logged in successfully
        if response:
            # Check the visible/non-visible links on the index page
            index_response = self.client.get(reverse('choonz:index'))
            self.assertContains(index_response, '/accounts/logout')
            self.assertContains(index_response, '/choonz/list_playlists')

class ProfileViewTests(TestCase):
    def test_profile_view_differentiates_page_owner_and_logged_in_user(self):
        '''
        When logged in as USER viewing user USER-X's profile we should see their profile picture, not USER's
        '''
        user, owner = create_user_and_log_in('user', 'test_password', 'owner')

        response = self.client.login(username='user', password='test_password')

        # User logged in successfully
        if response:
            profile_response = self.client.get('/choonz/profile/owner/')

            # Test the header for the correct username
            self.assertContains(profile_response, "owner's Profile")
            self.assertNotContains(profile_response, "My Profile")

            # Test to see if the Edit Profile button is visible
            self.assertNotContains(profile_response, "Edit Profile")
        else:
            self.assertEqual(response, True)

class AddPlaylistViewTests(TestCase):
    def test_add_playlist_view_tags_visible(self):
        '''
        When adding a playlist, check that all tags are available as options
        '''
        user, owner = create_user_and_log_in('user', 'test_password')
        tag1 = add_tag('tag 1')
        tag2 = add_tag('tag 2')

        response = self.client.login(username='user', password='test_password')

        # User logged in successfully
        if response:
            add_playlist_response = self.client.get(reverse('choonz:add_playlist'))

            # Test the header for the correct username
            self.assertContains(add_playlist_response, "Choonbuilder")
            self.assertContains(add_playlist_response, 'tag 1')
            self.assertContains(add_playlist_response, 'tag 2')
        else:
            self.assertEqual(response, True)

    def test_add_playlist_post_form(self):
        '''
        When adding a playlist, check what is posted is being validated, and playlist created
        '''
        user, owner = create_user_and_log_in('user', 'test_password')
        tag1 = add_tag('tag 1')
        tag2 = add_tag('tag 2')

        response = self.client.login(username='user', password='test_password')

        # User logged in successfully
        if response:
            # Create a playlist by adding form data as required
            today = "2020-03-09 12:52:17.867600"
            form_data = {'name': 'test_playlist', 'description': 'test playlist description', 'tags': [tag1, tag2], 'createdDate': today, 'lastUpdatedDate': today, 'averageRating': 0}

            # Check that the form is valid
            form = PlaylistForm(data=form_data)
            self.assertTrue(form.is_valid())

            # Check that the post request is valid
            add_playlist_response = self.client.post(reverse('choonz:add_playlist'), form_data)
            self.assertTrue(add_playlist_response)

            # Check that playlist is created in database
            playlist = Playlist.objects.get(name='test_playlist')
            self.assertEqual(playlist.name, 'test_playlist')
        else:
            self.assertEqual(response, True)

'''
    Helper methods for use in testing
'''
def create_user_and_log_in(username, password, optional_username=None):
    user = add_user(username)
    user.set_password(password)
    user.save()

    if optional_username:
        profile_owner = add_user(optional_username)
        profile_owner.save()
    else:
        profile_owner = None

    return user, profile_owner


def add_user(username):
    user = User.objects.get_or_create(username=username)[0]
    user.save()
    return user


def add_rating(playlist, user, stars=0, comment="blank test comment"):
    rating = Rating.objects.get_or_create(user=user, playlist=playlist, stars=stars, comment=comment)[0]
    rating.save()

    return rating


def add_artist(name, webpage=None):
    artist = Artist.objects.get_or_create(name=name, webpage=webpage)[0]
    artist.save()

    return artist


def add_song(title, artist, link_spotify=None, link_other=None):
    song = Song.objects.get_or_create(title=title, artist=artist, linkToSpotify=link_spotify, linkOther=link_other)[0]
    song.save()

    return song


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
