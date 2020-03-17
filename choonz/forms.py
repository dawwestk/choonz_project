from django import forms
from django.contrib.auth.models import User
from choonz.models import Playlist, UserProfile, Rating
from datetime import datetime

class PlaylistForm(forms.ModelForm):
    name = forms.CharField(max_length=Playlist.max_length_char, help_text="Please enter the playlist name.")
    description = forms.CharField(max_length=Playlist.max_length_char * 2, help_text="Describe your playlist...",
                                  required=False)
    #averageRating = forms.FloatField(widget=forms.HiddenInput(), initial=0.0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    createdDate = forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.now, required=False)
    lastUpdatedDate = forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.now, required=False)
    tags = forms.CharField(max_length=Playlist.max_length_char,
                           help_text="Enter tags to help people find your playlist!", required=False)

    # Meta is an inline class to provide addition info
    class Meta:
        # Associate ModelForm and a model (in this case, Playlist)
        model = Playlist
        fields = ('name', 'description', 'createdDate', 'lastUpdatedDate', 'tags',) # 'averageRating')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)


class RatingForm(forms.ModelForm):
    stars = forms.FloatField(max_value=5.0, min_value=0.0, required=True,
                             error_messages={'required': 'Star value must be between 0.0 and 5.0!'})
    comment = forms.CharField(max_length=Playlist.max_length_char * 2,
                              help_text="What did you think of this playlist...", required=True,
                              error_messages={'required': 'A blank comment gives no feedback to the creator!'})

    class Meta:
        model = Rating
        fields = ('stars', 'comment')
