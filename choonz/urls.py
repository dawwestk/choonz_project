from django.urls import path
from choonz import views
from choonz.views import AboutView, AddPlaylistView, IndexView, PlaylistRatingView, ShowPlaylistView, RestrictedView, RegisterProfileView, ProfileView, ListPlaylistView,  ListProfileView, TagSuggestionView, PlaylistEditorView, TestView, AddSongView, ImportPlaylistView, RemoveSongView, PlaylistSuggestionView
# AddPageView,GoToView, SearchAddPage LikePlaylistView, 


app_name = 'choonz'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('playlist/<slug:playlist_name_slug>/', views.ShowPlaylistView.as_view(), name='show_playlist'),
    path('add_playlist/', views.AddPlaylistView.as_view(), name='add_playlist'),
    path('list_playlists/', views.ListPlaylistView.as_view(), name='list_playlists'),
    path('playlist/<slug:playlist_name_slug>/rate_playlist/', views.PlaylistRatingView.as_view(), name='rate_playlist'),
    path('playlist/<slug:playlist_name_slug>/edit_playlist/', views.PlaylistEditorView.as_view(), name='edit_playlist'),
    path('playlist/<slug:playlist_name_slug>/edit_playlist/add_song/', views.AddSongView.as_view(), name='add_song'),
    path('playlist/<slug:playlist_name_slug>/edit_playlist/remove_song/', views.RemoveSongView.as_view(), name='remove_song'),
    path('playlist/<slug:playlist_name_slug>/import/', views.ImportPlaylistView.as_view(), name='import_playlist'),
    path('restricted/', views.RestrictedView.as_view(), name='restricted'),
    #path('goto/', views.GoToView.as_view(), name='goto'),
    path('register_profile/', views.RegisterProfileView.as_view(), name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<username>/my_stats', views.MyStatsView.as_view(), name='my_stats'),
    path('all_profiles/', views.ListProfileView.as_view(), name='list_profiles'),
    #path('like_playlist/', views.LikePlaylistView.as_view(), name='like_playlist'),
    path('publish_playlist/', views.PublishPlaylistView.as_view(), name='publish_playlist'),
    path('suggest_tag/', views.TagSuggestionView.as_view(), name='suggest_tag'),
    path('suggest_playlist/', views.PlaylistSuggestionView.as_view(), name='suggest_playlist'),
    path('filter_playlists/', views.PlaylistFilterView.as_view(), name='filter_playlists'),
    path('drafts/', views.DraftView.as_view(), name='drafts'),
    #path('search_add_page/', views.SearchAddPage.as_view(), name='search_add_page'),
    path('test/', views.TestView.as_view(), name='test'),
]