from django.urls import path
from choonz import views
from choonz.views import AboutView, AddPlaylistView, IndexView, PlaylistRatingView, ShowPlaylistView, RestrictedView, RegisterProfileView, ProfileView, ListPlaylistView,  ListProfileView, LikePlaylistView
# AddPageView,GoToView, SearchAddPage


app_name = 'choonz'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('playlist/<slug:playlist_name_slug>/', views.ShowPlaylistView.as_view(), name='show_playlist'),
    path('add_playlist/', views.AddPlaylistView.as_view(), name='add_playlist'),
    path('list_playlists/', views.ListPlaylistView.as_view(), name='list_playlists'),
    path('playlist/<slug:playlist_name_slug>/rate_playlist/', views.PlaylistRatingView.as_view(), name='rate_playlist'),
    path('restricted/', views.RestrictedView.as_view(), name='restricted'),
    #path('goto/', views.GoToView.as_view(), name='goto'),
    path('register_profile/', views.RegisterProfileView.as_view(), name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('profiles/', views.ListProfileView.as_view(), name='list_profiles'),
    path('like_playlist/', views.LikePlaylistView.as_view(), name='like_playlist'),
    path('suggest/', views.PlaylistSuggestionView.as_view(), name='suggest'),
    path('playlist_creator/', views.PlaylistCreatorView.as_view(), name='playlist_creator'),
    path('drafts/', views.DraftView.as_view(), name='drafts'),
    #path('search_add_page/', views.SearchAddPage.as_view(), name='search_add_page'),
]