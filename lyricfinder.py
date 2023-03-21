from lyricy import Lyricy

class Lyrics:
    def __init__(self, song, artist):
        self.song = song
        self.artist = artist
        self.lyrics = self.search_lyrics

    def __str__(self):
        return f'{self.song} - {self.artist}'
    
    def search_lyrics(self):
        l = Lyricy()

        try:
            results = l.search(self.__str__)
            selected_lyrics = results[0]
            selected_lyrics.fetch()
            return selected_lyrics.lyrics
        except:
            print("This song cannot be found")
