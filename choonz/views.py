from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from choonz.models import Playlist, UserProfile, Song, Rating, Tag
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from choonz.forms import PlaylistForm, UserForm, UserProfileForm, RatingForm
from datetime import datetime
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from social_django.models import UserSocialAuth
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


'''

    Index View

'''


class IndexView(View):
    def get(self, request):
        # construct a dictionary to pass template engine as its context
        # boldmessage matches template variable in index.html
        # query database for all playlists, order by number of likes
        # retrieve only top 5, place in context_dict
        playlist_list = Playlist.objects.order_by('-likes')[:5]
        user_list = User.objects.order_by('-views')[:5]
        song_list = Song.objects.order_by('artist')

        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
        except:
            user = None
            user_profile = None

        context_dict = {}
        context_dict['boldmessage'] = 'Crunchy Tunes, Creamy Beats, Cookie Music Tastes, Like A Candy Treat!'
        context_dict['playlists'] = playlist_list
        context_dict['users'] = user_list
        context_dict['songs'] = song_list
        context_dict['user_profile'] = user_profile

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
        context_dict = {}

        visitor_cookie_handler(request)
        context_dict['visits'] = request.session['visits']

        return render(request, 'choonz/about.html', context_dict)


'''

    Playlist Views Section

'''


class ShowPlaylistView(View):

    def create_context_dict(self, playlist_name_slug, request):
        context_dict = {}
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
            ratings_by_user = list(Rating.objects.filter(user=user).values_list("playlist", flat=True))
            if playlist.id in ratings_by_user:
                context_dict['user_has_rated'] = True
                rating = Rating.objects.get(playlist=playlist, user=user)
                context_dict['rating'] = rating
            else:
                context_dict['user_has_rated'] = False
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
        form = PlaylistForm()
        return render(request, 'choonz/add_playlist.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = PlaylistForm(request.POST)

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
            return redirect(reverse('choonz:playlist_editor', kwargs={'playlist_name_slug': playlist.slug}))
        else:
            # form contained errors
            # print them to the terminal
            print(form.errors)

        return render(request, 'choonz/add_playlist.html', {'form': form})


class ListPlaylistView(View):
    @method_decorator(login_required)
    def get(self, request):
        playlists = Playlist.objects.filter(public=True)

        return render(request, 'choonz/list_playlists.html', {'playlist_list': playlists})


class PlaylistEditorView(View):
    @method_decorator(login_required)
    def get(self, request, playlist_name_slug):
        user_profile = UserProfile.objects.get(user=request.user)
        context_dict = {}
        context_dict['playlist_name_slug'] = playlist_name_slug

        return render(request, 'choonz/playlist_editor.html', context_dict)


class PlaylistRatingView(View):
    @method_decorator(login_required)
    def get(self, request, playlist_name_slug):
        playlist = Playlist.objects.get(slug=playlist_name_slug)
        form = RatingForm()
        context_dict = {'form': form, 'playlist': playlist}
        return render(request, 'choonz/rate_playlist.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, playlist_name_slug):
        playlist = Playlist.objects.get(slug=playlist_name_slug)
        if request.POST.get('rating'):
            rating = Rating.objects.get(id=request.POST.get('rating'))
            form = RatingForm()
            context_dict = {'form': form, 'playlist': playlist, 'rating': rating}
            return render(request, 'choonz/rate_playlist.html', context_dict)
        else:
            form = RatingForm(request.POST)

            # if the form valid?
            if form.is_valid():
                try:
                    rating = Rating.objects.get(user=request.user, playlist=playlist)
                    rating.stars = request.POST.get('stars')
                    rating.comment = request.POST.get('comment')
                    rating.date = datetime.today()
                    rating.save()

                except Rating.DoesNotExist:
                    rating = form.save(commit=False)
                    rating.user = request.user
                    rating.playlist = playlist
                    rating.date = datetime.today()
                    form.save(commit=True)

                context_dict = {}
                context_dict["playlist"] = playlist
                context_dict["songs"] = playlist.get_song_list
                return redirect(reverse('choonz:show_playlist', kwargs={'playlist_name_slug': playlist_name_slug}))
            else:
                # form contained errors
                # print them to the terminal
                print(form.errors)

            context_dict = {'form': form, 'playlist': playlist}
            return render(request, 'choonz/rate_playlist.html', context=context_dict)


class DraftView(View):
    @method_decorator(login_required)
    def get(self, request):
        profiles = UserProfile.objects.all()

        return render(request, 'choonz/drafts.html')


'''
class LikePlaylistView(View):
    @method_decorator(login_required)
    def get(self, request):
        playlist_id = request.GET.get('playlist_id')

        try:
            playlist = Playlist.objects.get(id=int(playlist_id))  # remember to cast int
        except Playlist.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        playlist.likes = playlist.likes + 1
        playlist.save()

        return HttpResponse(playlist.likes) # redirect(reverse('choonz:show_playlist', kwargs={'playlist_name_slug': playlist.slug}))
'''

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


class TagSuggestionView(View):
    def get(self, request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''

        # possibly change the ordering to be by number of playlists?
        tag_list = get_tag_list(max_results=8, starts_with=suggestion).order_by('description')

        # if nothing is written in the field so we want to show all or nothing?
        # if len(tag_list) == 0:
        #    tag_list = [] #Tag.objects.order_by('description')

        return render(request, 'choonz/tags.html', {'tags': tag_list})


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
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('choonz:index'))

        # All Playlists made by the profile owner
        playlists = Playlist.objects.filter(creator=user)

        public_playlists = Playlist.objects.filter(creator=user, public=True)
        draft_playlists = Playlist.objects.filter(creator=user, public=False)
        popular_playlists = public_playlists.order_by("-views")[:10]

        # All Ratings the profile owner has given
        ratings_by_user = list(Rating.objects.filter(user=user).values_list("playlist", flat=True))

        all_rated_tags = []
        rated_playlists = []
        flat_tags = []
        tag_obs = None
        for i in range(0, len(ratings_by_user)):
            playlist_info = {}
            playlist = Playlist.objects.get(id=ratings_by_user[i])
            playlist_info["playlist"] = playlist.name
            playlist_info["slug"] = playlist.slug
            playlist_info["averageRating"] = playlist.averageRating
            playlist_info["numberOfRatings"] = playlist.numberOfRatings
            playlist_info["tags"] = playlist.get_playlist_tag_list
            try:
                rating = Rating.objects.get(user=user, playlist=playlist)
                playlist_info["stars"] = rating.stars
            except Rating.DoesNotExist:
                playlist_info["stars"] = 0
            try:
                all_rated_tags.append(playlist_info['tags'])
                for i in all_rated_tags:
                  for j in i:
                    flat_tags.append(j)

                tag_obs = Tag.objects.filter(description__in=flat_tags)
            except:
                flat_tags = None
                tag_obs = None

            rated_playlists.append(playlist_info)
            # most_common_tags = rated_playlists.values("tags").annotate(count=Count('tags')).order_by("-count")
        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form,
                        'public_playlists': public_playlists, 'draft_playlists': draft_playlists,
                        'rated_playlists': rated_playlists, 'popular_playlists': popular_playlists,
                        'all_rated_tags':all_rated_tags, 'flat_tags':flat_tags, 'tag_obs':tag_obs}
        # , "common_tags":most_common_tags}

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


class ListProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        profiles = UserProfile.objects.all()

        return render(request, 'choonz/list_profiles.html', {'user_profile_list': profiles})


'''

    Misc Views/Methods

'''


class RestrictedView(View):
    def setup(self):
        SPOTIPY_CLIENT_ID = 'e09593bcb854470184181ebe501205af'
        SPOTIPY_CLIENT_SECRET = '35de71dede0449cd9df50f1f6fabc1d2'
        cid = SPOTIPY_CLIENT_ID
        secret = SPOTIPY_CLIENT_SECRET
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))
        return sp

    @method_decorator(login_required)
    def get(self, request):
        sp = self.setup()
		
        tracks = []
		
        results = sp.search(q='dolly parton', limit=20)
        for idx, track in enumerate(results['tracks']['items']):
            tracks.append(track['name'])
        context_dict = {}
        context_dict['tracks'] = tracks
        return render(request, 'choonz/restricted.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        sp = self.setup()
        results_list = []

        results = sp.search(q=request.POST.get('query'), limit=20)
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
        print(context_dict)
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
