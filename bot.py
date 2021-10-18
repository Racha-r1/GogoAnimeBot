from dotenv import load_dotenv
import discord
import os
import requests
from API.api import app
from threading import Thread
from functools import partial
from disputils import BotEmbedPaginator
from discord.ext import commands
import asyncio

load_dotenv() 

API_URL = "http://localhost:8080/"
GOGO_URL = "https://gogoanime.pe/category"

bot = commands.Bot(command_prefix='!')

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

def givePopularAnime():
    counter = 1
    embeds = []
    for i in range(1,6):
        response = requests.get(url = f'{API_URL}/popular', params={"page": i}).json()
        embed=discord.Embed(color=0x115599)
        ranking = []
        for anime in response:
            ranking.append("#{} - {}".format(counter, anime["name"]))
            counter += 1
        embed.add_field(name=f'✨ Top 100 Anime', value="\n".join(ranking))
        embeds.append(embed)
    return embeds

def giveRecentReleases():
    counter = 1
    embeds = []
    for i in range(1,6):
        response = requests.get(url = f'{API_URL}', params={"page": i}).json()
        embed=discord.Embed(color=0x115599)
        recent = []
        for anime in response:
            recent.append("{} (ep-{} out now)".format(anime["name"], anime["ep"]))
            counter += 1
        embed.add_field(name=f'📅 Recent releases', value="\n".join(recent))
        embeds.append(embed)
    return embeds

@bot.event
async def on_ready():
    print(bot.user.name + " is ready")

@bot.command()
async def popular(ctx):
    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
    bot.help_pages = givePopularAnime()
    current = 0
    msg = await ctx.send(embed=bot.help_pages[current])
    
    for button in buttons:
        await msg.add_reaction(button)
        
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=100000)

        except asyncio.TimeoutError:
            return print("test")

        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0
                
            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1
                    
            elif reaction.emoji == u"\u27A1":
                if current < len(bot.help_pages)-1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(bot.help_pages)-1

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)

            if current != previous_page:
                await msg.edit(embed=bot.help_pages[current])

@bot.command()
async def recent(ctx):
    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
    bot.help_pages = giveRecentReleases()
    current = 0
    msg = await ctx.send(embed=bot.help_pages[current])
    
    for button in buttons:
        await msg.add_reaction(button)
        
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=100000)

        except asyncio.TimeoutError:
            return print("test")

        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0
                
            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1
                    
            elif reaction.emoji == u"\u27A1":
                if current < len(bot.help_pages)-1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(bot.help_pages)-1

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)

            if current != previous_page:
                await msg.edit(embed=bot.help_pages[current])

@bot.command()
async def anime(ctx):
    anime_name = ctx.message.content.split(" ", 1)[1]
    embeds = giveAnimeEmbed(anime_name)
    if len(embeds) < 1:
        await ctx.message.channel.send("NOTHING FOUND FOR YOUR ANIME SEARCH")
    await ctx.message.channel.send(embed = embeds[0])
    
if __name__ == '__main__':

    # run the api in a different thread
    partial_run = partial(app.run, host="127.0.0.1", port=8080, debug=True, use_reloader=False)
    t = Thread(target=partial_run)
    t.start()
    
    # run the bot
    bot.run(os.environ.get("BOT-TOKEN"))
