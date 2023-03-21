import spotipy
import os
from spotifyconnection import SpotifyConnection
from lyricfinder import Lyrics

def main():
    spotify = SpotifyConnection()
    songInfo = spotify.get_playback()
    songLyrics = Lyrics(song=songInfo["songTitle"], artist=songInfo["artistName"])
    print(songLyrics.format_lyrics())


if __name__ == "__main__":
    main()

