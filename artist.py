
class Artist:

    def __init__(self, name, spotify_id):
        self.name = name
        self.spotify_id = spotify_id
        self.albums = {}
        self.songs = {}
