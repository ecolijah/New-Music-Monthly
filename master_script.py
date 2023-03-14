import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

import helpers
# env variables
load_dotenv()

# SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
# SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
# SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

SPOTIPY_CLIENT_ID = '5b2e0915fcbb42f6a03f85d4bf8a7391'
SPOTIPY_CLIENT_SECRET = '6b51587483274dbabd51391be05dafcd'
SPOTIPY_REDIRECT_URI = 'https://poopysite000.com/callback/'

print(SPOTIPY_CLIENT_ID)
# This is a very rough first draft at new monthly playlists.

# playlist id -- constant
playlist_id = "4V8Is0FlL4aNGbAYorwwqp"
scope = 'user-follow-read playlist-modify-private'

# creates and authorises our spotipy object with both necessary scopes.
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))

# gets current user data
user = sp.current_user()
user_id = user['id']
displayName = user['display_name']
print(displayName + 's spotify' + '\n')

# prints json data in a readable format -- helpful for testing
# print(json.dumps(followed_artists,sort_keys=True, indent=4))

# gets user's followed artists (name and id) and creates list of artist objects.
artists = helpers.get_user_followed_artists(sp)
print(displayName + ' follows ' + str(len(artists)) + ' artists.')
print("New Music:" + '\n')
# gets new albums/singles from artists and populates a dictionary within each artist object.
artists = helpers.get_artist_albums(artists, sp)

# creates list of all song ids to add to playlist.
song_ids = helpers.get_artist_tracks(artists, sp)

# remove duplicate songs
final_songs = helpers.remove_duplicates(song_ids)
print('\n' + "number of songs added to playlist: " + str(len(final_songs)) + '\n')

# this spotipy method empties the playlist and appends the new songs in one command, yay, limit?
sp.playlist_replace_items(playlist_id, final_songs)

print("It Worked!")