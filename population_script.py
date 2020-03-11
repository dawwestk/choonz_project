import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'choonz_project.settings')

import django
django.setup()

import pytz, random
from choonz.models import Tag, Playlist, Artist, Song, Rating
from datetime import datetime, timedelta
from django.contrib.auth.models import User

today = datetime.now(pytz.utc)
bob = User.objects.get_or_create(username="bobby")[0]
bob.set_password("bobby123!")
sue = User.objects.get_or_create(username="sue")[0]
sue.set_password("sue123!")
jim = User.objects.get_or_create(username="jim")[0]
jim.set_password("jim123!")
fran = User.objects.get_or_create(username="fran")[0]
fran.set_password("fran123!")

def populate():
    # Create a list of dictionaries containing pages to add to each Playlist
    # Then create dictionaries for our playlist
    # This allows us to iterate through each data structure and add data to out models

    tags = [
        "Metal", "Country", "Pop", "Blues", "Techno", "Disco", "Jazz", "Electro", "Relaxing", "Chill", "High Energy",
        "Upbeat", "Latin", "Melodic", "Epic", "Funky", "Ska", "Reggae", "Folk", "Dance", "Golden Oldies",
        "Guilty Pleasures", "Hipster", "Garage", "Emo", "K-Pop",
    ]

    playlist_info = {
        "Country Anthems": {"tags": ["Country", "Folk"], "creator": bob, "createdDate": today, "lastUpdatedDate": today,
                            "description": "Bangin country anthems", },
        "K-Pop Forever": {"tags": ["K-Pop"], "creator": bob, "createdDate": today, "lastUpdatedDate": today,
                          "description": "Bangin k-pop anthems", },
        "Now That's What I Call Romanian Folk-Pop": {"tags": ["Folk"], "creator": bob, "createdDate": today,
                                                     "lastUpdatedDate": today,
                                                     "description": "Bangin folk-pop anthems", },
        "NedBeatz": {"tags": ["Techno", "Electro", "High Energy", "Upbeat"], "creator": bob, "createdDate": today,
                     "lastUpdatedDate": today,
                     "description": "Bangin ned anthems", },
        "i luv you stacy plz come back": {"tags": tags, "creator": bob, "createdDate": today, "lastUpdatedDate": today,
                                          "description": "Why did you leave me", },
        "Pop anthems!": {"tags": ["Pop", "Disco", "Guilty Pleasures", "Dance"], "creator": sue, "createdDate": today,
                         "lastUpdatedDate": today,
                         "description": "Pop til' you drop!", },
        'Disco Oldies': {'tags': ['Golden Oldies', 'Disco'], 'creator': sue, 'createdDate': today,
                              'lastUpdatedDate': today, 'description': 'Playlist full of Golden Oldies and Disco'},
        'Guilty Feet Have Got No Rhythm': {'tags': ['Guilty Pleasures', 'Dance'], 'creator': sue, 'createdDate': today,
                              'lastUpdatedDate': today,
                              'description': 'Playlist full of Guilty Pleasures and Dance'},
        'Off-Beats': {'tags': ['Ska', 'Latin', 'Reggae'], 'creator': sue, 'createdDate': today,
                              'lastUpdatedDate': today, 'description': 'Playlist full of Ska and Latin and Reggae'},
        'Folky-Jazz-Melodies in my Garage': {'tags': ['Folk', 'Jazz', 'Melodic', 'Garage'], 'creator': bob, 'createdDate': today,
                              'lastUpdatedDate': today,
                              'description': 'Playlist full of Folk and Jazz and Melodic and Garage'},
        'Cut My Life Into Pizzas, This Is My Plastic Fork': {'tags': ['Emo'], 'creator': sue, 'createdDate': today, 'lastUpdatedDate': today,
                              'description': 'Playlist full of Emo'},
        'OK Pops': {'tags': ['Disco', 'K-Pop', 'Pop'], 'creator': sue, 'createdDate': today,
                              'lastUpdatedDate': today, 'description': 'Playlist full of Disco and K-Pop and Pop'},
        'Chilled Latin Vibes': {'tags': ['Chill', 'Latin', 'High Energy'], 'creator': bob, 'createdDate': today,
                              'lastUpdatedDate': today,
                              'description': 'Playlist full of Chill and Latin and High Energy'},
        'Relaxi-Ska-Hipster-Metal': {'tags': ['Relaxing', 'Ska', 'Hipster', 'Metal', 'Guilty Pleasures'], 'creator': sue,
                              'createdDate': today, 'lastUpdatedDate': today,
                              'description': 'Playlist full of Relaxing and Ska and Hipster and Metal and Guilty Pleasures'},
        'Yoga-Mix 2k20': {'tags': ['Disco', 'Upbeat', 'Relaxing'], 'creator': sue, 'createdDate': today,
                              'lastUpdatedDate': today,
                              'description': 'Playlist full of Disco and Upbeat and Relaxing'},
        'Sounds of the 70s': {'tags': ['Golden Oldies', 'Upbeat'], 'creator': bob, 'createdDate': today,
                               'lastUpdatedDate': today, 'description': 'Playlist full of Golden Oldies and Upbeat'},
        'boots n cats': {'tags': ['Garage'], 'creator': fran, 'createdDate': today,
                               'lastUpdatedDate': today, 'description': 'Playlist full of Garage'},
        'How does Bob Marley like his Donuts?': {'tags': ['Reggae'], 'creator': jim, 'createdDate': today,
                               'lastUpdatedDate': today, 'description': 'Playlist full of Reggae'},
        'Beard Appreciation Society Jams': {'tags': ['Techno', 'Golden Oldies', 'Pop', 'Folk', 'Hipster'], 'creator': jim,
                               'createdDate': today, 'lastUpdatedDate': today,
                               'description': 'Playlist full of Techno and Golden Oldies and Pop and Folk and Hipster'},
        'Downtown Funk': {'tags': ['Upbeat', 'Golden Oldies', 'Funky'], 'creator': fran, 'createdDate': today,
                               'lastUpdatedDate': today,
                               'description': 'Playlist full of Upbeat and Golden Oldies and Funky'},
        'summer vibin': {'tags': ['Techno', 'Chill', 'Electro', 'Pop', 'Folk'], 'creator': jim,
                               'createdDate': today, 'lastUpdatedDate': today,
                               'description': 'Playlist full of Techno and Chill and Electro and Pop and Folk'},
        'I blue myself': {'tags': ['Pop', 'Relaxing', 'Blues', 'Emo'], 'creator': bob, 'createdDate': today,
                               'lastUpdatedDate': today,
                               'description': 'Playlist full of Pop and Relaxing and Blues and Emo'},
        'Thrash Bandicoot': {'tags': ['High Energy', 'Metal'], 'creator': fran, 'createdDate': today,
                               'lastUpdatedDate': today, 'description': 'Playlist full of High Energy and Metal'},
        'Blues Brothers': {'tags': ['Blues', 'Blues'], 'creator': bob, 'createdDate': today,
                               'lastUpdatedDate': today, 'description': 'Playlist full of Blues and Blues'},
        'Jazz in my Pants': {'tags': ['Jazz', 'Disco'], 'creator': fran, 'createdDate': today,
                               'lastUpdatedDate': today, 'description': 'Playlist full of Jazz and Disco'},
        'Jims eclectic mix': {'tags': ['Reggae', 'Disco', 'Techno', 'Reggae', 'K-Pop'], 'creator': jim,
                               'createdDate': today, 'lastUpdatedDate': today,
                               'description': 'Playlist full of Reggae and Disco and Techno and Reggae and K-Pop'},
    }

    artist_info = {
        'Country Anthems':
            [
                {'artist': 'Panic! At The Disco', 'songs': ['High Hopes', 'Hey Look Ma, I Made It', 'I Write Sins Not Tragedies']},
                {'artist': 'Milo', 'songs': ['Someday', 'Flesh & Bone', 'Like the Zombies Do']}
            ],
        'K-Pop Forever': [{'artist': 'K-Pop Rap Battles', 'songs': ['RM vs. Suga vs. J-Hope']}, {'artist': 'Jbrisko', 'songs': ['9 Tailz', 'On Me', 'Gone']}], "Now That's What I Call Romanian Folk-Pop": [{'artist': 'Panic! At The Disco', 'songs': ['High Hopes', 'Hey Look Ma, I Made It', 'I Write Sins Not Tragedies']}, {'artist': 'Milo', 'songs': ['Someday', 'Flesh & Bone', 'Like the Zombies Do']}], 'NedBeatz': [{'artist': 'adam feegan', 'songs': ['Upbeat']}, {'artist': 'Michael Bolton', 'songs': ['How Am I Supposed to Live Without You', 'When a Man Loves a Woman', 'Jack Sparrow']}], 'i luv you stacy plz come back': [{'artist': 'iann dior', 'songs': ['emotions', 'molly', 'Good Day']}, {'artist': 'Drake', 'songs': ['Life Is Good (feat. Drake)', 'Money In The Grave (Drake ft. Rick Ross)', 'Going Bad (feat. Drake)']}], 'Pop anthems!': [{'artist': 'Tones and I', 'songs': ['Dance Monkey', 'Never Seen The Rain', 'Dance Monkey']}, {'artist': 'Fall Out Boy', 'songs': ["Sugar, We're Goin Down", 'Centuries', 'Thnks fr th Mmrs']}], 'Disco Oldies': [{'artist': '50 Cent', 'songs': ['In Da Club', 'Candy Shop', '21 Questions']}, {'artist': 'Surf Curse', 'songs': ['Freaks', 'Disco', 'Disco']}], 'Guilty Feet Have Got No Rhythm': [{'artist': 'Tones and I', 'songs': ['Dance Monkey', 'Never Seen The Rain', 'Dance Monkey']}, {'artist': 'Fall Out Boy', 'songs': ["Sugar, We're Goin Down", 'Centuries', 'Thnks fr th Mmrs']}], 'Off-Beats': [{'artist': 'J Balvin', 'songs': ['RITMO (Bad Boys For Life)', 'LA CANCIÓN', 'Morado']}, {'artist': 'CNCO', 'songs': ['Reggaetón Lento (Bailemos)', 'Pegao', 'Me Necesita']}], 'Folky-Jazz-Melodies in my Garage': [{'artist': 'Gorillaz', 'songs': ['Feel Good Inc.', 'Clint Eastwood', 'Momentary Bliss (feat. slowthai and Slaves)']}, {'artist': 'Wiz Khalifa', 'songs': ['See You Again (feat. Charlie Puth)', 'Hopeless Romantic (feat. Swae Lee)', 'Payphone']}], 'Cut My Life Into Pizzas, This Is My Plastic Fork': [{'artist': 'iann dior', 'songs': ['emotions', 'molly', 'Good Day']}, {'artist': 'Drake', 'songs': ['Life Is Good (feat. Drake)', 'Money In The Grave (Drake ft. Rick Ross)', 'Going Bad (feat. Drake)']}], 'OK Pops': [{'artist': 'Polo G', 'songs': ['Pop Out (feat. Lil Tjay)', 'Go Stupid', 'Heartless (feat. Mustard)']}, {'artist': 'Falling In Reverse', 'songs': ['Popular Monster', 'The Drug In Me Is Reimagined', 'The Drug In Me Is You']}], 'Chilled Latin Vibes': [{'artist': 'adam roster', 'songs': ['High Energy']}, {'artist': 'Overnoob', 'songs': ['Stay Calm', 'Secrets in Your Pocket', 'High Energy']}], 'Relaxi-Ska-Hipster-Metal': [{'artist': 'Fallen Roses', 'songs': ['Sorry', 'Naive', "Don't Mind Me"]}, {'artist': 'Catch 22', 'songs': ['Catch 22', 'Catch 22', 'Keasbey Nights']}], 'Yoga-Mix 2k20': [{'artist': 'Nature Sounds', 'songs': ['Relaxing Constant Rain Storm with Distant Thunder Sfx', 'Calm Rolling Thunder and Soothing Rain', 'Rain And Thunder']}, {'artist': 'Mr Pillow', 'songs': ['Comfy', 'Comfortable Night', 'Relaxing Pillow']}], 'Sounds of the 70s': [{'artist': 'adam feegan', 'songs': ['Upbeat']}, {'artist': 'Michael Bolton', 'songs': ['How Am I Supposed to Live Without You', 'When a Man Loves a Woman', 'Jack Sparrow']}], 'boots n cats': [{'artist': 'Gorillaz', 'songs': ['Feel Good Inc.', 'Clint Eastwood', 'Momentary Bliss (feat. slowthai and Slaves)']}, {'artist': 'Wiz Khalifa', 'songs': ['See You Again (feat. Charlie Puth)', 'Hopeless Romantic (feat. Swae Lee)', 'Payphone']}], 'How does Bob Marley like his Donuts?': [{'artist': 'J Balvin', 'songs': ['RITMO (Bad Boys For Life)', 'LA CANCIÓN', 'Morado']}, {'artist': 'CNCO', 'songs': ['Reggaetón Lento (Bailemos)', 'Pegao', 'Me Necesita']}], 'Beard Appreciation Society Jams': [{'artist': 'Sango', 'songs': ['Sangoloteadito - En Vivo Desde El Lunario/Mariachi/Banda', 'Sangoloteadito', 'Sango']}, {'artist': 'Dirty Heads', 'songs': ['Vacation', 'Oxygen', 'Lay Me Down']}], 'Downtown Funk': [{'artist': 'Lipps Inc.', 'songs': ['Funky Town', 'Funkytown - Single Version', 'Funkytown']}, {'artist': 'Tone-Loc', 'songs': ['Wild Thing', 'Funky Cold Medina', 'Funky Cold Medina (Re-Recorded / Remastered)']}], 'summer vibin': [{'artist': 'Panic! At The Disco', 'songs': ['High Hopes', 'Hey Look Ma, I Made It', 'I Write Sins Not Tragedies']}, {'artist': 'Milo', 'songs': ['Someday', 'Flesh & Bone', 'Like the Zombies Do']}], 'I blue myself': [{'artist': 'iann dior', 'songs': ['emotions', 'molly', 'Good Day']}, {'artist': 'Drake', 'songs': ['Life Is Good (feat. Drake)', 'Money In The Grave (Drake ft. Rick Ross)', 'Going Bad (feat. Drake)']}], 'Thrash Bandicoot': [{'artist': 'Quiet Riot', 'songs': ['Cum on Feel the Noize', 'Cum on Feel the Noize', 'Metal Health (Bang Your Head)']}, {'artist': 'Alter Bridge', 'songs': ['Metalingus', 'Watch Over You', 'Blackbird']}], 'Blues Brothers': [{'artist': 'Shotgun Willy', 'songs': ['Cheat Codes for Hoes', 'Wendy', 'Last Chance']}, {'artist': 'Jackson C. Frank', 'songs': ['Blues Run the Game - 2001 Remaster', 'My Name Is Carnival - 2001 Remaster', 'Milk and Honey - 2001 Remaster']}], 'Jazz in my Pants': [{'artist': '50 Cent', 'songs': ['In Da Club', 'Candy Shop', '21 Questions']}, {'artist': 'Surf Curse', 'songs': ['Freaks', 'Disco', 'Disco']}], 'Jims eclectic mix': [{'artist': 'K-Pop Rap Battles', 'songs': ['RM vs. Suga vs. J-Hope']}, {'artist': 'Jbrisko', 'songs': ['9 Tailz', 'On Me', 'Gone']}]}

    rating_info = {'Rating 1': {'playlist': 'Thrash Bandicoot', 'user': jim, 'stars': 0.3, 'date': today, 'comment': 'Pile of garbage'}, 'Rating 2': {'playlist': 'Thrash Bandicoot', 'user': jim, 'stars': 3.5, 'date': today, 'comment': 'My kind of playlist!'}, 'Rating 3': {'playlist': 'Downtown Funk', 'user': fran, 'stars': 2.0, 'date': today, 'comment': 'Simply epic'}, 'Rating 4': {'playlist': "Now That's What I Call Romanian Folk-Pop", 'user': bob, 'stars': 4.0, 'date': today, 'comment': 'Awesome - I wish i was as cool as they are'}, 'Rating 5': {'playlist': 'Beard Appreciation Society Jams', 'user': bob, 'stars': 1.9, 'date': today, 'comment': 'This made my baby cry. And Im not even a father.'}, 'Rating 6': {'playlist': 'Relaxi-Ska-Hipster-Metal', 'user': bob, 'stars': 0.5, 'date': today, 'comment': 'Not my cup of tea'}, 'Rating 7': {'playlist': 'i luv you stacy plz come back', 'user': sue, 'stars': 0.1, 'date': today, 'comment': 'What did i ever do to you?'}, 'Rating 8': {'playlist': 'OK Pops', 'user': bob, 'stars': 1.8, 'date': today, 'comment': 'Not my cup of tea'}, 'Rating 9': {'playlist': 'Jazz in my Pants', 'user': sue, 'stars': 0.9, 'date': today, 'comment': 'I wouldnt play this to my worst enemy'}, 'Rating 10': {'playlist': 'boots n cats', 'user': sue, 'stars': 1.0, 'date': today, 'comment': 'What did i ever do to you?'}, 'Rating 11': {'playlist': 'I blue myself', 'user': bob, 'stars': 1.6, 'date': today, 'comment': 'What a shambles'}, 'Rating 12': {'playlist': 'OK Pops', 'user': fran, 'stars': 3.2, 'date': today, 'comment': 'Simply epic'}, 'Rating 13': {'playlist': 'OK Pops', 'user': sue, 'stars': 1.8, 'date': today, 'comment': 'What a shambles'}, 'Rating 14': {'playlist': 'Beard Appreciation Society Jams', 'user': jim, 'stars': 3.2, 'date': today, 'comment': 'Simply epic'}, 'Rating 15': {'playlist': 'Beard Appreciation Society Jams', 'user': sue, 'stars': 1.8, 'date': today, 'comment': 'This made my baby cry. And Im not even a father.'}, 'Rating 16': {'playlist': 'Blues Brothers', 'user': bob, 'stars': 4.4, 'date': today, 'comment': 'Got me right through my divorce, would recommend'}, 'Rating 17': {'playlist': 'Blues Brothers', 'user': bob, 'stars': 0.0, 'date': today, 'comment': 'What did i ever do to you?'}, 'Rating 18': {'playlist': 'Beard Appreciation Society Jams', 'user': sue, 'stars': 4.8, 'date': today, 'comment': 'Never heard anything like this before'}, 'Rating 19': {'playlist': 'Off-Beats', 'user': jim, 'stars': 2.9, 'date': today, 'comment': 'My kind of playlist!'}, 'Rating 20': {'playlist': 'Jims eclectic mix', 'user': sue, 'stars': 4.8, 'date': today, 'comment': 'This will always be my summer 2019 playlist'}, 'Rating 21': {'playlist': 'Off-Beats', 'user': sue, 'stars': 1.1, 'date': today, 'comment': 'Not my cup of tea'}, 'Rating 22': {'playlist': 'Beard Appreciation Society Jams', 'user': sue, 'stars': 3.6, 'date': today, 'comment': 'Never heard anything like this before'}, 'Rating 23': {'playlist': 'summer vibin', 'user': sue, 'stars': 0.3, 'date': today, 'comment': 'I wouldnt play this to my worst enemy'}, 'Rating 24': {'playlist': 'Jims eclectic mix', 'user': fran, 'stars': 3.1, 'date': today, 'comment': 'Simply epic'}, 'Rating 25': {'playlist': 'Cut My Life Into Pizzas, This Is My Plastic Fork', 'user': fran, 'stars': 1.9, 'date': today, 'comment': 'Too loud'}, 'Rating 26': {'playlist': 'NedBeatz', 'user': fran, 'stars': 4.5, 'date': today, 'comment': 'Simply epic'}, 'Rating 27': {'playlist': 'I blue myself', 'user': jim, 'stars': 1.1, 'date': today, 'comment': 'Not my cup of tea'}, 'Rating 28': {'playlist': 'Blues Brothers', 'user': bob, 'stars': 2.7, 'date': today, 'comment': 'Never heard anything like this before'}, 'Rating 29': {'playlist': 'Relaxi-Ska-Hipster-Metal', 'user': jim, 'stars': 1.5, 'date': today, 'comment': 'Pile of garbage'}, 'Rating 30': {'playlist': 'Sounds of the 70s', 'user': sue, 'stars': 2.1, 'date': today, 'comment': 'My kind of playlist!'}, 'Rating 31': {'playlist': 'i luv you stacy plz come back', 'user': jim, 'stars': 3.3, 'date': today, 'comment': 'Pretty decent'}, 'Rating 32': {'playlist': 'i luv you stacy plz come back', 'user': fran, 'stars': 3.8, 'date': today, 'comment': 'Loved it - such drama, such mourning.'},}

    print(" - Populating all Tags")
    for tag_description in tags:
        add_tag(tag_description)
        #print("Tag {0} added successfully".format(str(tag_description)))

    print(" - Populating Playlists")
    for p, pdata in playlist_info.items():
        add_playlist(p, pdata['tags'], pdata['creator'], pdata['createdDate'],
                     pdata['description'])
        #print("Playlist data for {0} added successfully".format(str(p)))

    print(" - Populating Artists and associated songs")
    for playlist_name, artist_and_songs in artist_info.items():
        playlist = Playlist.objects.get(name=playlist_name)
        artist = add_artist(artist_and_songs[0]['artist'])
        for s in artist_and_songs[0]['songs']:
            song = add_song(artist, s)
            playlist.songs.add(song)

    print(" - Adding ratings to Playlists")
    for rating, rating_data in rating_info.items():
        playlist = Playlist.objects.get(name=rating_data["playlist"])
        user = User.objects.get(username=rating_data["user"])
        add_rating(user, playlist, rating_data["stars"], rating_data["comment"], rating_data["date"])
        #print("Rating: <{0} - {1}> added".format(str(user), str(playlist)))


