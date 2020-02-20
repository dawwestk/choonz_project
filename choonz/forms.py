from django import forms
from django.contrib.auth.models import User
from choonz.models import Playlist, UserProfile
from datetime import datetime, date

class PlaylistForm(forms.ModelForm):
    name = forms.CharField(max_length=Playlist.max_length_char, help_text="Please enter the playlist name.")
    description = forms.CharField(max_length=Playlist.max_length_char*2, help_text="Describe your playlist...", required=False)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    createdDate = forms.DateField(widget=forms.HiddenInput(), initial=date.today())
    lastUpdatedDate = forms.DateField(widget=forms.HiddenInput(), initial=date.today())

    '''
    songs = models.ManyToManyField("Song")
    tags = models.ManyToManyField("Tag")
        averageRating = models.FloatField(default=0.0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
        createdDate = models.DateTimeField(blank=True, null=True)
        lastUpdatedDate = models.DateTimeField(blank=True, null=True)
        numberOfRatings = models.IntegerField(default=0)
        description = models.CharField(max_length=max_char_length*2, default='Description...')
    image = models.FileField(blank=True)
        public = models.BooleanField(default=False)
    '''

    # Meta is an inline class to provide addition info
    class Meta:
        # Associate ModelForm and a model (in this case, Playlist)
        model = Playlist
        fields = ('name', 'description', 'createdDate', 'lastUpdatedDate',)


'''
class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Playlist.max_length_char, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page

        # decide fields to include in form
        # here we hide the foreign key (Playlist)
        exclude = ('playlist',)

        # we need either a fields or exclude line

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # if url not empty and doesn't begin with http:// we add it
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data
'''

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)