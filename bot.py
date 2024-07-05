#importing necessary discord commands
import discord
from discord.ext import commands
#importing datetime for menu timestamps
from datetime import datetime
#installed requests using pip
import requests
#importing tokens and api keys from another file for safety
from botconnectioninfo import returntoken
from api_info import returnapikey

#settings intents to make sure the bot has appropriate permissions
intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)

#notifying the user when the bot is ready
@client.event
async def on_ready():
    print("Bot is online")
    print("----------------------")

#function to return summoner information
async def get_summoner_details(ctx):
    #asking for the summoner name 
        await ctx.send("Please input the summoner name! (This does not include the part after the hash, just the in-game name)")

        #asking for the user input, check lambda to ensure that the bot only takes answers from the user that invoked the !summoner command, timeout to make sure that the bot doesnt stay active if the user doesnt respond
        gamenamemessage = await client.wait_for("message", check=lambda msg: msg.author == ctx.author, timeout=30.0)
        gamename_input = gamenamemessage.content

        #same as above
        await ctx.send ("Please input the tagline! (This is the word/numbers after the hash)")
        taglinemessage = await client.wait_for("message", check=lambda msg: msg.author == ctx.author, timeout=30.0)
        tagline_input = taglinemessage.content

        #returning gamename and tagline
        return gamename_input, tagline_input


#function to return puuid
#PUUID is extremely important for requesting any information via the api, gamename and tagline wont suffice so the PUUID is mandatory
async def get_summoner_puuid(ctx, gamename_input, tagline_input):
    #the api url that will execute the appropriate end point along with the user input
    puuid_api_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gamename_input}/{tagline_input}"
    
    # headers required for the api, X-Riot-Token is obligatory to make sure that the api request is successful 
    headers = {
        'X-Riot-Token': returnapikey()
    }
    #making the api call, with the api request and the api key
    puuidresponse = requests.get(puuid_api_url, headers=headers)
    print(puuidresponse.status_code)

    if puuidresponse.status_code == 200:
        #converting puuiddata object into json, so key value pairs can be accessed
        puuiddata = puuidresponse.json()
        #accessing puuid
        puuid = puuiddata['puuid']

        #200 is successful api call
        return puuid, puuidresponse.status_code
    else:
        #if error code 200 isnt returned, the appropriate api code will be returned, which will in turn re-run the code
        await ctx.send ("This wasn't a correct input!")
        return None, puuidresponse.status_code


    
#returning a menu choice system, an integer will be returned which will in turn direct the program to the correct function, returning the correct information   
async def menu_choice(ctx):
    embed = discord.Embed(title="Menu",
                description="Select here what you would like to do with Heimerdinge!",
                colour=0xf50000,
                timestamp=datetime.now())
    #menu options
    embed.add_field(name="1.) Advanced Account Details",
                value="Here you can get information such as blah blah blah",
                inline=False)
    embed.add_field(name="2.) Match History",
                value="Here you can access your match history!  The last 5 games will populate",
                inline=False)
    embed.add_field(name="3.) Challenges",
                value="Here you can access challenges, and what your ranking is per category!",
                inline=False)
    embed.add_field(name="4.) Champion Mastery",
                value="Here you can bring up your mastery, the top 5 champions will populate",
                inline=False)
    await ctx.send(embed=embed)  
    await ctx.send ("Please select a number! The appropriate details will be loaded!")
    
    #accepting user input
    menu_message = await client.wait_for("message", check=lambda msg: msg.author == ctx.author, timeout=30.0)
    menu_choice_func = menu_message.content
    return menu_choice_func


#the summoner command will allow the bot to make an api request to figure out the puuid of the user, once the puuid has been requested successfully, this can be used to make subsequent api calls
@client.command()
async def summoner(ctx):
    #setting a boolean, if api code is correct, while loop is disabled
    apiBool = False
    puuid = ""
    while apiBool == False:

        #function for gamename and tagline being called, returning values
        gamename_input, tagline_input = await get_summoner_details(ctx)

        #returning puuid from function
        puuid, api_return_code = await get_summoner_puuid(ctx, gamename_input, tagline_input)
        if(api_return_code == 200):
            #breaking for loop if api code is correct
            apiBool = True
        else:
            #maintaining for loop if api code isnt correct
            apiBool = False
    #returning the menu choice from above function
    menu_choice_func = await menu_choice(ctx)

    
#create menu
#lol-challenges via puuid

#invoking function from other file
client.run(returntoken())
