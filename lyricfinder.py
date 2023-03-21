from lyricy import Lyricy
import re

class Lyrics:
    def __init__(self, song, artist):
        self.song = song
        self.artist = artist
        self.lyrics = []
        self.timeStamps = []
        self.timeStampedlyrics = {}

        self.search_lyrics()

    def __lyrics__(self):
        return self.lyrics
    
    def __timeStamps__(self):
        return self.timeStamps
    
    def search_lyrics(self):
        l = Lyricy()

        try:
            query = self.song.lower()
            print(query)
            results = l.search(query)
            selected_lyrics = results[0]
            selected_lyrics.fetch()
            print(selected_lyrics.lyrics)
            self.format_lyrics(selected_lyrics.lyrics)
        except:
            print("This song cannot be found")
            return None
        
    def format_lyrics(self,lyrics):
        self.timeStamps = re.findall("\[(0.*?)\]", lyrics)
        self.lyrics = re.findall("(?<=\]).*[^-\s]", lyrics)

        for i in range (0,len(self.timeStamps)):
            hours, minutes, seconds = (["0", "0"] + self.timeStamps[i].split(":"))[-3:]
            hours = int(hours)
            minutes = int(minutes)
            seconds = float(seconds)
            miliseconds = int(3600000 * hours + 60000 * minutes + 1000 * seconds)
            self.timeStamps[i] = miliseconds


        self.timeStampedlyrics = dict(zip(self.timeStamps,lyrics))
