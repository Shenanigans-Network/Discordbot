# Made by RajDave69
#
# Contacts -
#   Raj Dave -
#       Instagram - raj_clicks25
#       Discord - Raj Dave#3215
#       Reddit - Itz_Raj69_
#
#
#   Please Do not use this bot's files or code for your own projects without credit
#   Owner(s) include Raj Dave#3215 (discord)
#
#       Remember to insert your Bot Token, Pterodactyl API key and all other fill-able inputs!
#       Thank you for your time here, and I hope this code is useful to you =D
#
#   Github - https://moonball.io/opensource
#


import discord, requests, json, sqlite3, os, asyncio
from discord.ext import commands  # Imports required Modules
from mcstatus import MinecraftServer
from dotenv import load_dotenv
from pathlib import Path


intents = discord.Intents.all()
intents.members = True
load_dotenv(dotenv_path=Path('data/.env'))


#
# Assigning Global Variables
#

bot_version = "0.4.4"              # Bot Version
prefix = "+"                            # Bot Prefix
ptero_apikey = os.getenv("PTERO_KEY")   # Getting Pterodactyl API Key
serv_ips = {'proxy': '192.186.100.60:25565', 'limbo': '192.168.100.60:25566', 'auth': '192.168.100.60:25567',
            'lobby': '192.168.100.60:25568', 'survival': '192.168.100.80:25569', 'bedwars': '192.168.100.70:25570',
            'duels': '192.168.100.60:25571', 'skyblock': '192.168.100.70:25572', 'prison': '192.168.100.60:25573',
            'parkour': '192.168.100.60:25574'}  # Put your Pterodactyl server IPs here


# Embed related variables
embed_footer = f"Moonball Bot • {bot_version}"  # Embed footer
embed_color = 0x1a1aff                          # Embed Color
embed_header = "Moonball Network"               # Header/Author used in embeds
embed_icon = "https://media.discordapp.net/attachments/951055432833695767/972792440572493884/logo-circle.png"

client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=intents, help_command=None, case_insensitive=True)  # Setting prefix


@client.event
async def on_ready():  # Stuff the bot does when it starts
    await client.change_presence(activity=discord.Game(f'on the Moonball Network'))  # Set Presence
    global log_channel, cmd_channel
    log_channel = client.get_channel(974324304470761482)  # Put your log channel's channel ID here
    cmd_channel = 960196816605950042  # Put your command channel id
    await asyncio.sleep(2) # Waits for cogs to be loaded
    print("---------------------")
    print("Connected to Discord!")  # Print this when the bot starts
    print("---------------------")

#
# == Cog Commands ==
#
@client.command()
async def loadcog(ctx, extention):
    if await checkperm(ctx, 5): return
    client.load_extension(f'cogs.{extention}')
    await ctx.reply(f'Loaded `{extention}`')

@client.command()
async def unloadcog(ctx, extention):
    if await checkperm(ctx, 5): return
    client.unload_extension(f'cogs.{extention}')
    await ctx.reply(f'Unloaded `{extention}`')

@client.command()
async def reloadcog(ctx, extention):
    if await checkperm(ctx, 5): return
    if extention == "all":
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                client.unload_extension(f'cogs.{filename[:-3]}')
                client.load_extension(f'cogs.{filename[:-3]}')
        await ctx.reply(f'Reloaded all cogs')
        return
    client.unload_extension(f'cogs.{extention}')
    client.load_extension(f'cogs.{extention}')
    await ctx.reply(f'Reloaded `{extention}`')



#
# == Embeds ==
#

async def ip_embed(ctx):
    if await checkperm(ctx, 0): return
    ipembed = discord.Embed(title="Here's the Server IP!", url="https://moonball.io", color=embed_color)
    ipembed.set_author(name=embed_header, icon_url=embed_icon)
    ipembed.add_field(name="Java ", value="play.moonball.io", inline=True)
    ipembed.add_field(name="Bedrock ", value="play.moonball.io (Port 25565)", inline=False)
    ipembed.set_footer(text=embed_footer)
    await ctx.reply(embed=ipembed)
    await logger("i", f'Sent IP Embed to message of {ctx.author.name}#{ctx.author.discriminator}', "info", f"Sent IP embed to message of {ctx.author.name}#{ctx.author.discriminator}")

