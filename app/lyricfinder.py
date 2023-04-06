from lyricy import Lyricy
import json
import re
import os
import hashlib

from texttoimg import MinDalleTextToImage
from promtgeneration import PromptGenerator

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

def genImageForLyrics(song_id, lyrics):
        
        promtGen = PromptGenerator()
        d = MinDalleTextToImage()

        completed = []

        if not(os.path.exists("static/IMG/" + str(song_id))):
            for lyric in lyrics:

                if not(hashString(lyric.lower()) in completed):
                    prompt = promtGen.generatePromtFromString(lyric)

                    print(lyric)
                    print(prompt)

                    if prompt != '':
                        d.generate_image(
                        is_mega=d.__args__().mega,
                        text= prompt + ", Photorealistic",
                        seed=d.__args__().seed,
                        grid_size=d.__args__().grid_size,
                        top_k=d.__args__().top_k,
                        image_path= str(hashString(lyric.lower())),
                        models_root=d.__args__().models_root,
                        fp16=d.__args__().fp16,
                        file_dir= "static/IMG/" + str(song_id)
                        )

                        completed.append(hashString(lyric.lower()))
    

class Lyrics:
    def __init__(self, songId, song, artist):

        self.songId = songId
        self.song = song
        self.artist = artist

        self.lyrics = []
        self.timeStampsMs = []
        self.imgs = []
        self.lyricJson = {}

        self.fetch_lyrics()

    def __JSON__(self):
         return self.lyricJson
    
    def fetch_lyrics(self):
        l = Lyricy()
        songFound = False

        query = self.song.lower()
        print("Searching for... " + query)

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

        self.timeStampsMs = timestampsToMs(re.findall("\[(0.*?)\]", lyrics))
        self.lyrics = re.findall("(?<=\]).*[^-\s]", lyrics)
        genImageForLyrics(self.songId, self.lyrics)


        for i in range(0,len(self.lyrics)-1):
            self.lyricJson[self.timeStampsMs[i]] = {"lyric" : self.lyrics[i], "hash_id" : hashString(self.lyrics[i].lower())} #Set to lower for consitence beutiful != Beutiful otherwise
        self.lyricJson["time_stamps_ms"] = self.timeStampsMs

        self.lyricJson = json.dumps(self.lyricJson, indent=4)