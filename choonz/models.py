from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

max_char_length = 128
# Create your models here.


class Tag(models.Model):
    description = models.CharField(max_length=30)
    numberOfPlaylists = models.IntegerField(default=0)

    def __str__(self):
        return self.description

class Playlist(models.Model):
    max_length_char = max_char_length   # including here because other pieces of code reference Playlist.max_length_char
    name = models.CharField(max_length=max_char_length, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
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

    @property
    def get_song_list(self):
        return list(self.songs.all())

    @property
    def get_tag_list(self):
        return list(self.tags.all())

    def __str__(self):
        return self.name



    '''
    
    See:
    https://stackoverflow.com/questions/1110153/what-is-the-most-efficient-way-to-store-a-list-in-the-django-models
    
    Using ManyToManyField relations and properties:

class MyDjangoClass(models.Model):
    name = models.CharField(...)
    friends = models.ManyToManyField("self")

    @property
    def friendlist(self):
        # Watch for large querysets: it loads everything in memory
        return list(self.friends.all())
You can access a user's friend list this way:

joseph = MyDjangoClass.objects.get(name="Joseph")
friends_of_joseph = joseph.friendlist
Note however that these relations are symmetrical: if Joseph is a friend of Bob, then Bob is a friend of Joseph.
    
    '''

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Playlist, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Playlists'

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=max_char_length, blank=False)
    webpage = models.URLField(blank=True)
    linkToSpotify = models.URLField(blank=True)
    numberOfPlaylists = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Song(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=max_char_length, blank=False)
    linkToSpotify = models.URLField(blank=True)
    numberOfPlaylists = models.IntegerField(default=0)
    linkOther = models.URLField(blank=True)

    def __str__(self):
        return self.title + " by " + self.artist.name

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    comment = models.CharField(max_length=max_char_length*2)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user + " review of " + self.playlist

class UserProfile(models.Model):
    # link UserProfile to User model instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


