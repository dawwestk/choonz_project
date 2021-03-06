from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from choonz.models import Playlist, UserProfile, Song, Rating, Tag, Artist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from choonz.forms import PlaylistForm, UserProfileForm, RatingForm
from choonz.templatetags import choonz_template_tags
from datetime import datetime, timedelta
import pytz
import collections
from django.views import View
from django.utils.decorators import method_decorator
from django.template.defaultfilters import slugify
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings
from django.db.models import Avg, Count

'''

    Index View

'''


class IndexView(View):
    def get(self, request):
        user_profile = get_user_profile(request)
        num_playlists_in_filter = 8

        # Playlists are split into most rated, highest rated and recently created for Index Page
        most_rated_playlists = Playlist.objects.annotate(num_ratings=Count('rating')).order_by('-num_ratings')[
                               :num_playlists_in_filter]
        highest_rated_playlists = Playlist.objects.annotate(
            average_rating=Avg('rating__stars')).order_by('-average_rating')
        recently_created_playlists = Playlist.objects.all().order_by('-createdDate')[:num_playlists_in_filter]

        # Highly rated are split into weekly/monthly
        this_week = datetime.today() - timedelta(days=7)
        this_month = datetime.today() - timedelta(days=31)
        playlists_this_week = highest_rated_playlists.filter(createdDate__gte=this_week)[:num_playlists_in_filter]
        playlists_this_month = highest_rated_playlists.filter(createdDate__gte=this_month)[:num_playlists_in_filter]

        context_dict = {'boldmessage': 'Crunchy Tunes, Creamy Beats, Cookie Music Tastes, Like A Candy Treat!',
                        'most_rated_playlists': most_rated_playlists,
                        'highest_rated_playlists': highest_rated_playlists[:num_playlists_in_filter],
                        'playlists_this_week': playlists_this_week,
                        'playlists_this_month': playlists_this_month,
                        'recent_playlists': recently_created_playlists, 'user_profile': user_profile}

        # return rendered response to send to the client
        response = render(request, 'choonz/index.html', context=context_dict)
        return response


'''

    About View

'''


class AboutView(View):
    def get(self, request):
        user_profile = get_user_profile(request)
        context_dict = {'user_profile': user_profile}
        visitor_cookie_handler(request)
        context_dict['visits'] = request.session['visits']

        return render(request, 'choonz/about.html', context_dict)


class ContactView(View):
    def get(self, request):
        user_profile = get_user_profile(request)
        context_dict = {'user_profile': user_profile}

        return render(request, 'choonz/contact.html', context_dict)


'''

    Playlist Views Section

'''


class ShowPlaylistView(View):
    # Helper method creates context dictionary with Playlist/User details
    def create_context_dict(self, playlist_name_slug, request):
        user_profile = get_user_profile(request)
        context_dict = {'user_profile': user_profile}
        user = request.user
        context_dict['user'] = user
        try:
            # find playlist from slug?
            playlist = Playlist.objects.get(slug=playlist_name_slug)

            # retrieve all users in this playlist (using filter())
            songs = Song.objects.filter(playlist=playlist)

            # Add results to context dict
            context_dict['songs'] = songs

            # Also add playlist to verify (in the template) it exists
            context_dict['playlist'] = playlist

            all_ratings = Rating.objects.filter(playlist_id=playlist.id)
            context_dict['ratings'] = all_ratings

            # All Ratings the profile owner has given
            try:
                ratings_by_user = list(Rating.objects.filter(user=user).values_list("playlist", flat=True))
                if playlist.id in ratings_by_user:
                    context_dict['user_has_rated'] = True
                    rating = Rating.objects.get(playlist=playlist, user=user)
                    context_dict['rating'] = rating
                else:
                    context_dict['user_has_rated'] = False
            except:
                context_dict['user_has_rated'] = None
                context_dict['rating'] = None
        except Playlist.DoesNotExist:
            context_dict['playlist'] = None
            context_dict['songs'] = None
            context_dict['user_has_rated'] = None
            context_dict['rating'] = None
            context_dict['ratings'] = None

        return context_dict

    # Viewing a playlist does not require a login
    def get(self, request, playlist_name_slug):
        context_dict = self.create_context_dict(playlist_name_slug, request)
        return render(request, 'choonz/playlist.html', context_dict)

    # Posting a rating does require a login
    @method_decorator(login_required)
    def post(self, request, playlist_name_slug):
        context_dict = self.create_context_dict(playlist_name_slug, request)

        return render(request, 'choonz/playlist.html', context_dict)


