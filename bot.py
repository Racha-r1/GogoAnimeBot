from dotenv import load_dotenv
import discord
import os

load_dotenv() 

class MyClient(discord.Client):
    async def on_ready(self):
        print('Bot is running !')

    async def on_message(self, message):
        if message.content.startswith('!anime '):
            anime_name = message.content.split(" ", 1)[1]
            await message.channel.send(anime_name)

client = MyClient()
client.run(os.environ.get("BOT-TOKEN"))