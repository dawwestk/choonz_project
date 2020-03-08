from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from choonz.models import Playlist, UserProfile, Song, Rating, Tag, Artist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from choonz.forms import PlaylistForm, UserForm, UserProfileForm, RatingForm
from datetime import datetime, timedelta
import pytz
import collections
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from social_django.models import UserSocialAuth
from django.template.defaultfilters import slugify
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings
from django.db.models import Avg, Q, Count

'''

    Index View

'''


class IndexView(View):
    def get(self, request):
        # construct a dictionary to pass template engine as its context
        # boldmessage matches template variable in index.html
        # query database for all playlists, order by number of likes
        # retrieve only top 5, place in context_dict
        user_profile = get_user_profile(request)

        most_rated_playlists = Playlist.objects.annotate(num_ratings=Count('rating')).order_by('-num_ratings')[:10]
        highest_rated_playlists = Playlist.objects.values('slug', 'name').annotate(
            average_rating=Avg('rating__stars')).order_by('-average_rating')[:10]
        recently_created_playlists = Playlist.objects.all().order_by('-createdDate')[:10]

        context_dict = {'boldmessage': 'Crunchy Tunes, Creamy Beats, Cookie Music Tastes, Like A Candy Treat!',
                        'most_rated_playlists': most_rated_playlists,
                        'highest_rated_playlists': highest_rated_playlists,
                        'recent_playlists': recently_created_playlists, 'user_profile': user_profile}

        # keep this call to increment the counter
        visitor_cookie_handler(request)

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
        visitor_cookie_handler(request)
        context_dict['visits'] = request.session['visits']

        return render(request, 'choonz/contact.html', context_dict)


'''

    Playlist Views Section

'''


