import spotipy
import os
from spotifyconnection import SpotifyConnection
from lyricfinder import Lyrics
from time import sleep

def main():
    spotify = SpotifyConnection()
    songInfo = spotify.get_playback()
    songLyrics = Lyrics(song=songInfo["songTitle"], artist=songInfo["artistName"])
    lyrics = songLyrics.__lyrics__()
    timeStamps = songLyrics.__timeStamps__()
    
    maxIndex = len(timeStamps)-1
    lastTimeStamp = 0
    currentIndex = -1

    print("Ready")

    while True:
        state = spotify.get_playback_state()
         
        if state["is_playing"] == True:
            progressMs = state["progress_ms"]

            if progressMs <= timeStamps[0]: #If not past first lyric
                currentIndex = -1
            elif progressMs >= timeStamps[maxIndex]: #If past last lyric
                currentIndex = maxIndex
            else:
                for i in range(0,maxIndex-1): #Else find position and current lyric DOES IT NEED TO BE ZERO OR CAN DO LAST INDEX?
                    if progressMs >= timeStamps[i] and progressMs <= timeStamps[i+1]: #If between two lyrics its the current i
                        currentIndex = i

            if currentIndex > -1: #If song past first lyric
                currentLyric = lyrics[currentIndex]
                currentTimeStamp = timeStamps[currentIndex]
                if lastTimeStamp != currentTimeStamp: #If not last printed to user print the lyric
                    print(currentLyric)
                    lastTimeStamp = currentTimeStamp
                        

if __name__ == "__main__":
    main()