class AddPlaylistView(View):
    @method_decorator(login_required)
    def get(self, request):
        user_profile = get_user_profile(request)
        context_dict = {'user_profile': user_profile}
        form = PlaylistForm()
        context_dict['form'] = form
        return render(request, 'choonz/add_playlist.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        form = PlaylistForm(request.POST)
        user_profile = get_user_profile(request)
        context_dict = {'user_profile': user_profile}

        # is the form valid?
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.creator = request.user
            playlist.save()
            if request.POST.get('tags'):
                tag_string = request.POST.get('tags')
                tag_string = tag_string.replace(', ', ',')
                tag_list = tag_string.split(',')
                for t in tag_list:
                    if t:
                        found_tag = Tag.objects.get(description=t)
                        playlist.tags.add(found_tag)
                playlist.save()
            # redirect back to index
            return redirect(reverse('choonz:edit_playlist', kwargs={'playlist_name_slug': playlist.slug}))
        else:
            # form contained errors
            # print them to the terminal
            print(form.errors)
        context_dict['form'] = form

        return render(request, 'choonz/add_playlist.html', context_dict)


class PlaylistEditorView(View):
    @method_decorator(login_required)
    def get(self, request, playlist_name_slug):
        user_profile = get_user_profile(request)
        playlist = Playlist.objects.get(slug=playlist_name_slug)

        # Give user opportunity to edit any of their own playlists
        playlist_list = Playlist.objects.filter(creator=request.user)

        context_dict = {'user_profile': user_profile, 'playlist': playlist, 'playlist_name_slug': playlist_name_slug,
                        'playlist_list': playlist_list}

        return render(request, 'choonz/edit_playlist.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, playlist_name_slug):
        playlist = Playlist.objects.get(slug=playlist_name_slug)

        # Response dictionary used to flag whether playlist edit was successful or not
        response_dict = {'status': False}

        # Trying to edit the playlist name
        if request.POST.get('playlist_name'):
            new_name = request.POST.get('playlist_name')
            playlist.name = new_name
            try:
                playlist.save()
            except:
                response_dict['message'] = "Playlist name already exists!"
                return HttpResponse(json.dumps(response_dict), content_type="application/json")

        # Editing the playlist description
        if request.POST.get('playlist_description'):
            new_description = request.POST.get('playlist_description')
            playlist.description = new_description
            try:
                playlist.save()
            except:
                # Description doesn't need to be unique, but there could be a database error
                print("description error")

        # If tags are being updated
        if request.POST.get('playlist_tags'):
            # Process tag string
            new_tags = request.POST.get('playlist_tags')
            tag_string = new_tags.replace(', ', ',')
            tag_list = tag_string.split(',')
            for t in tag_list:
                # Search for each tag in database
                if t:
                    found_tag = Tag.objects.get(description=t)
                    playlist.tags.add(found_tag)
            try:
                # Clear old tags, save
                playlist.tags.clear()
                playlist.save()
            except:
                response_dict['message'] = "Invalid tags!"
                return HttpResponse(json.dumps(response_dict), content_type="application/json")

        response_dict['status'] = True
        response_dict['message'] = "Playlist details updated"
        return HttpResponse(json.dumps(response_dict), content_type="application/json")


class AddSongDetailView(View):
    @method_decorator(login_required)
    def get(self, request):
        playlist_slug = request.GET['playlist_slug']
        song_slug = request.GET['song_slug']
        context_dict = choonz_template_tags.get_song_detail_for_edit_page(playlist_slug, song_slug)
        return render(request, 'choonz/edit_playlist_new_song.html', context_dict)


class PlaylistRatingView(View):
    @method_decorator(login_required)
    def post(self, request, playlist_name_slug):
        playlist = Playlist.objects.get(slug=playlist_name_slug)
        user_profile = get_user_profile(request)
        form = RatingForm(request.POST)

        # is the form valid?
        if form.is_valid():
            try:
                # Update an already existing rating
                rating = Rating.objects.get(user=request.user, playlist=playlist)
                rating.stars = request.POST.get('stars')
                rating.comment = request.POST.get('comment')
                rating.date = datetime.now(pytz.utc)
                rating.save()

            except Rating.DoesNotExist:
                # If not found, create a new rating
                rating = form.save(commit=False)
                rating.user = request.user
                rating.playlist = playlist
                rating.date = datetime.now(pytz.utc)
                form.save(commit=True)

            all_ratings = Rating.objects.filter(playlist=playlist)
            context_dict = {'user_profile': user_profile, "playlist": playlist, "songs": playlist.get_song_list,
                            'rating': rating, 'user_has_rated': True, 'ratings': all_ratings}
            return render(request, 'choonz/playlist.html', context_dict)
        else:
            # form contained errors
            # print them to the terminal
            print(form.errors)

        context_dict = {'user_profile': user_profile, 'form': form, 'playlist': playlist, 'user_has_rated': False}
        return render(request, 'choonz/playlist.html', context=context_dict)


# Process the other URL to ensure it has the relevant prefix
def check_other_url(url):
    if not 'www.' in url:
        url = 'www.' + url
    if not 'https://' in url:
        url = 'https://' + url
    elif not 'http://' in url:
        url = 'http://' + url
    return url


class AddSongView(View):
    @method_decorator(login_required)
    def get(self, request, playlist_name_slug):
        song_slug = request.GET.get('song_slug')
        song = Song.objects.get(slug=song_slug)

        if request.GET.get('link_to_spotify'):
            song.linkToSpotify = request.GET.get('link_to_spotify')

        if request.GET.get('link_other'):
            song.linkOther = check_other_url(request.GET.get('link_other'))

        song.save()

        return HttpResponse(True)

    @method_decorator(login_required)
    def post(self, request, playlist_name_slug):
        playlist_slug = request.POST.get('playlist_slug')

        # Response dictionary shows whether addition of song to playlist was successful
        response_dict = {'status': False}

        # Find the playlist (or stop method)
        try:
            playlist = Playlist.objects.get(slug=playlist_slug)  # remember to cast int
        except Playlist.DoesNotExist:
            response_dict['message'] = "Playlist does not exist!"
            return HttpResponse(json.dumps(response_dict), content_type="application/json")
        except ValueError:
            response_dict['message'] = "Value error, please check song details"
            return HttpResponse(json.dumps(response_dict), content_type="application/json")

        # Pull relevant data from POST request
        song_title = request.POST.get('song_title')
        song_artist = request.POST.get('song_artist')
        artist_slug = slugify(song_artist)

        # Does the artist already exist? If not, create
        try:
            artist = Artist.objects.get(slug=artist_slug)
        except Artist.DoesNotExist:
            artist = Artist.objects.create(name=song_artist)

        # Get or create the song - check for invalid charaters
        try:
            song = Song.objects.get_or_create(artist=artist, title=song_title)[0]
        except ValueError:
            response_dict['message'] = "Value error, please check song details"
            return HttpResponse(json.dumps(response_dict), content_type="application/json")

        # If the song is already on the playlist, are the details being updated?
        updated_song_details = False
        if request.POST.get('link_to_spotify'):
            form_input_spotify_url = request.POST.get('link_to_spotify')
            spotify_url = 'https://open.spotify.com/'

            # Check whether the user has copied the open.spotify.com section
            if spotify_url in form_input_spotify_url:
                link_to_spotify = form_input_spotify_url
            elif spotify_url[8:] in form_input_spotify_url:
                link_to_spotify = 'https://' + form_input_spotify_url
            else:
                link_to_spotify = spotify_url + request.POST.get('link_to_spotify')
            song.linkToSpotify = link_to_spotify
            updated_song_details = True
        if request.POST.get('link_other'):
            link_other = request.POST.get('link_other')
            song.linkOther = link_other
            updated_song_details = True

        song.save()

        # Song already features on this playlist
        if song in playlist.get_song_list:
            if updated_song_details:
                response_dict['status'] = True
                response_dict['message'] = "Song data updated"
                return HttpResponse(json.dumps(response_dict), content_type="application/json")
            else:
                response_dict['status'] = True
                response_dict['message'] = "Song already on playlist"
                return HttpResponse(json.dumps(response_dict), content_type="application/json")
        else:
            playlist.songs.add(song)
            playlist.save()

        response_dict['status'] = True
        response_dict['message'] = "Song successfully added to playlist"
        response_dict['new_slug'] = song.slug
        return HttpResponse(json.dumps(response_dict), content_type="application/json")


class RemoveSongView(View):
    @method_decorator(login_required)
    def post(self, request, playlist_name_slug):
        playlist_slug = request.POST.get('playlist_slug')

        if not request.POST.get('confirmed'):
            return HttpResponse(-1)

        response_dict = {'status': False}

        try:
            playlist = Playlist.objects.get(slug=playlist_slug)  # remember to cast int
        except Playlist.DoesNotExist:
            response_dict['message'] = "Playlist does not exist!"
            return HttpResponse(json.dumps(response_dict), content_type="application/json")
        except ValueError:
            response_dict['message'] = "Value error, please check song details"
            return HttpResponse(json.dumps(response_dict), content_type="application/json")

        # Identify the song by its slug
        song_slug = request.POST.get('song_slug')
        song = Song.objects.get(slug=song_slug)

        # Song already features on this playlist
        if song in playlist.get_song_list:
            playlist.songs.remove(song)
            response_dict['status'] = True
            response_dict['message'] = "Song removed from playlist"
            return HttpResponse(json.dumps(response_dict), content_type="application/json")
        else:
            response_dict['message'] = "Song not on playlist"
            return HttpResponse(json.dumps(response_dict), content_type="application/json")


class PublishPlaylistView(View):
    @method_decorator(login_required)
    def get(self, request):
        playlist_id = request.GET['playlist_id']

        try:
            playlist = Playlist.objects.get(id=int(playlist_id))  # remember to cast int
        except Playlist.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        # GET method used to make playlist hidden (not public)
        playlist.public = False
        playlist.save()
        user = request.user

        return redirect(reverse('choonz:show_playlist', kwargs={'playlist_name_slug': playlist.slug}))

    @method_decorator(login_required)
    def post(self, request):
        playlist_id = request.POST['playlist_id']

        try:
            playlist = Playlist.objects.get(id=int(playlist_id))  # remember to cast int
        except Playlist.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        # POST method used to make playlist public
        playlist.public = True
        playlist.save()
        user = request.user

        return redirect(reverse('choonz:show_playlist', kwargs={'playlist_name_slug': playlist.slug}))


class DeletePlaylistView(View):
    @method_decorator(login_required)
    def post(self, request, playlist_name_slug):
        playlist_id = request.POST['playlist_id']

        try:
            playlist = Playlist.objects.get(id=int(playlist_id))  # remember to cast int
        except Playlist.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        playlist.delete()
        user = request.user

        return redirect(reverse('choonz:profile', kwargs={'username': user.username}))


class PlaylistFilterView(View):
    def get(self, request):
        user_profile = get_user_profile(request)

        # Process filter data - clean tags
        if 'tags' in request.GET:
            tags = request.GET['tags']
            tags = tags.split(",")
            tags = [slugify(t) for t in tags]
        else:
            tags = ''

        # Process filter data - collect creator info
        if 'creator' in request.GET:
            creator = request.GET['creator']
        else:
            creator = ''

        # Process filter data - collect date info
        if 'createdDate' in request.GET:
            created_date = request.GET['createdDate']
        else:
            created_date = ''

        # Send to helper method
        playlist_list = filter_playlists(tags, creator, created_date)

        if len(playlist_list) == 0:
            playlist_list = Playlist.objects.order_by('name')

        context_dict = {'user_profile': user_profile, 'playlist_suggestions': playlist_list,
                        'user': request.GET.get('user'), 'tags_wanted': True, 'minimised_stars': True}

        return render(request, 'choonz/playlist_suggestion.html', context_dict)


def filter_playlists(tags, creator, created_date):
    # Start with all playlist objects
    playlist_list = Playlist.objects.all()

    # If the user provided tags to filter by
    if tags:
        for t in tags:
            if t:
                # List all playlists which contain these tags
                playlist_list = playlist_list.filter(tags__slug__contains=t)

    # If the user provided a creator to search by
    if creator:
        # Filter playlists by creator = <username provided>
        try:
            creator = User.objects.get(username=creator)
        except User.DoesNotExist:
            creator = None
        except:
            creator = None
        playlist_list = playlist_list.filter(creator=creator)

    # If a date was given, filter by it (greater than or equal to it)
    # i.e. Playlists made ON or AFTER date
    if created_date:
        playlist_list = playlist_list.filter(createdDate__gte=created_date)

    return playlist_list


class ListPlaylistView(View):
    @method_decorator(login_required)
    def get(self, request):
        user_profile = get_user_profile(request)
        playlists = Playlist.objects.filter(public=True)
        context_dict = {'user_profile': user_profile, 'playlist_list': playlists}

        return render(request, 'choonz/list_playlists.html', context_dict)


class PlaylistSuggestionView(View):
    def get(self, request):
        user_profile = get_user_profile(request)

        # If the search input is not blank, filter by it
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''

        playlist_list = get_playlist_list(max_results=10, starts_with=suggestion)

        if len(playlist_list) == 0:
            playlist_list = Playlist.objects.order_by('name')

        context_dict = {'user_profile': user_profile, 'playlist_suggestions': playlist_list,
                        'user': request.GET.get('user'), 'tags_wanted': True, 'minimised_stars': True}

        return render(request, 'choonz/playlist_suggestion.html', context_dict)


def get_playlist_list(max_results=0, starts_with=''):
    # Initially, suggestion list is empty
    playlist_list = []

    # If playlists begin with suggestion text, add them
    if starts_with:
        playlist_list = Playlist.objects.filter(name__istartswith=starts_with)

    # Slice results to limit list of suggestions
    if max_results > 0:
        if len(playlist_list) > max_results:
            playlist_list = playlist_list[:max_results]

    return playlist_list


class TagSuggestionView(View):
    @method_decorator(login_required)
    def get(self, request):
        user_profile = get_user_profile(request)
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''

        tag_list = get_tag_list(max_results=10, starts_with=suggestion).order_by('description')

        # If nothing is written in the field show all
        if len(tag_list) == 0:
            if suggestion == '*':
                tag_list = Tag.objects.order_by('description')
            else:
                tag_list = None

        context_dict = {'user_profile': user_profile, 'tags': tag_list}

        return render(request, 'choonz/tags.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        tag_text = request.POST.get('tag_text')

        # Slugify tag to ensure uniqueness
        tag_slug = slugify(tag_text)
        response_dict = {'status': False}

        try:
            tag = Tag.objects.get(slug=tag_slug)
            response_dict['message'] = "Tag already exists - check your spelling!"
            return HttpResponse(json.dumps(response_dict), content_type="application/json")
        except Tag.DoesNotExist:
            tag = Tag.objects.create(description=tag_text)
            tag.save()
            response_dict['status'] = True
            response_dict['message'] = "Tag \"" + tag_text + "\" added!"
            return HttpResponse(json.dumps(response_dict), content_type="application/json")
        except:
            response_dict['message'] = "Invalid create-tag string"
            return HttpResponse(json.dumps(response_dict), content_type="application/json")


def get_tag_list(max_results=0, starts_with=''):
    tag_list = []

    if starts_with:
        tag_list = Tag.objects.filter(description__istartswith=starts_with)

    if max_results > 0:
        if len(tag_list) > max_results:
            tag_list = tag_list[:max_results]

    return tag_list


'''
    ------------------------------------------------------------------------------------

    Profile Views section
    
    ------------------------------------------------------------------------------------
'''


class RegisterProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = UserProfileForm()
        context_dict = {'form': form}
        return render(request, 'choonz/profile_registration.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        profile_form = UserProfileForm(request.POST, request.FILES)
        # if the form is valid
        if profile_form.is_valid():
            # now sort out the UserProfile instance
            # needed the User attribute first so commit = False for now
            profile = profile_form.save(commit=False)
            profile.user = request.user

            profile.save()
            return redirect(reverse('choonz:index'))
        else:
            print(profile_form.errors)

        context_dict = {'form': profile_form}
        return render(request, 'choonz/profile_registration.html', context_dict)


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'picture': user_profile.picture})

        return (user, user_profile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, page_user_profile, form) = self.get_user_details(username)
            if username != request.user.username:
                # visiting someone else's profile
                my_user_profile = get_user_profile(request)
            else:
                my_user_profile = page_user_profile
        except TypeError:
            return redirect(reverse('choonz:index'))

        # Filter playlists for different displays
        public_playlists = Playlist.objects.filter(creator=user, public=True)
        draft_playlists = Playlist.objects.filter(creator=user, public=False)
        popular_playlists = Playlist.objects.filter(creator=user).annotate(
            average_rating=Avg('rating__stars')).order_by('-average_rating')[:10]

        # All Ratings the profile owner has given
        ratings_by_user = list(Rating.objects.filter(user=user).values_list("playlist", flat=True).order_by('-stars'))

        all_rated_tags = []
        rated_playlists = []
        tag_obs = {}

        # Need to create a dictionary to list rated playlists with both playlist info
        # and info related to the user's rating of said playlist
        for i in range(0, len(ratings_by_user)):
            playlist_info = {}
            playlist = Playlist.objects.get(id=ratings_by_user[i])
            playlist_info["playlist"] = playlist.name
            playlist_info["slug"] = playlist.slug
            playlist_info["averageRating"] = playlist.get_average_rating
            playlist_info["numberOfRatings"] = playlist.get_number_of_ratings
            playlist_info["tags"] = playlist.get_playlist_tag_descriptions
            playlist_info['tag_list'] = playlist.get_playlist_tag_descriptions_as_string
            try:
                rating = Rating.objects.get(user=user, playlist=playlist)
                playlist_info["stars"] = rating.stars
            except Rating.DoesNotExist:
                playlist_info["stars"] = 0

            if playlist_info["stars"] >= 2.5:
                for j in playlist_info['tags']:
                    try:
                        tag_obs[j] = tag_obs[j] + 1
                    except:
                        tag_obs[j] = 1
                    all_rated_tags.append(tag_obs)

            rated_playlists.append(playlist_info)

        # Tags are sorted by number of times rated
        sorted_tag_obs = sort_dicts_by_values(tag_obs, True, 10)
        tag_obs = collections.OrderedDict(sorted_tag_obs)
        playlist_suggestions = suggest_playlist_from_tags(tag_obs, user, ratings_by_user)
        context_dict = {'page_user_profile': page_user_profile, 'user_profile': my_user_profile, 'selected_user': user,
                        'form': form, 'public_playlists': public_playlists, 'draft_playlists': draft_playlists,
                        'rated_playlists': rated_playlists, 'popular_playlists': popular_playlists,
                        'all_rated_tags': all_rated_tags, 'tag_obs': tag_obs,
                        'playlist_suggestions': playlist_suggestions}

        return render(request, 'choonz/profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('choonz:index'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('choonz:profile', kwargs={'username': username}))
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}

        return render(request, 'choonz/profile.html', context_dict)


def sort_dicts_by_values(dict, reverse=False, limit=10):
    # Sort dictionary by values (largest first)
    return {key: val for key, val in sorted(dict.items(), reverse=reverse, key=lambda item: item[1])[:limit]}


def suggest_playlist_from_tags(tag_obs, user, already_rated):
    # User should not be suggested their own playlist
    all_playlists = Playlist.objects.exclude(creator=user)

    tag_count = {}
    recommendations = {}

    # To generate a % weighting for each tag, we need sum of number of ratings per tag
    total_tag_weighting = sum(tag_obs.values())

    # If there are tags with ratings
    if total_tag_weighting > 0:
        for tag in tag_obs:
            # Each tag should be given a % weighting
            tag_count[tag] = round(tag_obs[tag] / total_tag_weighting * 100)

        for playlist in all_playlists:
            # Only show playlists the user has NOT already rated in the past
            if playlist.id not in already_rated:
                # Count the number of tags on a playlist
                tags_on_playlist = len(playlist.get_playlist_tag_descriptions)

                # If there are tags - we might want to suggest this playlist
                if tags_on_playlist > 0:
                    tag_match_counter = 0
                    tag_match_percentage = 0

                    # Loop through tags on playlist
                    # IF the tag has a user-liking %, add this to total
                    # And increase the tag_match_counter (total number of tags which the user likes)
                    for tag in playlist.get_playlist_tag_descriptions:
                        try:
                            tag_match_percentage = tag_match_percentage + tag_count[tag]
                            tag_match_counter = tag_match_counter + 1
                        except:
                            continue
                    # How many of the tags on this playlist are on the user's tag list?
                    tag_match_coverage = round(tag_match_counter / tags_on_playlist, 2)
                    # How many of the users favourite tags are on there?
                    overall_percentage = round(tag_match_percentage * tag_match_coverage, 2)
                    if overall_percentage > 0:
                        recommendations[playlist] = overall_percentage
        recommendations = sort_dicts_by_values(recommendations, True, 10)

    return recommendations


'''

    Misc Views/Methods

'''


class ImportPlaylistView(View):
    @method_decorator(login_required)
    def get(self, request, playlist_name_slug):
        user_profile = get_user_profile(request)
        playlist = Playlist.objects.get(slug=playlist_name_slug)
        context_dict = {'user_profile': user_profile, 'playlist': playlist}

        return render(request, 'choonz/import_playlist.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, playlist_name_slug):

        # Create a connection to spotify
        sp = setup_spotify()
        choonz_playlist = Playlist.objects.get(slug=playlist_name_slug)

        # Collect Spotify username and playlist to search for
        username = request.POST.get('spotify_username')
        playlist_name = request.POST.get('spotify_playlist_name')

        # Find the user on Spotify, collect their playlists
        playlists = sp.user_playlists(username)
        while playlists:
            for i, playlist in enumerate(playlists['items']):
                # If the user has a playlist that matches the user input
                if playlist['name'] == playlist_name:
                    # Pull all songs from it
                    results = sp.playlist(playlist['id'], fields="tracks")
                    tracks = results['tracks']

                    # Use add_tracks method to add songs to the playlist
                    add_tracks(tracks, choonz_playlist)
                try:
                    if playlists['next']:
                        playlists = sp.next(playlists)
                    else:
                        playlists = None
                except:
                    playlists = None

        return redirect(reverse('choonz:show_playlist', kwargs={'playlist_name_slug': choonz_playlist.slug}))


# Parse tracks, pull out relevant info to add songs to database
def add_tracks(tracks, playlist):
    choonz_playlist = playlist
    for i, item in enumerate(tracks['items']):
        track = item['track']
        artist_name_slug = slugify(track['artists'][0]['name'])
        try:
            artist = Artist.objects.get(slug=artist_name_slug)
        except Artist.DoesNotExist:
            artist = Artist.objects.create(name=track['artists'][0]['name'])

        song_slug = slugify(track['name'] + "-" + track['artists'][0]['name'])
        try:
            song = Song.objects.get(slug=song_slug)
        except Song.DoesNotExist:
            song = Song.objects.create(title=track['name'], artist=artist)

        if track['external_urls']['spotify']:
            song.linkToSpotify = track['external_urls']['spotify']

        song.save()

        choonz_playlist.songs.add(song)
        choonz_playlist.save()
        print("Added " + track['artists'][0]['name'] + " - " + track['name'] + " to " + choonz_playlist.name)


def spotify_show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
                                    track['name']))


def setup_spotify():
    cid = settings.SPOTIPY_CLIENT_ID
    secret = settings.SPOTIPY_CLIENT_SECRET
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))
    return sp


