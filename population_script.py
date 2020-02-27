import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'choonz_project.settings')

import django

django.setup()
from choonz.models import Tag, Playlist, Artist, Song, Rating
from datetime import datetime
from django.contrib.auth.models import User

today = datetime.today()
bob = User.objects.get_or_create(username="bobby", password="bobby123!")[0]
sue = User.objects.get_or_create(username="sue", password="sue123!")[0]
jim = User.objects.get_or_create(username="jim", password="jim123!")[0]
fran = User.objects.get_or_create(username="fran", password="fran123!")[0]

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
        'Random Playlist 1': {'tags': ['Golden Oldies', 'Disco'], 'creator': sue, 'createdDate': today,
                              'lastUpdatedDate': today, 'description': 'Playlist full of Golden Oldies and Disco'},
        'Random Playlist 2': {'tags': ['Guilty Pleasures', 'Dance'], 'creator': sue, 'createdDate': today,
                              'lastUpdatedDate': today,
                              'description': 'Playlist full of Guilty Pleasures and Dance'},
        'Random Playlist 3': {'tags': ['Ska', 'Latin', 'Reggae'], 'creator': sue, 'createdDate': today,
                              'lastUpdatedDate': today, 'description': 'Playlist full of Ska and Latin and Reggae'},
        'Random Playlist 4': {'tags': ['Folk', 'Jazz', 'Melodic', 'Garage'], 'creator': bob, 'createdDate': today,
                              'lastUpdatedDate': today,
                              'description': 'Playlist full of Folk and Jazz and Melodic and Garage'},
        'Random Playlist 5': {'tags': ['Emo'], 'creator': sue, 'createdDate': today, 'lastUpdatedDate': today,
                              'description': 'Playlist full of Emo'},
        'Random Playlist 6': {'tags': ['Disco', 'K-Pop', 'Pop'], 'creator': sue, 'createdDate': today,
                              'lastUpdatedDate': today, 'description': 'Playlist full of Disco and K-Pop and Pop'},
        'Random Playlist 7': {'tags': ['Chill', 'Latin', 'High Energy'], 'creator': bob, 'createdDate': today,
                              'lastUpdatedDate': today,
                              'description': 'Playlist full of Chill and Latin and High Energy'},
        'Random Playlist 8': {'tags': ['Relaxing', 'Ska', 'Hipster', 'Metal', 'Guilty Pleasures'], 'creator': sue,
                              'createdDate': today, 'lastUpdatedDate': today,
                              'description': 'Playlist full of Relaxing and Ska and Hipster and Metal and Guilty Pleasures'},
        'Random Playlist 9': {'tags': ['Disco', 'Upbeat', 'Relaxing'], 'creator': sue, 'createdDate': today,
                              'lastUpdatedDate': today,
                              'description': 'Playlist full of Disco and Upbeat and Relaxing'},
        'Random Playlist 10': {'tags': ['Golden Oldies', 'Upbeat'], 'creator': bob, 'createdDate': today,
                               'lastUpdatedDate': today, 'description': 'Playlist full of Golden Oldies and Upbeat'},
        'Random Playlist 11': {'tags': ['Garage'], 'creator': fran, 'createdDate': today,
                               'lastUpdatedDate': today, 'description': 'Playlist full of Garage'},
        'Random Playlist 12': {'tags': ['Reggae'], 'creator': jim, 'createdDate': today,
                               'lastUpdatedDate': today, 'description': 'Playlist full of Reggae'},
        'Random Playlist 13': {'tags': ['Techno', 'Golden Oldies', 'Pop', 'Folk', 'Hipster'], 'creator': jim,
                               'createdDate': today, 'lastUpdatedDate': today,
                               'description': 'Playlist full of Techno and Golden Oldies and Pop and Folk and Hipster'},
        'Random Playlist 14': {'tags': ['Upbeat', 'Golden Oldies', 'Funky'], 'creator': fran, 'createdDate': today,
                               'lastUpdatedDate': today,
                               'description': 'Playlist full of Upbeat and Golden Oldies and Funky'},
        'Random Playlist 15': {'tags': ['Techno', 'Chill', 'Electro', 'Pop', 'Folk'], 'creator': jim,
                               'createdDate': today, 'lastUpdatedDate': today,
                               'description': 'Playlist full of Techno and Chill and Electro and Pop and Folk'},
        'Random Playlist 16': {'tags': ['Pop', 'Relaxing', 'Blues', 'Emo'], 'creator': bob, 'createdDate': today,
                               'lastUpdatedDate': today,
                               'description': 'Playlist full of Pop and Relaxing and Blues and Emo'},
        'Random Playlist 17': {'tags': ['High Energy', 'Metal'], 'creator': fran, 'createdDate': today,
                               'lastUpdatedDate': today, 'description': 'Playlist full of High Energy and Metal'},
        'Random Playlist 18': {'tags': ['Blues', 'Blues'], 'creator': bob, 'createdDate': today,
                               'lastUpdatedDate': today, 'description': 'Playlist full of Blues and Blues'},
        'Random Playlist 19': {'tags': ['Jazz', 'Disco'], 'creator': fran, 'createdDate': today,
                               'lastUpdatedDate': today, 'description': 'Playlist full of Jazz and Disco'},
        'Random Playlist 20': {'tags': ['Reggae', 'Disco', 'Techno', 'Reggae', 'K-Pop'], 'creator': jim,
                               'createdDate': today, 'lastUpdatedDate': today,
                               'description': 'Playlist full of Reggae and Disco and Techno and Reggae and K-Pop'},
    }

    artist_info = {
        'Country Anthems':
            [
                {'artist': 'Panic! At The Disco', 'songs': ['High Hopes', 'Hey Look Ma, I Made It', 'I Write Sins Not Tragedies']},
                {'artist': 'Milo', 'songs': ['Someday', 'Flesh & Bone', 'Like the Zombies Do']}
            ],
        'K-Pop Forever': [{'artist': 'K-Pop Rap Battles', 'songs': ['RM vs. Suga vs. J-Hope']}, {'artist': 'Jbrisko', 'songs': ['9 Tailz', 'On Me', 'Gone']}], "Now That's What I Call Romanian Folk-Pop": [{'artist': 'Panic! At The Disco', 'songs': ['High Hopes', 'Hey Look Ma, I Made It', 'I Write Sins Not Tragedies']}, {'artist': 'Milo', 'songs': ['Someday', 'Flesh & Bone', 'Like the Zombies Do']}], 'NedBeatz': [{'artist': 'adam feegan', 'songs': ['Upbeat']}, {'artist': 'Michael Bolton', 'songs': ['How Am I Supposed to Live Without You', 'When a Man Loves a Woman', 'Jack Sparrow']}], 'i luv you stacy plz come back': [{'artist': 'iann dior', 'songs': ['emotions', 'molly', 'Good Day']}, {'artist': 'Drake', 'songs': ['Life Is Good (feat. Drake)', 'Money In The Grave (Drake ft. Rick Ross)', 'Going Bad (feat. Drake)']}], 'Pop anthems!': [{'artist': 'Tones and I', 'songs': ['Dance Monkey', 'Never Seen The Rain', 'Dance Monkey']}, {'artist': 'Fall Out Boy', 'songs': ["Sugar, We're Goin Down", 'Centuries', 'Thnks fr th Mmrs']}], 'Random Playlist 1': [{'artist': '50 Cent', 'songs': ['In Da Club', 'Candy Shop', '21 Questions']}, {'artist': 'Surf Curse', 'songs': ['Freaks', 'Disco', 'Disco']}], 'Random Playlist 2': [{'artist': 'Tones and I', 'songs': ['Dance Monkey', 'Never Seen The Rain', 'Dance Monkey']}, {'artist': 'Fall Out Boy', 'songs': ["Sugar, We're Goin Down", 'Centuries', 'Thnks fr th Mmrs']}], 'Random Playlist 3': [{'artist': 'J Balvin', 'songs': ['RITMO (Bad Boys For Life)', 'LA CANCIÓN', 'Morado']}, {'artist': 'CNCO', 'songs': ['Reggaetón Lento (Bailemos)', 'Pegao', 'Me Necesita']}], 'Random Playlist 4': [{'artist': 'Gorillaz', 'songs': ['Feel Good Inc.', 'Clint Eastwood', 'Momentary Bliss (feat. slowthai and Slaves)']}, {'artist': 'Wiz Khalifa', 'songs': ['See You Again (feat. Charlie Puth)', 'Hopeless Romantic (feat. Swae Lee)', 'Payphone']}], 'Random Playlist 5': [{'artist': 'iann dior', 'songs': ['emotions', 'molly', 'Good Day']}, {'artist': 'Drake', 'songs': ['Life Is Good (feat. Drake)', 'Money In The Grave (Drake ft. Rick Ross)', 'Going Bad (feat. Drake)']}], 'Random Playlist 6': [{'artist': 'Polo G', 'songs': ['Pop Out (feat. Lil Tjay)', 'Go Stupid', 'Heartless (feat. Mustard)']}, {'artist': 'Falling In Reverse', 'songs': ['Popular Monster', 'The Drug In Me Is Reimagined', 'The Drug In Me Is You']}], 'Random Playlist 7': [{'artist': 'adam roster', 'songs': ['High Energy']}, {'artist': 'Overnoob', 'songs': ['Stay Calm', 'Secrets in Your Pocket', 'High Energy']}], 'Random Playlist 8': [{'artist': 'Fallen Roses', 'songs': ['Sorry', 'Naive', "Don't Mind Me"]}, {'artist': 'Catch 22', 'songs': ['Catch 22', 'Catch 22', 'Keasbey Nights']}], 'Random Playlist 9': [{'artist': 'Nature Sounds', 'songs': ['Relaxing Constant Rain Storm with Distant Thunder Sfx', 'Calm Rolling Thunder and Soothing Rain', 'Rain And Thunder']}, {'artist': 'Mr Pillow', 'songs': ['Comfy', 'Comfortable Night', 'Relaxing Pillow']}], 'Random Playlist 10': [{'artist': 'adam feegan', 'songs': ['Upbeat']}, {'artist': 'Michael Bolton', 'songs': ['How Am I Supposed to Live Without You', 'When a Man Loves a Woman', 'Jack Sparrow']}], 'Random Playlist 11': [{'artist': 'Gorillaz', 'songs': ['Feel Good Inc.', 'Clint Eastwood', 'Momentary Bliss (feat. slowthai and Slaves)']}, {'artist': 'Wiz Khalifa', 'songs': ['See You Again (feat. Charlie Puth)', 'Hopeless Romantic (feat. Swae Lee)', 'Payphone']}], 'Random Playlist 12': [{'artist': 'J Balvin', 'songs': ['RITMO (Bad Boys For Life)', 'LA CANCIÓN', 'Morado']}, {'artist': 'CNCO', 'songs': ['Reggaetón Lento (Bailemos)', 'Pegao', 'Me Necesita']}], 'Random Playlist 13': [{'artist': 'Sango', 'songs': ['Sangoloteadito - En Vivo Desde El Lunario/Mariachi/Banda', 'Sangoloteadito', 'Sango']}, {'artist': 'Dirty Heads', 'songs': ['Vacation', 'Oxygen', 'Lay Me Down']}], 'Random Playlist 14': [{'artist': 'Lipps Inc.', 'songs': ['Funky Town', 'Funkytown - Single Version', 'Funkytown']}, {'artist': 'Tone-Loc', 'songs': ['Wild Thing', 'Funky Cold Medina', 'Funky Cold Medina (Re-Recorded / Remastered)']}], 'Random Playlist 15': [{'artist': 'Panic! At The Disco', 'songs': ['High Hopes', 'Hey Look Ma, I Made It', 'I Write Sins Not Tragedies']}, {'artist': 'Milo', 'songs': ['Someday', 'Flesh & Bone', 'Like the Zombies Do']}], 'Random Playlist 16': [{'artist': 'iann dior', 'songs': ['emotions', 'molly', 'Good Day']}, {'artist': 'Drake', 'songs': ['Life Is Good (feat. Drake)', 'Money In The Grave (Drake ft. Rick Ross)', 'Going Bad (feat. Drake)']}], 'Random Playlist 17': [{'artist': 'Quiet Riot', 'songs': ['Cum on Feel the Noize', 'Cum on Feel the Noize', 'Metal Health (Bang Your Head)']}, {'artist': 'Alter Bridge', 'songs': ['Metalingus', 'Watch Over You', 'Blackbird']}], 'Random Playlist 18': [{'artist': 'Shotgun Willy', 'songs': ['Cheat Codes for Hoes', 'Wendy', 'Last Chance']}, {'artist': 'Jackson C. Frank', 'songs': ['Blues Run the Game - 2001 Remaster', 'My Name Is Carnival - 2001 Remaster', 'Milk and Honey - 2001 Remaster']}], 'Random Playlist 19': [{'artist': '50 Cent', 'songs': ['In Da Club', 'Candy Shop', '21 Questions']}, {'artist': 'Surf Curse', 'songs': ['Freaks', 'Disco', 'Disco']}], 'Random Playlist 20': [{'artist': 'K-Pop Rap Battles', 'songs': ['RM vs. Suga vs. J-Hope']}, {'artist': 'Jbrisko', 'songs': ['9 Tailz', 'On Me', 'Gone']}]}

    rating_info = {'Rating 1': {'playlist': 'Random Playlist 17', 'user': jim, 'stars': 0.3, 'date': today, 'comment': 'Pile of garbage'}, 'Rating 2': {'playlist': 'Random Playlist 17', 'user': jim, 'stars': 3.5, 'date': today, 'comment': 'My kind of playlist!'}, 'Rating 3': {'playlist': 'Random Playlist 14', 'user': fran, 'stars': 2.0, 'date': today, 'comment': 'Simply epic'}, 'Rating 4': {'playlist': "Now That's What I Call Romanian Folk-Pop", 'user': bob, 'stars': 4.0, 'date': today, 'comment': 'Awesome - I wish i was as cool as they are'}, 'Rating 5': {'playlist': 'Random Playlist 13', 'user': bob, 'stars': 1.9, 'date': today, 'comment': 'This made my baby cry. And Im not even a father.'}, 'Rating 6': {'playlist': 'Random Playlist 8', 'user': bob, 'stars': 0.5, 'date': today, 'comment': 'Not my cup of tea'}, 'Rating 7': {'playlist': 'i luv you stacy plz come back', 'user': sue, 'stars': 0.1, 'date': today, 'comment': 'What did i ever do to you?'}, 'Rating 8': {'playlist': 'Random Playlist 6', 'user': bob, 'stars': 1.8, 'date': today, 'comment': 'Not my cup of tea'}, 'Rating 9': {'playlist': 'Random Playlist 19', 'user': sue, 'stars': 0.9, 'date': today, 'comment': 'I wouldnt play this to my worst enemy'}, 'Rating 10': {'playlist': 'Random Playlist 11', 'user': sue, 'stars': 1.0, 'date': today, 'comment': 'What did i ever do to you?'}, 'Rating 11': {'playlist': 'Random Playlist 16', 'user': bob, 'stars': 1.6, 'date': today, 'comment': 'What a shambles'}, 'Rating 12': {'playlist': 'Random Playlist 6', 'user': fran, 'stars': 3.2, 'date': today, 'comment': 'Simply epic'}, 'Rating 13': {'playlist': 'Random Playlist 6', 'user': sue, 'stars': 1.8, 'date': today, 'comment': 'What a shambles'}, 'Rating 14': {'playlist': 'Random Playlist 13', 'user': jim, 'stars': 3.2, 'date': today, 'comment': 'Simply epic'}, 'Rating 15': {'playlist': 'Random Playlist 13', 'user': sue, 'stars': 1.8, 'date': today, 'comment': 'This made my baby cry. And Im not even a father.'}, 'Rating 16': {'playlist': 'Random Playlist 18', 'user': bob, 'stars': 4.4, 'date': today, 'comment': 'Got me right through my divorce, would recommend'}, 'Rating 17': {'playlist': 'Random Playlist 18', 'user': bob, 'stars': 0.0, 'date': today, 'comment': 'What did i ever do to you?'}, 'Rating 18': {'playlist': 'Random Playlist 13', 'user': sue, 'stars': 4.8, 'date': today, 'comment': 'Never heard anything like this before'}, 'Rating 19': {'playlist': 'Random Playlist 3', 'user': jim, 'stars': 2.9, 'date': today, 'comment': 'My kind of playlist!'}, 'Rating 20': {'playlist': 'Random Playlist 20', 'user': sue, 'stars': 4.8, 'date': today, 'comment': 'This will always be my summer 2019 playlist'}, 'Rating 21': {'playlist': 'Random Playlist 3', 'user': sue, 'stars': 1.1, 'date': today, 'comment': 'Not my cup of tea'}, 'Rating 22': {'playlist': 'Random Playlist 13', 'user': sue, 'stars': 3.6, 'date': today, 'comment': 'Never heard anything like this before'}, 'Rating 23': {'playlist': 'Random Playlist 15', 'user': sue, 'stars': 0.3, 'date': today, 'comment': 'I wouldnt play this to my worst enemy'}, 'Rating 24': {'playlist': 'Random Playlist 20', 'user': fran, 'stars': 3.1, 'date': today, 'comment': 'Simply epic'}, 'Rating 25': {'playlist': 'Random Playlist 5', 'user': fran, 'stars': 1.9, 'date': today, 'comment': 'Too loud'}, 'Rating 26': {'playlist': 'NedBeatz', 'user': fran, 'stars': 4.5, 'date': today, 'comment': 'Simply epic'}, 'Rating 27': {'playlist': 'Random Playlist 16', 'user': jim, 'stars': 1.1, 'date': today, 'comment': 'Not my cup of tea'}, 'Rating 28': {'playlist': 'Random Playlist 18', 'user': bob, 'stars': 2.7, 'date': today, 'comment': 'Never heard anything like this before'}, 'Rating 29': {'playlist': 'Random Playlist 8', 'user': jim, 'stars': 1.5, 'date': today, 'comment': 'Pile of garbage'}, 'Rating 30': {'playlist': 'Random Playlist 10', 'user': sue, 'stars': 2.1, 'date': today, 'comment': 'My kind of playlist!'}}

    print(" - Populating all Tags")
    for tag_description in tags:
        add_tag(tag_description)
        #print("Tag {0} added successfully".format(str(tag_description)))

    print(" - Populating Playlists")
    for p, pdata in playlist_info.items():
        add_playlist(p, pdata['tags'], pdata['creator'], pdata['createdDate'], pdata['lastUpdatedDate'],
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


def add_playlist(list, tags, creator, date1, date2, description):
    p = Playlist.objects.get_or_create(name=list)[0]

    for t in tags:
        found_tag = Tag.objects.get(description=t)
        p.tags.add(found_tag)
        #print(" - - added tag {0} to playlist {1}".format(str(found_tag.description), str(p.name)))

    p.creator = creator
    p.createdDate = date1
    p.lastUpdatedDate = date2
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
