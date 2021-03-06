from flask import Flask, json, request
from API.anime import *

app = Flask(__name__)

@app.route("/")
def recentAnime():
    page = int(request.args.get("page")) if request.args.get("page") is not None else 1
    results = getRecentAnime(page)
    return json.dumps(results)
    
@app.route("/genre/<genre>")
def animeByGenre(genre):
    page = int(request.args.get("page")) if request.args.get("page") is not None else 1
    genre = genre.lower()
    results = getAnimeByGenre(genre, page)
    return json.dumps(results)

@app.route("/popular")
def popularAnime():
    page = int(request.args.get("page")) if request.args.get("page") is not None else 1
    results = getPopularAnime(page)
    return json.dumps(results)

@app.route("/search")
def searchAnime():
    searchValue = request.args.get("keyword")
    results = getAnimeBySearchValue(searchValue) if searchValue is not None else getAnimeBySearchValue()
    return json.dumps(results)

@app.route("/details/<id>")
def animeDetails(id):
    result = getAnimeDetails(id)
    return json.dumps(result)

@app.route("/watch/<id>")
def animeVideo(id):
    ep = request.args.get("episode")
    result = getAnimeEpisode(id, ep) if ep is not None else getAnimeEpisode(id)
    return json.dumps(result)  

    