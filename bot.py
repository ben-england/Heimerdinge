import discord
from discord.ext import commands
#installed requests using pip
import requests
#importing tokens and api keys from another file for safety
from botconnectioninfo import returntoken
from api_info import returnapikey

intents = discord.Intents.default()
intents.members = True

riot_id_api_url = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/benji/cring?api_key=RGAPI-a9395dac-f905-4fc3-9b10-d3392a299cce"

#command prefix
client = commands.Bot(command_prefix = '!', intents=intents)

@client.event
async def on_ready():
    print("Bot is online")
    print("----------------------")

@client.command()
async def summoner(ctx):
    await ctx.send("Please input the summoner name!")
    #gamenamemessage = await client.wait_for("message", check=lambda msg: msg.author == ctx.author, timeout=60.0)
    #gamename_input = gamenamemessage.content

    #await ctx.send ("Please input the tagline! (This is the word/numbers after the hash)")
    #taglinemessage = await client.wait_for("message", check=lambda msg: msg.author == ctx.author, timeout=60.0)
    #tagline_input = taglinemessage.content

    #async def get_puuid(ctx, gamename_input: str, tagline_input: str):
        #puuidresponse = requests.get(riot_id_api_url, returnapikey)
        #if puuidresponse.status_code == 200:
            #puuiddata = puuidresponse.json()
            #puuid = puuiddata['puuid']
            #await ctx.send("The PUUID for {gamename_input}#{tagline_input} is {puuid}")

        

#invoking function from other file
client.run(returntoken())
