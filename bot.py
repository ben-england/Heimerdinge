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
    
    #making the api call, with the api request and the api key
    puuidresponse = requests.get(puuid_api_url, headers=returnapikey())


    if puuidresponse.status_code == 200:
        #converting puuiddata object into json, so key value pairs can be accessed
        puuiddata = puuidresponse.json()
        puuid = puuiddata['puuid']
        #accessing puuid
        #200 is successful api call
        return puuid, puuidresponse.status_code
    else:
        #if error code 200 isnt returned, the appropriate api code will be returned, which will in turn re-run the code
        await ctx.send ("This wasn't a correct input!")
        return None, puuidresponse.status_code


    
#returning a menu choice system, an integer will be returned which will in turn direct the program to the correct function, returning the correct information   
async def menu(ctx):
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
    
#seperated menu and decision making, if an incorrect input is made then the entire menu wont be reloaded, reducing load
async def menu_choice(ctx):
    #accepting user input
    menu_message = await client.wait_for("message", check=lambda msg: msg.author == ctx.author, timeout=30.0)
    menu_choice_func = menu_message.content
    return menu_choice_func

#this function uses the puuid requested earlier in order to load match IDs
async def fetch_match_id(ctx, puuid):
     #first I must request the match IDs, to appropriately load them
     match_id_api = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=5"

     #getting api header for successful execution
     #returning match id data 
     match_id_response = requests.get(match_id_api, headers=returnapikey())
     match_id_data = match_id_response.json()
     return match_id_data

#meat and gravy
async def fetch_games(ctx, match_id, puuid, gamename_input):
     #getting api header for successful execution

    #for loop to loop through all of the match ids and then put them into a python object
     for matches in match_id:
          #creating an index, as cannot get/running .functions in literal strings doesnt work
          match_position = match_id.index(matches)

          #creating a temp variable to access the specific index of the array, due to literal strings i cannot suffix the position into the api key
          game_api = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id[match_position]}"

          #executing api call
          current_game_response = requests.get(game_api, headers=returnapikey())

          #returning api call as json
          current_game_data_json = current_game_response.json()
        
          #checking metadata puuid against user puuid, once index is found, all game information can be stored in a 2d array
          searched_summoner_index = current_game_data_json['metadata']['participants'].index(puuid)
          
          #defining our specific information as a new variable
          our_summoner_game_info = current_game_data_json['info']['participants'][searched_summoner_index]

          #summoner runes are embedded deeper than participants
          our_summoner_runes = our_summoner_game_info['perks']['styles']

          #calculation to figure out total user cs
          totalCS = our_summoner_game_info['totalMinionsKilled'] 
          + our_summoner_game_info['totalEnemyJungleMinionsKilled'] 
          + our_summoner_game_info['totalAllyJungleMinionsKilled']
          + our_summoner_game_info['neutralMinionsKilled']
          + our_summoner_game_info['wardsKilled']

          #calculation to figure out how many neutral wards are placed
          yellow_wards = our_summoner_game_info['wardsPlaced'] - our_summoner_game_info['detectorWardsPlaced']

          #array of all information to be outputted into discord
          searched_summoner_stats = {

               #summoner info
               'gamename': gamename_input,
               'profile_icon': our_summoner_game_info['profileIcon'],
               'champ': our_summoner_game_info['championName'],
               'gameMode': current_game_data_json['info']['gameMode'],

                #runes
               'keystone': our_summoner_runes[0]['selections'][0]['perk'],
               'rune1': our_summoner_runes[0]['selections'][1]['perk'],
               'rune2': our_summoner_runes[0]['selections'][2]['perk'],
               'rune3': our_summoner_runes[0]['selections'][3]['perk'],
               'off_tree_1': our_summoner_runes[1]['selections'][0]['perk'],
               'off_tree_2': our_summoner_runes[1]['selections'][1]['perk'],

               #core game info
               'champ_id':  our_summoner_game_info['championId'],
               'champ_name': our_summoner_game_info['championName'],
               'kills': our_summoner_game_info['kills'],
               'deaths': our_summoner_game_info['deaths'],
               'assists': our_summoner_game_info['assists'],
               'damage': our_summoner_game_info['totalDamageDealtToChampions'],
               'damage_taken': our_summoner_game_info['totalDamageTaken'],


               #creep score 
               'cs': totalCS,

               #vision
               'pink_wards': our_summoner_game_info['detectorWardsPlaced'],
               'wards':  yellow_wards
  
          }
          #defining array to hold multiple games worth of information
          player_stats = []

          #adding player stats to a dictionary
          player_stats.append(searched_summoner_stats)
          
          #outputting 5 discord forms each with a game
          embed = discord.Embed(
    title=f"Player Stats for {player_stats[0]['gamename']} {player_stats[0]['gameMode']}",
    description=f"Champion: {player_stats[0]['champ']}\n\n"
                f"Runes:\n"
                f"Keystone: {player_stats[0]['keystone']}\n"
                f"Rune 1: {player_stats[0]['rune1']}\n"
                f"Rune 2: {player_stats[0]['rune2']}\n"
                f"Rune 3: {player_stats[0]['rune3']}\n"
                f"Off-Tree Rune 1: {player_stats[0]['off_tree_1']}\n"
                f"Off-Tree Rune 2: {player_stats[0]['off_tree_2']}\n\n"
                f"Performance:\n"
                f"Kills: {player_stats[0]['kills']}\n"
                f"Deaths: {player_stats[0]['deaths']}\n"
                f"Assists: {player_stats[0]['assists']}\n"
                f"Damage Dealt: {player_stats[0]['damage']}\n"
                f"Damage Taken: {player_stats[0]['damage_taken']}\n"
                f"CS (Creep Score): {player_stats[0]['cs']}\n"
                f"Control Wards Placed: {player_stats[0]['pink_wards']}\n"
                f"Wards Placed: {player_stats[0]['wards']}",
    colour=0x00a3f5)
          await ctx.send(embed=embed)

#the summoner command will allow the bot to make an api request to figure out the puuid of the user, once the puuid has been requested successfully, this can be used to make subsequent api calls
@client.command()
async def summoner(ctx):
    #setting a boolean, if api code is correct, while loop is disabled
    apiBool = False
    puuid = ""
    summoner_name = ""
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

    menuBool = False
    #using match to filter through user responses
    await menu(ctx)
    while menuBool == False:
        menu_choice_func = await menu_choice(ctx)
        match menu_choice_func:
            case "1":
                    #insert func
                    menuBool = True
                    print ("a")
            case "2":
                    #breaking error handling for menu
                    match_id = await fetch_match_id(ctx, puuid)
                    


                    await fetch_games(ctx, match_id, puuid, gamename_input)
                    menuBool = True
                         
            case "3":
                    #insert func
                    menuBool = True
                    print ("c")
            case "4":
                    #insert func
                    menuBool = True
                    print ("d")
            case  _:
                await ctx.send ("That is not a valid menu choice! Please select again")

#create menu
#lol-challenges via puuid

#invoking function from other file
client.run(returntoken())
