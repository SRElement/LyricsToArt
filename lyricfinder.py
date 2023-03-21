from lyricy import Lyricy
import re

class Lyrics:
    def __init__(self, song, artist):
        self.song = song
        self.artist = artist
        self.lyrics = self.search_lyrics()

    def __str__(self):
        return self.lyrics
    
    def search_lyrics(self):
        l = Lyricy()

        try:
            query = self.song.lower()
            print(query)
            results = l.search(query)
            selected_lyrics = results[0]
            selected_lyrics.fetch()
            return selected_lyrics.lyrics
        except:
            print("This song cannot be found")
            return None
        
    def format_lyrics(self):
        timestamps = re.findall("\[(0.*?)\]", self.lyrics)  
        words = re.findall("(?<=\]).*[^-\s]", self.lyrics)
        print(timestamps)
        print(words)
