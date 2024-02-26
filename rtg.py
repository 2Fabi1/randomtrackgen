import discord
from discord.ext import commands
import requests
from urllib.parse import urlparse
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='$', intents=intents)
possibletags = ["normal","stunt","maze","offroad","laps","fullspeed","lol","tech","speedtech","rpg","press forward","trial","grass"]
gamemodes = ["race","puzzle","platform","stunts"]
envis = ["snow","desert","rally","island","coast","bay","stadium"]
moods = ["sunrise","day","sunset","night"]
diffs = ["beginner","intermediate","expert","lunatic"]
routes = ["single","multi","symmetric"]
game = ""
author = ""
primarytype = ""
tags = ""
envi = ""
vehicle = ""
route = ""
diff = ""
mood = ""
minat = ""
maxat = ""
tagnumber = ""
actualtags = []
def get_random_track_id():
    global tags, actualtags, tagnumber, primarytype, game, envi, vehicle, mood, diff, route, minat, maxat, author
    url = f"https://{game}.exchange/trackrandom?"
    response = requests.get(url, allow_redirects=False)
    if author != "":
        url += f"author={author}&"
    if primarytype != "":    
        primarytype = gamemodes.index[primarytype]
        url += f"primary_type={primarytype}&"
    if tags != "":
        for i in range(len(actualtags)):
            tagnumber = possibletags.index[actualtags[i]]
            if i == 0:
                url += f"type={tagnumber}"
            else:
                url +=f"2C%{tagnumber}"
            if (i + 1) > len(actualtags):
                url = url[:-1]
    if envi != "":
        url += f"environment={envis.index[envi]}&"
    
    if vehicle != "":
        url += f"vehicle={envis.index[vehicle]}&"
    
    if route != "":
        url += f"routes={routes.index[route]}&"
    
    if diff != "":
        url += f"difficulty={diffs.index[diff]}&"
    
    if mood != "":
        url += f"mood={moods.index[mood]}&"
    
    if minat != "":
        url += f"authortimemin={minms}&"
    
    if minat != "":
        url += f"authortimemax={maxms}&"
    
    if url.endswith("&"):
        url -= "&"
    
    if response.status_code == 302:
        redirect_location = response.headers.get('Location', '')
        track_id = urlparse(redirect_location).path.split('/')[-1]
        return track_id
    else:
        print(f"Unexpected response: {response.status_code}")
        return None 

def checktags(tags):
    global actualtags
    tag_list = tags.split(",")
    actualtags = []
    for i in range(len(possibletags)):
        for j in range(len(tag_list)):
            if possibletags[i] == tag_list[j]:
                actualtags.append(tag_list[j])

def converttimemin():
    global minat, minms
    parts = minat.split()
    total_seconds = 0
    for part in parts:
        value = int(part[:-1])  # Extract the numeric value
        unit = part[-1].lower()  # Extract the unit (h, m, or s)

        if unit == 'h':
            total_seconds += value * 3600
        elif unit == 'm':
            total_seconds += value * 60
        elif unit == 's':
            total_seconds += value
    minms = total_seconds * 1000
def converttimemax():
    global maxat, maxms
    parts = maxat.split()
    total_seconds = 0
    for part in parts:
        value = int(part[:-1])  # Extract the numeric value
        unit = part[-1].lower()  # Extract the unit (h, m, or s)
        if unit == 'h':
            total_seconds += value * 3600
        elif unit == 'm':
            total_seconds += value * 60
        elif unit == 's':
            total_seconds += value
    maxms = total_seconds * 1000

@client.command(name="tmnfrandom")
async def tmnfrandom(ctx,author = None,primarytype = None,tags = None,envi = None,vehicle = None,route = None, diff = None, mood = None, minat = None, maxat = None):
    global game
    if tags:
        checktags(tags)
    if minat:
        converttimemin()
    if maxat:
        converttimemax()
    game = "tmnf"
    track_id = get_random_track_id()
    await ctx.send(f"Your random track is: https://tmnf.exchange/trackshow/{track_id}")
@client.command(name="tmufrandom")
async def tmufrandom(ctx, author=None,primarytype = None,tags = None,envi = None,vehicle = None,route = None, diff = None, mood = None, minat = None, maxat = None):
    global game
    if tags:
        checktags(tags)
    if minat:
        converttimemin()
    if maxat:
        converttimemax()
    game = "tmuf"
    track_id = get_random_track_id()
    await ctx.send(f"Your random track is: https://tmuf.exchange/trackshow/{track_id}")

client.run("BOT_TOKEN_HERE")