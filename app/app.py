from flask import Flask, redirect, render_template, request, jsonify
from dotenv import load_dotenv
import os

from lyricfinder import Lyrics
from spotifyconnection import SpotifyConnection

load_dotenv('./.flaskenv')

app = Flask(__name__)

spotify = SpotifyConnection()

test = "test"

@app.route('/')
def index():
    return render_template("lyricstoart.html")
    

@app.route("/getSongInfo", methods=["GET"])
def getSongInfo():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return(jsonify(spotify.get_playback()))


@app.route("/getLyrics/<artist>/<song>/<songID>", methods=["GET"])
def getLyrics(artist,song,songID):
    songInfo = spotify.get_playback()
    songLyrics = Lyrics(songID, song, artist)#Get the lyrics

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return(songLyrics.__JSON__())
    


@app.route("/getPlayback", methods=["GET"])
def getPlayback():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return(jsonify(spotify.get_playback_state()))
    


@app.route("/getSongImages/<songID>", methods=["GET"])
def getSongImages(songID):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        IMG_FOLDER = os.path.join('static/IMG', songID)
        app.config['UPLOAD_FOLDER'] = IMG_FOLDER

        IMG_LIST = os.listdir('static/IMG/' + songID)
        IMG_JSON = {}
        for img in IMG_LIST:
            IMG_JSON[img.replace(".png", "")] = "static/IMG/" + songID + "/" + img
        return(jsonify(IMG_JSON))
        



if __name__ == '__main__':
    app.run()