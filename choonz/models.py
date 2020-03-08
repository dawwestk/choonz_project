from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Avg, Count

max_char_length = 128


# Create your models here.

class Tag(models.Model):
    description = models.CharField(max_length=30)
    numberOfPlaylists = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    @property
    def getNumberOfPlaylists(self):
        playlist_tags = Tag.objects.annotate(num_playlists=Count('playlist'))  # annotate the queryset
        return playlist_tags.get(id=self.id).num_playlists

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.slug = slugify(self.description)
        if self.numberOfPlaylists < 0:
            self.numberOfPlaylists = 0
        super(Tag, self).save(*args, **kwargs)


class Playlist(models.Model):
    max_length_char = max_char_length  # including here because other pieces of code reference Playlist.max_length_char
    name = models.CharField(max_length=max_char_length, unique=True)
    slug = models.SlugField(unique=True)
    songs = models.ManyToManyField("Song")
    tags = models.ManyToManyField("Tag")
    averageRating = models.FloatField(default=0.0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    createdDate = models.DateTimeField(blank=True, null=True)
    lastUpdatedDate = models.DateTimeField(blank=True, null=True)
    numberOfRatings = models.IntegerField(default=0)
    description = models.CharField(max_length=max_char_length * 2, default='Description...')
    public = models.BooleanField(default=False)

    @property
    def get_average_rating(self):
        ave = self.rating_set.aggregate(Avg('stars'))['stars__avg']
        if not ave:
            ave = 0.0
        return ave

    @property
    def get_number_of_ratings(self):
        playlist_ratings = Playlist.objects.annotate(num_ratings=Count('rating'))  # annotate the queryset
        num = playlist_ratings.get(id=self.id).num_ratings
        if not num:
            num = 0
        return num

    @property
    def get_song_list(self):
        return list(self.songs.all())

    @property
    def get_playlist_tag_list(self):
        return list(self.tags.all())

    @property
    def get_playlist_tag_descriptions(self):
        return [tag.description for tag in self.tags.all()]

    @property
    def get_playlist_tag_descriptions_as_string(self):
        list_of_tags = self.get_playlist_tag_descriptions
        return ", ".join(list_of_tags)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.averageRating < 0:
            self.averageRating = 0
        super(Playlist, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Playlists'

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=max_char_length, blank=False)
    webpage = models.URLField(blank=True, null=True)
    linkToSpotify = models.URLField(blank=True)
    numberOfPlaylists = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Artist, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Song(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=max_char_length, blank=False)
    linkToSpotify = models.URLField(blank=True, null=True)
    numberOfPlaylists = models.IntegerField(default=0)
    linkOther = models.URLField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title + '-' + self.artist.name)
        super(Song, self).save(*args, **kwargs)

    @property
    def number_of_playlists(self):
        playlist_count = Song.objects.annotate(num_playlists=Count('playlist'))  # annotate the queryset
        return playlist_count.get(id=self.id).num_playlists

    def __str__(self):
        return self.title + " by " + self.artist.name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    stars = models.FloatField(default=0)
    comment = models.CharField(max_length=max_char_length * 2)
    date = models.DateTimeField(blank=True, null=True)

    @property
    def get_rated_playlist_creator(self):
        return self.playlist.creator

    def __str__(self):
        return self.user.username + " review of " + self.playlist.name

    def save(self, *args, **kwargs):
        if self.stars < 0:
            self.stars = 0
        if self.stars > 5:
            self.stars = 5
        super(Rating, self).save(*args, **kwargs)


class UserProfile(models.Model):
    # link UserProfile to User model instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
