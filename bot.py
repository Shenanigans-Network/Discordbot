# Made by RajDave69, muhdrayan and nivedvenugopalan on GitHub
#
# Contacts -
#       Instagram - raj_clicks25
#       Discord - Raj Dave#3215
#       Reddit - Itz_Raj69_
#
#   Do not use this bot's files or codes for your own projects without credits
#   Owners include 𝓡𝓸𝓬𝓴𝔂_𝓡𝓾𝓽𝔀𝓲𝓴#5333 Raj Dave#3215 and Kabashi-Kun#5099 (discord)
#
#       Remember to insert your Bot Token and your Pterodactyl API key!
#       Thank you for your time here, and I hope this code is useful to you =D
#

from discord.ext import commands #Imports required Modules
import discord, psutil, requests
from mcstatus import MinecraftServer


intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="+", intents=intents, help_command=None) #Setting prefix

#Stuff the bot does when it starts
@client.event
async def on_ready():
    print("Connected to Discord!")
    await client.change_presence(activity=discord.Game(f'on the Shenanigans Network')) #Set Presence

    #Global Variables
    #global startTime        #Set bot start time for the `Stats` Uptime monitor
    #startTime = time.time()

    global embed_footer     #Sets the default Embed footer
    embed_footer = "Made with Love ♥ Shenanigans Bot"

    global embed_color      #Sets the default Embed color
    embed_color = 0xff0000

    global embed_header
    embed_header = "Shenanigans Network"

    #global server_name
    #server_name = "Shenanigans Network"




async def serverstatus(message, st_server,st_ip):
    placeholder = await status(st_server)  # Gets server info from API

    server = MinecraftServer.lookup(f"{st_ip}")
    try:
        query = server.query()
        playerCount = query.players.online
    except:
        playerCount = 0

    serverstatus = placeholder["state"]
    if serverstatus == "offline":  # Adds emoji for up/down/starting/stopping
        serverstatus = "Offline <:offline:915916197797715979> "
    elif serverstatus == "running":
        serverstatus = "Online <:online:915916197973864449>"
    elif serverstatus == "starting":
        serverstatus = "Starting <:partial:915916197848047646>"
    elif serverstatus == "stopping":
        serverstatus = "Stopping <:outage:915916198032588800>"
    # The embed for this server
    serverembed = discord.Embed(title=f"{st_server.capitalize()} Status", url="https://moonball.io", description=f"Live Status for the {st_server.capitalize()} Server. \nTriggered by {message.author.name}#{message.author.discriminator}", color=embed_color)
    serverembed.set_author(name=embed_header)
    serverembed.set_thumbnail(url="https://media.discordapp.net/attachments/880368661104316459/950775364928561162/logo.png")
    serverembed.add_field(name="<:load_bot:952580881367826542> Status", value=f'{serverstatus}', inline=True)
    serverembed.add_field(name="<:member_bot:953308738234748928> Players", value=f'{playerCount} Online', inline=False)
    serverembed.add_field(name="<:cpu_bot:951055641395478568> CPU Usage", value=f'{placeholder["cpuUsage"]}%',inline=False)
    serverembed.add_field(name="<:ram_bot:951055641332563988> Memory Usage", value=f'{placeholder["memUsage"]}',inline=False)
    serverembed.add_field(name="<:disk_bot:952580881237803028> Disk Space", value=f'{placeholder["spaceOccupied"]}',inline=False)
    serverembed.add_field(name="<:uptime_bot:951055640967675945> Uptime", value=f'{placeholder["uptime"]}',inline=False)
    serverembed.set_footer(text=embed_footer)
    await message.reply(embed = serverembed)  # Sends the embed
    print(f'Server Status : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}')  # Logs to Console


