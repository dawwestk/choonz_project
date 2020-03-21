from django.urls import path
from choonz import views
from choonz.templatetags import choonz_template_tags
from choonz.views import AboutView, AddPlaylistView, IndexView, PlaylistRatingView, ShowPlaylistView, SearchSpotifyView,\
    RegisterProfileView, ProfileView, ListPlaylistView, TagSuggestionView, PlaylistEditorView, \
    AddSongView, ImportPlaylistView, RemoveSongView, PlaylistSuggestionView, DeletePlaylistView, \
    AddSongDetailView
# AddPageView,GoToView, SearchAddPage LikePlaylistView, 


app_name = 'choonz'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('add_playlist/', views.AddPlaylistView.as_view(), name='add_playlist'),
    path('list_playlists/', views.ListPlaylistView.as_view(), name='list_playlists'),
    path('playlist/<slug:playlist_name_slug>/', views.ShowPlaylistView.as_view(), name='show_playlist'),
    path('playlist/<slug:playlist_name_slug>/rate_playlist/', views.PlaylistRatingView.as_view(), name='rate_playlist'),
    path('playlist/<slug:playlist_name_slug>/edit_playlist/', views.PlaylistEditorView.as_view(), name='edit_playlist'),
    path('playlist/<slug:playlist_name_slug>/edit_playlist/add_song/', views.AddSongView.as_view(), name='add_song'),
    path('playlist/<slug:playlist_name_slug>/edit_playlist/remove_song/', views.RemoveSongView.as_view(), name='remove_song'),
    path('playlist/<slug:playlist_name_slug>/edit_playlist/delete_playlist/', views.DeletePlaylistView.as_view(), name='delete_playlist'),
    path('playlist/<slug:playlist_name_slug>/import/', views.ImportPlaylistView.as_view(), name='import_playlist'),
    path('search_spotify/', views.SearchSpotifyView.as_view(), name='search_spotify'),
    path('register_profile/', views.RegisterProfileView.as_view(), name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<username>/my_stats/', views.MyStatsView.as_view(), name='my_stats'),
    path('publish_playlist/', views.PublishPlaylistView.as_view(), name='publish_playlist'),
    path('suggest_tag/', views.TagSuggestionView.as_view(), name='suggest_tag'),
    path('suggest_playlist/', views.PlaylistSuggestionView.as_view(), name='suggest_playlist'),
    path('filter_playlists/', views.PlaylistFilterView.as_view(), name='filter_playlists'),
    path('add_new_song_details/', views.AddSongDetailView.as_view(), name='add_new_song_details'),
]