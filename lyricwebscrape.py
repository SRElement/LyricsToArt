from lyricy import Lyricy

l = Lyricy()
results = l.search("As the world caves in")
selected_lyrics = results[0]
selected_lyrics.fetch()

print(selected_lyrics.lyrics)