# Made by RajDave69, muhdrayan and nivedvenugopalan on GitHub
#
# Contacts -
#   RajDave69 - 
#       Instagram - raj_clicks25
#       Discord - Raj Dave#3215
#       Reddit - Itz_Raj69_
#
#   muhdrayan -
#       Discord - Rayan10#6539
#
#   nivedvenugopalan - 
#       Discord - nivedvenugopalan
#
#
#
#   Do not use this bot's files or codes for your own projects without credits
#   Owner(s) include Raj Dave#3215 (discord)
#
#       Remember to insert your Bot Token, Pterodactyl API key and all other fillable inputs!
#       Thank you for your time here, and I hope this code is useful to you =D
#
#
#
#

from http import server
from discord.ext import commands #Imports required Modules
import discord, requests, pickle, random, json
from mcstatus import MinecraftServer
from random import choice
#from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType


intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=commands.when_mentioned_or("+"), intents=intents, help_command=None) #Setting prefix

@client.event
async def on_ready(): #Stuff the bot does when it starts
    print("Connected to Discord!")  #Print this when the bot starts
    await client.change_presence(activity=discord.Game(f'on the Moonball Network')) #Set Presence

    #DiscordComponents(client, change_discord_methods=True)

    global bot_version      #Sets the bot_version global variable
    bot_version = "Beta 0.3.1"

    global embed_footer     #Sets the default Embed footer
    embed_footer = f"Moonball Bot • {bot_version}"

    global embed_color      #Sets the default Embed color
    embed_color = 0x1a1aff

    global embed_header     #Sets the default Embed Header (Author)
    embed_header = "Moonball Network"

    global guild
    guild = client.get_guild(894902529039687720)  # Replace "894902529039687720" with your server ID (Server Settings > Widget > Copy Server ID)

    global general_channel  #The general_channel, where welcome messages are posted
    general_channel = guild.get_channel(953482572850139136) # Put your welcome announcements channel id (for us, that's general)

    global cmd_channel
    cmd_channel = 956876742574878800

    global suggestion_channel   #The suggestions channel, where +suggest posts.
    suggestion_channel = guild.get_channel(956806563950112848) # Put your suggestions channel's channel ID here

    global log_channel  #The channel to log Everything except suggestions and embeds in
    log_channel = guild.get_channel(957135623607689296)

    global embed_log
    embed_log = guild.get_channel(957608675210559558)

    global staff_ids
    staff_ids = [837584356988944396, 493852865907916800, 448079898515472385, 744835948558286899, 865232500744519680, 891307274935607306]
#                   #Raj                    #Iba                #Rocky              #Kabashi            #Jagadesh           #Amoricito

    global prefix   #Changing this does not change the prefix, but this prefix shows in embeds, etc.
    prefix = "+"

    global ptero_apikey
    ptero_apikey = "RgmFkDPifgyM88B9wytIgJ9iK4UNd0Gh0EHSVKB4BS8k5OHR"


@client.event   # When user does an invalid command
async def on_command_error(ctx, error):
    if not isinstance(error, commands.CheckFailure):
        await ctx.reply("**Error!** The command may not exist, The Syntax may be wrong or there was an Internal Error. Use `+help` to view all available commands.", delete_after=10.0)
        await ctx.message.add_reaction("<:cross_bot:953561649254649866>")
        print(f"Sent Invalid-Command message to {ctx.author.name}#{ctx.author.discriminator}")
        cat = "h"
        await log_channel.send(f'**Info** : #{countadd(cat)} Sent Error Embed to message of {ctx.author.name}#{ctx.author.discriminator}')    #Logs to Log channel


async def checkcommandchannel(ctx): # Check if the channel in which a command is executed in is a command-channel
    channel = ctx.channel.id
    if channel != cmd_channel: 
        if ctx.author.id in staff_ids:
            await ctx.reply(f"Ugh fine. I guess I'll let you use bot commands here, since you're a staff member- :rolling_eyes: ")
            return False
        else:
            await ctx.reply(f"Please execute commands only in <#{cmd_channel}>", delete_after=10.0)
            await ctx.message.add_reaction("<:cross_bot:953561649254649866>")
            return True
    else: return False
# False = Continue with Command
# True = Return, Not continuing with command



@client.event   # No reacting to both in suggestions
async def on_raw_reaction_add(payload): # checks whenever a reaction is added to a message
    # whether the message is in the cache or not
    if payload.channel_id == 956806563950112848:    # check which channel the reaction was added in
        channel = await client.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        # iterating through each reaction in the message
        for r in message.reactions:
            # checks the reactant isn't a bot and the emoji isn't the one they just reacted with
            if payload.member in await r.users().flatten() and not payload.member.bot and str(r) != str(payload.emoji):
                await message.remove_reaction(r.emoji, payload.member) # Removes the reaction
    


