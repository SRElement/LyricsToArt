from lyricy import Lyricy
import json
import re
import hashlib

from textemotions import TextToEmotion

def timestampsToMs(timeStamps):

    for i in range (0,len(timeStamps)):
            hours, minutes, seconds = (["0", "0"] + timeStamps[i].split(":"))[-3:]
            hours = int(hours)
            minutes = int(minutes)
            seconds = float(seconds)
            miliseconds = int(3600000 * hours + 60000 * minutes + 1000 * seconds)
            timeStamps[i] = miliseconds

    return timeStamps

def hashString(strToHash): #To find imgs?
    hash = hashlib.md5()
    hash.update(strToHash.encode('utf-8'))
    hashedStr = str(int(hash.hexdigest(), 16))[0:12]

    return hashedStr
    

class Lyrics:
    def __init__(self, song, artist):
        self.song = song
        self.artist = artist

        self.lyrics = []
        self.timeStampsMs = []
        self.emotions = []
        self.lyricJson = {}

        self.fetch_lyrics()

    def __JSON__(self):
         return self.lyricJson
    
    def fetch_lyrics(self):
        l = Lyricy()
        songFound = False

        query = self.song.lower()
        print("Searching... " + query)

        results = l.search(query)
        resultIndex = 0
        resultMaxIndex = len(results)

        while songFound == False and resultIndex != resultMaxIndex:
            if self.artist.lower() in results[resultIndex].title.lower():
                selected_lyrics = results[int(results[resultIndex].index)-1]
                selected_lyrics.fetch()
                self.format(selected_lyrics.lyrics)
                songFound = True
            elif "no result found" in results[resultIndex].title.lower():
                self.lyricJson = {}

            resultIndex += 1

        print("SongFound = " + str(songFound))


        

        
    def format(self,lyrics):

        emotionModel = TextToEmotion()

        self.timeStampsMs = timestampsToMs(re.findall("\[(0.*?)\]", lyrics))
        self.lyrics = re.findall("(?<=\]).*[^-\s]", lyrics)
        self.emotions = emotionModel.labelEmotionsFromList(self.lyrics)


        for i in range(0,len(self.lyrics)-1):
            self.lyricJson[self.timeStampsMs[i]] = {"lyric" : self.lyrics[i], "emotion" : self.emotions[i], "hash_id" : hashString(self.lyrics[i])}
        self.lyricJson["time_stamps_ms"] = self.timeStampsMs

        self.lyricJson = json.dumps(self.lyricJson, indent=4)

