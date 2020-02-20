import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'choonz_project.settings')

import django
django.setup()
from choonz.models import Tag, Playlist, Artist, Song, Rating
from datetime import datetime
from django.contrib.auth.models import User

today = datetime.today()
bob = User.objects.get_or_create(username="bobby")[0]

def populate():
    # Create a list of dictionaries containing pages to add to each Playlist
    # Then create dictionaries for our playlist
    # This allows us to iterate through each data structure and add data to out models

    tags = [
        "Metal",
        "Pop",
        "Blues",
        "Techno",
        "Disco",
        "Jazz",
        "Electro",
        "Relaxing",
        "Chill",
        "High Energy",
        "Upbeat",
    ]

    playlist_info = {
        "Country Anthems": {"tags": tags[:3], "creator": bob, "createdDate": today, "lastUpdatedDate": today, "description": "Bangin country anthems", },
        "K-Pop Forever": {"tags": tags[4:6], "creator": bob, "createdDate": today, "lastUpdatedDate": today, "description": "Bangin k-pop anthems", },
        "Now That's What I Call Romanian Folk-Pop": {"tags": tags[8:], "creator": bob, "createdDate": today, "lastUpdatedDate": today, "description": "Bangin folk-pop anthems", },
        "NedBeatz": {"tags": tags[7:], "creator": bob, "createdDate": today, "lastUpdatedDate": today, "description": "Bangin ned anthems", },
        "i luv you stacy plz come back": {"tags": tags, "creator": bob, "createdDate": today, "lastUpdatedDate": today, "description": "Why did you leave me", },
    }

    '''
    name = models.CharField(max_length=max_char_length, blank=False)
    webpage = models.URLField(blank=True)
    linkToSpotify = models.URLField(blank=True)
    numberOfPlaylists = models.IntegerField(default=0)
    '''

    dolly_songs = ["9-5", "Jolene"]
    kpop_songs = ["kpop song1", "i love kpop"]
    folk_songs = ["folky-polky", "Romanian boogaloo"]
    eminem_songs = ["Stan", "Lose Yourself", "Eminem song"]
    rammstein_songs = ["Ich Will", "Reise, Reise"]
    panther_songs = ["Death to all but Metal", "Girl from Oklahoma", "It won't suck itself"]
    garth_songs = ["Beer Run", "If Tomorrow Never Comes"]
    george_songs = ["Careless Whisper", "Wake Me Up"]

    artist_info = {
        "Dolly Parton": {"songs": dolly_songs, "playlist": "Country Anthems"},
        "KpopBand": {"songs": kpop_songs, "playlist": "K-Pop Forever"},
        "RomanianFolkPopBand": {"songs": folk_songs, "playlist": "Now That's What I Call Romanian Folk-Pop"},
        "Eminem": {"songs": eminem_songs, "playlist": "NedBeatz"},
        "Rammstein": {"songs": rammstein_songs, "playlist": "i luv you stacy plz come back"},
        "Steel Panther": {"songs": panther_songs, "playlist": "i luv you stacy plz come back"},
        "Garth Brooks": {"songs": garth_songs, "playlist": "Country Anthems"},
        "George Michael": {"songs": george_songs, "playlist": "i luv you stacy plz come back"},
    }


    for tag_description in tags:
        add_tag(tag_description)
        print("Tag {0} added successfully".format(str(tag_description)))

    for p, pdata in playlist_info.items():
        add_playlist(p, pdata['tags'], pdata['creator'], pdata['createdDate'], pdata['lastUpdatedDate'], pdata['description'])
        print("Playlist data for {0} added successfully".format(str(p)))

    for artist_name, artist_songs in artist_info.items():
        artist = add_artist(artist_name)
        print("Artist {0} successfully added".format(str(artist_name)))
        for s in artist_songs['songs']:
            add_song(artist, s)

    for artist, data in artist_info.items():
        playlist = Playlist.objects.get(name=data["playlist"])
        print(playlist.name + " is ready for song population:")
        for s in data["songs"]:
            song = Song.objects.get(title=s)
            print(" - - readying song {0} for addition".format(song.title))
            playlist.songs.add(song)
            print(" - - Song {0} added to playlist {1}".format(song.title, playlist.name))

def add_tag(description):
    t = Tag.objects.get_or_create(description=description,)[0]
    t.save()
    return t

def add_playlist(list, tags, creator, date1, date2, description):
    p = Playlist.objects.get_or_create(name=list)[0]

    for t in tags:
        found_tag = Tag.objects.get(description=t)
        p.tags.add(found_tag)
        print(" - - added tag {0} to playlist {1}".format(str(found_tag.description), str(p.name)))

    p.creator = creator
    p.createdDate = date1
    p.lastUpdatedDate = date2
    p.description = description
    p.save()
    return p

def add_artist(name):
    artist = Artist.objects.get_or_create(name=name)[0]
    artist.website = "www." + name + ".com"
    artist.save()
    return artist

def add_song(artist, song_title):
    s = Song.objects.get_or_create(artist=artist, title=song_title)[0]
    print(" - Song {0} created".format(str(song_title)))
    s.save()
    return s

if __name__ == '__main__':
    print("Starting choonz population script...")
    populate()

