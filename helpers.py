from datetime import datetime
from dateutil.relativedelta import relativedelta
import artist
from collections import OrderedDict


def is_new(release_date):
    """
    :param release_date: release date of album.
    :return: boolean depicting if new or not.
    """
    # date to be greater than.
    new_date = datetime.today() - relativedelta(months=1)
    try:
        release_date_obj = datetime.strptime(release_date, '%Y-%m-%d')
    except:
        print("error for this album date: " + release_date)
        return False

    if new_date < release_date_obj:
        return True
    else:
        return False


def get_user_followed_artists(sp):
    """
    :param sp: spotipy object for api queries.
    :return: return list (artists) with updated artist objects.
    """
    followed_artists = sp.current_user_followed_artists(49)
    artists = []
    for i, item in enumerate(followed_artists['artists']['items']):
        temp_artist_obj = artist.Artist(item['name'], item['id'])
        artists.append(temp_artist_obj)

    return artists


def get_artist_albums(artists, sp):
    """
    :param artists: list of artist objects.
    :param sp: spotipy object for api queries.
    :return: we return the updated artist list.
    """
    for x in artists:

        artist_albums = sp.artist_albums(x.spotify_id, album_type='album')
        artist_singles = sp.artist_albums(x.spotify_id, album_type='single')

        for i, item in enumerate(artist_albums['items']):
            if is_new(item['release_date']):
                temp_album_name = item['name']
                temp_album_id = item['id']
                x.albums.update({temp_album_name: temp_album_id})
                print(x.name + " - " + temp_album_name)

        for i, item in enumerate(artist_singles['items']):
            if is_new(item['release_date']):
                temp_album_name = item['name']
                temp_album_id = item['id']
                x.albums.update({temp_album_name: temp_album_id})
                print(x.name + " - " + temp_album_name)

    return artists


def get_artist_tracks(artists, sp):
    """
    :param artists: list of artist objects.
    :param sp: spotipy object for api queries.
    :return: a list containing desired song ids.
    """
    song_ids_to_add = []
    for x in artists:
        for key in x.albums:
            temp_album_id = x.albums[key]
            songs_in_album = sp.album_tracks(temp_album_id)

            for i, item in enumerate(songs_in_album['items']):
                tmp_song_id = item['id']
                song_ids_to_add.append(tmp_song_id)

    return song_ids_to_add


def remove_duplicates(songs):
    """
    :param songs: list of songs, may have duplicates.
    :return: new list of songs, no duplicates.
    """
    # preserves order, removes duplicates
    tmp_list = list(OrderedDict.fromkeys(songs))
    return tmp_list