class ShowPlaylistView(View):

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
            song_list = songs.order_by('title')
            # Add results to context dict
            context_dict['songs'] = song_list

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

    def get(self, request, playlist_name_slug):
        context_dict = self.create_context_dict(playlist_name_slug, request)
        return render(request, 'choonz/playlist.html', context_dict)

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
        # if the form valid?
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
        playlist_list = Playlist.objects.filter(creator=request.user)

        context_dict = {'user_profile': user_profile, 'playlist': playlist, 'playlist_name_slug': playlist_name_slug,
                        'playlist_list': playlist_list}

        return render(request, 'choonz/edit_playlist.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, playlist_name_slug):
        playlist = Playlist.objects.get(slug=playlist_name_slug)

        response_dict = {'status': False}

        if request.POST.get('playlist_name'):
            new_name = request.POST.get('playlist_name')
            playlist.name = new_name
            try:
                playlist.save()
            except:
                response_dict['message'] = "Playlist name already exists!"
                return HttpResponse(json.dumps(response_dict), content_type="application/json")
        if request.POST.get('playlist_description'):
            new_description = request.POST.get('playlist_description')
            playlist.description = new_description
            try:
                playlist.save()
            except:
                # description doesn't need to be unique - error?
                print("description error")
        if request.POST.get('playlist_tags'):
            playlist.tags.clear()
            new_tags = request.POST.get('playlist_tags')
            tag_string = new_tags.replace(', ', ',')
            tag_list = tag_string.split(',')
            for t in tag_list:
                if t:
                    found_tag = Tag.objects.get(description=t)
                    playlist.tags.add(found_tag)
            try:
                playlist.save()
            except:
                response_dict['message'] = "Invalid tags!"
                return HttpResponse(json.dumps(response_dict), content_type="application/json")

        response_dict['status'] = True
        response_dict['message'] = "Playlist details updated"
        return HttpResponse(json.dumps(response_dict), content_type="application/json")


class PlaylistRatingView(View):
    @method_decorator(login_required)
    def get(self, request, playlist_name_slug):
        user_profile = get_user_profile(request)
        playlist = Playlist.objects.get(slug=playlist_name_slug)
        form = RatingForm()
        context_dict = {'user_profile': user_profile, 'form': form, 'playlist': playlist}
        return render(request, 'choonz/rate_playlist.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, playlist_name_slug):
        playlist = Playlist.objects.get(slug=playlist_name_slug)
        user_profile = get_user_profile(request)
        if request.POST.get('rating'):
            rating = Rating.objects.get(id=request.POST.get('rating'))
            form = RatingForm()
            context_dict = {'user_profile': user_profile, 'form': form, 'playlist': playlist, 'rating': rating}
            return render(request, 'choonz/rate_playlist.html', context_dict)
        else:
            form = RatingForm(request.POST)

            # if the form valid?
            if form.is_valid():
                try:
                    rating = Rating.objects.get(user=request.user, playlist=playlist)
                    rating.stars = request.POST.get('stars')
                    rating.comment = request.POST.get('comment')
                    rating.date = datetime.now(pytz.utc)
                    rating.save()

                except Rating.DoesNotExist:
                    rating = form.save(commit=False)
                    rating.user = request.user
                    rating.playlist = playlist
                    rating.date = datetime.now(pytz.utc)
                    form.save(commit=True)

                context_dict = {'user_profile': user_profile, "playlist": playlist, "songs": playlist.get_song_list}
                return redirect(reverse('choonz:show_playlist', kwargs={'playlist_name_slug': playlist_name_slug}))
            else:
                # form contained errors
                # print them to the terminal
                print(form.errors)

            context_dict = {'user_profile': user_profile, 'form': form, 'playlist': playlist}
            return render(request, 'choonz/rate_playlist.html', context=context_dict)


class DraftView(View):
    @method_decorator(login_required)
    def get(self, request):
        user_profile = get_user_profile(request)
        profiles = UserProfile.objects.all()
        context_dict = {'user_profile': user_profile, 'profiles': profiles}

        return render(request, 'choonz/drafts.html', context_dict)


class AddSongView(View):
    @method_decorator(login_required)
    def post(self, request, playlist_name_slug):
        playlist_slug = request.POST.get('playlist_slug')

        response_dict = {'status': False}

        try:
            playlist = Playlist.objects.get(slug=playlist_slug)  # remember to cast int
        except Playlist.DoesNotExist:
            response_dict['message'] = "Playlist does not exist!"
            return HttpResponse(json.dumps(response_dict), content_type="application/json")
        except ValueError:
            response_dict['message'] = "Value error, please check song details"
            return HttpResponse(json.dumps(response_dict), content_type="application/json")

        song_title = request.POST.get('song_title')
        song_artist = request.POST.get('song_artist')
        artist_slug = slugify(song_artist)
        artist = None
        try:
            artist = Artist.objects.get(slug=artist_slug)
        except Artist.DoesNotExist:
            artist = Artist.objects.create(name=song_artist)

        try:
            song = Song.objects.get_or_create(artist=artist, title=song_title)[0]
        except ValueError:
            response_dict['message'] = "Value error, please check song details"
            return HttpResponse(json.dumps(response_dict), content_type="application/json")

        link_to_spotify = ''
        link_other = ''
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
        if updated_song_details:
            response_dict['status'] = True
            response_dict['message'] = "Song data updated"
            return HttpResponse(json.dumps(response_dict), content_type="application/json")

        # Song already features on this playlist
        if song in playlist.get_song_list:
            response_dict['status'] = True
            response_dict['message'] = "Song already on playlist"
            return HttpResponse(json.dumps(response_dict), content_type="application/json")
        else:
            playlist.songs.add(song)
            playlist.save()

        response_dict['status'] = True
        response_dict['message'] = "Song successfully added to playlist"
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

        playlist.public = True
        playlist.save()
        user = request.user

        return redirect(reverse('choonz:show_playlist', kwargs={'playlist_name_slug': playlist.slug}))


class PlaylistFilterView(View):
    def get(self, request):
        user_profile = get_user_profile(request)
        playlist_list = None
        if 'tags' in request.GET:
            tags = request.GET['tags']
            tags = tags.split(",")
            tags = [slugify(t) for t in tags]
        else:
            tags = ''

        if 'creator' in request.GET:
            creator = request.GET['creator']
        else:
            creator = ''

        if 'createdDate' in request.GET:
            created_date = request.GET['createdDate']
        else:
            created_date = ''

        playlist_list = filter_playlists(tags, creator, created_date)

        if len(playlist_list) == 0:
            playlist_list = Playlist.objects.order_by('name')

        context_dict = {'user_profile': user_profile, 'playlist_suggestions': playlist_list}

        return render(request, 'choonz/playlist_suggestion.html', context_dict)


def filter_playlists(tags, creator, created_date):
    playlist_list = Playlist.objects.all()

    if tags:
        for t in tags:
            if t:
                playlist_list = playlist_list.filter(tags__slug__contains=t)

    if creator:
        try:
            creator = User.objects.get(username=creator)
        except User.DoesNotExist:
            creator = None
        except:
            creator = None
        playlist_list = playlist_list.filter(creator=creator)

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
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''

        playlist_list = get_playlist_list(max_results=10, starts_with=suggestion)

        if len(playlist_list) == 0:
            playlist_list = Playlist.objects.order_by('name')

        context_dict = {'user_profile': user_profile, 'playlist_suggestions': playlist_list}

        return render(request, 'choonz/playlist_suggestion.html', context_dict)


def get_playlist_list(max_results=0, starts_with=''):
    playlist_list = []

    if starts_with:
        playlist_list = Playlist.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(playlist_list) > max_results:
            playlist_list = playlist_list[:max_results]

    return playlist_list


class TagSuggestionView(View):
    def get(self, request):
        user_profile = get_user_profile(request)
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''

        # possibly change the ordering to be by number of playlists?
        tag_list = get_tag_list(max_results=10, starts_with=suggestion).order_by('description')

        # if nothing is written in the field so we want to show all or nothing?
        if len(tag_list) == 0:
            tag_list = Tag.objects.order_by('description')

        context_dict = {'user_profile': user_profile, 'tags': tag_list}

        return render(request, 'choonz/tags.html', context_dict)


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
            # did the user provide a picture
            # if 'picture' in request.FILES:
            #    profile.picture = request.FILES['picture']

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

        public_playlists = Playlist.objects.filter(creator=user, public=True)
        draft_playlists = Playlist.objects.filter(creator=user, public=False)
        popular_playlists = Playlist.objects.filter(creator=user).annotate(average_rating=Avg('rating__stars')).order_by('-average_rating')[:10]

        # All Ratings the profile owner has given
        ratings_by_user = list(Rating.objects.filter(user=user).values_list("playlist", flat=True).order_by('-stars'))

        all_rated_tags = []
        rated_playlists = []
        tag_obs = {}
        for i in range(0, len(ratings_by_user)):
            playlist_info = {}
            playlist = Playlist.objects.get(id=ratings_by_user[i])
            playlist_info["playlist"] = playlist.name
            playlist_info["slug"] = playlist.slug
            playlist_info["averageRating"] = playlist.getAverageRating
            playlist_info["numberOfRatings"] = playlist.getNumberOfRatings
            playlist_info["tags"] = playlist.get_playlist_tag_descriptions
            try:
                rating = Rating.objects.get(user=user, playlist=playlist)
                playlist_info["stars"] = rating.stars
            except Rating.DoesNotExist:
                playlist_info["stars"] = 0

            if playlist_info["stars"] > 2.5:
                for j in playlist_info['tags']:
                    try:
                        tag_obs[j] = tag_obs[j] + 1
                    except:
                        tag_obs[j] = 1
                    all_rated_tags.append(tag_obs)

            rated_playlists.append(playlist_info)

        sorted_tag_obs = sort_dicts_by_values(tag_obs, True, 10)
        tag_obs = collections.OrderedDict(sorted_tag_obs)
        playlist_suggestions = suggest_playlist_from_tags(tag_obs, user)
        context_dict = {'page_user_profile': page_user_profile, 'user_profile': my_user_profile, 'selected_user': user,
                        'form': form,
                        'public_playlists': public_playlists, 'draft_playlists': draft_playlists,
                        'rated_playlists': rated_playlists, 'popular_playlists': popular_playlists,
                        'all_rated_tags': all_rated_tags, 'tag_obs': tag_obs, 'playlist_suggestions': playlist_suggestions}

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
    return {k: v for k, v in sorted(dict.items(), reverse=reverse, key=lambda item: item[1])[:limit]}

def suggest_playlist_from_tags(tag_obs, user):
    all_playlists = Playlist.objects.exclude(creator=user)
    tag_count = {}

    total_tag_weighting = sum(tag_obs.values())
    recommendations = {}

    for tag in tag_obs:
        tag_count[tag] = round(tag_obs[tag] / total_tag_weighting * 100)

    for playlist in all_playlists:
        tags_on_playlist = len(playlist.get_playlist_tag_descriptions)
        tag_match_counter = 0
        tag_match_percentage = 0
        for tag in playlist.get_playlist_tag_descriptions:
            try:
                tag_match_percentage = tag_match_percentage + tag_count[tag]
                tag_match_counter = tag_match_counter + 1
            except:
                continue
        tag_match_coverage = round(tag_match_counter/tags_on_playlist)
        overall_percentage = round(tag_match_percentage * tag_match_coverage)
        if overall_percentage > 0:
            recommendations[playlist] = overall_percentage

    recommendations = sort_dicts_by_values(recommendations, True, 10)
    return recommendations



class ListProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        user_profile = get_user_profile(request)
        profiles = UserProfile.objects.all()

        context_dict = {'user_profile': user_profile, 'user_profile_list': profiles}

        return render(request, 'choonz/list_profiles.html', context_dict)


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
        sp = setup_spotify()
        choonz_playlist = Playlist.objects.get(slug=playlist_name_slug)
        username = request.POST.get('spotify_username')
        playlist_name = request.POST.get('spotify_playlist_name')

        playlists = sp.user_playlists(username)
        while playlists:
            for i, playlist in enumerate(playlists['items']):
                if playlist['name'] == playlist_name:
                    # print(playlist)
                    # print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'], playlist['name']))
                    results = sp.playlist(playlist['id'], fields="tracks")
                    tracks = results['tracks']
                    add_tracks(tracks, choonz_playlist)
                try:
                    if playlists['next']:
                        playlists = sp.next(playlists)
                    else:
                        playlists = None
                except:
                    playlists = None

        return redirect(reverse('choonz:show_playlist', kwargs={'playlist_name_slug': choonz_playlist.slug}))


class TestView(View):
    @method_decorator(login_required)
    def get(self, request):
        sp = setup_spotify()
        username = request.user.username

        playlists = sp.user_playlists(username)
        while playlists:
            for i, playlist in enumerate(playlists['items']):
                print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'], playlist['name']))
                results = sp.playlist(playlist['id'], fields="tracks")
                tracks = results['tracks']
                spotify_show_tracks(tracks)
            if playlists['next']:
                playlists = sp.next(playlists)
            else:
                playlists = None

        return HttpResponse("Printed playlists")


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
    # SPOTIPY_CLIENT_ID = 'e09593bcb854470184181ebe501205af'
    # SPOTIPY_CLIENT_SECRET = '35de71dede0449cd9df50f1f6fabc1d2'
    cid = settings.SPOTIPY_CLIENT_ID
    secret = settings.SPOTIPY_CLIENT_SECRET
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))
    return sp


