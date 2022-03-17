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
import discord, psutil, requests, asyncio, datetime
from mcstatus import MinecraftServer

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=commands.when_mentioned_or("+"), intents=intents, help_command=None) #Setting prefix

@client.event
async def on_ready(): #Stuff the bot does when it starts
    print("Connected to Discord!")  #Print this when the bot starts
    await client.change_presence(activity=discord.Game(f'on the Shenanigans Network')) #Set Presence

    global bot_version      #Sets the bot_version global variable
    bot_version = "Beta 0.3.1"

    global embed_footer     #Sets the default Embed footer
    embed_footer = f"Shenanigans Bot • {bot_version}"

    global embed_color      #Sets the default Embed color
    embed_color = 0xff0000

    global embed_header     #Sets the default Embed Header (Author)
    embed_header = "Shenanigans Network"

    global general_channel  #The general_channel, where welcome messages are posted
    general_channel = 953482572850139136 # Put your welcome announcements channel id (for us, that's general)

    global suggestion_channel   #The suggestions channel, where +suggest posts.
    suggestion_channel = 950720150032752680 # Put your suggestions channel's channel ID here

    global prefix   #Changing this does not change the prefix, but this prefix shows in embeds, etc.
    prefix = "+"





async def serverstatus(message, st_server,st_ip):   # Server Status front end
    server = MinecraftServer.lookup(f"{st_ip}")     #Gets server player-info from API
    try:
        query = server.query()
        playerCount = query.players.online
    except: playerCount = 0
    placeholder = await status(st_server)  # Gets server info from Ptero API

    serverstatus = placeholder["state"] #Setting serverstatus as placeholder state
    if serverstatus == "offline":  # Adds emoji for up/down/starting/stopping
        serverstatus = "Offline <:offline:915916197797715979> "
    elif serverstatus == "running":
        serverstatus = "Online <:online:915916197973864449>"
    elif serverstatus == "starting":
        serverstatus = "Starting <:partial:915916197848047646>"
    elif serverstatus == "stopping":
        serverstatus = "Stopping <:outage:915916198032588800>"
    #The embed it sends.
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
async def on_message(message):  #On message, Checks every message for...
    if message.author.bot: return   # checks if author is a bot.
    else:
        if " ip " in f" {message.content} ":    #On word "ip" send the IP embed
            # Sends IP embed
            ipembed = discord.Embed(title="Here's the Server ip!", url="https://moonball.io", color=embed_color)
            ipembed.set_author(name=embed_header)
            ipembed.set_thumbnail(url="https://media.discordapp.net/attachments/880368661104316459/950775364928561162/logo.png")
            ipembed.add_field(name="Java ", value="play.moonball.io", inline=True)
            ipembed.add_field(name="Bedrock ", value="play.moonball.io (Port 25565)", inline=False)
            ipembed.set_footer(text="Maybe check the pins next time? eh.")
            await message.reply(embed = ipembed)
            print(f'Sent IP Embed to message of {message.author.name}#{message.author.discriminator}')      # Logs to Console

        elif client.user in message.mentions:       #Replies to when the Bot in @mentioned
            await message.reply(f"Hello! The prefix is `{prefix}`. Use `{prefix}help` to view available commands.")
            print(f"Sent Mention message to {message.author.name}#{message.author.discriminator}")

        #Check Messages for [servername] and "Down" A repeat of the same thing multiple times for every server
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

        elif ".suggest" in f" {message.content} ":  #If a member uses the old .suggest command, tell them to use the new one
            await message.reply("Please use `+suggest` from now on, instead!")

        await client.process_commands(message)



@client.event   # When a user does an invalid command
async def on_command_error(ctx, error):
    if not isinstance(error, commands.CheckFailure):
        #await ctx.message.add_reaction(':false:508021839981707304')
        await ctx.reply("Invalid Command! Do `+help` to view available commands.")
        print(f"Sent Invalid-Command message to {ctx.author.name}#{ctx.author.discriminator}")



