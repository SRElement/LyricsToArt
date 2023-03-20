import spotipy
import os
import lyricgrabber

def main():
    song = lyricgrabber.get_playback()
    print(song["songTitle"])
    lyricgrabber.get_lyrics_genius(song)

if __name__ == "__main__":
    main()

