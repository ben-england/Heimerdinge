import discord
from discord.ext import commands
import requests
from botconnectioninfo import returntoken
from api_info import returnapikey

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)

@client.event
async def on_ready():
    print("Bot is online")
    print("----------------------")


#invoking function from other file
client.run(returntoken())