@client.event   # Welcome Announcement
async def on_member_join(member):
    guild = client.get_guild(894902529039687720)  # Replace "894902529039687720" with your server ID (Server Settings > Widget > Copy Server ID)
    channel = guild.get_channel(general_channel)  # To change this, Go on top of this file
    #The embed for Welcome Announcements
    welc_embed = discord.Embed(title=f'Welcome to the Discord Server!', url="https://moonball.io", color=embed_color)
    welc_embed.add_field(name="Shenanigans Network",value=f"<a:malconfetti:910127223791554570> Welcome {member.mention} to the Discord! <a:malconfetti:910127223791554570>\n<a:Read_Rules:910128684751544330> Please check out the Server Rules here <#894902529039687722> <a:Read_Rules:910128684751544330>\n <a:hypelove:901476784204288070> Take your Self Roles at <#910130264905232424> <a:hypelove:901476784204288070>\n <:02cool:910128856550244352> Head over to ⛧╭･ﾟgeneral-eng to talk with others! <:02cool:910128856550244352> \n<a:Hearts:952919562846875650> Server info and IP can be found here <#897502089025052693> <a:Hearts:952919562846875650>",inline=True)
    welc_embed.set_image(url="https://media.discordapp.net/attachments/896348336972496936/952940944175554590/ezgif-1-e6eb713fa2.gif")
    welc_embed.set_footer(text=embed_footer)
    await channel.send(embed=welc_embed)
    #role = discord.utils.get(member.server.roles, name="Member")  # Gets the member role as a `role` object
    #await client.add_roles(member, role)  # Gives the role to the user
    #print(f"Sent Welcome Embed and Member Role to {member.name}") # This part does not work.



@client.group(pass_context=True, aliases=['info', 'help'], invoke_without_command=True) #Help Command
async def bothelp(ctx):
    #Base Help command embed
    bothelp = discord.Embed(title="Help Command", url="https://moonball.io",description="`+help <module>` to learn more about that specific module\nModules Include - ```fix\nping, status, suggestion, ip, embed```", color=embed_color)
    bothelp.set_author(name=f"{embed_header}")
    bothelp.add_field(name="Prefix", value=f"The prefix is `{prefix}`", inline=True)
    bothelp.add_field(name="Bot Version", value=f"{bot_version}", inline=True)
    bothelp.add_field(name="Bot Dev", value="<@837584356988944396>", inline=True)
    bothelp.add_field(name="Ping",value=f"Check the Bot's Ping and extra info relating to the bot's instance.\n`{prefix}help ping` to learn more",inline=True)
    bothelp.add_field(name="Server Status",value=f"Check the live status of any one of our servers. Through a simple auto-trigger or a manual command (+servername). Details received include Player Count, CPU/RAM/Disk Usage and Uptime. \n`{prefix}help status`  to learn more.",inline=False)
    bothelp.add_field(name="Suggestions ",value=f"Do you have any suggestions for our Discord Server or Minecraft Server? If yes, you can suggest with this command!. \n `{prefix}help Suggestions` to learn more.",inline=False)
    bothelp.add_field(name="Server IP",value=f"This command is very simple, It just sends the IP to the server for both the Minecraft Java and Bedrock edition in a nice-looking embed. \n`{prefix}help ip` to learn more.",inline=False)
    bothelp.add_field(name="Embed",value=f"Send a nice-looking embed in the current channel, With a simple syntax supporting Title, Content and a Image.\n`{prefix}help embed` to learn more.",inline=False)
    bothelp.add_field(name="Reminder [Coming Soon]",value=f"Wanna remind someone about something, and you're sure they will forget 'bout it? Use this command to set a reminder for them for a specific time. \n`{prefix}help reminder` to learn more.",inline=False)
    bothelp.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=bothelp)
    print(f'Sent Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}') #Logs to Console