async def version_embed(ctx):
    if await checkperm(ctx, 0): return
    vembed = discord.Embed(title="Here's the Server Version!", url="https://moonball.io", color=embed_color).set_footer(text=embed_footer)
    vembed.set_author(name=embed_header, icon_url=embed_icon)
    vembed.add_field(name="Java ", value="1.13 - 1.18.2", inline=True)
    vembed.add_field(name="Bedrock ", value="1.17.40 - 1.18.30", inline=False)
    await ctx.reply(embed=vembed)
    print(f'Sent Version Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console
    await logger("i", f'Sent Version Embed to message of {ctx.author.name}#{ctx.author.discriminator}', "info", f"Sent Version embed to message of {ctx.author.name}#{ctx.author.discriminator}")

#
# == Server Status ==
#

async def serverstatus(ctx, st_server):  # Server Status front end
    if await checkperm(ctx, 0): return
    server = MinecraftServer.lookup(serv_ips.get(st_server.lower()))  # Gets server player-info from API
    msg = await ctx.reply(embed=discord.Embed(title=f"{st_server.capitalize()} Server Status",description="*Server Status is loading*\nPlease hold on!",color=embed_color))
    try:
        server_info = await status(st_server.lower())  # Gets server info from Pterodactyl API
    except:
        await msg.edit(embed=discord.Embed(title=f"{st_server.capitalize()} Server Status - Error",description=f"**There was an error while trying to get server info from the panel!**\nUse `{prefix}help` to learn more!",color=embed_color))
        return
    server_status = server_info["state"]  # Setting this as placeholder state
    player_count = 0
    if server_status == "offline":  # If server is offline
        server_status = "Offline <:offline:915916197797715979>"
    elif server_status == "running":
        server_status = "Online <:online:915916197973864449>"
        if not st_server in ["proxy", "bot", "auth", "lobby", "limbo"]:  # If not one of these servers
            try:
                player_count = server.query().players.online  # Gets player count from API
            except:
                print("Error getting player count, It is 0")  # If error in getting Playercount
    elif server_status == "starting":  # If server is starting
        server_status = "Starting <:partial:915916197848047646>"
    elif server_status == "stopping":  # If server is stopping
        server_status = "Stopping <:outage:915916198032588800>"
    # Embed
    server_embed = discord.Embed(title=f"{st_server.capitalize()} Status", url="https://moonball.io",description=f"Live Status for the {st_server.capitalize()} Server.\nTriggered by {ctx.author.name}#{ctx.author.discriminator}",color=embed_color)
    server_embed.set_author(name=embed_header, icon_url=embed_icon)
    server_embed.set_thumbnail(url=embed_icon)
    server_embed.add_field(name="<:load_bot:952580881367826542> Status", value=f'{server_status}', inline=True)
    server_embed.add_field(name="<:member_bot:953308738234748928> Players", value=f'{player_count} Online',inline=False)
    server_embed.add_field(name="<:cpu_bot:951055641395478568> CPU Usage", value=f'{server_info["cpuUsage"]}%',inline=False)
    server_embed.add_field(name="<:ram_bot:951055641332563988> Memory Usage", value=f'{server_info["memUsage"]}',inline=False)
    server_embed.add_field(name="<:disk_bot:952580881237803028> Disk Space", value=f'{server_info["spaceOccupied"]}',inline=False)
    server_embed.add_field(name="<:uptime_bot:951055640967675945> Uptime", value=f'{server_info["uptime"]}',inline=False)
    server_embed.set_footer(text=embed_footer)
    await msg.edit(embed=server_embed)
    await logger("s",f'Server Status : Sent Server {st_server.capitalize()} embed to message of {ctx.author.name}#{ctx.author.discriminator}',"server",f"Sent Server {st_server.capitalize()} embed to message of {ctx.author.name}#{ctx.author.discriminator}")


#     False = Connected
#     True = Not Connected

async def get_mc(disc_id):
    con = sqlite3.connect('./data/data.db')
    c = con.cursor()
    c.execute(f"SELECT mc_username FROM connection WHERE disc_id = '{disc_id}';")
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return None

async def mc_exists(mc_username):
    con = sqlite3.connect('./data/data.db')
    c = con.cursor()
    c.execute(f"SELECT mc_username FROM connection WHERE mc_username = '{mc_username}';")
    result = c.fetchone()
    if result:
        return True
    else:
        return False
    # True = Exists
    # False = Doesn't Exist

async def bad_char(input_str) -> str | None:
    illegal_chars = [";", "'", '"', ".", ",", ":", "!", "?", "`", "~", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "=", "[", "]", "{", "}", "|", "\\", "/", ">", "<", "`"]
    chars_found = []
    for i in illegal_chars:
        if i in input_str:
            chars_found.append(i)
    if not chars_found:
        return None
    else:
        # Converts list to string with Discord ` formatting
        return f"`{'`, `'.join(chars_found)}`"



async def logger(cat, printmsg, logtype, logmsg):  # Logs to Log channel
    await log_channel.send(f'**{logtype.capitalize()}** : ' + f'#{countadd(cat)} ' + logmsg)  # Logs to Log channel
    print(printmsg)

async def checkcommandchannel(ctx) -> bool:  # Check if the channel in which a command is executed in is a command-channel
    channel = ctx.channel.id
    if channel != cmd_channel:
        if not await checkperm(ctx, 1):
            # await ctx.reply(f"Ugh fine. I guess I'll let you use bot commands here, since you're a staff member- :rolling_eyes:")
            return False
        else:
            await ctx.reply(f"Please execute commands only in <#{cmd_channel}>", delete_after=10.0)
            await ctx.message.add_reaction("<:cross_bot:953561649254649866>")
            return True
    else:
        return False
# False = Continue with Command
# True = Return, Not continuing with command




#
#   ===BACKEND===
#
# Do not touch this, other than putting in your API key and server list
# Trust me messing stuff up here can cause a lot of bad!
#

async def resetcount(ctx, kw, name):  # Counter Add Function
    try:
        db = sqlite3.connect('./data/data.db')
    except:
        print("Error: Could not connect to the database.")
        return
    c = db.cursor()
    if kw == "all":
        for cat in ["a", "s", "f", "i", "h"]:
            c.execute(f'UPDATE counters SET count=:c WHERE cname=:n', {"c": 0, "n": cat})
    else:
        c.execute(f'UPDATE counters SET count=:c WHERE cname=:n', {"c": 0, "n":kw})
    db.commit()
    db.close()
    await ctx.send(f'Done! Reset the {name} Counter')
    await logger("a", f"{name} Counter was reset by {ctx.author.name}#{ctx.author.discriminator}", "admin", f"{name} counter was reset by {ctx.author.name}#{ctx.author.discriminator}")  # Logs to Log channel


def form_dict(stats):  # Takes raw data from the Pterodactyl API and converts it into usable variables
    placeholders = {}
    ph_keys = ["state", "memUsage", "cpuUsage", "spaceOccupied", "uptime"]
    ph_values = [stats["attributes"]["current_state"],
                 str(round(stats["attributes"]["resources"]["memory_bytes"] / 1073741824, 2)) + " GB",
                 str(round(stats["attributes"]["resources"]["cpu_absolute"], 2)),
                 str(round(stats["attributes"]["resources"]["disk_bytes"] / 1073741824, 2)) + " GB",
                 str(round(stats["attributes"]["resources"]["uptime"] / 3600000, 2)) + " hour(s)"]
    for ind, ph_key in enumerate(ph_keys): placeholders[ph_key] = ph_values[ind]
    return placeholders


def countadd(cat):  # Counter Add Function
    try:
        db = sqlite3.connect('./data/data.db')
    except:
        print("Error: Could not connect to the database.")
        return
    c = db.cursor()
    c.execute(f'SELECT * FROM counters')
    counters = c.fetchall()
    count = 0
    for counter in counters:
      if counter[0] == cat:
        count += int(counter[1])
        break
    c.execute(f'UPDATE counters SET count=:c WHERE cname=:n', {"c": int(count) + 1, "n":cat})
    db.commit()
    db.close()
    return int(count)+1


#
# Server Status BACKEND
#

async def status(servername):
    ptero_panel = "panel.moonball.io"  # Put your Pterodactyl Panel's URL here
    server_guide = {'fe5a4fe1': 'proxy', 'd1e50e31': 'limbo', 'a9aa4f09': 'auth', 'b7b7c4b3': 'lobby', '777f305b': 'survival',
                    '33cbad29': 'skyblock', '04cc6bb3': 'duels', '583e6fbc': 'bedwars', '5426b68e': 'bot', '10770164': 'parkour'}
    # Add your server name and the Pterodactyl identifier

    headers = {"Authorization": f"Bearer {ptero_apikey}", "Accept": "application/json", "Content-Type": "application/json"}
    if servername == "all":
        servers = {}
        for server_id in list(server_guide.keys()):
            url = f"https://{ptero_panel}/api/client/servers/{server_id}/resources"
            servers[server_guide[server_id]] = form_dict(requests.request('GET', url, headers=headers).json())
        return servers
    if servername not in list(server_guide.values()): return "Invalid server name"
    return form_dict(requests.request('GET', f"https://{ptero_panel}/api/client/servers/{[x[0] for x in server_guide.items() if x[1] == servername][0]}/resources", headers=headers).json())


async def server_status():
    guides = [  # Add your server name and the Pterodactyl identifier
        ["fe5a4fe1", "proxy"],
        ["d1e50e31", "limbo"],
        ["a9aa4f09", "auth"],
        ["b7b7c4b3", "lobby"],
        ["777f305b", "survival"],
        ["33cbad29", "skyblock"],
        ["04cc6bb3", "duels"],
        ["583e6fbc", "bedwars"],
        ["5426b68e", "bot"],
        ["10770164", "parkour"],
        ["a321d8fa", "prison"]
    ]

    global server_status  # Sets global variables for the server status
    server_status = {}
    for i in range(len(guides)):
        server_status[guides[i][1]] = await status(guides[i][1])

#
# Server Power BACKEND
#

async def serverpower(servername, power, ctx):
    ptero_panel = "panel.moonball.io"  # Put your Ptero Panel's URL here
    server_guide = {'proxy': 'fe5a4fe1', 'limbo': "d1e50e31", 'auth': 'e91b165c', 'lobby': 'b7b7c4b3',
                    'survival': '777f305b', 'skyblock': '33cbad29', 'duels': '04cc6bb3', 'bedwars': '583e6fbc',
                    'bot': '5426b68e', 'parkour': '10770164', 'prison': 'a321d8fa'}
    # Add your server name and the Pterodactyl identifier (in https://panel.moonball.io/server/5426b68e "5426b68e" is the ID)

    placeholder = await status(servername)  # Gets server info
    serverstatus = placeholder["state"]  # Gets its state

    # Checks if specific conditions are true
    if serverstatus == "running" and power == "start":
        await ctx.reply(f"The server, `{servername.capitalize()}` is already running!")
        return "exception"
    elif serverstatus == "offline" and power == "stop":
        await ctx.reply(f"The server, `{servername.capitalize()}` is already off")
        return "exception"
    elif serverstatus == "offline" and power == "kill":
        await ctx.reply(f"The server, `{servername.capitalize()}` is already off")
        return "exception"
    elif serverstatus == "starting" and power == "start":
        await ctx.reply(f"The server, `{servername.capitalize()}` is already starting")
        return "exception"
    elif serverstatus == "stopping" and power == "stop":
        await ctx.reply(f"The server, `{servername.capitalize()}` is already stopping")
        return "exception"
    elif servername == "bot":
        await ctx.reply(f"I can't do anything to myself.")
        return "exception"

    playerCount = 0
    # server =     #Gets server player-info from API
    if power in ["stop", "restart", "kill"]:
        if not servername in ["proxy", "auth", "limbo", "lobby"]:
            try:
                playerCount = MinecraftServer.lookup(serv_ips.get(servername)).query().players.online
            except:
                await ctx.send("There was an error trying to get the player count of the server. The panel is perhaps down. Anyways ill continue with it being 0")


    if power in ["stop", "kill", "restart"]:
        if playerCount != 0:
            sent_message = await ctx.reply(f"There are {playerCount} Player(s) Online!. Are you sure you want to proceed with the destructive action? If you do wish to, say `yes`\n*Waiting for a Response...*")
            try:
                res = await client.wait_for("message",
                check=lambda x: x.channel.id == ctx.channel.id
                                and ctx.author.id == x.author.id
                                and x.content.lower() == "yes", timeout=30)
            except asyncio.TimeoutError:
                await sent_message.edit("You took too long to respond or didn't say `yes`. The action has been cancelled.")
                return

            if res.content.lower() == "yes":
                await ctx.reply("Okay! As you wish, master. Here I begin!")
            else:
                return

    url = f'https://{ptero_panel}/api/client/servers/{server_guide.get(servername)}/power'
    headers = {"Authorization": f"Bearer {ptero_apikey}", "Accept": "application/json", "Content-Type": "application/json"}
    if power == "start":
        payload = '{"signal": "start"}'
    elif power == "stop":
        payload = '{"signal": "stop"}'
    elif power == "restart":
        payload = '{"signal": "restart"}'
    elif power == "kill":
        payload = '{"signal": "kill"}'
    else:
        return "invalid_power"

    response = requests.request('POST', url, data=payload, headers=headers)
    return response.text


#
#   Send Command to Server BACKEND
#

async def sendcmd(ctx, servername, cmd):
    ptero_panel = "panel.moonball.io"  # Put your Pterodactyl Panel's URL here
    server_guide = {'proxy': 'fe5a4fe1', 'limbo': "d1e50e31", 'auth': 'a9aa4f09', 'lobby': 'b7b7c4b3', 'survival': '777f305b', 'skyblock': '33cbad29', 'duels': '04cc6bb3', 'bedwars': '583e6fbc', 'bot': '5426b68e', 'parkour': '10770164', 'prison': 'a321d8fa'}  # Change this part, Add your server name and the ptero identifier (example in https://panel.moonball.io/server/5426b68e "5426b68e" is the ID)
    url = f'https://{ptero_panel}/api/client/servers/{server_guide[servername]}/command'
    headers = {"Authorization": f"Bearer {ptero_apikey}", "Accept": "application/json","Content-Type": "application/json"}
    payload = json.dumps({"command": cmd})
    response = "."
    try:
        response = requests.request('POST', url, data=payload, headers=headers)
        return "done"
    except:
        ctx.send("Invalid Request")
    print(response.text)

#
# Permission Level System
#

async def get_permlvl(user, class_type=True) -> -1 | 0 | 1 | 2 | 3 | 4 | 5:
    user = user.id if class_type else user
    con = sqlite3.connect('./data/data.db')
    cur = con.cursor()
    cur.execute(f"SELECT * FROM perms WHERE user_id={user}")
    result = cur.fetchone()
    if result is None:
        cur.execute(f"INSERT INTO perms (user_id, lvl) VALUES ({user}, 0)")
        con.commit()
        cur.execute(f"SELECT * FROM perms WHERE user_id={user}")
        result = cur.fetchone()
    con.close()
    return result[1]


async def checkperm(ctx, level) -> bool:
    currentlvl = await get_permlvl(ctx.author, True)
    if int(currentlvl) < int(level):
        await ctx.reply(f"You don't have the required permissions to use this command. You have permission level `{currentlvl}`, but required level is `{level}`!", delete_after=10)
        return True
    else:
        return False

print("---------------------")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(os.getenv("DISCORD_TOKEN"))