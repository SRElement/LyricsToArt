import spotipy
import os
from spotifyconnection import SpotifyConnection
from lyricfinder import Lyrics
from time import sleep

def main():
    spotify = SpotifyConnection()
    while True:
        spotify.get_playback()
    print(spotify.get_playback_state())
    #songLyrics = Lyrics(song=songInfo["songTitle"], artist=songInfo["artistName"])
    #songLyrics = Lyrics(song="Budapest",artist="George Ezra")
    
    print("Ready")

    

    # while True:
    #     state = spotify.get_playback_state()
         
    #     if state["is_playing"] == True:
    #         progressMs = state["progress_ms"]

    #         if progressMs <= timeStamps[0]: #If not past first lyric
    #             currentIndex = -1
    #         elif progressMs >= timeStamps[maxIndex]: #If past last lyric
    #             currentIndex = maxIndex
    #         else:
    #             for i in range(0,maxIndex-1): #Else find position and current lyric DOES IT NEED TO BE ZERO OR CAN DO LAST INDEX?
    #                 if progressMs >= timeStamps[i] and progressMs <= timeStamps[i+1]: #If between two lyrics its the current i
    #                     currentIndex = i

    #         if currentIndex > -1: #If song past first lyric
    #             currentLyric = lyrics[currentIndex]
    #             currentTimeStamp = timeStamps[currentIndex]
    #             currentEmotion = emotions[currentIndex]
    #             if lastTimeStamp != currentTimeStamp: #If not last printed to user print the lyric
    #                 print(currentLyric + ' = ' + currentEmotion)
    #                 lastTimeStamp = currentTimeStamp
                        

if __name__ == "__main__":
    main()