@bothelp.command(aliases=['ping', 'stats', 'mem', 'stat', 'cpu'])   #Sub-command for help.
async def ping_bothelp(ctx):
    embed = discord.Embed(title="Help Command - Ping", url="https://moonball.io",description="This is the Help category for the `ping` command.", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name="Description", value="The `ping` Command sends information relating to the bot's status.  ",inline=False)
    embed.add_field(name="Features", value="Can be used to check Latency, CPU Usage, RAM Usage and Uptime.",inline=False)
    embed.add_field(name="Version introduced in", value="\>0.05", inline=False)
    embed.add_field(name="Aliases", value="```fix\nmem, memory, cpu, ram, lag, ping, stats```", inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.send(embed=embed)
    print(f'Sent Ping-Help sub-Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console

@bothelp.command(aliases=['status'])    #Sub-command for help.
async def status_bothelp(ctx):
    embed = discord.Embed(title="Help Command - Status", url="https://moonball.io",
                              description="This is the Help category for the `status` command.", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name="Description",value=f"The `status` command sends info about a specific mentioned server. It can be triggered in 2 ways.\n►**Auto Trigger** - When user says 'up'/'down' and (servername) in the same message.\n►**Manual Trigger** - Using the command `{prefix}servername`",inline=False)
    embed.add_field(name="Features", value="Can be used to check the Status, Players Online, CPU/RAM/Disk and Uptime information for a specific server",inline=False)
    embed.add_field(name="Version introduced in", value="\>0.1", inline=False)
    embed.add_field(name="Aliases", value=f"```fix\nProxy/Velocity, Auth/AuthServer, Lobby/Hub, Survival, Skyblock, Bedwars/Bedwar/bw, Duels/Duel```", inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.send(embed=embed)
    print(f'Sent status-Help sub-Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console

@bothelp.command(aliases=['suggest', 'suggestion']) #Sub-command for help.
async def suggest_bothelp(ctx):
    embed = discord.Embed(title="Help Command - Suggestion", url="https://moonball.io",description="This is the Help category for the `Suggestion` command.", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name="Description", value=f"The `Suggest` Command sends a user's suggestion to the <#{suggestion_channel}> channel. ",inline=False)
    embed.add_field(name="Features", value="It posts your suggestion to the official suggestion channel of the server. Reacts to it with <:tick_bot:953561636566863903> and <:cross_bot:953561649254649866> so that it can be voted on and implemented!",inline=False)
    embed.add_field(name="Version introduced in", value="0.2", inline=False)
    embed.add_field(name="Aliases", value="```fix\nsuggest, suggestion```", inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.send(embed=embed)
    print(f'Sent suggest-Help sub-Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console

@bothelp.command(aliases=['ip'])    #Sub-command for help.
async def ip_bothelp(ctx):
    embed = discord.Embed(title="Help Command - IP", url="https://moonball.io",description="This is the Help category for the `IP` command.", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name="Description", value=f"The `IP` Command sends a nice-looking embed to the user.\nCan be triggered in 2 ways\n►**Automatic Trigger** - Any message with the word `ip` in it will trigger the embed\n**Manual Trigger** - Doing `+ip` will also send the embed",inline=False)
    embed.add_field(name="Features", value="Posts the IPs of both Java and Bedrock in a convenient Embed. Reducing the manual work to post the ip message again and again.",inline=False)
    embed.add_field(name="Version introduced in", value="0.01", inline=False)
    embed.add_field(name="Aliases", value="```fix\nip```", inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.send(embed=embed)
    print(f'Sent ip-Help sub-Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console

@bothelp.command(aliases=['embed', 'announce', 'ann'])  #Sub-command for help.
async def embed_bothelp(ctx):
    embed = discord.Embed(title="Help Command - Embed", url="https://moonball.io",description="This is the Help category for the `Embed` command.", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name="Description", value=f"The `Embed` Command creates a nice embed with a simple syntax ```yaml\n{prefix}embed The Embed Title - The Embed Content - https://insert.a/embed/image.png```\n Use `-` to separate all the 3 Items. Embed URL needs to be valid or else the embed won't send!",inline=False)
    embed.add_field(name="Features", value="Posts a Embed with the user's liking's content to any channel and at any time!",inline=False)
    embed.add_field(name="Version introduced in", value="0.05", inline=False)
    embed.add_field(name="Aliases", value="```fix\nann, announce, embed```", inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.send(embed=embed)
    print(f'Sent embed-Help sub-Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console



@client.command()   # The IP command
async def ip(message):
        #IP embed
    ipembed = discord.Embed(title="Here's the Server ip!", url="https://moonball.io", color=embed_color)
    ipembed.set_author(name=embed_header)
    ipembed.set_thumbnail(url="https://media.discordapp.net/attachments/880368661104316459/950775364928561162/logo.png")
    ipembed.add_field(name="Java ", value="play.moonball.io", inline=True)  # <:java:914118540959813632>
    ipembed.add_field(name="Bedrock ", value="play.moonball.io (Port 25565)",inline=False)  # <:Mc_Pocket_edition:903568186413293589>
    ipembed.set_footer(text=embed_footer)
    await message.reply(embed=ipembed)
    print(f'Sent IP Embed to message of {message.author.name}#{message.author.discriminator}')



@client.command(aliases=['suggestion']) # Suggest Command
async def suggest(message, *data):
    guild = client.get_guild(894902529039687720)  # Replace "894902529039687720" with your server ID (Server Settings > Widget > Copy Server ID)
    channel = guild.get_channel(suggestion_channel)  # To change this, Go on top of this file
    data = " ".join(data).split(' - ') # Input Splitter
        #The embed
    s_embed = discord.Embed(title=f"Suggestion", url="https://moonball.io", color=embed_color)
    s_embed.add_field(name=f"Submitted by {message.author.name}#{message.author.discriminator}", value=f"{data[0]}", inline=True)
    s_embed.set_footer(text=f"{embed_footer}")
    s = await channel.send(embed=s_embed)
        #Adding reactions and logging
    await s.add_reaction("<:tick_bot:953561636566863903>")  #adding tick reaction
    await s.add_reaction("<:cross_bot:953561649254649866>") #adding cross reaction
    await message.reply("Your Suggestion was sent! Check <#950720150032752680> to see how its doing!")
    print(f"Sent {message.author.name}#{message.author.discriminator}'s suggestion!")



@client.command(aliases=['memory', 'mem', 'cpu', 'ram', 'lag', 'ping']) #Bot Stats Command
async def stats(message):
        #Import the status finder for Bot
    st_server = "bot"  # Put the name for the server here (non-capitalised)
    placeholder = await status(st_server)
        #Stats Embed
    stats = discord.Embed(title = 'System Resource Usage', description = 'See CPU and memory usage of the system.', url="https://moonball.io", color=embed_color)
    stats.set_author(name=embed_header)
    stats.add_field(name = '<:latency_bot:951055641307381770> Latency' , value=f'{round(client.latency * 1000)}ms', inline=False)
    stats.add_field(name = '<:cpu_bot:951055641395478568> CPU Usage', value = f'{placeholder["cpuUsage"]}%', inline = False)
    stats.add_field(name = '<:ram_bot:951055641332563988> Memory Usage', value = f'{placeholder["memUsage"]}', inline = False)
    stats.add_field(name = '<:uptime_bot:951055640967675945> Uptime', value=f'{placeholder["uptime"]}', inline=False)
    stats.set_footer(text=embed_footer)
    await message.reply(embed = stats)
    print(f'Sent bot Stats to message of {message.author.name}#{message.author.discriminator}')  # Logs to Console



@client.command(aliases=['announce, ann'])  #The announcement Embed creator
async def embed(ctx, *data):
    data = " ".join(data).split(' - ')  #Input Splitter
    syntax_error = False
    if not ("https" in data[2] or "http" in data[2]) or not (".png" in data[2] or ".jpg" in data[2]):   #Veifying that it is a link, not random text (which would cause error)
        syntax_error = True
        await ctx.send("Not a valid link")
    if len(data) != 3:  #verifying complete syntax
        syntax_error = True
        await ctx.send("The syntax is as follows: `+embed <title> - <description> - <image-url>")
    if syntax_error: return
        #Embed Builder
    announcement = discord.Embed(title=f"Embed by {ctx.author.name}#{ctx.author.discriminator}", url="https://moonball.io", color=embed_color)
    announcement.set_thumbnail(url=f"{data[2]}")
    announcement.add_field(name=f"{data[0]}", value=f"{data[1]}", inline=True)
    announcement.set_footer(text=embed_footer)
    try:    #Try to send the embed
        await ctx.send(embed=announcement)
        await ctx.message.delete()  # delete original
    except: await ctx.send("Could not send the Embed. An error occurred. Re-Check the syntax or read the embed help page with `+help embed`")  #If it can not send the embed, send error msg
    print(f'Sent Embed (Embed Creator) from message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console




#This part is making aliases for each server's status. Just copy-paste of code, but with server-name and IP changed
@client.command(aliases=['survival'])   #Status cmd for survival
async def statussurvival(message):
    st_server = "survival"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.80:25575"  # Put the IP for the Server here
    await serverstatus(message, st_server, st_ip)
@client.command(aliases=['skyblock'])   #Status cmd for skyblock
async def statusskyblock(message):
    st_server = "skyblock"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.70:25572"  # Put the IP for the Server here
    await serverstatus(message, st_server, st_ip)
@client.command(aliases=['duels', 'duel'])  #Status cmd for duels
async def statusduels(message):
    st_server = "duels"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.70:25573"  # Put the IP for the Server here
    await serverstatus(message, st_server, st_ip)
@client.command(aliases=['bedwars', 'bedwar', 'bw'])    #Status cmd for bedwars
async def statusbedwars(message):
    st_server = "bedwars"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.70:25571"  # Put the IP for the Server here
    await serverstatus(message, st_server, st_ip)
@client.command(aliases=['lobby', 'hub'])   #Status cmd for lobby
async def statuslobby(message):
    st_server = "lobby"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.70:25577"  # Put the IP for the Server here
    await serverstatus(message, st_server, st_ip)
@client.command(aliases=['auth', 'authserver']) #Status cmd for auth
async def statusauth(message):
    st_server = "auth"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.70:25578"  # Put the IP for the Server here
    await serverstatus(message, st_server, st_ip)
@client.command(aliases=['proxy', 'velocity'])  #Status cmd for proxy
async def statusproxy(message):
    st_server = "proxy"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.60:25565"  # Put the IP for the Server here
    await serverstatus(message, st_server, st_ip)




#
# Server Status BACKEND
#
# Do not touch this, other than putting in your API key and server list
# Trust me this is very scary
#

def form_dict(stats):   #Takes raw data from the ptero API and converts it into usable variables
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
    ptero_panel = "panel.moonball.io" #Put your panels URL here
    ptero_apikey = "apikey" # Put your API key here!

    server_guide = {'fe5a4fe1': 'proxy', 'e91b165c': 'auth', 'd0f6701c': 'lobby', '5d0ac930': 'survival',   #Change this part, Add your server name and the ptero identifier (example in https://panel.moonball.io/server/5426b68e "5426b68e" is the ID)
                    '3a0eaf97': 'skyblock', '6e5ed2ac': 'duels', 'edeeff53': 'bedwars', '5426b68e': 'bot'}
    headers = {
        "Authorization": f"Bearer {ptero_apikey}",
        "Accept": "application/json", "Content-Type": "application/json"}
    if servername == "all":
        servers = {}
        for server_id in list(server_guide.keys()):
            url = f"https://panel.moonball.io/api/client/servers/{server_id}/resources"
            servers[server_guide[server_id]] = form_dict(requests.request('GET', url, headers=headers).json())
        return servers
    if servername not in list(server_guide.values()): return "Invalid server name"
    return form_dict(requests.request('GET', f"https://{ptero_panel}/api/client/servers/{[x[0] for x in server_guide.items() if x[1] == servername][0]}/resources", headers=headers).json())


async def server_status():
    guides = [  #Change this part, Add your server name and the ptero identifier (example in https://panel.moonball.io/server/5426b68e "5426b68e" is the ID)
    ["fe5a4fe1", "proxy"],
    ["e91b165c", "auth"],
    ["d0f6701c", "lobby"],
    ["5d0ac930", "survival"],
    ["3a0eaf97", "skyblock"],
    ["6e5ed2ac", "duels"],
    ["edeeff53", "bedwars"],
    ["5426b68e", "bot"]
    ]

    global server_status    #Sets global variables for the server status
    server_status = {}
    for i in range(len(guides)):
        server_status[guides[i][1]] = await stats(guides[i][1])

client.run('token')