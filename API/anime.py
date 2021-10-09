from bs4 import BeautifulSoup
import requests

BASEURL = "https://gogoanime.pe/"

# get the recently added anime per page
# parameter page defaults to 1
def getRecentAnime(page = 1):
    params = { "page" : page}
    html = requests.get(url = BASEURL, params = params).text
    soup = BeautifulSoup(html, 'html.parser')
    recentlyAdded = []
    for element in soup.select("ul.items li"):
        anime = {}
        anime["id"] = "-".join(element.p.a.attrs['href'].rsplit("-", 2)[:1])[1:]
        anime["name"] = element.div.a.attrs['title']
        anime["img"] = element.div.img.attrs['src']
        recentlyAdded.append(anime)
    return recentlyAdded

# get anime per page based on the genre
# parameter genre defaults to action
# parameter page defaults to 1
def getAnimeByGenre(genre = "action", page = 1):
    params = { "page" : page}
    html = requests.get(url = f'{BASEURL}/genre/{genre}', params = params).text
    soup = BeautifulSoup(html, 'html.parser')
    animeByGenre = []
    for element in soup.select("ul.items li"):
        anime = {}
        anime["id"] = element.p.a.attrs['href'][10:]
        anime["name"] = element.div.a.attrs['title']
        anime["img"] = element.div.img.attrs['src']
        animeByGenre.append(anime)
    return animeByGenre

# get the popular anime per page
# parameter page defaults to 1
def getPopularAnime(page = 1):
    params = { "page" : page}
    html = requests.get(url = f'{BASEURL}/popular.html', params = params).text
    soup = BeautifulSoup(html, 'html.parser')
    popularAnime = []
    for element in soup.select("ul.items li"):
        anime = {}
        anime["id"] = element.p.a.attrs['href'][10:]
        anime["name"] = element.div.a.attrs['title']
        anime["img"] = element.div.img.attrs['src']
        popularAnime.append(anime)
    return popularAnime
