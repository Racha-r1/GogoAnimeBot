from bs4 import BeautifulSoup
import requests

BASEURL = "https://gogoanime.pe/"

def getRecentAnime(page = 1):
    params = { "page" : page}
    html = requests.get(url = BASEURL, params = params).text
    soup = BeautifulSoup(html, 'html.parser')
    recentlyAdded = []
    for element in soup.select("div.img"):
        anime = {}
        anime["id"] = element.a.attrs['title']
        anime["name"] = element.a.attrs['title']
        anime["img"] = element.img.attrs['src']
        recentlyAdded.append(anime)
    return recentlyAdded

def getAnimeByGenre(genre = "action", page = 1):
    params = { "page" : page}
    html = requests.get(url = f'{BASEURL}/genre/{genre}', params = params).text
    soup = BeautifulSoup(html, 'html.parser')
    animeByGenre = []
    for element in soup.select("div.img"):
        anime = {}
        anime["id"] = element.a.attrs['title']
        anime["name"] = element.a.attrs['title']
        anime["img"] = element.img.attrs['src']
        animeByGenre.append(anime)
    return animeByGenre

def getPopularAnime(page = 1):
    params = { "page" : page}
    html = requests.get(url = f'{BASEURL}/popular.html', params = params).text
    soup = BeautifulSoup(html, 'html.parser')
    popularAnime = []
    for element in soup.select("div.img"):
        anime = {}
        anime["id"] = element.a.attrs['title']
        anime["name"] = element.a.attrs['title']
        anime["img"] = element.img.attrs['src']
        popularAnime.append(anime)
    return popularAnime

