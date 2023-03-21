from spotipy import Spotify, SpotifyOAuth
from dotenv import load_dotenv
import json
import os

load_dotenv()

class SpotifyConnection():
    def __init__(self):
        self.scope = ''

    def set_scope(self, scope):
        if self.scope != scope:
            self.scope = scope
        auth_manager = SpotifyOAuth(scope=self.scope)
        self.connection = Spotify(auth_manager=auth_manager)

    def get_playback(self):
        self.set_scope("user-read-currently-playing")

        playback = self.connection.currently_playing()

        songTitle = playback['item']['name']
        artistName = playback['item']['album']['artists'][0]['name']
        return {'songTitle':songTitle, "artistName":artistName}
    
    def get_playback_state(self):
        self.set_scope("user-read-playback-state")

        playback = self.connection.current_playback()
        # print(json.dumps(playback, indent=4))

        isPlaying = playback['is_playing']
        progressMs = playback['progress_ms']

        return {'is_playing':isPlaying,'progress_ms':progressMs}

        






