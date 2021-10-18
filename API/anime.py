from bs4 import BeautifulSoup
import requests

BASEURL = "https://gogoanime.pe/"

# get the recently added anime per page
# parameter page defaults to 1
def getRecentAnime(page = 1):
    params = { "page" : page}
    recentlyAdded = []
    try:
        html = requests.get(url = BASEURL, params = params).text
        soup = BeautifulSoup(html, 'html.parser')
        for element in soup.select("ul.items li"):
            anime = {}
            anime["id"] = "-".join(element.p.a.attrs['href'].rsplit("-", 2)[:1])[1:]
            anime["name"] = element.div.a.attrs['title']
            anime["img"] = element.div.img.attrs['src']
            anime["ep"] = element.select("p.episode")[0].string.split(" ")[1]
            recentlyAdded.append(anime)
    except:
        return recentlyAdded
    return recentlyAdded

# get anime per page based on the genre
# parameter genre defaults to action
# parameter page defaults to 1
def getAnimeByGenre(genre = "action", page = 1):
    params = { "page" : page}
    animeByGenre = []
    try:
        html = requests.get(url = f'{BASEURL}/genre/{genre}', params = params).text
        soup = BeautifulSoup(html, 'html.parser')
        for element in soup.select("ul.items li"):
            anime = {}
            anime["id"] = element.p.a.attrs['href'][10:]
            anime["name"] = element.div.a.attrs['title']
            anime["img"] = element.div.img.attrs['src']
            animeByGenre.append(anime)
    except:
        return animeByGenre
    return animeByGenre

# get the popular anime per page
# parameter page defaults to 1
def getPopularAnime(page = 1):
    params = { "page" : page}
    popularAnime = []
    try:
        html = requests.get(url = f'{BASEURL}popular.html', params = params).text
        soup = BeautifulSoup(html, 'html.parser')
        for element in soup.select("ul.items li"):
            anime = {}
            anime["id"] = element.p.a.attrs['href'][10:]
            anime["name"] = element.div.a.attrs['title']
            anime["img"] = element.div.img.attrs['src']
            anime["released"] = element.select("p.released")[0].string.strip().strip("\n")
            popularAnime.append(anime)
    except:
        return popularAnime
    return popularAnime

# get the corresponding anime back based on the search value
# value defaults to ""
def getAnimeBySearchValue(value = ""):
    params = { "keyword" : value}
    searchResults = []
    try:
        html = requests.get(url = f'{BASEURL}/search.html', params = params).text
        soup = BeautifulSoup(html, 'html.parser')
        for element in soup.select("ul.items li"):
            anime = {}
            anime["id"] = element.p.a.attrs['href'][10:]
            anime["name"] = element.div.a.attrs['title']
            anime["img"] = element.div.img.attrs['src']
            searchResults.append(anime)
    except:
        return searchResults
    return searchResults

# get the details of an anime based on the id 
# id defaults to ""
def getAnimeDetails(id = ""):
    anime = {}
    try:
        html = requests.get(url = f'{BASEURL}/category/{id}').text
        soup = BeautifulSoup(html, 'html.parser')
        img = soup.select("div.anime_info_body_bg img")[0].attrs['src']
        name = soup.select("div.anime_info_body_bg h1")[0].string
        extra = soup.select("p.type")
        type = extra[0].a.attrs['title']
        plot_summary = extra[1].contents[1]
        released = extra[3].contents[1]
        status = extra[4].a.string
        totalEpisode = soup.select("#episode_page a")[-1].attrs["ep_end"]
        genres = [element.string for element in extra[2].find_all("a")]
        anime = {
            "img" : img,
            "name": name,
            "plot summary" : plot_summary,
            "type" : type,
            "status": status,
            "released": released,
            "genres": genres,
            "totalEpisodes": totalEpisode
        }
    except:
        return anime
    return anime

# get the episode of the specified anime
# id is required
# ep defaults to 1
def getAnimeEpisode(id, ep = 1):
    video = {}
    try:
        html = requests.get(url = f'{BASEURL}{id}-episode-{ep}').text
        soup = BeautifulSoup(html, 'html.parser')
        video_src = "https:" + soup.select("div.play-video")[0].iframe.attrs['src']
        print(soup.select("div.play-video"))
        video = {
            "video": video_src
        }      
    except:
        return video
    return video

if __name__ == "__main__":
    getPopularAnime()