async def serverstatus(ctx, st_server,st_ip):   # Server Status front end
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    server = MinecraftServer.lookup(f"{st_ip}")     #Gets server player-info from API
    try:
        placeholder = await status(st_server)  # Gets server info from Ptero API
    except:
        await ctx.reply("There was an error while trying to get server info, the panel is perhaps down. Please ping the Staff")
        return
    serverstatus = placeholder["state"] #Setting serverstatus as placeholder state
    if serverstatus == "offline":  # Adds emoji for up/down/starting/stopping
        serverstatus = "Offline <:offline:915916197797715979>"
        playerCount = 0
    elif serverstatus == "running":
        serverstatus = "Online <:online:915916197973864449>"
        try:
            query = server.query()  #Try to get player info from server, only IF it is online
            playerCount = query.players.online
        except: playerCount = 0 #If unreachable, set it to 0
    elif serverstatus == "starting":
        serverstatus = "Starting <:partial:915916197848047646>"
        playerCount = 0
    elif serverstatus == "stopping":
        serverstatus = "Stopping <:outage:915916198032588800>"
        playerCount = 0
    cat = "i"
    #The embed it sends.
    serverembed = discord.Embed(title=f"{st_server.capitalize()} Status", url="https://moonball.io", description=f"Live Status for the {st_server.capitalize()} Server.\nTriggered by {ctx.author.name}#{ctx.author.discriminator}", color=embed_color)
    serverembed.set_author(name=embed_header)
    serverembed.set_thumbnail(url="https://media.discordapp.net/attachments/880368661104316459/950775364928561162/logo.png")
    serverembed.add_field(name="<:load_bot:952580881367826542> Status", value=f'{serverstatus}', inline=True)
    serverembed.add_field(name="<:member_bot:953308738234748928> Players", value=f'{playerCount} Online', inline=False)
    serverembed.add_field(name="<:cpu_bot:951055641395478568> CPU Usage", value=f'{placeholder["cpuUsage"]}%',inline=False)
    serverembed.add_field(name="<:ram_bot:951055641332563988> Memory Usage", value=f'{placeholder["memUsage"]}',inline=False)
    serverembed.add_field(name="<:disk_bot:952580881237803028> Disk Space", value=f'{placeholder["spaceOccupied"]}',inline=False)
    serverembed.add_field(name="<:uptime_bot:951055640967675945> Uptime", value=f'{placeholder["uptime"]}',inline=False)
    serverembed.set_footer(text=embed_footer)
    await ctx.reply(embed = serverembed)  # Sends the embed
    print(f'Server Status : Sent Server {st_server.capitalize()} embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console
    await log_channel.send(f"**Info** : #{countadd(cat)} Sent Server {st_server.capitalize()} embed to message of {ctx.author.name}#{ctx.author.discriminator}")



@client.event
async def on_message(message):  #On message, Checks every message for...
    if message.author.bot: return   # checks if author is a bot.
    else:
        if " ip " in f" {message.content} ":    # On word "ip" send the IP embed     
                ipembed = discord.Embed(title="Here's the Server ip!", url="https://moonball.io", color=embed_color)
                ipembed.set_author(name=embed_header)
                ipembed.set_thumbnail(url="https://media.discordapp.net/attachments/880368661104316459/950775364928561162/logo.png")
                ipembed.add_field(name="Java ", value="play.moonball.io", inline=True)
                ipembed.add_field(name="Bedrock ", value="play.moonball.io (Port 25565)", inline=False)
                ipembed.set_footer(text="Maybe check the pins next time? eh.")
                await message.reply(embed = ipembed)
                print(f'Sent IP Embed to message of {message.author.name}#{message.author.discriminator}')      # Logs to Console
                cat = "i"
                await log_channel.send(f"**Info** : #{countadd(cat)} Sent IP embed to message of {message.author.name}#{message.author.discriminator}")

        elif " version " in f" {message.content} ": # On word "version" send the version embed
            vembed = discord.Embed(title="Here's the Server Version!", url="https://moonball.io", color=embed_color)
            vembed.set_author(name=embed_header)
            vembed.set_thumbnail(url="https://media.discordapp.net/attachments/880368661104316459/950775364928561162/logo.png")
            vembed.add_field(name="Java ", value="1.13 - 1.18.2", inline=True)
            vembed.add_field(name="Bedrock ", value="1.17.40 - 1.18.12", inline=False)
            vembed.set_footer(text=embed_footer)
            await message.reply(embed = vembed)
            print(f'Sent Version Embed to message of {message.author.name}#{message.author.discriminator}')      # Logs to Console
            cat = "i"
            await log_channel.send(f"**Info** : #{countadd(cat)} Sent Version embed to message of {message.author.name}#{message.author.discriminator}")


        elif client.user in message.mentions:       #Replies to when the Bot in @mentioned
            await message.reply(f"Hello! my prefix is `{prefix}`. Use `{prefix}help` to view available commands.", delete_after=10.0)
            print(f"Sent Mention message to {message.author.name}#{message.author.discriminator}")
            cat = "h"
            await log_channel.send(f"**Help** : #{countadd(cat)} Sent mention-message to message of {message.author.name}#{message.author.discriminator}")
            

        #Check Messages for [servername] and "Down/up" A repeat of the same thing multiple times for every server
        elif " survival " in f" {message.content} " and "down" in f" {message.content} ":    #Sends server info for survival
            st_server = "survival"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.80:25575"  # Put the IP for the Server here
            #await log_channel.send(f"**Server Status** : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}")
            await serverstatus(message, st_server, st_ip)
        elif " skyblock " in f" {message.content} " and "down" in f" {message.content} ":    #Sends server info for Skyblock
            st_server = "skyblock"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25572"  # Put the IP for the Server here
            await log_channel.send(f"**Server Status** : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}")
            await serverstatus(message, st_server, st_ip)
        elif " duels " in f" {message.content} " and "down" in f" {message.content} ":       #Sends server info for Duels
            st_server = "duels"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25573"  # Put the IP for the Server here
            await log_channel.send(f"**Server Status** : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}")
            await serverstatus(message, st_server, st_ip)
        elif " bedwars " in f" {message.content} " and "down" in f" {message.content} ":     #Sends server info for Bedwars
            st_server = "bedwars"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25571"  # Put the IP for the Server here
            await log_channel.send(f"**Server Status** : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}")
            await serverstatus(message, st_server, st_ip)
        elif " auth " in f" {message.content} " and "down" in f" {message.content} ":        #Sends server info for Auth
            st_server = "auth"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25578"  # Put the IP for the Server here
            await log_channel.send(f"**Server Status** : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}")
            await serverstatus(message, st_server, st_ip)
        elif " proxy " in f" {message.content} " and "down" in f" {message.content} ":       #Sends server info for Proxy
            st_server = "proxy"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.60:25565"  # Put the IP for the Server here
            await log_channel.send(f"**Server Status** : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}")
            await serverstatus(message, st_server, st_ip)
        elif " lobby " in f" {message.content} " and "down" in f" {message.content} ":       #Sends server info for Lobby
            st_server = "lobby"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25577"  # Put the IP for the Server here
            await log_channel.send(f"**Server Status** : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}")
            await serverstatus(message, st_server, st_ip)
        #Check messages for [servername] and "Up"
        elif " survival " in f" {message.content} " and "up" in f" {message.content} ":    #Sends server info for survival
            st_server = "survival"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.80:25575"  # Put the IP for the Server here
            await log_channel.send(f"**Server Status** : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}")
            await serverstatus(message, st_server, st_ip)
        elif " skyblock " in f" {message.content} " and "up" in f" {message.content} ":    #Sends server info for Skyblock
            st_server = "skyblock"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25572"  # Put the IP for the Server here
            await log_channel.send(f"**Server Status** : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}")
            await serverstatus(message, st_server, st_ip)
        elif " duels " in f" {message.content} " and "up" in f" {message.content} ":       #Sends server info for Duels
            st_server = "duels"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25573"  # Put the IP for the Server here
            await log_channel.send(f"**Server Status** : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}")
            await serverstatus(message, st_server, st_ip)
        elif " bedwars " in f" {message.content} " and "up" in f" {message.content} ":     #Sends server info for Bedwars
            st_server = "bedwars"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25571"  # Put the IP for the Server here
            await log_channel.send(f"**Server Status** : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}")
            await serverstatus(message, st_server, st_ip)
        elif " auth " in f" {message.content} " and "up" in f" {message.content} ":        #Sends server info for Auth
            st_server = "auth"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25578"  # Put the IP for the Server here
            await log_channel.send(f"**Server Status** : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}")
            await serverstatus(message, st_server, st_ip)
        elif " proxy " in f" {message.content} " and "up" in f" {message.content} ":       #Sends server info for Proxy
            st_server = "proxy"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.60:25565"  # Put the IP for the Server here
            await log_channel.send(f"**Server Status** : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}")
            await serverstatus(message, st_server, st_ip)
        elif " lobby " in f" {message.content} " and "up" in f" {message.content} ":       #Sends server info for Lobby
            st_server = "lobby"  # Put the name for the server here (non-capitalised)
            st_ip = "192.168.100.70:25577"  # Put the IP for the Server here
            await log_channel.send(f"**Server Status** : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}")
            await serverstatus(message, st_server, st_ip)
            await log_channel.send(f"**Server Status** : Sent Server {st_server.capitalize()} embed to message of {message.author.name}#{message.author.discriminator}")
        elif ".suggest" in f" {message.content} ":  #If a member uses the old .suggest command, tell them to use the new one
            await message.reply("Please use `+suggest` from now on, instead!")
            cat = "h"
            await log_channel.send(f'**Help** : #{countadd(cat)} Sent wrong suggest command usage message to message of {message.author.name}#{message.author.discriminator}')    #Logs to Log channel




        await client.process_commands(message)





#
#
#   Info Catagory
#
#



@client.command(aliases=['bedrock', 'java'])   # The IP command
async def ip(message):
    ipembed = discord.Embed(title="Here's the Server ip!", url="https://moonball.io", color=embed_color)
    ipembed.set_author(name=embed_header)
    ipembed.set_thumbnail(url="https://media.discordapp.net/attachments/880368661104316459/950775364928561162/logo.png")
    ipembed.add_field(name="Java ", value="play.moonball.io", inline=True)  # <:java:914118540959813632>
    ipembed.add_field(name="Bedrock ", value="play.moonball.io (Port 25565)",inline=False)  # <:Mc_Pocket_edition:903568186413293589>
    ipembed.set_footer(text=embed_footer)
    await message.reply(embed=ipembed)
    cat = "i"
    await log_channel.send(f"**Info** : #{countadd(cat)} Sent IP embed to message of {message.author.name}#{message.author.discriminator}")
    print(f'Info : Sent IP Embed to message of {message.author.name}#{message.author.discriminator}')



@client.command()
async def version(message): # Sends version embed
    vembed = discord.Embed(title="Here's the Server Version!", url="https://moonball.io", color=embed_color)
    vembed.set_author(name=embed_header)
    vembed.set_thumbnail(url="https://media.discordapp.net/attachments/880368661104316459/950775364928561162/logo.png")
    vembed.add_field(name="Java ", value="1.13 - 1.18.2", inline=True)
    vembed.add_field(name="Bedrock ", value="1.17.40 - 1.18.12", inline=False)
    vembed.set_footer(text=embed_footer)
    await message.reply(embed = vembed) #Sends the Embed
    await log_channel.send(f'Sent `Version` Embed to message of {message.author.name}#{message.author.discriminator}')    #Logs to Log channel
    cat = "i"
    await log_channel.send(f"**Info** : #{countadd(cat)} Sent Version embed to message of {message.author.name}#{message.author.discriminator}")
    print(f'Info : Sent Version Embed to message of {message.author.name}#{message.author.discriminator}')      # Logs to Console



@client.command(aliases=['memory', 'mem', 'cpu', 'ram', 'lag', 'ping']) #Bot Stats Command
async def stats(ctx):
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
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
    await ctx.reply(embed = stats)
    cat = "i"
    print(f'Sent bot Stats to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console
    await log_channel.send(f"**Info** : #{countadd(cat)} Sent Stats embed to message of {ctx.author.name}#{ctx.author.discriminator}")


@client.command()
async def shop(ctx):
    await ctx.send("Visit our shop here! \nhttps://shop.moonball.io")


#This part is making aliases for each server's status. Just copy-paste of code, but with server-name and IP changed
@client.command(aliases=['survival'])   #Status cmd for survival
async def statussurvival(ctx):
    st_server = "survival"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.80:25575"  # Put the IP for the Server here
    await serverstatus(ctx, st_server, st_ip)
@client.command(aliases=['skyblock'])   #Status cmd for skyblock
async def statusskyblock(ctx):
    st_server = "skyblock"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.70:25572"  # Put the IP for the Server here
    await serverstatus(ctx, st_server, st_ip)
@client.command(aliases=['duels', 'duel'])  #Status cmd for duels
async def statusduels(ctx):
    st_server = "duels"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.70:25573"  # Put the IP for the Server here
    await serverstatus(ctx, st_server, st_ip)
@client.command(aliases=['bedwars', 'bedwar', 'bw'])    #Status cmd for bedwars
async def statusbedwars(ctx):
    st_server = "bedwars"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.70:25571"  # Put the IP for the Server here
    await serverstatus(ctx, st_server, st_ip)
@client.command(aliases=['lobby', 'hub'])   #Status cmd for lobby
async def statuslobby(ctx):
    st_server = "lobby"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.70:25577"  # Put the IP for the Server here
    await serverstatus(ctx, st_server, st_ip)
@client.command(aliases=['auth', 'authserver']) #Status cmd for auth
async def statusauth(ctx):
    st_server = "auth"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.70:25578"  # Put the IP for the Server here
    await serverstatus(ctx, st_server, st_ip)
@client.command(aliases=['proxy', 'velocity'])  #Status cmd for proxy
async def statusproxy(ctx):
    st_server = "proxy"  # Put the name for the server here (non-capitalised)
    st_ip = "192.168.100.60:25565"  # Put the IP for the Server here
    await serverstatus(ctx, st_server, st_ip)

#
#
#   Other Catagory
#
#


@client.event   # Welcome Announcement
async def on_member_join(member):
    guild = client.get_guild(894902529039687720)  # Replace "894902529039687720" with your server ID (Server Settings > Widget > Copy Server ID)
    #The embed for Welcome Announcements
    welc_embed = discord.Embed(title=f'Welcome to the Discord Server!', url="https://moonball.io", color=embed_color)
    welc_embed.add_field(name="Shenanigans Network",value=f"<a:malconfetti:910127223791554570> Welcome {member.mention} to the Discord! <a:malconfetti:910127223791554570>\n<a:Read_Rules:910128684751544330> Please check out the Server Rules here <#894902529039687722> <a:Read_Rules:910128684751544330>\n <a:hypelove:901476784204288070> Take your Self Roles at <#910130264905232424> <a:hypelove:901476784204288070>\n <:02cool:910128856550244352> Head over to ⛧╭･ﾟgeneral-eng to talk with others! <:02cool:910128856550244352> \n<a:Hearts:952919562846875650> Server info and IP can be found here <#897502089025052693> <a:Hearts:952919562846875650>",inline=True)
    welc_embed.set_image(url="https://media.discordapp.net/attachments/896348336972496936/952940944175554590/ezgif-1-e6eb713fa2.gif")
    welc_embed.set_footer(text=embed_footer)
    await general_channel.send(embed=welc_embed)
    #role = discord.utils.get(member.server.roles, name="Member")  # Gets the member role as a `role` object
    #await client.add_roles(member, role)  # Gives the role to the user
    print(f"Other : Sent Welcome Embed {member.name}#{member.discriminator}") # This part does not work.
    await log_channel.send(f'**Other** : Sent Welcome Embed to {member.name}#{member.discriminator}')    #Logs to Log channel



@client.command()
async def opensource(ctx):
    await checkcommandchannel(ctx)
    await ctx.reply(f"This Discord Bot is opensource and made with discord.py.\nIf you would like to check out the source code, Visit the GitHub Repo here - https://moonball.io/opensource")
    cat = "i"
    await log_channel.send(f'**Info** : #{countadd(cat)} Sent Bot GitHub URL (rickroll) to message of {ctx.author.name}#{ctx.author.discriminator}')    #Logs to Log channel



@client.command()
async def botversion(ctx):
    await checkcommandchannel(ctx)
    ctx.reply(f"I am currentlly on Version `{version}`!")



@client.command()
async def invite(ctx):
    await checkcommandchannel(ctx)
    await ctx.reply("To invite me to your server, Click on the link below\nhttps://moonball.io/bot")
    cat = "i"
    await log_channel.send(f'**Info** : #{countadd(cat)} Sent Bot invite URL (rickroll) to message of {ctx.author.name}#{ctx.author.discriminator}')    #Logs to Log channel

#
#
#   Help Catagory
#
#

@client.group(pass_context=True, aliases=['info', 'help'], invoke_without_command=True) #Help Command
async def bothelp(ctx):
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    #Base Help command embed
    bothelp = discord.Embed(title="Help Command", url="https://moonball.io", description=f"Use `{prefix}help <module>` to learn more about that specific module\nModules Include - ```ini\n[ping, status, suggestion, ip/version, embed, poll, coinflip, admin]```", color=embed_color)
    bothelp.set_author(name=f"{embed_header}")
    bothelp.add_field(name="Prefix", value=f"The prefix is `{prefix}`", inline=True)
    bothelp.add_field(name="Bot Version", value=f"{bot_version}", inline=True)
    bothelp.add_field(name="Bot Dev", value="<@837584356988944396>", inline=True)
    bothelp.add_field(name="Info",value=f"Get info about the Server/Bot with this catagory of commands.\n Commands include ```ini\n[ip, version, ping, status]```",inline=True)
    bothelp.add_field(name="Help",value=f"Commands assisting the usage of this Discord Bot or our MC Server can be found in this catagory. Commands include ```ini\n[help, error_message, @ping_message]```",inline=False)
    bothelp.add_field(name="Fun",value=f"The commands which enrich the user experiance of being in this Discord Server.\n Commands include ```ini\n[suggest, embed, coinflip, poll, reminder(Coming-Soon)]``` \n",inline=False)
    bothelp.add_field(name="Admin",value=f"Functions and Commands made to modify details about the bot/server are within this catagory. Only server Staff can access/use them. Commands include ```ini\n[changeServerState\css, resetcounter]```",inline=False)
    bothelp.add_field(name="Other",value=f"Any other command that does not fit in any other catagory can be found here.\nCommands include ```ini\n[opensource, botversion, prefix, invite]```",inline=False)
    bothelp.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=bothelp)
    cat = "h"
    await log_channel.send(f'**Help** : #{countadd(cat)} Sent Base Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')    #Logs to Log channel
    print(f'Help : Sent Base Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console


#
#  Bot Help for Info Catagory
#

@bothelp.command(aliases=['ping', 'stats', 'mem', 'stat', 'cpu'])   #Sub-command for help.
async def ping_bothelp(ctx):
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    embed = discord.Embed(title="Help Command - Ping", url="https://moonball.io",description="This is the Help category for the `ping` command.", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name="Description", value="The `ping` Command sends information relating to the bot's status.  ",inline=False)
    embed.add_field(name="Features", value="Can be used to check Latency, CPU Usage, RAM Usage and Uptime.",inline=False)
    embed.add_field(name="Version introduced in", value="\>0.05", inline=False)
    embed.add_field(name="Aliases", value="```ini\n[mem, memory, cpu, ram, lag, ping, stats]```", inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=embed)
    cat = "h"
    await log_channel.send(f'**Help** : #{countadd(cat)} Sent Ping-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')    #Logs to Log channel
    print(f'Help : Sent Ping-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console


@bothelp.command(aliases=['status'])    #Sub-command for help.
async def status_bothelp(ctx):
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    embed = discord.Embed(title="Help Command - Status", url="https://moonball.io",description="This is the Help category for the `status` command.", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name="Description",value=f"The `status` command sends info about a specific mentioned server. It can be triggered in 2 ways.\n►**Auto Trigger** - When user says 'up'/'down' and (servername) in the same message.\n►**Manual Trigger** - Using the command `{prefix}servername`",inline=False)
    embed.add_field(name="Features", value="Can be used to check the Status, Players Online, CPU/RAM/Disk and Uptime information for a specific server",inline=False)
    embed.add_field(name="Version introduced in", value="\>0.1", inline=False)
    embed.add_field(name="Aliases", value=f"```ini\n[Proxy/Velocity, Auth/AuthServer, Lobby/Hub, Survival, Skyblock, Bedwars/Bedwar/bw, Duels/Duel]```", inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=embed)
    cat = "h"
    await log_channel.send(f'**Help** : #{countadd(cat)} Sent Status-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')    #Logs to Log channel
    print(f'Help : Sent Status-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console


@bothelp.command(aliases=['ip', 'version'])    #Sub-command for help.
async def ip_bothelp(ctx):
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    embed = discord.Embed(title="Help Command - IP", url="https://moonball.io",description="This is the Help category for the `IP`/`version` command.", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name="Description", value=f"The `IP`/`version` Command sends a nice-looking embed to the user.\nCan be triggered in 2 ways\n►**Automatic Trigger** - Any message with the word `ip` or `version` in it will trigger the embed\n**Manual Trigger** - Doing `+ip` or `+version` will also send the embed",inline=False)
    embed.add_field(name="Features", value="Posts the IPs/Versions of both Java and Bedrock in a convenient Embed. Reducing the manual work to post the ip message again and again.",inline=False)
    embed.add_field(name="Version introduced in", value="0.01", inline=False)
    embed.add_field(name="Aliases", value="```ini\n[ip, java, bedrock / version]```", inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=embed)
    cat = "h"
    await log_channel.send(f'**Help** : #{countadd(cat)} Sent IP-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')    #Logs to Log channel
    print(f'Help : Sent IP-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console

#
#   Bot Help for Fun catagory
#


@bothelp.command(aliases=['suggest', 'suggestion']) #Sub-command for help.
async def suggest_bothelp(ctx):
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    embed = discord.Embed(title="Help Command - Suggestion", url="https://moonball.io",description="This is the Help category for the `Suggestion` command.", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name="Description", value=f"The `Suggest` Command sends a user's suggestion to the <#{suggestion_channel}> channel. ",inline=False)
    embed.add_field(name="Features", value="It posts your suggestion to the official suggestion channel of the server. Reacts to it with <:tick_bot:953561636566863903> and <:cross_bot:953561649254649866> so that it can be voted on and implemented! Say `nl` within the embed to put the proceeding text in the next line.",inline=False)
    embed.add_field(name="Version introduced in", value="0.2", inline=False)
    embed.add_field(name="Aliases", value="```ini\n[suggest, suggestion, createsuggestion]```", inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=embed)
    cat = "h"
    await log_channel.send(f'**Help** : #{countadd(cat)} Sent Suggest-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')    #Logs to Log channel
    print(f'Help : Sent Suggest-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console


@bothelp.command(aliases=['embed', 'announce', 'ann'])  #Sub-command for help.
async def embed_bothelp(ctx):
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    embed = discord.Embed(title="Help Command - Embed", url="https://moonball.io", description="This is the Help category for the `Embed` command.", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name="Description", value=f"The `Embed` Command creates a nice embed with a simple syntax ```ini\n{prefix}embed [The Embed Title] | [The Embed Content]```\n Use `|` to separate all the 2 arguments.",inline=False)
    embed.add_field(name="Features", value="Posts a Embed with the user's liking's content to any channel Say `nl` within the embed to put the proceeding text in the next line.",inline=False)
    embed.add_field(name="Version introduced in", value="0.05", inline=False)
    embed.add_field(name="Aliases", value="```ini\n[ann, announce, embed]```", inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=embed)
    cat = "h"
    await log_channel.send(f'**Help** : #{countadd(cat)} Sent Embed-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')    #Logs to Log channel
    print(f'Help : Sent Embed-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console


@bothelp.command(aliases=['coinflip', 'head', 'tail'])  #Sub-command for help.
async def Coinflip_bothelp(ctx):
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    embed = discord.Embed(title="Help Command - Coin Flip", url="https://moonball.io",description="This is the Help category for the `Coin Flip` command.", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name="Description", value=f"The `Coin Flip` Command Picks either heads or tails randomlly ", inline=False)
    embed.add_field(name="Features", value="Picks either heads or tails randomlly and sends the responce with a nice-looking heads/tails picture.",inline=False)
    embed.add_field(name="Version introduced in", value="0.2.3", inline=False)
    embed.add_field(name="Aliases", value="```ini\n[head, tail, CoinFlip, FlipCoin]```", inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=embed)
    cat = "h"
    await log_channel.send(f'**Help** : #{countadd(cat)} Sent CoinFlip-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')    #Logs to Log channel
    print(f'Help : Sent CoinFlip-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console


@bothelp.command(aliases=['poll', 'cpoll', 'spoll', 'createpoll', 'sendpoll'])  #Sub-command for help.
async def poll_bothelp(ctx):
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    embed = discord.Embed(title="Help Command - Poll", url="https://moonball.io",description="This is the Help category for the `Poll` command.", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name="Description", value=f"The `Poll` Command Sends a multiple option poll with upto 4 options", inline=False)
    embed.add_field(name="Features", value=f"The Poll Command sends a poll with the user's input with upto 4 reactions/options. It has a simple syntax - \n```ini\n{prefix}poll [number of options] | [Your poll Text here]```\nUse `|` to seperate the 2 arguments. Say `nl` within the poll to put the proceeding text in the next line.",inline=False)
    embed.add_field(name="Version introduced in", value="0.2.3", inline=False)
    embed.add_field(name="Aliases", value="```ini\n[cpoll, spoll, createpoll, sendpoll]```", inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=embed)
    cat = "h"
    await log_channel.send(f'**Help** : #{countadd(cat)} Sent Poll-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')    #Logs to Log channel
    print(f'Help : Sent Poll-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console



#
#   Admin Help
#


#Admin Help
@client.group(pass_context=True, invoke_without_command=True, aliases=['adminhelp'])
async def admin(ctx):
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    #Base Admin-Help command embed
    bothelp = discord.Embed(title="Admin Command", url="https://moonball.io",description=f"Use `{prefix}admin <module>` to execute the command\nModules Include - ```ini\n[changeServerState/css, resetcounter]```", color=embed_color)
    bothelp.set_author(name=f"{embed_header}")
    bothelp.add_field(name="Prefix", value=f"The prefix is `{prefix}`", inline=True)
    bothelp.add_field(name="Bot Version", value=f"{bot_version}", inline=True)
    bothelp.add_field(name="Bot Dev", value="<@837584356988944396>", inline=True)
    bothelp.add_field(name="Change Server State",value=f"Changes the state of the mentioned server, Can Start/Stop/Restart and Kill any server.\nTo learn more, do `{prefix}admin css`",inline=True)
    bothelp.add_field(name="Reset Command Counter",value=f"Resets a command counter from the 5 options with a single command.\n To learn more do `{prefix}admin resetcounter`",inline=False)
    bothelp.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=bothelp)
    cat = "a"
    await log_channel.send(f'**Help** : #{countadd(cat)} Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')    #Logs to Log channel
    print(f'Help : Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console

@admin.group(aliases=['resetcounter']) # Help reset counter
async def resetcounter_admin(ctx):
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    #Base Admin-Help command embed
    bothelp = discord.Embed(title="Admin Help - Reset Counter", url="https://moonball.io",description=f"Use `{prefix}admin [suffix]` to execute the command.\nResets a specific command counter", color=embed_color)
    bothelp.set_author(name=f"{embed_header}")
    bothelp.add_field(name="RSC",value=f"**Reset Suggestion Count**. Resets the Suggestion Count.\nAliases Include -\n```ini\n[rsc, Resetsuggestioncount, resetsuggest, resetscount]```",inline=True)
    bothelp.add_field(name="RHC",value=f"**Reset Help Count** Resets the Help Count, The counter of how many times a Help catagory command has been executed\nAliases Include -\n```ini\n[rhc, Resethelpcount, resethelp, resetHcount]```",inline=False)
    bothelp.add_field(name="RIC ",value=f"**Reset Info Count** Resets the Info Count, The counter of how many times a Info catagory command has been executed\nAliases Include -\n```ini\n[ric, Resetinfocount, resetinfo, resetIcount]```",inline=False)
    bothelp.add_field(name="RFC",value=f"**Reset Fun Count** Resets the Fun Count, The counter of how many times a Fun catagory command has been executed\nAliases Include -\n```ini\n[rfc, Resetfuncount, resetfun, resetFcount]```",inline=False)
    bothelp.add_field(name="RAC",value=f"**Reset Admin Count** Resets the Admin Count, The counter of how many times a Admin catagory command has been executed\nAliases Include -\n```ini\n[rac, Resetadmincount, resetadmin, resetAcount]```",inline=False)
    bothelp.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=bothelp)
    cat = "a"
    await log_channel.send(f'**Help** : #{countadd(cat)} Sent Reset-Counter sub-Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')    #Logs to Log channel
    print(f'Help : Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console

@admin.group(aliases=['css', 'changeserverstate'])
async def changeserverpower_admin(ctx): #Help changeserverstate
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    #Base Admin-Help command embed
    bothelp = discord.Embed(title="Admin Help - Change Server State", url="https://moonball.io",description=f"Use `{prefix}admin [state] [servername]` to execute the command.\nChanges the status of a specific mentioned server ", color=embed_color)
    bothelp.set_author(name=f"{embed_header}")
    bothelp.add_field(name="Description",value=f"This command changes the power/state of any server",inline=True)
    bothelp.add_field(name="Features",value=f"Start/Stop/Restart or Kill a server just with one single command here on Discord, using a conveniently easy command!",inline=False)
    bothelp.add_field(name="Valid States",value=f"```ini\n[start, stop, restart, kill]```",inline=False)
    bothelp.add_field(name="Valid Servers",value="```ini\n[proxy, auth, lobby, survival, skyblock, duels, bedwars]```",inline=False)
    bothelp.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=bothelp)
    cat = "a"
    await log_channel.send(f'**Help** : #{countadd(cat)} Sent Admin Change-Server-State sub-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')    #Logs to Log channel
    print(f'Help : Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console



#
#
#   Fun Catagory
#
#



@client.command(aliases=['announce, ann'])  #The announcement Embed creator
async def embed(ctx, *data):
    try:
        data = " ".join(data).split(' | ')  #Input Splitter
        a = data[1].replace(" nl ", " \n")
        syntax_error = False
        if len(data) != 2:  #verifying complete syntax
            syntax_error = True
            await ctx.send(f"The syntax is as follows: `{prefix}embed <title> | <description>`")
            await ctx.add_reaction("<:cross_bot:953561649254649866>")
        if syntax_error: return
    except: 
        await ctx.send("Could not send the Embed. An error occurred. Re-Check the syntax or read the embed help page with `+help embed`")  #If it can not send the embed, send error msg
        return
        #Embed Builder
    announcement = discord.Embed(title=f"Embed by {ctx.author.name}#{ctx.author.discriminator}", url="https://moonball.io", color=embed_color)
    announcement.add_field(name=f"{data[0]}", value=f"{a}", inline=True)
    announcement.set_footer(text=embed_footer)
    try:    #Try to send the embed
        await ctx.send(embed=announcement)
        await embed_log.send(embed=announcement)
        await ctx.message.delete()  # delete original
        cat = "f"
        countadd(cat) 
    except: 
        await ctx.send("Could not send the Embed. An error occurred. Re-Check the syntax or read the embed help page with `+help embed`")  #If it can not send the embed, send error msg
        return
    print(f'Sent Embed (Embed Creator) from message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console
    await log_channel.send(f"**Fun** : #{countadd(cat)} Sent embed-creator embed to message of {ctx.author.name}#{ctx.author.discriminator}")    # Logging to log channel



@client.command(aliases=['cpoll', 'spoll', 'createpoll', 'sendpoll']) # Poll Command
async def poll(ctx, *data):
    #if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    #guild = client.get_guild(894902529039687720)  # Replace "894902529039687720" with your server ID (Server Settings > Widget > Copy Server ID)
    try:
        data = " ".join(data).split(' | ') # Input Splitter
        reactionc = data[0]
        content = data[1].replace(" nl ", " \n")
    except: 
        await ctx.send(f"There was an error! The Syntax is perhaps incorrect. The corret Syntax is ```ini\n{prefix}poll [number of options] | [Your poll Text here]```\n For more, check out `{prefix}help poll`.")
        return
        #The embed
    p_embed = discord.Embed(title=f"Poll", url="https://moonball.io", color=embed_color)
    p_embed.add_field(name=f"Poll by {ctx.author.name}#{ctx.author.discriminator}", value=f"{content}", inline=True)
    p_embed.set_footer(text=f"{embed_footer}")
    if int(reactionc) > 4:  # Check if number of reactions is more than 4
        await ctx.send("Sorry, You can't have more than 4 options in a Poll")
        return
    elif int(reactionc) < 2: # Check if number of reactions is less than 2
        await ctx.send("Sorry, You can't have less than 2 options in a Poll")
        return
    else:
        p = await ctx.send(embed=p_embed)   # Sending the Embed
        await p.add_reaction("<:1_bot:957922958502952981>")  # Adding 1 reaction
        await p.add_reaction("<:2_bot:957922954119888917>")  # Adding 2 reaction
        if int(reactionc) == 3: await p.add_reaction("<:3_bot:957922953893384192>") # Checking if number is 3, if yes add 3 reaction 
        elif int(reactionc) == 4:   # Checking of the number is 4
            await p.add_reaction("<:3_bot:957922953893384192>") # Adding 3 reaction
            await p.add_reaction("<:4_bot:957922953381707797>") # Adding 4 reaction
        cat = "f"
        await log_channel.send(f"**Fun** : #{countadd(cat)} Sent Poll embed to message of {ctx.author.name}#{ctx.author.discriminator}")    # Logging to log channel
        print(f"Fun : Sent {ctx.author.name}#{ctx.author.discriminator}'s Poll!")
        #dm = await ctx.member.create_dm()
        #await dm.send("hi this is a dear message")
        #await ctx.reply("Your Poll was sent!")




@client.command(aliases=['head', 'tail', 'flip', 'flipcoin'])   
async def coinflip(ctx):    # Coin Flip Command
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    determine_flip = [1, 0] # The options
    if random.choice(determine_flip) == 1: value = "Heads"
    else: value = "Tails"
    embed = discord.Embed(title="Coin Flip", description=f"{ctx.author.mention} Flipped a coin!, They got **{value}**", color=embed_color)
    if value == "Heads": embed.set_image(url="https://cdn.discordapp.com/attachments/918916688693587968/957634026880004166/head.png")   # Setting head image
    else: embed.set_image(url="https://cdn.discordapp.com/attachments/918916688693587968/957634026661904404/tail.png")  # Setting tails image
    embed.set_author(name=embed_header)
    embed.set_footer(text=embed_footer)
    await ctx.send(embed=embed)
    cat = "f"
    await log_channel.send(f'**Fun** : #{countadd(cat)} Sent Coin Flip result to message of {ctx.author.name}#{ctx.author.discriminator}')    #Logs to Log channel
    print(f'Fun : Sent Coin Flip result to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console




@client.command(aliases=['suggestion', 'createsuggestion']) # Suggest Command
async def suggest(ctx, *data):
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    cat = "s"
    data = " ".join(data).split() # Input Splitter
    a = data[0].replace(" nl ", " \n")
            #The embed
    s_embed = discord.Embed(title=f"Suggestion", url="https://moonball.io", color=embed_color)
    s_embed.add_field(name=f"Submitted by {ctx.author.name}#{ctx.author.discriminator}", value=f"Suggestion #{countadd(cat)}\n{a}", inline=True)
    s_embed.set_footer(text=f"{embed_footer}")
    s = await suggestion_channel.send(embed=s_embed)
        #Adding reactions
    await s.add_reaction("<:tick_bot:953561636566863903>")  #adding tick reaction
    await s.add_reaction("<:cross_bot:953561649254649866>") #adding cross reaction
    await embed_log.send(embed=s_embed)   #Sending it to the Logs channel
    await ctx.reply(f"Your Suggestion was sent! Check <#956806563950112848> to see how its doing!")
    print(f"Sent {ctx.author.name}#{ctx.author.discriminator}'s Suggestion")




#
#
#   Admin Command & Logging Function Section
#
# 


@admin.command(aliases=['startserver', 'serverstart', 'ss', 'start'])
@commands.has_permissions(administrator=True)   
async def start_admin(ctx, *data):
    data = " ".join(data).split() # Input Splitter
    valid_names = ["proxy", "auth", "lobby", "survival", "skyblock", "duels", "bedwars", "bot"]
    power = "start"
    if data[0] not in valid_names:
        await ctx.reply(f"Error : Invalid Server Name. Use `{prefix}admin css` to learn more!")
        return
    servername = data[0]
    try: e = await serverpower(servername, power, ctx)
    except: 
        await ctx.reply(f"There was an error. Use `{prefix}admin css` to learn more")
        return

    if e == "exception": return
    embed=discord.Embed(title="Server Power", url="https://moonball.io/", description=f"Starts/Stops/Restarts or Kills a specific server on command.\n `{prefix}admin {power}` to learn more!", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name=f'Operation Successful!', value=f'Successfully Started the {servername.capitalize()} Server!', inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=embed)

@admin.command(aliases=['stopserver', 'serverstop', 'sts', 'stop'])
@commands.has_permissions(administrator=True)   
async def stop_admin(ctx, *data):
    data = " ".join(data).split() # Input Splitter
    valid_names = ["proxy", "auth", "lobby", "survival", "skyblock", "duels", "bedwars", "bot"]
    power = "stop"
    if data[0] not in valid_names:
        await ctx.reply(f"Error : Invalid Server Name. Use `{prefix}admin css` to learn more!")
        return
    servername = data[0]
    try : e = await serverpower(servername, power, ctx)
    except: 
        await ctx.reply(f"There was an error. Use `{prefix}admin css` to learn more")
        return
    if e == "exception": return
    embed=discord.Embed(title="Server Power", url="https://moonball.io/", description=f"Starts/Stops/Restarts or Kills a specific server on command.\n `{prefix}admin {power}` to learn more!", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name=f'Operation Successful!', value=f'Successfully Stopped the {servername.capitalize()} Server!', inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=embed)

@admin.command(aliases=['restartserver', 'serverrestart', 'rs', 'restart'])
@commands.has_permissions(administrator=True)   
async def restart_admin(ctx, *data):
    data = " ".join(data).split() # Input Splitter
    valid_names = ["proxy", "auth", "lobby", "survival", "skyblock", "duels", "bedwars", "bot"]
    power = "restart"
    servername = data[0]
    print(servername)
    if servername not in valid_names:
        await ctx.reply(f"Error : Invalid Server Name. Use `{prefix}admin css` to learn more!")
        return

    try : e = await serverpower(servername, power, ctx)
    except: 
        await ctx.reply(f"There was an error. Use `{prefix}admin css` to learn more")
        return
    if e == "exception": return
    
    embed=discord.Embed(title="Server Power", url="https://moonball.io/", description=f"Starts/Stops/Restarts or Kills a specific server on command.\n `{prefix}admin {power}` to learn more!", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name=f'Operation Successful!', value=f'Successfully Restarted the {servername.capitalize()} Server!', inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=embed)

@admin.command(aliases=['killserver', 'serverkill', 'sk', 'kill'])
@commands.has_permissions(administrator=True)   
async def kill_admin(ctx, *data):
    data = " ".join(data).split() # Input Splitter
    valid_names = ["proxy", "auth", "lobby", "survival", "skyblock", "duels", "bedwars", "bot"]
    power = "kill"
    if data[0] not in valid_names:
        await ctx.reply(f"Error : Invalid Server Name. Use `{prefix}admin css` to learn more!")
        return
    servername = data[0]
    try : e = await serverpower(servername, power, ctx)
    except: 
        await ctx.send(f"There was an error. Use `{prefix}admin css` to learn more")
        return
    if e == "exception": return
    
    embed=discord.Embed(title="Server Power", url="https://moonball.io/", description=f"Starts/Stops/Restarts or Kills a specific server on command.\n `{prefix}admin {power}` to learn more!", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name=f'Operation Successful!", value="Successfully Killed the {servername.capitalize()} Server!', inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=embed)




@admin.command(aliases = ['cmd', 'send', 'sendcmd'])
@commands.has_permissions(administrator=True)
async def sendcmd_admin(ctx, *data):
    data = " ".join(data).split(' | ') # Input Splitter
    valid_names = ["proxy", "auth", "lobby", "survival", "skyblock", "duels", "bedwars", "bot"]
    if data[0] not in valid_names:
        await ctx.send("Invalid Name")
        return "invalid_name"
    else : servername = data[0]
    if data[1] == "":
        await ctx.send("Invalid command to send")
        return "invalid_cmd"
    else : cmd = data[1]
    
    p = await sendcmd(ctx, data[0], data[1])
    #try : await sendcmd(ctx, servername, cmd)
    #except: 
    #    await ctx.reply("There was a error in sending the command")
    #    return
    if p == "done":
        await ctx.reply("Sucessfully sent the command")





async def resetcount(ctx, kw, name):
    file = open(f'./data/{kw}count.txt', 'wb')  # Opens the file
    a = 0   # Declares a variable with the value "0"
    pickle.dump(a, file)    # Puts 0 in the file
    file.close()    # Closes the file
    await ctx.send(f"Done! Reset the {name} Counter")
    print(f"Reset the {name} Counter")
    cat = "a"
    
    await log_channel.send(f"**Admin** : #{countadd(cat)} {name} Counter was reset by {ctx.author.name}#{ctx.author.discriminator}") #Logs to Log channel 



@admin.command(aliases=['rsc', 'Resetsuggestioncount', 'resetsuggest', 'resetscount'])
@commands.has_permissions(administrator=True)   
async def resetscount_admin(ctx):
    kw = "s"
    name = "Suggestion"
    await resetcount(ctx, kw, name)

@admin.command(aliases=['rhc', 'resethelpcount', 'resethelp', 'resethcount'])
@commands.has_permissions(administrator=True)
async def resethcount_admin(ctx):
    kw = "h"
    name = "Help"
    await resetcount(ctx, kw, name)

@admin.command(aliases=['ric', 'resetinfocount', 'resetinfo', 'reseticount'])
@commands.has_permissions(administrator=True)
async def reseticount_admin(ctx):
    kw = "i"
    name = "Info"
    await resetcount(ctx, kw, name)

@admin.command(aliases=['rfc', 'resetfuncount', 'resetfun', 'resetfcount'])
@commands.has_permissions(administrator=True)
async def resetfcount_admin(ctx):
    kw = "f"
    name = "Fun"
    await resetcount(ctx, kw, name)

@admin.command(aliases=['rac', 'resetadmincount', 'resetadmin', 'resetacount'])
@commands.has_permissions(administrator=True)
async def resetacount_admin(ctx):
    kw = "a"
    name = "Admin"
    await resetcount(ctx, kw, name)



def countadd(cat):  # Counter Add Function
    with open(f'./data/{cat}count.txt', 'rb') as f: # Opens the file  in READ mode 
        oldcount = pickle.load(f)   # Gets the old count
    newcount = oldcount+1   # Adds 1
    f.close()           #Closes file
    file = open(f'./data/{cat}count.txt', 'wb') # Opens the file in Write Mode
    pickle.dump(newcount, file) # Adds new value (After adding 1)
    file.close()        # Closes file
    return newcount 


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
    ptero_panel = "panel.moonball.io" #Put your Ptero Panel's URL here

    server_guide = {'fe5a4fe1': 'proxy', 'e91b165c': 'auth', 'd0f6701c': 'lobby', '5d0ac930': 'survival',   #Change this part, Add your server name and the ptero identifier (example in https://panel.moonball.io/server/5426b68e "5426b68e" is the ID)
                    '3a0eaf97': 'skyblock', '6e5ed2ac': 'duels', 'edeeff53': 'bedwars', '5426b68e': 'bot'}
    headers = {
        "Authorization": f"Bearer {ptero_apikey}",
        "Accept": "application/json", "Content-Type": "application/json"}
    if servername == "all":
        servers = {}
        for server_id in list(server_guide.keys()):
            url = f"https://{ptero_panel}/api/client/servers/{server_id}/resources"
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



#
#   Server Power backend
#


async def serverpower(servername, power, ctx):
    ptero_panel = "panel.moonball.io" #Put your Ptero Panel's URL here
    
    st_server = servername
    placeholder = await status(st_server)   #Gets server info
    serverstatus = placeholder["state"] #Gets its state

        #Checks if specific conditions are true
    if serverstatus == "running" and power == "start":
        await ctx.reply(f"The server, {servername} is already running!")
        return "exception"
    elif serverstatus == "offline" and power == "stop":
        await ctx.reply(f"The server, {servername} is already off")
        return "exception"
    elif serverstatus == "offline" and power == "kill":
        await ctx.reply(f"The server, {servername} is already off")
        return "exception"
    elif serverstatus == "starting" and power == "start":
        await ctx.reply(f"The server, {servername} is already starting")
        return "exception"
    elif serverstatus == "stopping" and power == "stop":
        await ctx.reply(f"The server, {servername} is already stopping")
        return "exception"
    elif servername == "bot":
        await ctx.reply(f"I can't do anything to myself.")
        return "exception"


    serv_ips = {'proxy': '192.186.100.60:25565', 'auth' : '192.168.100.70:25578', 'lobby' : '192.168.100.70:25577', 'survival' : '192.168.100.80:25575', 'skyblock' : '192.168.100.70:25572', 'bedwars' : '192.168.100.70:25571', 'duels' : '192.168.100.70:25573' }
    #server =     #Gets server player-info from API
    
    try:
           #Try to get player info from server, only IF it is online
        playerCount = MinecraftServer.lookup(serv_ips.get(servername)).query().players.online
    except: 
        playerCount = 0 #If unreachable, set it to 0
        await ctx.send("There was an error trying to get the player count of the server. The panel is perhaps down. Anyways ill continue with it being 0")


    if power in ("stop", "kill", "restart"):
        if playerCount != 0:
            #await ctx.reply(f"There are {playerCount} online")
            await ctx.reply("There is more than one person online on that server. Are you sure you want to proceed with the distructive action, while the players are online. If yes, say `yes` in chat")
            #await ctx.send(type=InteractionType.ChannelMessageWithSource, content="There is more than one person online on that server. Are you sure you want to proceed with the distructive action, while the players are online", components= Button(style=ButtonStyle.red, label="Confirm", custom_id="confirm_power_action")])
            msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
            if msg.content == "yes" or "YES" or "Yes": await ctx.reply("Okay! As you wish, master. Here I begin!")
            else: 
                ctx.reply("You took to long to reply or did not say `yes`. I am aborting the power action on the server.")
                return

    server_guide = { 'proxy' : 'fe5a4fe1',  'auth':'e91b165c', 'lobby':'d0f6701c', 'survival':'5d0ac930',   #Change this part, Add your server name and the ptero identifier (example in https://panel.moonball.io/server/5426b68e "5426b68e" is the ID)
                     'skyblock':'3a0eaf97',  'duels':'6e5ed2ac',  'bedwars':'edeeff53',  'bot':'5426b68e'}
   
    url = f'https://{ptero_panel}/api/client/servers/{server_guide.get(servername)}/power'
    headers = {"Authorization": f"Bearer {ptero_apikey}","Accept": "application/json","Content-Type": "application/json"}
    if power == "start": payload = '{"signal": "start"}'
    elif power == "stop": payload = '{"signal": "stop"}'
    elif power == "restart": payload = '{"signal": "restart"}'
    elif power == "kill": payload = '{"signal": "kill"}'
    else: return "invalid_power"

    response = requests.request('POST', url, data=payload, headers=headers)
    print(response.text)
    return response.text


#
#   Send Command to server BACKEND
#


async def sendcmd(ctx, servername, cmd):
    ptero_panel = "panel.moonball.io" #Put your Ptero Panel's URL here

    server_guide = { 'proxy' : 'fe5a4fe1',  'auth':'e91b165c', 'lobby':'d0f6701c', 'survival':'5d0ac930',   #Change this part, Add your server name and the ptero identifier (example in https://panel.moonball.io/server/5426b68e "5426b68e" is the ID)
                     'skyblock':'3a0eaf97',  'duels':'6e5ed2ac',  'bedwars':'edeeff53',  'bot':'5426b68e'}
    
    
    url = f'https://{ptero_panel}/api/client/servers/{server_guide[servername]}/command'
    print(url)
    headers = {"Authorization": f"Bearer {ptero_apikey}", "Accept": "application/json", "Content-Type": "application/json"}
    payload = json.dumps({"command": f'{cmd}'})


    try: 
        response = requests.request('POST', url, data=payload, headers=headers)
        return "done"
    except:
        ctx.send("Invalid Request")
    print(response.text)


client.run('OTQ4OTExNDM3NzM1MTM3MzIw.YiCspA.BTMQBCUiklTDhC70-aBUYMf8bow')