class RestrictedView(View):
    @method_decorator(login_required)
    def get(self, request):
        sp = setup_spotify()

        tracks = []

        results = sp.search(q='dolly parton', limit=20)
        for idx, track in enumerate(results['tracks']['items']):
            tracks.append(track['name'])
        context_dict = {}
        context_dict['tracks'] = tracks
        return render(request, 'choonz/restricted.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        sp = setup_spotify()
        results_list = []

        query = request.POST.get('query')
        results = sp.search(q=query, limit=20)
        for idx, track in enumerate(results['tracks']['items']):
            # track + any of the below (and more)
            # ['popularity'], ['preview_url'], ['external_urls']['spotify']
            # ['album']['name'], ['album']['images'][0]
            # ['artists']['name']
            track_info = {}
            track_info['track_name'] = track['name']
            track_info['album_name'] = track['album']['name']
            track_info['artist_name'] = track['artists'][0]['name']
            track_info['album_image'] = track['album']['images'][0]['url']
            track_info['link'] = track['external_urls']['spotify']
            results_list.append(track_info)
        context_dict = {}
        context_dict['results'] = results_list
        context_dict['query'] = query

        return render(request, 'choonz/restricted.html', context_dict)


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
                    ave = round(playlist.getAverageRating, 1)
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


'''
class StatsGraphView(View):
    @method_decorator(login_required)
    def get(self, request, username):
        def get_labels():
            return ["January", "February", "March", "April", "May", "June", "July"]

        def get_data():
            return [75, 44, 92, 11, 44, 95, 35]

        ratings = get_data()
        labels = get_labels()
        output = {'labels': labels, 'ratings': ratings}
        return HttpResponse(json.dumps(output), content_type="application/json")
'''

'''
@login_required
def add_playlist(request):
    form = PlaylistForm()

    # HTTP POST?
    if request.method == "POST":
        form = PlaylistForm(request.POST)

        # if the form valid?
        if form.is_valid():
            form.save(commit=True)
            # redirect back to index
            return redirect('/choonz/')
        else:
            # form contained errors
            # print them to the terminal
            print(form.errors)

    return render(request, 'choonz/add_playlist.html', {'form': form})


class AddPageView(View):
    def get_playlist_name(self, playlist_name_slug):
        try:
            playlist = Playlist.objects.get(slug=playlist_name_slug)
        except Playlist.DoesNotExist:
            playlist = None

        return playlist

    @method_decorator(login_required)
    def get(self, request, playlist_name_slug):
        form = PageForm()
        playlist = self.get_playlist_name(playlist_name_slug)

        if playlist is None:
            return redirect(reverse('choonz:index'))

        context_dict = {'form': form, 'playlist': playlist}
        return render(request, 'choonz/add_page.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, playlist_name_slug):
        form = PageForm(request.POST)
        playlist = self.get_playlist_name(playlist_name_slug)

        if playlist is None:
            return redirect(reverse('choonz:index'))

        if form.is_valid():
            page = form.save(commit=False)
            page.playlist = playlist
            page.views = 0
            page.save()

            return redirect(reverse('choonz:show_playlist', kwargs={'playlist_name_slug': playlist_name_slug}))
        else:
            print(form.errors)

        context_dict = {'form': form, 'playlist': playlist}
        return render(request, 'choonz/add_page.html', context_dict)
'''

'''
    --------------- Login/Registration code now handled by registration-redux
    
def register(request):
    registered = False

    if request.method == 'POST':
        # attempt to grab info from the raw form info
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # if the two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # now hash the password, and update
            user.set_password(user.password)
            user.save()

            # now sort out the UserProfile instance
            # needed the User attribute first so commit = False for now
            profile = profile_form.save(commit=False)
            profile.user = user

            # did the user provide a picture
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            # profile registrationg was successful
            registered = True
        else:
            # something was wrong on the forms
            print(user_form.errors, profile_form.errors)
    else:
        # not an HTTP POST
        # render blank forms for user input
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'choonz/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        # gather username and password from form
        # use request.POST.get('') as it returns None if not found
        # rather than a KeyError if we used request.POST['']
        username = request.POST.get('username')
        password = request.POST.get('password')

        # built-in django machinery checks if this combination is valid
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('choonz:index'))
            else:
                return HttpResponse("Your choonz account is disabled.")
        else:
            # login details do not match any User
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        # not a POST request
        return render(request, 'choonz/login.html')

@login_required
def user_logout(request):
    # We know the user is logged in because of the decorator
    logout(request)
    return redirect(reverse('choonz:index'))

    --------------- Login/Registration code now handled by registration-redux
'''

'''
def search(request):
    result_list = []
    query = ''
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
    return render(request, 'choonz/search.html', {'result_list': result_list, 'query': query})


class GoToView(View):
    def get(self, request):
        page_id = request.GET.get('page_id')
        try:
            page = Page.objects.get(id=page_id)
            page.views = page.views + 1
            page.save()
            return redirect(page.url)
        except Page.DoesNotExist:
            return redirect(reverse('index'))
'''

'''
class SearchAddPage(View):
    @method_decorator(login_required)
    def get(self, request):
        playlist_id = request.GET['playlist_id']
        title = request.GET['title']
        url = request.GET['url']

        try:
            playlist = Playlist.objects.get(id=int(playlist_id))
        except Playlist.DoesNotExist:
            return HttpResponse('Error - playlist not found.')
        except ValueError:
            return HttpResponse('Error - bad playlist ID.')

        p = Page.objects.get_or_create(playlist=playlist, title=title, url=url)

        pages = Page.objects.filter(playlist=playlist).order_by('-views')
        return render(request, 'choonz/page_listing.html', {'pages': pages})
'''