@client.event
async def on_member_join(member):
    guild = client.get_guild(894902529039687720)  # Replace "894902529039687720" with your server ID (Server Settings > Widget > Copy Server ID)
    channel = guild.get_channel(938483925498605639)  # Replace "938483925498605639" with your Welcome-Announcements channel's Channel-ID

    # embed

    embed = discord.Embed(title=f'Welcome to the Discord Server!', url="https://moonball.io", color=embed_color)
    embed.add_field(name="Shenanigans Network", value=f"<a:malconfetti:910127223791554570> Welcome {member.mention} to the Discord! <a:malconfetti:910127223791554570>\n<a:Read_Rules:910128684751544330> Please check out the Server Rules here <#894902529039687722> <a:Read_Rules:910128684751544330>\n <a:hypelove:901476784204288070> Take your Self Roles at <#910130264905232424> <a:hypelove:901476784204288070>\n <:02cool:910128856550244352> Head over to ⛧╭･ﾟgeneral-eng to talk with others! <:02cool:910128856550244352> \n<a:Hearts:952919562846875650> Server info and IP can be found here <#897502089025052693> <a:Hearts:952919562846875650>", inline=True)
    embed.set_image(url="https://media.discordapp.net/attachments/896348336972496936/952940944175554590/ezgif-1-e6eb713fa2.gif")
    embed.set_footer(text=embed_footer)
    await channel.send(embed=embed)

    role = discord.utils.get(member.server.roles, name="Member") #  Gets the member role as a `role` object
    await client.add_roles(member, role) # Gives the role to the user
    print(f"Sent Welcome Embed and Member Role to {member.name}")



#look for in message
@client.event
async def on_message(message):
    # checks if author is a bot.
    if message.author.bot: return

    else:
        #On word "ip" send the IP embed
        if " ip " in f" {message.content} ":
            # Sends main IP embed
            ipembed = discord.Embed(title="Here's the Server ip!", url="https://moonball.io", color=embed_color)
            ipembed.set_author(name=embed_header)
            ipembed.set_thumbnail(url="https://media.discordapp.net/attachments/880368661104316459/950775364928561162/logo.png")
            ipembed.add_field(name="Java ", value="play.moonball.io", inline=True) #<:java:914118540959813632>
            ipembed.add_field(name="Bedrock ", value="play.moonball.io (Port 25565)", inline=False) #<:Mc_Pocket_edition:903568186413293589>
            ipembed.set_footer(text="Maybe check the pins next time? eh.")
            await message.reply(embed = ipembed)
            print(f'Sent IP Embed to message of {message.author.name}#{message.author.discriminator}')


        #Check Messages for [servername] and "Down"
        elif " survival " in f" {message.content} " and "down" in f" {message.content} ":    #Sends server info for survival
            st_server = "survival"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.80:25575"  # Put the IP for the Server here
            await serverstatus(message, st_server, st_ip)

        elif " skyblock " in f" {message.content} " and "down" in f" {message.content} ":    #Sends server info for Skyblock
            st_server = "skyblock"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25572"  # Put the IP for the Server here
            await serverstatus(message, st_server, st_ip)

        elif " duels " in f" {message.content} " and "down" in f" {message.content} ":       #Sends server info for Duels
            st_server = "duels"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25573"  # Put the IP for the Server here
            await serverstatus(message, st_server, st_ip)

        elif " bedwars " in f" {message.content} " and "down" in f" {message.content} ":     #Sends server info for Bedwars
            st_server = "bedwars"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25571"  # Put the IP for the Server here
            await serverstatus(message, st_server, st_ip)

        elif " auth " in f" {message.content} " and "down" in f" {message.content} ":        #Sends server info for Auth
            st_server = "auth"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25578"  # Put the IP for the Server here
            await serverstatus(message, st_server, st_ip)

        elif " proxy " in f" {message.content} " and "down" in f" {message.content} ":       #Sends server info for Proxy
            st_server = "proxy"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.60:25565"  # Put the IP for the Server here
            await serverstatus(message, st_server, st_ip)

        elif " lobby " in f" {message.content} " and "down" in f" {message.content} ":       #Sends server info for Lobby
            st_server = "lobby"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25577"  # Put the IP for the Server here
            await serverstatus(message, st_server, st_ip)


        #Check messages for [servername] and "Up"

        elif " survival " in f" {message.content} " and "up" in f" {message.content} ":    #Sends server info for survival
            st_server = "survival"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.80:25575"  # Put the IP for the Server here
            await serverstatus(message, st_server, st_ip)

        elif " skyblock " in f" {message.content} " and "up" in f" {message.content} ":    #Sends server info for Skyblock
            st_server = "skyblock"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25572"  # Put the IP for the Server here
            await serverstatus(message, st_server, st_ip)

        elif " duels " in f" {message.content} " and "up" in f" {message.content} ":       #Sends server info for Duels
            st_server = "duels"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25573"  # Put the IP for the Server here
            await serverstatus(message, st_server, st_ip)

        elif " bedwars " in f" {message.content} " and "up" in f" {message.content} ":     #Sends server info for Bedwars
            st_server = "bedwars"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25571"  # Put the IP for the Server here
            await serverstatus(message, st_server, st_ip)

        elif " auth " in f" {message.content} " and "up" in f" {message.content} ":        #Sends server info for Auth
            st_server = "auth"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25578"  # Put the IP for the Server here
            await serverstatus(message, st_server, st_ip)

        elif " proxy " in f" {message.content} " and "up" in f" {message.content} ":       #Sends server info for Proxy
            st_server = "proxy"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.60:25565"  # Put the IP for the Server here
            await serverstatus(message, st_server, st_ip)

        elif " lobby " in f" {message.content} " and "up" in f" {message.content} ":       #Sends server info for Lobby
            st_server = "lobby"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25577"  # Put the IP for the Server here
            await serverstatus(message, st_server, st_ip)

        await client.process_commands(message)



    #Bot Stats Command
