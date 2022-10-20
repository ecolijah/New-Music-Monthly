import spotipy
from spotipy.oauth2 import SpotifyOAuth
import helpers

# This is a very rough first draft at new monthly playlists.

# playlist id -- constant
playlist_id = "4V8Is0FlL4aNGbAYorwwqp"

# creates and authorises our spotipy object
scope = 'user-follow-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# gets current user data
user = sp.current_user()
user_id = user['id']
displayName = user['display_name']

# prints json data in a readable format
# print(json.dumps(followed_artists,sort_keys=True, indent=4))

print(displayName + 's spotify' + '\n')

# gets user's followed artists (name and id) and creates list of artist objects.
artists = helpers.get_user_followed_artists(sp)
print(displayName + ' follows ' + str(len(artists)) + ' artists.')

# gets new albums/singles from artists and populates a dictionary within each artist object.
artists = helpers.get_artist_albums(artists, sp)

# creates list of all song ids to add to playlist.
song_ids_to_add = helpers.get_artist_tracks(artists, sp)
# need to check for duplicates. with itertools

# song limit to append is 100.
sng_ids_top = []
counter = 0
for x in song_ids_to_add:
    counter += 1
    if counter > 98:
        break
    sng_ids_top.append(x)
print("number of songs added to playlist: " + str(len(sng_ids_top)))

# remove duplicate songs
final_songs = helpers.remove_duplicates(sng_ids_top)
# redefine scope and create a new spotipy object
scope = 'playlist-modify-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# remove occurrences of tracks to avoid duplicates, then add tracks to playlist.
sp.user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, final_songs)
sp.playlist_add_items(playlist_id, final_songs)

print("It Worked!")