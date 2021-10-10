from dotenv import load_dotenv
import discord
import os
import requests
from API.api import app
from threading import Thread
from functools import partial

load_dotenv() 

API_URL = "http://localhost:8080/"
GOGO_URL = "https://gogoanime.pe/category";

def giveAnimeEmbed(anime_name):
    embeds = []
    try:
        response = requests.get(url = f'{API_URL}search?keyword={anime_name}').json()
        # get the first search result (should be the closest result for the searched keyword)
        firstMatch = response[0]
        anime = requests.get(url = f'{API_URL}details/{firstMatch["id"]}').json()
        # make the embed 
        embed=discord.Embed(title=anime["name"], url=f'{GOGO_URL}/{firstMatch["id"]}', description=anime["plot summary"], color=0x45B7C1)
        embed.set_thumbnail(url=anime["img"])
        embed.add_field(name=f'✨ Status', value=anime["status"], inline=True)
        embed.add_field(name='🔔 Type', value=anime["type"], inline=True)
        embed.add_field(name=f'▶️ Genres', value=" ".join(anime["genres"]), inline=False)
        embed.add_field(name=f'🌀 TotalEpisodes', value=anime["totalEpisodes"], inline=True)
        embed.add_field(name=f'📅 Released', value=anime["released"], inline=True)
        embeds.append(embed)
    except:
        return embeds
    return embeds

class MyClient(discord.Client):
    async def on_ready(self):
        print('Bot is running !')

    async def on_message(self, message):
        if message.content.startswith('!anime '):
            anime_name = message.content.split(" ", 1)[1]
            embeds = giveAnimeEmbed(anime_name)
            if len(embeds) < 1:
                await message.channel.send("NOTHING FOUND FOR YOUR ANIME SEARCH")
            await message.channel.send(embed = embeds[0])

if __name__ == '__main__':
    client = MyClient()
    partial_run = partial(app.run, host="127.0.0.1", port=8080, debug=True, use_reloader=False)
    t = Thread(target=partial_run)
    t.start()

    client.run(os.environ.get("BOT-TOKEN"))