@client.command(aliases=['memory', 'mem', 'cpu', 'ram', 'lag', 'ping'])
async def stats(message):
    #Import the status finder for Bot
    st_server = "bot"  # Put the name for the server here (non-capitalised)
    placeholder = await status(st_server)

    #Stats Embed
    stats = discord.Embed(title = 'System Resource Usage', description = 'See CPU and memory usage of the system.', url="https://moonball.io", color=embed_color)
    stats.set_author(name=embed_header)
    stats.add_field(name='<:latency_bot:951055641307381770> Latency' , value=f'{round(client.latency * 1000)}ms', inline=False)
    stats.add_field(name = '<:cpu_bot:951055641395478568> CPU Usage', value = f'{psutil.cpu_percent()}%', inline = False)
    stats.add_field(name = '<:ram_bot:951055641332563988> Memory Usage', value = f'{placeholder["memUsage"]}', inline = False)
    stats.add_field(name = '<:uptime_bot:951055640967675945> Uptime', value=f'{placeholder["uptime"]}', inline=False)
    stats.set_footer(text=embed_footer)
    await message.reply(embed = stats)
    print(f'Sent bot Stats to message of {message.author.name}#{message.author.discriminator}')  # Logs to Console



#The announcement Embed creator
@client.command(aliases=['announce, ann'])
async def embed(ctx, *data):
    #Input Splitter
    commands.has_permissions(administrator=True)
    data = " ".join(data).split(' - ')
    syntax_error = False

    #Veifying that it is a link, not random text (which would cause error)
    if not ("https" in data[2] or "http" in data[2]) or not (".png" in data[2] or ".jpg" in data[2]):
        syntax_error = True
        await ctx.send("Not a valid link")

    #verifying complete syntax
    if len(data) != 3:
        syntax_error = True
        await ctx.send("The syntax is as follows: `+embed <title> - <description> - <image-url>")
    if syntax_error: return

    #Announcement Builder
    announcement = discord.Embed(title=f"Embed by {ctx.author.name}#{ctx.author.discriminator}", url="https://moonball.io", color=embed_color)
    announcement.set_thumbnail(url=f"{data[2]}")
    announcement.add_field(name=f"{data[0]}", value=f"{data[1]}", inline=True)
    announcement.set_footer(text=embed_footer)
    await ctx.message.delete()
    await ctx.send(embed=announcement)
    print(f'Sent Embed (Embed Creator) from message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console


#This part is making aliases for each server's status
#Just copy-paste of code, but with some things changed =D
@client.command(aliases=['survival'])
async def statussurvival(message):
    st_server = "survival"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.80:25575"  # Put the IP for the Server here
    await serverstatus(message, st_server, st_ip)

@client.command(aliases=['skyblock'])
async def statusskyblock(message):
    st_server = "skyblock"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.70:25572"  # Put the IP for the Server here
    await serverstatus(message, st_server, st_ip)

@client.command(aliases=['duels'])
async def statusduels(message):
    st_server = "duels"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.70:25573"  # Put the IP for the Server here
    await serverstatus(message, st_server, st_ip)

@client.command(aliases=['bedwars'])
async def statusbedwars(message):
    st_server = "bedwars"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.70:25571"  # Put the IP for the Server here
    await serverstatus(message, st_server, st_ip)

@client.command(aliases=['lobby'])
async def statuslobby(message):
    st_server = "lobby"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.70:25577"  # Put the IP for the Server here
    await serverstatus(message, st_server, st_ip)

@client.command(aliases=['auth'])
async def statusauth(message):
    st_server = "auth"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.70:25578"  # Put the IP for the Server here
    await serverstatus(message, st_server, st_ip)

@client.command(aliases=['proxy'])
async def statusproxy(message):
    st_server = "proxy"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.60:25565"  # Put the IP for the Server here
    await serverstatus(message, st_server, st_ip)


@client.command()
async def test(ctx):

    st_ip = "192.168.100.70:25571"
    server = MinecraftServer.lookup(f"{st_ip}")
    query = server.query()
    print(f"The server has the following players online: {query.players.online}")
    await ctx.send(f"there are {query.players.online}")


#
# Server Status BACKEND
#
# Do not touch this, other than putting in your API key and server list
# Trust me this is very scary
#


def form_dict(stats):
    placeholders = {}
    ph_keys = ["state", "memUsage", "cpuUsage", "spaceOccupied", "uptime"]
    ph_values = [stats["attributes"]["current_state"],
                 str(round(stats["attributes"]["resources"]["memory_bytes"] / 1073741824, 2)) + " GB",
                 str(round(stats["attributes"]["resources"]["cpu_absolute"], 2)),
                 str(round(stats["attributes"]["resources"]["disk_bytes"] / 1073741824, 2)) + " GB",
                 str(round(stats["attributes"]["resources"]["uptime"] / 3600000, 2)) + " hour(s)"]


    for ind, ph_key in enumerate(ph_keys):
        placeholders[ph_key] = ph_values[ind]
    return placeholders


async def status(servername):
    server_guide = {'fe5a4fe1': 'proxy', 'e91b165c': 'auth', 'd0f6701c': 'lobby', '5d0ac930': 'survival',
                    '3a0eaf97': 'skyblock', '6e5ed2ac': 'duels', 'edeeff53': 'bedwars', '5426b68e': 'bot'}
    headers = {
        "Authorization": "Bearer apikey",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    if servername == "all":
        servers = {}
        for server_id in list(server_guide.keys()):
            url = f"https://panel.moonball.io/api/client/servers/{server_id}/resources"
            servers[server_guide[server_id]] = form_dict(requests.request('GET', url, headers=headers).json())
        return servers

    if servername not in list(server_guide.values()): return "Invalid server name"

    url = f"https://panel.moonball.io/api/client/servers/{[x[0] for x in server_guide.items() if x[1] == servername][0]}/resources"
    return form_dict(requests.request('GET', url, headers=headers).json())


async def server_status():
    guides = [
    ["fe5a4fe1", "proxy"],
    ["e91b165c", "auth"],
    ["d0f6701c", "lobby"],
    ["5d0ac930", "survival"],
    ["3a0eaf97", "skyblock"],
    ["6e5ed2ac", "duels"],
    ["edeeff53", "bedwars"],
    ["5426b68e", "bot"]
    ]

    global server_status
    server_status = {}
    for i in range(len(guides)):
        server_status[guides[i][1]] = await stats(guides[i][1])



client.run('token')