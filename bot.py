import discord
from discord.ext import commands
#installed requests using pip
import requests
#importing tokens and api keys from another file for safety
from botconnectioninfo import returntoken
from api_info import returnapikey

intents = discord.Intents.default()
intents.members = True

#command prefix
client = commands.Bot(command_prefix = '!', intents=intents)

@client.event
async def on_ready():
    print("Bot is online")
    print("----------------------")

@client.command()
async def summoner(ctx: commands.Context):
    await ctx.send("Please input the summoner name! Please include the hash to ensure the correct account is loaded")
    message = await client.wait_for("message", check=lambda msg: msg.author == ctx.author, timeout=60.0)
    value_input = message.content

    

    

#invoking function from other file
client.run(returntoken())
