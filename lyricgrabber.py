import lyricsgenius as lg
from spotipy import Spotify, SpotifyOAuth
from dotenv import load_dotenv
import json
import os

load_dotenv()

scope = "user-read-currently-playing"
auth_manager = SpotifyOAuth(scope=scope)
spotify = Spotify(auth_manager=auth_manager)

genius = lg.Genius(os.environ.get("GENIUS_SECRET"))

def get_playback():
    playback = spotify.currently_playing()
    print(json.dumps(playback, indent=4))
    songTitle = playback['item']['name']
    artistName = playback['item']['album']['artists'][0]['name']
    return {'songTitle':songTitle, "aritstName":artistName}

def get_lyrics_genius(song):
    geniusLyrics = genius.search_song(title=song["songTitle"],artist=song["aritstName"])
    print(geniusLyrics.lyrics)
