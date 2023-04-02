from flask import Flask, redirect, render_template, request, jsonify
from dotenv import load_dotenv
from lyricfinder import Lyrics

from spotifyconnection import SpotifyConnection

load_dotenv('./.flaskenv')

app = Flask(__name__)

spotify = SpotifyConnection()

test = "test"

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/lyricstoart")
def lyricstoart():
    return render_template("lyricstoart.html")

    
@app.route("/getSongInfo", methods=["GET"])
def getSongInfo():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return(jsonify(spotify.get_playback()))


@app.route("/getLyrics", methods=["GET"])
def getLyrics():
    songInfo = spotify.get_playback()
    songLyrics = Lyrics(song="Budapest",artist="George Ezra")
    #songLyrics = Lyrics(song=songInfo["songTitle"], artist=songInfo["artistName"])#Get the lyrics

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return(songLyrics.__JSON__())
    


@app.route("/getPlayback", methods=["GET"])
def getPlayback():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return(jsonify(spotify.get_playback_state()))
        



    #Is Spotify playing?
    #Yes = Get lyric
    #No = Display pause, click again to start

    #THEN
    #Once lyrics have been retrived
    #COnstantly get playback stated



if __name__ == '__main__':
    app.run()