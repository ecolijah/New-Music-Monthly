import spotipy
from spotipy.oauth2 import SpotifyOAuth
import artist
import json
import helpers
import sys
# This is a very rough first draft at new monthly playlists.

# variables
artists = []        # this will be an array of artist objects
artistsIDs = {}     # dict object with artists as keys, and their ID's as the corresponding values.


# scope defines what the query can read and return, or edit.
scope = 'user-follow-read'
# creates and authorises our spotify object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# gets user followed artists
followed_artists = sp.current_user_followed_artists(49)

# gets current user data
user = sp.current_user()
user_id = user['id']
displayName = user['display_name']


# prints json data in a readable format
# print(json.dumps(followed_artists,sort_keys=True, indent=4))


print(displayName + 's spotify' + '\n')
# HELL FUCKING YEAH, PRINTS OUT up to 50 FOLLOWED ARTISTS BEEN TRYING FOR HOURS
for i, item in enumerate(followed_artists['artists']['items']):
    temp = artist.Artist(item['name'], item['id'])
    artists.append(temp)
    # print(temp.name + ' ID: ' + temp.spotify_id)


print(displayName + ' follows ' + str(len(artists)) + ' artists.')


# print(artistsIDs.items())

# now we have a dict object with each of our followed artists keys.
# now we need to loop through all of our albums and append
# this would be easier with class objects like artist, album, etc

# artist_albums = sp.artist_albums(artists[3].spotify_id)
# print(json.dumps(artist_albums, sort_keys=True, indent=4))

for x in artists:
    # need to iterate between each artist and add each album of each artist into artist object dictionary
    artist_albums = sp.artist_albums(x.spotify_id,album_type='album' or 'single')
    for i, item in enumerate(artist_albums['items']):

        if helpers.isNew(item['release_date']):
            temp_album_name = item['name']
            temp_album_id = item['id']
            x.albums.update({temp_album_name: temp_album_id})
            print(x.name + " - " + temp_album_name)


# now we have all artist objects populated with their albums dictionary
song_ids_to_add = []



#print(json.dumps(artist_albums, sort_keys=True, indent=4))
# now let's create a master list of all the songs to add to the playlisTfor x in artists:
for x in artists:
    for key in x.albums:
        temp_album_id = x.albums[key]
        #print(temp_album_id)
        songs_in_album = sp.album_tracks(temp_album_id)
        #print(json.dumps(songs_in_album, sort_keys=True, indent=4))
        # for i, item in enumerated

        for i, item in enumerate(songs_in_album['items']):
            tmp_song_id = item['id']
            song_ids_to_add.append(tmp_song_id)
            #print(tmp_song_id)

        # sys.exit('bleh.')

sng_ids_top = []
for x in song_ids_to_add:
    print("id: " + x)

counter = 0
for x in song_ids_to_add:
    counter += 1
    if counter > 90:
        break
    sng_ids_top.append(x)

print("num songs to add: " + str(len(song_ids_to_add)))

playlist_id = "4V8Is0FlL4aNGbAYorwwqp"
scope = 'playlist-modify-private'
print("num top songs: " + str(len(sng_ids_top)))
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
sp.user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, sng_ids_top)
sp.playlist_add_items(playlist_id, sng_ids_top)

print("It Worked!")