class SearchSpotifyView(View):
    @method_decorator(login_required)
    def post(self, request):
        sp = setup_spotify()
        results_list = []

        # Pull search query from input
        query = request.POST.get('query')
        results = sp.search(q=query, limit=10)
        for idx, track in enumerate(results['tracks']['items']):
            # track + any of the below (and more)
            # ['popularity'], ['preview_url'], ['external_urls']['spotify']
            # ['album']['name'], ['album']['images'][0]
            # ['artists']['name']
            track_info = {'track_name': track['name'], 'album_name': track['album']['name'],
                          'artist_name': track['artists'][0]['name'], 'album_image': track['album']['images'][0]['url'],
                          'link': track['external_urls']['spotify']}

            results_list.append(track_info)
        context_dict = {'results': results_list, 'query': query}

        return HttpResponse(json.dumps(context_dict), content_type="application/json")


def visitor_cookie_handler(request):
    # get number of visits to site
    # use the COOKIES.get() function
    visits = int(get_server_side_cookie(request, 'visits', '1'))  # default = 1 if nothing found

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # if its been more than a day since last visit
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # update the last visit cookie
        request.session['last_visit'] = str(datetime.now())
    else:
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def get_user_profile(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None
    except:
        user_profile = None

    return user_profile


class MyStatsView(View):
    @method_decorator(login_required)
    def get(self, request, username):
        user = request.user
        user_profile = get_user_profile(request)
        selected_user = User.objects.get(username=username)
        context_dict = {'user_profile': user_profile, 'username': user.username, 'selected_user': selected_user}

        try:
            # if the user has rated anything
            user_ratings = Rating.objects.filter(user=user)
        except:
            user_ratings = None

        if user_ratings:
            number_of_ratings = user_ratings.count()
            user_favourite_playlist = user_ratings.order_by('-stars')[0].playlist
            user_least_favourite_playlist = user_ratings.order_by('stars')[0].playlist
            user_average_given_rating = user_ratings.aggregate(ave=Avg('stars')).get('ave')
        else:
            number_of_ratings = 0
            user_favourite_playlist = None
            user_least_favourite_playlist = None
            user_average_given_rating = 0

        user_stats = {'number_of_ratings': number_of_ratings, 'user_favourite_playlist': user_favourite_playlist,
                      'user_least_favourite_playlist': user_least_favourite_playlist, 'user_ratings': user_ratings,
                      'user_average_given_rating': user_average_given_rating}

        rating_dates = []
        rating_stars = []
        rating_playlist = []
        for r in user_ratings:
            rating_dates.append(r.date.strftime("%d/%m/%Y %H:%M:%S"))
            rating_stars.append(r.stars)
            rating_playlist.append(r.playlist.name)

        user_stats['rating_dates'] = rating_dates
        user_stats['rating_stars'] = rating_stars
        user_stats['rating_playlist'] = rating_playlist

        stats = {}
        try:
            # if the user has created any playlists
            playlists = Playlist.objects.filter(creator=user)
        except:
            playlists = None

        if playlists:
            try:
                user_playlist_average_rating = round(
                    playlists.aggregate(average_rating=Avg('rating__stars'))['average_rating'], 1)
            except:
                user_playlist_average_rating = 0

            most_rated_playlist = \
                Playlist.objects.filter(creator=user).annotate(num_ratings=Count('rating')).order_by('-num_ratings')[0]
            highest_rated_playlist = Playlist.objects.filter(creator=user).values('slug', 'name').annotate(
                average_rating=Avg('rating__stars')).order_by('-average_rating')[0]['name']

            stats = {'user_playlist_average_rating': user_playlist_average_rating,
                     'most_rated_playlist': most_rated_playlist,
                     'highest_rated_playlist': highest_rated_playlist}

            # arrays here are for graph production
            playlist_names = []
            playlist_aves = []
            all_playlists = []
            for playlist in playlists:
                playlist_names.append(playlist.name)
                try:
                    ave = round(playlist.get_average_rating, 1)
                except:
                    ave = 0
                playlist_aves.append(ave)
                all_playlists.append(playlist)
            stats['playlist_names'] = playlist_names
            stats['playlist_aves'] = playlist_aves
            stats['all'] = all_playlists

        context_dict['playlist_stats'] = stats
        context_dict['user_stats'] = user_stats
        return render(request, 'choonz/my_stats.html', context_dict)
