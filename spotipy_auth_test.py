import spotipy
from spotipy.oauth2 import SpotifyOAuth
import artist
import json
import helpers
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
    artist_albums = sp.artist_albums(x.spotify_id)
    for i, item in enumerate(artist_albums['items']):

        if helpers.isNew(item['release_date']):
            temp_album_name = item['name']
            temp_album_id = item['id']
            x.albums.update({temp_album_name: temp_album_id})
            print(x.name + " - " + temp_album_name)


# now we have all artist objects populated with their albums dictionary
song_ids_to_add = []
# now let's create a master list of all the songs to add to the playlisT
for x in artists:
    for key in x.albums:
        temp_id = key.value()
        a = sp.album_tracks()
