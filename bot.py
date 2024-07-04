#importing necessary discord commands
import discord
from discord.ext import commands
#installed requests using pip
import requests
#importing tokens and api keys from another file for safety
from botconnectioninfo import returntoken
from api_info import returnapikey

#settings intents to make sure the bot has appropriate permissions
intents = discord.Intents.all()
intents.members = True

#puuid_api_url_executable = puuid_api_url + "?" + returnapikey() + "="
client = commands.Bot(command_prefix = '!', intents=intents)

#notifying the user when the bot is ready
@client.event
async def on_ready():
    print("Bot is online")
    print("----------------------")

#the summoner command will allow the bot to make an api request to figure out the puuid of the user, once the puuid has been requested successfully, this can be used to make subsequent api calls

@client.command()
async def summoner(ctx):

    #asking for the summoner name 
    await ctx.send("Please input the summoner name! (This does not include the part after the hash, just the in-game name)")

    #asking for the user input, check lambda to ensure that the bot only takes answers from the user that invoked the !summoner command, timeout to make sure that the bot doesnt stay active if the user doesnt respond
    gamenamemessage = await client.wait_for("message", check=lambda msg: msg.author == ctx.author, timeout=30.0)
    gamename_input = gamenamemessage.content

    #same as above
    await ctx.send ("Please input the tagline! (This is the word/numbers after the hash)")
    taglinemessage = await client.wait_for("message", check=lambda msg: msg.author == ctx.author, timeout=30.0)
    tagline_input = taglinemessage.content
    print(tagline_input)

    #the api url that will execute the appropriate end point along with the user input
    puuid_api_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gamename_input}/{tagline_input}"
    
    # headers required for the api, X-Riot-Token is obligatory to make sure that the api request is successful 
    headers = {
        'X-Riot-Token': returnapikey()
    }

    #making the api call, with the api request and the api key
    puuidresponse = requests.get(puuid_api_url, headers=headers)
    print(puuidresponse.status_code)

    #error handling, if the response code is 200 then the appropriate thing is outputted, otherwise there will be a different
    if puuidresponse.status_code == 200:
        #converting puuiddata object into json, so key value pairs can be accessed
        puuiddata = puuidresponse.json()
        #accessing puuid
        puuid = puuiddata['puuid']
        await ctx.send("The PUUID for " + gamename_input + "#" + tagline_input + " is " + puuid)
    else:
        await ctx.send("Failed to retrieve PUUID. Please check the game name and tagline.")
    
#invoking function from other file
client.run(returntoken())