def add_tag(description):
    t = Tag.objects.get_or_create(description=description, )[0]
    t.save()
    return t


def add_playlist(list, tags, creator, date1, description):
    p = Playlist.objects.get_or_create(name=list)[0]

    for t in tags:
        found_tag = Tag.objects.get(description=t)
        p.tags.add(found_tag)
        #print(" - - added tag {0} to playlist {1}".format(str(found_tag.description), str(p.name)))

    random_hours = random.randint(30, 100)
    random_minutes = random.randint(0, 60)
    p.createdDate = date1 - timedelta(hours=random_hours, minutes=random_minutes)
    p.lastUpdatedDate = p.createdDate + timedelta(hours=10, minutes=36)

    p.creator = creator
    p.description = description
    p.public = True
    p.save()
    return p


def add_artist(name):
    artist = Artist.objects.get_or_create(name=name)[0]
    artist.webpage = "www." + name.replace(" ", "") + ".com"
    artist.save()
    return artist


def add_song(artist, song_title):
    s = Song.objects.get_or_create(artist=artist, title=song_title)[0]
    #print(" - Song {0} created".format(str(song_title)))
    s.save()
    return s


def add_rating(user, playlist, stars, comment, date):
    rating = Rating.objects.get_or_create(user=user, playlist=playlist)[0]
    rating.stars = stars
    rating.comment = comment
    rating.date = date
    rating.save()
    return rating


if __name__ == '__main__':
    print("Starting choonz population script...")
    populate()
    print("Database population complete")
