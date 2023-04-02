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

def hashString(stringToHash):
    hash = hashlib.md5()
    hash.update(stringToHash)
    str(int(hash.hexdigest(), 16))[0:12]

    return stringToHash
    


class Lyrics:
    def __init__(self, song, artist):
        self.song = song
        self.artist = artist

        self.lyrics = []
        self.timeStampsMs = []
        self.emotions = []
        self.lyricJson = {}

        self.fetch()

    def __lyrics__(self):
        return self.lyrics
    
    def __timeStamps__(self):
        return self.timeStamps
    
    def __emotions__(self):
        return self.emotions
    
    def fetch(self):
        l = Lyricy()

        try:
            query = self.song.lower()
            results = l.search(query)
            selected_lyrics = results[0]
            selected_lyrics.fetch()
            self.format(selected_lyrics.lyrics)
        except:
            print("This song cannot be found")
            return None
        
    def format(self,lyrics):
        emotionModel = TextToEmotion()

        self.timeStamps = timestampsToMs(re.findall("\[(0.*?)\]", lyrics))
        self.lyrics = re.findall("(?<=\]).*[^-\s]", lyrics)
        self.emotions = emotionModel.labelEmotionsFromList(self.lyrics)

        lyricJson = {}

        for i in range(0,len(self.timeStamps)):
            lyricJson.append({"id" : hashString(self.lyrics),"timeStampMs" : self.timeStampsMs[i], "lyric" : self.lyrics[i]})

        self.lyricJson = json.dumps(lyricJson)

