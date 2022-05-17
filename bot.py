# Made by RajDave69
#
# Contacts -
#   RajDave69 -
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


import discord, requests, random, json, sqlite3, os, aiohttp, io
from discord.ext import commands  # Imports required Modules
from mcstatus import MinecraftServer
from dotenv import load_dotenv
from pathlib import Path


intents = discord.Intents.all()
intents.members = True
dotenv_path = Path('data/.env')
load_dotenv(dotenv_path=dotenv_path)

#
# Assigning Global Variables
#

bot_version = "Beta 0.4.0"              # Bot Version
prefix = "+"                            # Bot Prefix
ptero_apikey = os.getenv("PTERO_KEY")   # Getting Pterodactyl API Key
serv_ips = {'proxy': '192.186.100.60:25565', 'limbo': '192.168.100.60:25566', 'auth': '192.168.100.60:25567',
            'lobby': '192.168.100.60:25568', 'survival': '192.168.100.80:25569', 'bedwars': '192.168.100.80:25570',
            'duels': '192.168.100.60:25571', 'skyblock': '192.168.100.70:25572', 'prison': '192.168.100.60:25573',
            'parkour': '192.168.100.60:25574'}  # Put your Pterodactyl server IPs here


# Embed related variables
embed_footer = f"Moonball Bot • {bot_version}"  # Embed footer
embed_color = 0x1a1aff                          # Embed Color
embed_header = "Moonball Network"               # Header/Author used in embeds
embed_icon = "https://media.discordapp.net/attachments/951055432833695767/972792440572493884/logo-circle.png"
# staff_ids = [837584356988944396, 493852865907916800, 448079898515472385, 744835948558286899, 865232500744519680,
#              891307274935607306, 787144674422423563]

client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=intents,
                      help_command=None, case_insensitive=True)  # Setting prefix


@client.event
async def on_ready():  # Stuff the bot does when it starts
    await client.change_presence(activity=discord.Game(f'on the Moonball Network'))  # Set Presence
    # DiscordComponents(client, change_discord_methods=True)
    global guild, general_channel, suggestion_channel, log_channel, embed_log, cmd_channel
    guild = client.get_guild(894902529039687720)  # Server Settings > Widget > Copy Server ID
    general_channel = guild.get_channel(960196760565841941)  # Put your welcome announcements channel id
    suggestion_channel = guild.get_channel(960203053103972403)  # Put your suggestions channel's channel ID here
    log_channel = guild.get_channel(974324304470761482)  # Put your log channel's channel ID here
    embed_log = guild.get_channel(960204173989789736)  # Put your embed log channel's channel ID here
    cmd_channel = 960196816605950042  # Put your command channel id

    print("Connected to Discord!")  # Print this when the bot starts


#
#   On Message
#


@client.event
async def on_message(ctx):  # On message, Checks every message for...
    if ctx.author.bot: return  # checks if author is a bot.
    else:
        if " ip " in f" {ctx.content.lower()} ": await ip_embed(ctx)  # On word IP send ip embed
        elif " version " in f" {ctx.content.lower()} ": await version_embed(ctx)  # On word "version" send the version embed
        elif client.user in ctx.mentions:  # Replies to when the Bot in @mentioned
            await ctx.reply(f"Hello! my prefix is `{prefix}`. Use `{prefix}help` to view available commands.",delete_after=10.0)
            await logger("h", f"Sent Mention message to {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent mention-message to message of {ctx.author.name}#{ctx.author.discriminator}")

        elif " down " in f" {ctx.content.lower()} " or " up " in f" {ctx.content.lower()} " or " on " in f" {ctx.content.lower()} " or " off " in f" {ctx.content.lower()} ":
            if " proxy " in f" {ctx.content.lower()} ": await serverstatus(ctx, "proxy")
            elif " limbo " in f" {ctx.content.lower()} ": await serverstatus(ctx, "limbo")
            elif " auth " in f" {ctx.content.lower()} ": await serverstatus(ctx, "auth")
            elif " lobby " in f" {ctx.content.lower()} ": await serverstatus(ctx, "lobby")
            elif " survival " in f" {ctx.content.lower()} ": await serverstatus(ctx, "survival")
            elif " bedwars " in f" {ctx.content.lower()} ": await serverstatus(ctx, "bedwars")
            elif " duels " in f" {ctx.content.lower()} ": await serverstatus(ctx, "duels")
            elif " skyblock " in f" {ctx.content.lower()} ": await serverstatus(ctx, "skyblock")
            elif " prison " in f" {ctx.content.lower()} ": await serverstatus(ctx, "prison")
            elif " parkour " in f" {ctx.content.lower()} ": await serverstatus(ctx, "parkour")

        await client.process_commands(ctx)


#
#
#   Info Category
#
#

@client.command(aliases=["players"])
async def playercount(ctx, st_server):
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was used in a valid channel
    if st_server.lower() == "proxy":
        ctx.send("Playercount for Proxy is not available.")
    elif not st_server.lower() in ["limbo", "auth", "lobby", "survival", "bedwars", "duels", "skyblock", "prison", "parkour"]:
        return await ctx.reply(f"`{st_server.capitalize()}` is not a valid server. `{prefix}help playerlist` to learn more!")
    players = MinecraftServer.lookup(serv_ips.get(st_server)).query().players.names
    playerCount = MinecraftServer.lookup(serv_ips.get(st_server)).query().players.online
    pc_embed = discord.Embed(title=f"Player List", description=f"Online player list for the server {st_server.capitalize()}.\n Requested by {ctx.author.name}#{ctx.author.discriminator}", color=embed_color, url="https://moonball.io")
    pc_embed.set_author(name=embed_header, icon_url=embed_icon)
    pc_embed.add_field(name="Player Count", value=playerCount, inline=False)
    if playerCount != 0:
        pc_embed.add_field(name="Players", value='\n'.join(players), inline=False)
    await ctx.reply(embed=pc_embed)
    await logger("i", f"{ctx.author.name}#{ctx.author.discriminator} used Player List Command for server {st_server.capitalize()}", "info", f"{ctx.author.name}#{ctx.author.discriminator} used Player-Count Command for server {st_server.capitalize()}")


@client.command(aliases=['bedrock', 'java'])  # The IP command
async def ip(ctx): await ip_embed(ctx)

@client.command()
async def version(ctx): await version_embed(ctx)

@client.command(aliases=['memory', 'mem', 'cpu', 'ram', 'lag', 'ping'])  # Bot Stats Command
async def stats(ctx):
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    placeholder = await status("bot")
    # Stats Embed
    stats_embed = discord.Embed(title='System Resource Usage', description='See CPU and memory usage of the system.', url="https://moonball.io", color=embed_color).set_footer(text=embed_footer)
    stats_embed.set_author(name=embed_header,icon_url=embed_icon)
    stats_embed.add_field(name='<:latency_bot:951055641307381770> Latency', value=f'{round(client.latency * 1000)}ms',inline=False)
    stats_embed.add_field(name='<:cpu_bot:951055641395478568> CPU Usage', value=f'{placeholder["cpuUsage"]}%', inline=False)
    stats_embed.add_field(name='<:ram_bot:951055641332563988> Memory Usage', value=f'{placeholder["memUsage"]}', inline=False)
    stats_embed.add_field(name='<:uptime_bot:951055640967675945> Uptime', value=f'{placeholder["uptime"]}', inline=False)
    await ctx.reply(embed=stats_embed)
    await logger("i", f'Sent bot Stats to message of {ctx.author.name}#{ctx.author.discriminator}', "info", f"Sent Stats embed to message of {ctx.author.name}#{ctx.author.discriminator}")



# This part is making aliases for each server's status. Just copy-paste of code, but with server-name and IP changed
@client.command(aliases=['proxy', 'velocity'])  # Status cmd for proxy
async def statusproxy(ctx): await serverstatus(ctx, "proxy")

@client.command(aliases=['limbo'])  # Status cmd for limbo
async def statuslimbo(ctx): await serverstatus(ctx, "limbo")

@client.command(aliases=['auth', 'authserver'])  # Status cmd for auth
async def statusauth(ctx): await serverstatus(ctx, "auth")

@client.command(aliases=['lobby', 'hub'])  # Status cmd for lobby
async def statuslobby(ctx): await serverstatus(ctx, "lobby")

@client.command(aliases=['survival'])  # Status cmd for survival
async def statussurvival(ctx): await serverstatus(ctx, "survival")

@client.command(aliases=['bedwars', 'bedwar', 'bw'])  # Status cmd for Bedwars
async def statusbedwars(ctx): await serverstatus(ctx, "bedwars")

@client.command(aliases=['duels', 'duel'])  # Status cmd for duels
async def statusduels(ctx): await serverstatus(ctx, "duels")

@client.command(aliases=['skyblock'])  # Status cmd for Skyblock
async def statusskyblock(ctx): await serverstatus(ctx, "skyblock")

@client.command(aliases=['parkour'])  # Status cmd for parkour
async def statusparkour(ctx): await serverstatus(ctx, "parkour")

@client.command(aliases=['prison'])  # Status cmd for parkour
async def statusprison(ctx): await serverstatus(ctx, "prison")



#
#
#   Other Category
#
#


@client.event  # Welcome Announcement
async def on_member_join(member):
    # The embed for Welcome Announcements
    welc_embed = discord.Embed(title=f'Welcome to the Discord Server!', url="https://moonball.io", color=embed_color)
    welc_embed.add_field(name="Moonball Network",value=f"<a:malconfetti:910127223791554570> Welcome {member.mention} to the Server! <a:malconfetti:910127223791554570>\n<a:Read_Rules:910128684751544330> Please check out the Server Rules here <#960196761656385546> <a:Read_Rules:910128684751544330>\n <a:hypelove:901476784204288070> Take your Self Roles at <#960196767251570749> <a:hypelove:901476784204288070>\n <:02cool:910128856550244352> Head over to <#960196776579719278> to talk with others! <:02cool:910128856550244352> \n<a:Hearts:952919562846875650> Server info and IP can be found here <#960212885332705290> <a:Hearts:952919562846875650>",inline=True)
    welc_embed.set_image(url="https://media.discordapp.net/attachments/896348336972496936/952940944175554590/ezgif-1-e6eb713fa2.gif")
    welc_embed.set_footer(text=embed_footer)
    await general_channel.send(embed=welc_embed)
    # role = discord.utils.get(member.server.roles, id="960196710766895134")
    # await client.add_roles(member, role)
    print(f"Other : Sent Welcome Embed {member.name}#{member.discriminator}")  # This part does not work.
    await log_channel.send(f'**Other** : Sent Welcome Embed to {member.name}#{member.discriminator}')  # Logs to Log channel



@client.command()
async def shop(ctx):
    if await checkperm(ctx, 0): return
    await ctx.send("Visit our shop here!- \nhttps://shop.moonball.io")
    await logger("i", f"Sent Shop link to message of {ctx.author.name}#{ctx.author.discriminator}", "info", f"Sent Shop link to message of {ctx.author.name}#{ctx.author.discriminator}")


@client.command()
async def opensource(ctx):
    if await checkperm(ctx, 0): return
    await checkcommandchannel(ctx)
    await ctx.reply(f"This Discord Bot is opensource and made with discord.py.\nIf you would like to check out the source code, Visit the GitHub Repo here - https://moonball.io/opensource")
    await logger("i", f"Sent Bot GitHub URL to message of {ctx.author.name}#{ctx.author.discriminator}", "info", f"Sent Bot GitHub URL to message of {ctx.author.name}#{ctx.author.discriminator}")


@client.command()
async def botversion(ctx):
    if await checkperm(ctx, 0): return
    await checkcommandchannel(ctx)
    ctx.reply(f"I am currently on Version `{version}`!")
    await logger("i", f"Sent Bot Version to message of {ctx.author.name}#{ctx.author.discriminator}", "info", f"Sent Bot Version to message of {ctx.author.name}#{ctx.author.discriminator}")


@client.command()
async def invite(ctx):
    if await checkperm(ctx, 0): return
    await checkcommandchannel(ctx)
    await ctx.reply("To invite me to your server, Click on the link below\nhttps://moonball.io/bot")
    await logger("i", f"Sent Bot invite URL to message of {ctx.author.name}#{ctx.author.discriminator}", "info", f"Sent Bot invite URL to message of {ctx.author.name}#{ctx.author.discriminator}")


@client.command()
async def shard(ctx):
    if await checkperm(ctx, 0): return
    await checkcommandchannel(ctx)
    await ctx.reply(f"I am currently on Shard `{shard}`!")
    await logger("i", f"Sent Bot Shard to message of {ctx.author.name}#{ctx.author.discriminator}", "info", f"Sent Bot Shard to message of {ctx.author.name}#{ctx.author.discriminator}")


@client.command()
async def socials(ctx):
    if await checkperm(ctx, 0): return
    await checkcommandchannel(ctx)
    embed = discord.Embed(title="Social Media", description="Here are the links to our Socials!", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon).set_thumbnail(url=embed_icon)
    embed.add_field(name="<:discordlogo:972789364981661716> Discord" , value="https://moonball.io/discord", inline=True)
    embed.add_field(name="<:twitterlogo:972789038727708712> Twitter", value="https://moonball.io/twitter", inline=False)
    embed.add_field(name="<:youtubelogo:972789038677385226> YouTube", value="https://moonball.io/youtube", inline=False)
    embed.add_field(name="<:instagramlogo:972789038572527657> Instagram", value="https://moonball.io/instagram", inline=False)
    embed.add_field(name="<:redditlogo:972789038731886603> Reddit", value="https://moonball.io/reddit", inline=False)
    await ctx.reply(embed=embed)
    await logger("i", f"Sent Bot Socials to message of {ctx.author.name}#{ctx.author.discriminator}", "info", f"Sent Bot Socials to message of {ctx.author.name}#{ctx.author.discriminator}")

#
#
#   Help Category
#
#


@client.group(pass_context=True, aliases=['info', 'help'], invoke_without_command=True)  # Help Command
async def bothelp(ctx):
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    # Base Help command embed
    bothelp = discord.Embed(title="Help Command", url="https://moonball.io", description=f"Use `{prefix}help <module>` to learn more about that specific module\nModules Include - ```ini\n[ping, status, suggestion, ip/version, embed, poll, coinflip, admin]```",color=embed_color)
    bothelp.set_author(name=embed_header, icon_url=embed_icon)
    bothelp.add_field(name="Prefix", value=f"The prefix is `{prefix}`", inline=True)
    bothelp.add_field(name="Bot Version", value=f"{bot_version}", inline=True)
    bothelp.add_field(name="Bot Dev", value="<@837584356988944396>", inline=True)
    bothelp.add_field(name="Info", value=f"Get info about the Server/Bot with this category of commands.\n Commands include ```ini\n[ip, version, ping, status]```",inline=True)
    bothelp.add_field(name="Help", value=f"Commands assisting the usage of this Discord Bot or our MC Server can be found in this category. Commands include ```ini\n[help, error_message, @ping_message]```",inline=False)
    bothelp.add_field(name="Fun", value=f"The commands which enrich the user experience of being in this Discord Server.\n Commands include ```ini\n[suggest, embed, coinflip, poll, reminder(Coming-Soon)]``` \n",inline=False)
    bothelp.add_field(name="Admin", value=f"Functions and Commands made to modify details about the bot/server are within this category. Only server Staff can access/use them. Commands include ```ini\n[changeServerState\css, resetcounter]```",inline=False)
    bothelp.set_footer(text=embed_footer)
    await ctx.reply(embed=bothelp)
    await logger("h", f"Sent Base Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent Base Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")


#
#  Bot Help for Info Category
#


@bothelp.command(aliases=['ping', 'stats', 'mem', 'stat', 'cpu'])  # Sub-command for help.
async def ping_bothelp(ctx):
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    embed = discord.Embed(title="Help Command - Ping", url="https://moonball.io",description="This is the Help category for the `ping` command.", color=embed_color)
    embed.set_author(name=embed_header, icon_url=embed_icon)
    embed.add_field(name="Description", value="The `ping` Command sends information relating to the bot's status.  ",inline=False)
    embed.add_field(name="Features", value="Can be used to check Latency, CPU Usage, RAM Usage and Uptime.",inline=False)
    embed.add_field(name="Version introduced in", value="\>0.05", inline=False)
    embed.add_field(name="Aliases", value="```ini\n[mem, memory, cpu, ram, lag, ping, stats]```", inline=False)
    embed.set_footer(text=embed_footer)
    await ctx.reply(embed=embed)
    await logger("h", f"Sent Ping-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent Ping-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")


@bothelp.command(aliases=['status'])  # Sub-command for help.
async def status_bothelp(ctx):
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    embed = discord.Embed(title="Help Command - Status", url="https://moonball.io",description="This is the Help category for the `status` command.", color=embed_color)
    embed.set_author(name=embed_header, icon_url=embed_icon)
    embed.add_field(name="Description",value=f"The `status` command sends info about a specific mentioned server. It can be triggered in 2 ways.\n►**Auto Trigger** - When user says 'up'/'down' and (servername) in the same message.\n►**Manual Trigger** - Using the command `{prefix}servername`",inline=False)
    embed.add_field(name="Features",value="Can be used to check the Status, Players Online, CPU/RAM/Disk and Uptime information for a specific server",inline=False)
    embed.add_field(name="Version introduced in", value="\>0.1", inline=False)
    embed.add_field(name="Aliases",value=f"```ini\n[Proxy/Velocity, Limbo, Auth/AuthServer, Lobby/Hub, Survival, Skyblock, Bedwars/Bedwar/bw, Duels/Duel, Parkour]```",inline=False)
    embed.set_footer(text=embed_footer)
    await ctx.reply(embed=embed)
    await logger("h", f"Sent Status-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent Status-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")

@bothelp.command(aliases=['ip', 'version'])  # Sub-command for help.
async def ip_bothelp(ctx):
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    embed = discord.Embed(title="Help Command - IP", url="https://moonball.io",description="This is the Help category for the `IP`/`version` command.", color=embed_color)
    embed.set_author(name=embed_header, icon_url=embed_icon)
    embed.add_field(name="Description",value=f"The `IP`/`version` Command sends a nice-looking embed to the user.\nCan be triggered in 2 ways\n►**Automatic Trigger** - Any message with the word `ip` or `version` in it will trigger the embed\n**Manual Trigger** - Doing `+ip` or `+version` will also send the embed",inline=False)
    embed.add_field(name="Features",value="Posts the IPs/Versions of both Java and Bedrock in a convenient Embed. Reducing the manual work to post the ip message again and again.",inline=False)
    embed.add_field(name="Version introduced in", value="0.01", inline=False)
    embed.add_field(name="Aliases", value="```ini\n[ip, java, bedrock / version]```", inline=False)
    embed.set_footer(text=embed_footer)
    await ctx.reply(embed=embed)
    await logger("h", f"Sent IP-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent IP-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")

@bothelp.command(aliases=['playerlist', "players"])  # Sub-command for help.
async def playerlist_bothelp(ctx):
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    embed = discord.Embed(title="Help Command - Playerlist", url="https://moonball.io",description="This is the Help category for the `playerlist` command.", color=embed_color)
    embed.set_author(name=embed_header, icon_url=embed_icon)
    embed.add_field(name="Description",value=f"The `playerlist` command sends a nice-looking embed to the user.\nSyntax - `{prefix}players [servername]`",inline=False)
    embed.add_field(name="Version introduced in", value="0.3.9", inline=False)
    embed.add_field(name="Valid Servers", value="```ini\n[limbo, auth, lobby, survival, skyblock, duels, bedwars, parkour]```",inline=False)
    embed.add_field(name="Aliases", value="```ini\n[playerlist, players]```", inline=False)
    embed.set_footer(text=embed_footer)
    await ctx.reply(embed=embed)

#
#   Bot Help for Fun category
#


@bothelp.command(aliases=['suggest', 'suggestion'])  # Sub-command for help.
async def suggest_bothelp(ctx):
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    embed = discord.Embed(title="Help Command - Suggestion", url="https://moonball.io",description="This is the Help category for the `Suggestion` command.", color=embed_color)
    embed.set_author(name=embed_header, icon_url=embed_icon)
    embed.add_field(name="Description",value=f"The `Suggest` Command sends a user's suggestion to the <#{suggestion_channel}> channel. Reacts to it with <:tick_bot:953561636566863903> and <:cross_bot:953561649254649866> so that it can be voted on and implemented! You can also add a image (jpg, png or jpeg) into the suggestion.\n Syntax - ```ini\n{prefix}suggest [Line 1 nl line 2] | [https://image.link.png]```",inline=False)
    embed.add_field(name="Features",value="It posts your suggestion to the official suggestion channel of the server. Say `nl` within the embed to put the proceeding text in the next line.",inline=False)
    embed.add_field(name="Version introduced in", value="0.2", inline=False)
    embed.add_field(name="Aliases", value="```ini\n[suggest, suggestion, createsuggestion]```", inline=False)
    embed.set_footer(text=embed_footer)
    await ctx.reply(embed=embed)
    await logger("h", f"Sent Suggest-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent Suggest-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")


@bothelp.command(aliases=['embed', 'announce', 'ann'])  # Sub-command for help.
async def embed_bothelp(ctx):
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    embed = discord.Embed(title="Help Command - Embed", url="https://moonball.io",description="This is the Help category for the `Embed` command.", color=embed_color)
    embed.set_author(name=embed_header, icon_url=embed_icon)
    embed.add_field(name="Description",value=f"The `Embed` Command creates a nice embed with a simple syntax ```ini\n{prefix}embed [The Embed Title] | [The Embed Content]```\n Use `|` to separate all the 2 arguments.",inline=False)
    embed.add_field(name="Features",value="Posts a Embed with the user's liking's content to any channel Say `nl` within the embed to put the proceeding text in the next line.",inline=False)
    embed.add_field(name="Version introduced in", value="0.05", inline=False)
    embed.add_field(name="Aliases", value="```ini\n[ann, announce, embed]```", inline=False)
    embed.set_footer(text=embed_footer)
    await ctx.reply(embed=embed)
    await logger("h", f"Sent Embed-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent Embed-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")


@bothelp.command(aliases=['coinflip', 'head', 'tail'])  # Sub-command for help.
async def Coinflip_bothelp(ctx):
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    embed = discord.Embed(title="Help Command - Coin Flip", url="https://moonball.io",description="This is the Help category for the `Coin Flip` command.", color=embed_color)
    embed.set_author(name=embed_header, icon_url=embed_icon)
    embed.add_field(name="Description", value=f"The `Coin Flip` Command Picks either heads or tails randomlly ",inline=False)
    embed.add_field(name="Features",value="Picks either heads or tails randomly and sends the response with a nice-looking heads/tails picture.",inline=False)
    embed.add_field(name="Version introduced in", value="0.2.3", inline=False)
    embed.add_field(name="Aliases", value="```ini\n[head, tail, CoinFlip, FlipCoin]```", inline=False)
    embed.set_footer(text=embed_footer)
    await ctx.reply(embed=embed)
    await logger("h", f"Sent CoinFlip-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent CoinFlip-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")

@bothelp.command(aliases=['poll', 'cpoll', 'spoll', 'createpoll', 'sendpoll'])  # Sub-command for help.
async def poll_bothelp(ctx):
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    embed = discord.Embed(title="Help Command - Poll", url="https://moonball.io",description="This is the Help category for the `Poll` command.", color=embed_color)
    embed.set_author(name=embed_header, icon_url=embed_icon)
    embed.add_field(name="Description", value=f"The `Poll` Command Sends a multiple option poll with upto 4 options",inline=False)
    embed.add_field(name="Features",value=f"The Poll Command sends a poll with the user's input with upto 4 reactions/options. It has a simple syntax - \n```ini\n{prefix}poll [number of options] | [Your poll Text here]```\nUse `|` to seperate the 2 arguments. Say `nl` within the poll to put the proceeding text in the next line.",inline=False)
    embed.add_field(name="Version introduced in", value="0.2.3", inline=False)
    embed.add_field(name="Aliases", value="```ini\n[cpoll, spoll, createpoll, sendpoll]```", inline=False)
    embed.set_footer(text=embed_footer)
    await ctx.reply(embed=embed)
    await logger("h", f"Sent Poll-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent Poll-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")


#
#   Admin Help
#


@client.group(pass_context=True, invoke_without_command=True, aliases=['adminhelp'])
async def admin(ctx):
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    # Base Admin-Help command embed
    bothelp = discord.Embed(title="Admin Command", url="https://moonball.io",description=f"Use `{prefix}admin <module>` to execute the command\nModules Include - ```ini\n[changeServerState/css, resetcounter, helpcmd, helppw]```",color=embed_color)
    bothelp.set_author(name=embed_header, icon_url=embed_icon)
    bothelp.add_field(name="Prefix", value=f"The prefix is `{prefix}`", inline=True)
    bothelp.add_field(name="Bot Version", value=f"{bot_version}", inline=True)
    bothelp.add_field(name="Bot Dev", value="<@837584356988944396>", inline=True)
    bothelp.add_field(name="Change Server State",value=f"Changes the state of the mentioned server, Can Start/Stop/Restart and Kill any server.\nTo learn more, do `{prefix}admin css`",inline=True)
    bothelp.add_field(name="Send Command",value=f"Sends a command to any server mentioned with a simple syntax.\nTo learn more, do `{prefix}admin helpcmd`",inline=False)
    bothelp.add_field(name="Add/Take Money",value=f"Give or Take money to/from a mentioned user (survival).\nTo learn more, do `{prefix}admin helptake/helpgive`",inline=False)
    bothelp.add_field(name="Change Password",value=f"Changes the password of the user mentioned, right from Discord.\nTo learn more, do `{prefix}admin helppw`",inline=False)
    bothelp.add_field(name="Permission Level", value=f"The permission level system allows easy management of giving specific command permissions to users.\n `{prefix}admin permlvl` to learn more! ", inline=True)
    bothelp.add_field(name="Reset Command Counter",value=f"Resets a command counter from the 5 options with a single command.\n To learn more do `{prefix}admin resetcounter`",inline=False)
    bothelp.set_footer(text=embed_footer)
    await ctx.reply(embed=bothelp)
    await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")

@admin.group(aliases=['resetcounter'])  # Help reset counter
async def resetcounter_admin(ctx):
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    # Base Admin-Help command embed
    bothelp = discord.Embed(title="Admin Help - Reset Counter", url="https://moonball.io",description=f"Use `{prefix}admin [suffix]` to execute the command.\nResets a specific command counter",color=embed_color)
    bothelp.set_author(name=embed_header, icon_url=embed_icon)
    bothelp.add_field(name="Description", value=f"This command resets one of the 5 total command use counters`", inline=True)
    bothelp.add_field(name="Counter Names", value=f"```ini\n[suggestion, help, info, fun, admin]```", inline=True)
    bothelp.add_field(name="Valid suffixes", value=f"```ini\n[s, h, i, f, a]```", inline=True)
    bothelp.set_footer(text=embed_footer)
    await ctx.reply(embed=bothelp)
    await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")

@admin.group(aliases=['css', 'changeserverstate'])
async def changeserverpower_admin(ctx):  # Help changeserverstate
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    # Base Admin-Help command embed
    bothelp = discord.Embed(title="Admin Help - Change Server State", url="https://moonball.io",description=f"Use `{prefix}admin [state] [servername]` to execute the command.\nChanges the status of a specific mentioned server ",color=embed_color)
    bothelp.set_author(name=embed_header, icon_url=embed_icon)
    bothelp.add_field(name="Description", value=f"This command changes the power/state of any server", inline=True)
    bothelp.add_field(name="Features",value=f"Start/Stop/Restart or Kill a server just with one single command here on Discord, using a conveniently easy command!",inline=False)
    bothelp.add_field(name="Valid States", value=f"```ini\n[start, stop, restart, kill]```", inline=False)
    bothelp.add_field(name="Valid Servers", value="```ini\n[proxy, limbo, auth, lobby, survival, skyblock, duels, bedwars, parkour]```",inline=False)
    bothelp.set_footer(text=embed_footer)
    await ctx.reply(embed=bothelp)
    await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}") # Logs to Log channel

@admin.group(aliases=['helpcmd'])
async def changecmd_admin(ctx):  # Help sendcmd
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    # Base Admin-Help command embed
    bothelp = discord.Embed(title="Admin Help - Send Command", url="https://moonball.io",description=f"Use `{prefix}admin cmd [server] | [command]` to execute the command.\nSends a command to the mentioned server ",color=embed_color)
    bothelp.set_author(name=embed_header, icon_url=embed_icon)
    bothelp.add_field(name="Description", value=f"This command can send a command to the mentioned server", inline=True)
    bothelp.add_field(name="Features",value=f"Send a in-game command to any mentioned server here on Discord, using a conveniently easy command and easy syntax!",inline=False)
    bothelp.add_field(name="Valid Servers", value="```ini\n[proxy, limbo, auth, lobby, survival, skyblock, duels, bedwars, parkour]```",inline=False)
    bothelp.add_field(name="Syntax", value=f"```ini\n{prefix}admin cmd server | command here!```", inline=False)
    bothelp.set_footer(text=embed_footer)
    await ctx.reply(embed=bothelp)
    await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}") # Logs to Log channel

@admin.group(aliases=['helppw'])
async def password_admin(ctx):  # Help password
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    # Base Admin-Help command embed
    bothelp = discord.Embed(title="Admin Help - Change Password", url="https://moonball.io",description=f"Use `{prefix}admin pw [username] [new-password]` to execute the command.\nChanges the password of the mentioned user ",color=embed_color)
    bothelp.set_author(name=embed_header, icon_url=embed_icon)
    bothelp.add_field(name="Description", value=f"This command can change the password of a user", inline=True)
    bothelp.add_field(name="Features",value=f"Change the password of any mentioned user with a simple and easy command, here from Discord.",inline=False)
    bothelp.add_field(name="Syntax", value=f"```ini\n{prefix}admin pw Username NewPassword```", inline=False)
    bothelp.set_footer(text=embed_footer)
    await ctx.reply(embed=bothelp)
    await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}") # Logs to Log channel

@admin.group(aliases=['helpgive', 'helptake'])
async def helptg_admin(ctx):  # Help password
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    # Base Admin-Help command embed
    bothelp = discord.Embed(title="Admin Help - Give/Take Money", url="https://moonball.io", description=f"Use `{prefix}admin give/take [username] [money]` to execute the command.\nGive or take money from a user", color=embed_color)
    bothelp.set_author(name=embed_header, icon_url=embed_icon)
    bothelp.add_field(name="Description", value=f"This command can give or take money from a user", inline=True)
    bothelp.add_field(name="Features",value=f"Gives or takes money from a specific user.",inline=False)
    bothelp.add_field(name="Syntax", value=f"```ini\n{prefix}admin give/take Username Money```", inline=False)
    bothelp.set_footer(text=embed_footer)
    await ctx.reply(embed=bothelp)
    await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}") # Logs to Log channel

@admin.group(aliases=['permlvl'])
async def permlevel_admin(ctx):  # Help password
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    # Base Admin-Help command embed
    bothelp = discord.Embed(title="Admin Help - Permission Level", url="https://moonball.io", description=f"For permission level hierarchy list, do `{prefix}admin permlist`\n Use `{prefix}admin setlvl [@mention] [level]` or `{prefix}admin getlvl [@mention]` to execute the command.\nSet/Get the permission level of a user", color=embed_color)
    bothelp.add_field(name="Description", value=f"This command can set or get the permission level of a user. Permission levels are used to give specific command access to different levels of permissions a user can have. Permissions vary between `-1` and `5`, -1 disabling access to all commands and 5 giving access to all.", inline=True)
    bothelp.add_field(name="Features",value=f"Manage usage of commands easilly with one command giving a permission level to a user",inline=False)
    bothelp.add_field(name="Syntax", value=f"```ini\n{prefix}admin setlvl [@mention] [level]\n{prefix}admin getlvl [@mention]```", inline=False)
    bothelp.set_footer(text=embed_footer)
    bothelp.set_author(name=embed_header, icon_url=embed_icon)
    await ctx.reply(embed=bothelp)

@admin.group(aliases=['permlist'])
async def permlist_admin(ctx):  # Help password
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    # Base Admin-Help command embed
    bothelp = discord.Embed(title="Admin Help - Permission Level", url="https://moonball.io", description=f"This command gives the permission list and what commands it lets you use.", color=embed_color)
    bothelp.add_field(name="5 | Developer", value=f"Gives access to all commands", inline=True)
    bothelp.add_field(name="4 | Owner", value=f"Gives access to all commands except\n►Bot Backend/Database", inline=False)
    bothelp.add_field(name="3 | Admin", value=f"Gives access to all commands except\n►affecting Permission Levels\n►Bot Backend/Database", inline=False)
    bothelp.add_field(name="2 | Moderator", value=f"Gives access to all commands except\n►►affecting Permission Levels\n►Bot Backend/Database\n►Kill/Stop Servers\n►Give/Take Money", inline=False)
    bothelp.add_field(name="1 | Helper", value=f"Gives access to\n►Execute command in any channel", inline=False)
    bothelp.add_field(name="0 | User", value=f"Gives access to normal user commands", inline=False)
    bothelp.add_field(name="-1 | Disabled", value=f"Gives access to no command", inline=False)
    bothelp.set_footer(text=embed_footer)
    bothelp.set_author(name=embed_header, icon_url=embed_icon)
    await ctx.reply(embed=bothelp)
#
#
#   Fun Category
#
#


@client.command(aliases=['announce, ann'])  # The announcement Embed creator
async def embed(ctx, *data):
    if await checkperm(ctx, 0): return
    try:
        data = " ".join(data).split(' | ')  # Input Splitter
        a = data[1].replace(" nl ", " \n")
        syntax_error = False
        if len(data) != 2:  # verifying complete syntax
            syntax_error = True
            await ctx.send(f"The syntax is as follows: `{prefix}embed <title> | <description>`")
            await ctx.add_reaction("<:cross_bot:953561649254649866>")
        if syntax_error: return
    except:
        await ctx.send(f"Could not send the Embed. An error occurred. Re-Check the syntax or read the embed help page with `{prefix}help embed`")
        return
        # Embed Builder
    announcement = discord.Embed(title=f"Embed by {ctx.author.name}#{ctx.author.discriminator}",url="https://moonball.io", color=embed_color)
    announcement.add_field(name=f"{data[0]}", value=f"{a}", inline=True)
    announcement.set_footer(text=embed_footer)
    try:  # Try to send the embed
        await ctx.send(embed=announcement)
        await embed_log.send(embed=announcement)
        await ctx.message.delete()  # delete original
    except: await ctx.send(f"Could not send the Embed. An error occurred. Re-Check the syntax or read the embed help page with `{prefix}help embed`"); return
    await logger("f", f"Sent Embed (Embed Creator) to message of {ctx.author.name}#{ctx.author.discriminator}", "fun", f"Sent Embed (Embed Creator) to message of {ctx.author.name}#{ctx.author.discriminator}")  # Logs to Log channel



# @client.command(aliases=['8ball'])  # The 8ball Embed creator
# async def eightball(ctx, *data):
#     try:
#         data = " ".join(data).split(' | ')  # Input Splitter
#         a = data[1].replace(" nl ", " \n")
#         syntax_error = False
#         if len(data) != 2:  # verifying complete syntax
#             syntax_error = True
#             await ctx.send(f"The syntax is as follows: `{prefix}eightball <question> | <answer>`")
#             await ctx.add_reaction("<:cross_bot:953561649254649866>")
#         if syntax_error: return
#     except:
#         await ctx.send("Could not send the Embed. An error occurred. Re-Check the syntax or read the embed help page with `+help eightball`")
#         return
#         Embed Builder
#     announcement = discord.Embed(title=f"8ball by {ctx.author.name}#{ctx.author.discriminator}",url="https://moonball.io", color=embed_color)
#     announcement.add_field(name=f"{data[0]}", value=f"{a}", inline=True)
    # announcement.set_footer(text=embed_footer)
    # try:  # Try to send the embed
    #     await ctx.send(embed=announcement)
    #     await embed_log.send(embed=announcement)
    #     await ctx.message.delete()  # delete original
    # except: await ctx.send("Could not send the Embed. An error occurred. Re-Check the syntax or read the embed help page with `+help eightball`"); return
    # await logger("f", f"Sent Embed (8ball) to message of {ctx.author.name}#{ctx.author.discriminator}", "fun", f"Sent Embed (8ball) to message of {ctx.author.name}#{ctx.author.discriminator}")  # Logs to Log channel



@client.command(aliases=['cpoll', 'spoll', 'createpoll', 'sendpoll'])  # Poll Command
async def poll(ctx, *data):
    if await checkperm(ctx, 0): return
    try:
        data = " ".join(data).split(' | ')  # Input Splitter
        reaction_count = int(data[0])
        content = data[1].replace(" nl ", " \n")
    except:
        await ctx.send(f"There was an error! The Syntax is perhaps incorrect. The correct Syntax is ```ini\n{prefix}poll [number of options] | [Your poll Text here]```\n For more, check out `{prefix}help poll`."); return
        # The embed
    p_embed = discord.Embed(title=f"Poll", url="https://moonball.io", color=embed_color)
    p_embed.add_field(name=f"Poll by {ctx.author.name}#{ctx.author.discriminator}", value=f"{content}", inline=True)
    p_embed.set_footer(text=f"{embed_footer}")
    if reaction_count > 4:  # Check if number of reactions is more than 4
        await ctx.send("Sorry, You can't have more than 4 options in a Poll")
        return
    elif reaction_count < 2:  # Check if number of reactions is less than 2
        await ctx.send("Sorry, You can't have less than 2 options in a Poll")
        return
    else:
        p = await ctx.send(embed=p_embed)  # Sending the Embed
        await p.add_reaction("<:1_bot:957922958502952981>")  # Adding 1 reaction
        await p.add_reaction("<:2_bot:957922954119888917>")  # Adding 2 reaction
        if int(reaction_count) == 3:
            await p.add_reaction("<:3_bot:957922953893384192>")  # Checking if number is 3, if yes add 3 reaction
        elif int(reaction_count) == 4:  # Checking of the number is 4
            await p.add_reaction("<:3_bot:957922953893384192>")  # Adding 3 reaction
            await p.add_reaction("<:4_bot:957922953381707797>")  # Adding 4 reaction
        # dm = await ctx.member.create_dm()
        # await dm.send("hi this is a dear message")
        # await ctx.reply("Your Poll was sent!")
        await logger("f", f"Sent Poll embed to message of {ctx.author.name}#{ctx.author.discriminator}", "fun", f"Sent Poll embed to message of {ctx.author.name}#{ctx.author.discriminator}")  # Logs to Log channel



@client.command(aliases=['head', 'tail', 'flip', 'flipcoin'])
async def coinflip(ctx):  # Coin Flip Command
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    determine_flip = [1, 0]  # The options
    if random.choice(determine_flip) == 1: value = "Heads"
    else: value = "Tails"
    embed = discord.Embed(title="Coin Flip", description=f"{ctx.author.mention} Flipped a coin!, They got **{value}**",color=embed_color)
    if value == "Heads": embed.set_image(url="https://cdn.discordapp.com/attachments/951055432833695767/960211489254436935/head.png")  # Setting head image
    else: embed.set_image(url="https://cdn.discordapp.com/attachments/951055432833695767/960211488772083752/tail.png")  # Setting tails image
    embed.set_author(name=embed_header, icon_url=embed_icon)
    embed.set_footer(text=embed_footer)
    await ctx.send(embed=embed)
    await logger("f", f'Sent Coin Flip result to message of {ctx.author.name}#{ctx.author.discriminator}', "fun", f'Sent Coin Flip result to message of {ctx.author.name}#{ctx.author.discriminator}')



@client.command(aliases=['suggestion', 'createsuggestion']) # Suggest Command
async def suggest(ctx, *data):
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    data = " ".join(data).split(' | ')  # Input Splitter
    """
    if data[0] == " " or "": # Checks if the first input is empty
        await ctx.send("Please enter a suggestion!")
        return
    """
    if len(data) != 1: # Checks if there is more than one input
        if not data[1].startswith("https://") or data[1].startswith("http://"): # Checks if the second input starts with https://
            await ctx.send("0- Please enter a valid image link!")
            return
        """"
        elif not data[1].endswith(".png") or not data[1].endswith(".jpg") or not data[1].endswith(".jpeg"): # Checks if the second input ends with .png, .jpg or .jpeg
            await ctx.send("1- Please enter a valid image link!")
            return
        """
    s = data[0].replace(" nl ", " \n")  # Replacing nl with \n
            #The embed
    cat = "s"
    s_embed = discord.Embed(title=f"Suggestion", url="https://moonball.io", color=embed_color)
    s_embed.add_field(name=f"Submitted by {ctx.author.name}#{ctx.author.discriminator}", value=f"Suggestion #{countadd(cat)}\n{s}", inline=True)
    if len(data) > 1: s_embed.set_image(url=data[1])  # Setting image
    s_embed.set_footer(text=embed_footer)
    s = await suggestion_channel.send(embed=s_embed)
        #Adding reactions
    await s.add_reaction("<:tick_bot:953561636566863903>")      # Adding tick reaction
    await s.add_reaction("<:cross_bot:953561649254649866>")     # Adding cross reaction
    await embed_log.send(embed=s_embed)     # Sending it to the Logs channel
    await ctx.reply(f"Your Suggestion was sent! Check <#960203053103972403> to see how its doing!")
    print(f"Sent {ctx.author.name}'s suggestion to the suggestion channel!")



@client.command(aliases=['pfp', 'avatar'])
async def av(ctx, *, user: discord.User = None):
    if await checkperm(ctx, 0): return
    if await checkcommandchannel(ctx): return # Checks if command was executed in the Command Channel
    format = "gif"
    user = user or ctx.author
    if user.is_avatar_animated() != True:
        format = "png"
    avatar = user.avatar_url_as(format=format if format != "gif" else None)
    async with aiohttp.ClientSession() as session:
        async with session.get(str(avatar)) as resp:
            image = await resp.read()
    with io.BytesIO(image) as file:
        await ctx.reply(file=discord.File(file, f"Avatar.{format}"))
    await logger("i", f"Sent {ctx.author.name}'s avatar to message of {ctx.author.name}#{ctx.author.discriminator}", "fun", f"Sent {ctx.author.name}'s avatar to message of {ctx.author.name}#{ctx.author.discriminator}")

#
#
#   Admin Command & Logging Function Section
#
#


# Send Command to Server
@admin.command(aliases=['cmd', 'send', 'sendcmd'])
async def sendcmd_admin(ctx, *data):    # Send Command Admin Command
    if await checkperm(ctx, 4): return
    data = " ".join(data).split(' | ')  # Input Splitter
    valid_names = ["proxy", "limbo", "parkour", "auth", "lobby", "survival", "skyblock", "duels", "bedwars", "bot"]
    if data[0] not in valid_names: await ctx.send("Invalid Name"); return "invalid_name"
    if data[1] == "": await ctx.send("Invalid command to send"); return "invalid_cmd"
    try:
        p = await sendcmd(ctx, data[0], data[1])
    except:
        await ctx.reply("There was a error in sending the command")
        return
    if p != "done": return
    embed = discord.Embed(title="Admin - Send Command", url="https://moonball.io", color=embed_color)
    embed.set_author(name=embed_header, icon_url=embed_icon)
    embed.add_field(name="Operation Successful!", value=f"Successfully Sent the Command. Issued by {ctx.author.name}#{ctx.author.discriminator} \n \n**Server** - `{data[0]}` \n **Command** - `{data[1]}`",inline=False)
    embed.set_footer(text=embed_footer)
    await ctx.reply(embed=embed)
    await embed_log.send(embed=embed)  # Sending it to the Logs channel
    await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} sent a command to `{data[0]}`', "admin", f'{ctx.author.name}#{ctx.author.discriminator} sent a command to `{data[0]}\nCommand - ```ini\n{data[1]}```')


# Economy Commands
@admin.command(aliases=['takemoney', 'take', 'take_money'])
async def take_money_admin(ctx, *data):  # Take Money Admin Command
    if await checkperm(ctx, 3): return
    if len(data[0]) <= 3 or len(data[0]) >= 16: await ctx.send("Invalid Username"); return "invalid_username"
    elif not data[1].isnumeric(): await ctx.send("Invalid Amount"); return "invalid_amount"
    try:
        p = await sendcmd(ctx, "survival", f"eco take {data[0]} {data[1]}")
    except:
        await ctx.reply("There was a error in sending the command"); return
    if p != "done": return
    embed = discord.Embed(title="Admin - Take Money", url="https://moonball.io", color=embed_color)
    embed.set_author(name=embed_header, icon_url=embed_icon)
    embed.add_field(name="Operation Successful!", value=f"Successfully took {data[1]} from {data[0]} \n \n**User** - `{data[0]}` \n **Amount** - `{data[1]}`",inline=False)
    embed.set_footer(text=embed_footer)
    await ctx.reply(embed=embed)
    await embed_log.send(embed=embed)  # Sending it to the Logs channel
    await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} took ${data[1]} from {data[0]}', "admin", f'{ctx.author.name}#{ctx.author.discriminator} took ${data[1]} from {data[0]}')

@admin.command(aliases=['givemoney', 'give', 'give_money'])
async def give_money_admin(ctx, *data):  # Take Money Admin Command
    if await checkperm(ctx, 3): return
    if len(data[0]) <= 3 or len(data[0]) >= 16: await ctx.send("Invalid User Name"); return
    elif not data[1].isnumeric(): await ctx.send("Invalid Amount"); return
    try:
        p = await sendcmd(ctx, "survival", f"eco give {data[0]} {data[1]}")
    except:
        await ctx.reply("There was a error in sending the command")
        return
    if p != "done": return
    embed = discord.Embed(title="Admin - Take Money", url="https://moonball.io", color=embed_color)
    embed.set_author(name=embed_header, icon_url=embed_icon)
    embed.add_field(name="Operation Successful!", value=f"Successfully gave {data[1]} from {data[0]} \n \n**User** - `{data[0]}` \n **Amount** - `{data[1]}`",inline=False)
    embed.set_footer(text=embed_footer)
    await ctx.reply(embed=embed)
    await embed_log.send(embed=embed)  # Sending it to the Logs channel
    await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} gave ${data[1]} to {data[0]}', "admin", f'{ctx.author.name}#{ctx.author.discriminator} gave ${data[1]} to {data[0]}')



# Change User Password
@admin.command(aliases=['changepw', 'changepassword', 'pw', 'password'])
async def changepw_admin(ctx, *data):   # Change Password Command
    if await checkperm(ctx, 4): return
    if len(data[0]) <= 3 or len(data[0]) >= 16:
        await ctx.send("Invalid Username | Username must be between 3 and 16 characters")
        return "invalid_username"
    # Format = +admin changepw | username | password
    if len(data[1]) <= 5 or len(data[1]) >= 30:
        await ctx.send("Invalid Password | Password must be between 6 and 30 characters")
        return "invalid_password"
    cmd = f"authme cp {data[0]} {data[1]}"
    try:
        p = await sendcmd(ctx, "auth", cmd)
    except:
        await ctx.reply("There was a error in sending the command")
        return
    if p != "done": return
    embed = discord.Embed(title="Admin - Change Password", url="https://moonball.io", color=embed_color)
    embed.set_author(name=embed_header, icon_url=embed_icon)
    embed.add_field(name="Operation Successful!",value=f"Successfully Changed the Password. Issued by {ctx.author.name}#{ctx.author.discriminator} \n \n**Player** - `{data[0]}` \n **Password** - ||{data[1]}||",inline=False)
    embed.set_footer(text=embed_footer)
    await ctx.reply(embed=embed)
    await embed_log.send(embed=embed)  # Sending it to the Logs channel
    await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} changed the password of {data[0]}', "admin", f'{ctx.author.name}#{ctx.author.discriminator} changed the password of {data[0]}')



# Power Commands
@admin.command(aliases=['startserver', 'serverstart', 'ss', 'start'])
async def start_admin(ctx, *data):  # Start Server Command
    if await checkperm(ctx, 2): return
    data = " ".join(data).split()  # Input Splitter
    valid_names = ["proxy", "limbo", "auth", "lobby", "survival", "skyblock", "duels", "bedwars", "bot", "parkour"]
    if data[0] not in valid_names:
        await ctx.reply(f"Error : Invalid Server Name. Use `{prefix}admin css` to learn more!")
        return
    try:
        e = await serverpower(data[0], "start", ctx)
    except:
        await ctx.reply(f"There was an error. Use `{prefix}admin css` to learn more")
        return
    if e == "exception": return
    embed = discord.Embed(title="Server Power", url="https://moonball.io/", color=embed_color)
    embed.set_author(name=embed_header, icon_url=embed_icon)
    embed.add_field(name=f'Operation Successful!', value=f'Successfully Started the {data[0].capitalize()} Server!', inline=False)
    embed.set_footer(text=embed_footer)
    await ctx.reply(embed=embed)
    await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} started server {data[0]}', "admin", f'{ctx.author.name}#{ctx.author.discriminator} started server {data[0]}')

@admin.command(aliases=['stopserver', 'serverstop', 'sts', 'stop'])
async def stop_admin(ctx, *data):   # Stop Server Command
    if await checkperm(ctx, 3): return
    valid_names = ["proxy", "limbo", "auth", "lobby", "survival", "skyblock", "duels", "bedwars", "bot", "parkour"]
    if data[0] not in valid_names:
        await ctx.reply(f"Error : Invalid Server Name. Use `{prefix}admin css` to learn more!")
        return
    try:
        e = await serverpower(data[0], "stop", ctx)
    except:
        await ctx.reply(f"There was an error. Use `{prefix}admin css` to learn more")
        return
    if e == "exception": return
    embed = discord.Embed(title="Server Power", url="https://moonball.io/", color=embed_color)
    embed.set_author(name=f"{embed_header}")
    embed.add_field(name=f'Operation Successful!', value=f'Successfully Stopped the {data[0].capitalize()} Server!',inline=False)
    embed.set_footer(text=f"{embed_footer}")
    await ctx.reply(embed=embed)
    await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} stopped server {data[0]}', "admin", f'{ctx.author.name}#{ctx.author.discriminator} stopped server {data[0]}')

@admin.command(aliases=['restartserver', 'serverrestart', 'rs', 'restart'])
async def restart_admin(ctx, *data): # Restart Server Command
    if await checkperm(ctx, 2): return
    valid_names = ["proxy", "limbo", "auth", "lobby", "survival", "skyblock", "duels", "bedwars", "bot", "parkour"]
    if data[0] not in valid_names:
        await ctx.reply(f"Error : Invalid Server Name. Use `{prefix}admin css` to learn more!")
        return
    try: e = await serverpower(data[0], "restart", ctx)
    except:
        await ctx.reply(f"There was an error. Use `{prefix}admin css` to learn more")
        return
    if e == "exception": return
    embed = discord.Embed(title="Server Power", url="https://moonball.io/", color=embed_color)
    embed.set_author(name=embed_header, icon_url=embed_icon)
    embed.add_field(name=f'Operation Successful!',value=f'Successfully Restarted the {data[0].capitalize()} Server!', inline=False)
    embed.set_footer(text=embed_footer)
    await ctx.reply(embed=embed)
    await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} restarted server {data[0]}', "admin", f'{ctx.author.name}#{ctx.author.discriminator} restarted server {data[0]}')

@admin.command(aliases=['killserver', 'serverkill', 'sk', 'kill'])
async def kill_admin(ctx, *data): # Kill Server Command
    if await checkperm(ctx, 3): return
    valid_names = ["proxy", "limbo", "auth", "lobby", "survival", "skyblock", "duels", "bedwars", "bot", "parkour"]
    if data[0] not in valid_names:
        await ctx.reply(f"Error : Invalid Server Name. Use `{prefix}admin css` to learn more!")
        return
    try:
        e = await serverpower(data[0], "kill", ctx)
    except:
        await ctx.send(f"There was an error. Use `{prefix}admin css` to learn more")
        return
    if e == "exception": return
    killembed = discord.Embed(title="Server Power", url="https://moonball.io/", color=embed_color)
    killembed.set_author(name=embed_header, icon_url=embed_icon)
    killembed.add_field(name=f'Operation Successful!', value=f"Successfully Killed the {data[0].capitalize()} Server!", inline=False)
    killembed.set_footer(text=embed_footer)
    await ctx.reply(embed=killembed)
    await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} killed server {data[0]}', "admin", f'{ctx.author.name}#{ctx.author.discriminator} killed server {data[0]}')



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


@admin.command(aliases=['reset', 'resetcount', "rc"])
async def reset_admin(ctx, *data): # Reset Counter Command
    if await checkperm(ctx, 5): return
    data = " ".join(data).split()  # Input Splitter
    if data[0] == "all":
        await resetcount(ctx, "all", "all")
    elif data[0] == "suggestion" or data[0] == "s":
        await resetcount(ctx, "s", "suggestion")
    elif data[0] == "help" or data[0] == "h":
        await resetcount(ctx, "h", "help")
    elif data[0] == "info" or data[0] == "i":
        await resetcount(ctx, "i", "info")
    elif data[0] == "fun" or data[0] == "f":
        await resetcount(ctx, "f", "fun")
    elif data[0] == "admin" or data[0] == "a":
        await resetcount(ctx, "a", "admin")


#
# Permission Level System
#

@admin.command(aliases=['setlvl', "setlevel", "sl"])
async def set_level(ctx, *data): # Set Level Command
    if await checkperm(ctx, 4): return
    # Syntax: admin set_level <user(ctx.message.mentions[0].id)> <level(data[1])>
    if len(data) != 2:
        await ctx.reply(f"Error: Invalid Input. Use `{prefix}admin setlvl <user> <level>` to set a user's level.")
        return
    elif not ctx.message.mentions:
        await ctx.reply("Please specify a user!")
        return
    elif -1 < int(data[1]) > 5:
        await ctx.reply("**Error**: Invalid Level. It must be a number between -1 and 5.")
        return
    con = sqlite3.connect('./data/data.db')
    cur = con.cursor()
    oldLevel = await get_permlvl(ctx.message.mentions[0])
    cur.execute(f"UPDATE perms SET lvl = {data[1]} WHERE user_id = {ctx.message.mentions[0].id}")
    con.commit()
    con.close()
    perm_embed = discord.Embed(title="Permission Level", description=f"Permission Level successfully changed!", color=embed_color)
    perm_embed.set_author(name=embed_header, icon_url=embed_icon)
    perm_embed.set_footer(text=embed_footer)
    perm_embed.add_field(name="User", value=f"`{ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator}`", inline=False)
    perm_embed.add_field(name="Old Level", value=f"`{oldLevel}`", inline=True)
    perm_embed.add_field(name="New Level", value=f"`{data[1]}`", inline=True)
    await ctx.reply(embed=perm_embed)
    await logger("a", f"{ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator}'s permission level has been set to {data[1]} from {oldLevel}", "admin", f"{ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator}'s permission level has been set to {data[1]} from {oldLevel}")  # Logs to Log channel


@admin.command(aliases=['getlvl', "getlevel", "gl"])
async def get_level(ctx): # Get Level Command
    level_embed = discord.Embed(title="Permission Level", description=f"Got the Permission Level!", color=embed_color)
    level_embed.set_author(name=embed_header, icon_url=embed_icon)
    level_embed.set_footer(text=embed_footer)
    level_embed.add_field(name="User", value=f"`{ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator}`", inline=False)
    level_embed.add_field(name="Level", value=f"`{await get_permlvl(ctx.message.mentions[0])}`", inline=True)
    await ctx.reply(embed=level_embed)
    await logger("a", f"{ctx.author.name}#{ctx.author.discriminator} requested the Permission Level of {ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator}", "admin", f"{ctx.author.name}#{ctx.author.discriminator} requested the Permission Level of {ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator}")  # Logs to Log channel


#
#
#   Minecraft - Discord Connection Category
#
#

# @client.command
# async def connect(ctx):
#     pass



#
#
#   Reusable Functions
#
#

async def ip_embed(ctx):
    if await checkperm(ctx, 0): return
    ipembed = discord.Embed(title="Here's the Server IP!", url="https://moonball.io", color=embed_color)
    ipembed.set_author(name=embed_header, icon_url=embed_icon)
    ipembed.add_field(name="Java ", value="play.moonball.io", inline=True)
    ipembed.add_field(name="Bedrock ", value="play.moonball.io (Port 25565)", inline=False)
    ipembed.set_footer(text="Maybe check the pins next time? eh.")
    await ctx.reply(embed=ipembed)
    await logger("i", f'Sent IP Embed to message of {ctx.author.name}#{ctx.author.discriminator}', "help", f"Sent IP embed to message of {ctx.author.name}#{ctx.author.discriminator}")


async def version_embed(ctx):
    if await checkperm(ctx, 0): return
    vembed = discord.Embed(title="Here's the Server Version!", url="https://moonball.io", color=embed_color).set_footer(text=embed_footer)
    vembed.set_author(name=embed_header, icon_url=embed_icon)
    vembed.add_field(name="Java ", value="1.13 - 1.18.2", inline=True)
    vembed.add_field(name="Bedrock ", value="1.17.40 - 1.18.12", inline=False)
    await ctx.reply(embed=vembed)
    print(f'Sent Version Embed to message of {ctx.author.name}#{ctx.author.discriminator}')  # Logs to Console
    await logger("i", f'Sent Version Embed to message of {ctx.author.name}#{ctx.author.discriminator}', "help", f"Sent Version embed to message of {ctx.author.name}#{ctx.author.discriminator}")


async def serverstatus(ctx, st_server):  # Server Status front end
    if await checkperm(ctx, 0): return
    server = MinecraftServer.lookup(serv_ips.get(st_server.lower()))  # Gets server player-info from API
    try: placeholder = await status(st_server.lower())  # Gets server info from Pterodactyl API
    except:
        await ctx.reply("There was an error while trying to get server info, the panel is perhaps down. Please ping the Staff")
        return
    server_status = placeholder["state"]  # Setting this as placeholder state
    playerCount = 0
    if server_status == "offline":   # If server is offline
        server_status = "Offline <:offline:915916197797715979>"
    elif server_status == "running":
        server_status = "Online <:online:915916197973864449>"
        if not st_server == "proxy" or st_server == "bot":
            try:
                playerCount = server.query().players.online
            except:
                print("Error getting player count, It is 0")
    elif server_status == "starting":    # If server is starting
        server_status = "Starting <:partial:915916197848047646>"
    elif server_status == "stopping":    # If server is stopping
        server_status = "Stopping <:outage:915916198032588800>"
    # The embed it sends.
    serverembed = discord.Embed(title=f"{st_server.capitalize()} Status", url="https://moonball.io",
                                description=f"Live Status for the {st_server.capitalize()} Server.\nTriggered by {ctx.author.name}#{ctx.author.discriminator}", color=embed_color)
    serverembed.set_author(name=embed_header, icon_url=embed_icon)
    serverembed.set_thumbnail(url=embed_icon)
    serverembed.add_field(name="<:load_bot:952580881367826542> Status", value=f'{server_status}', inline=True)
    serverembed.add_field(name="<:member_bot:953308738234748928> Players", value=f'{playerCount} Online', inline=False)
    serverembed.add_field(name="<:cpu_bot:951055641395478568> CPU Usage", value=f'{placeholder["cpuUsage"]}%',inline=False)
    serverembed.add_field(name="<:ram_bot:951055641332563988> Memory Usage", value=f'{placeholder["memUsage"]}',inline=False)
    serverembed.add_field(name="<:disk_bot:952580881237803028> Disk Space", value=f'{placeholder["spaceOccupied"]}',inline=False)
    serverembed.add_field(name="<:uptime_bot:951055640967675945> Uptime", value=f'{placeholder["uptime"]}',inline=False)
    serverembed.set_footer(text=embed_footer)
    await ctx.reply(embed=serverembed)  # Sends the embed
    await logger("i", f'Server Status : Sent Server {st_server.capitalize()} embed to message of {ctx.author.name}#{ctx.author.discriminator}', "info", f"Sent Server {st_server.capitalize()} embed to message of {ctx.author.name}#{ctx.author.discriminator}")

async def logger(cat, printmsg, logtype, logmsg):  # Logs to Log channel
    await log_channel.send(f'**{logtype.capitalize()}** : ' + f'#{countadd(cat)} ' + logmsg)  # Logs to Log channel
    print(printmsg)

@client.event  # When user does an invalid command
async def on_command_error(ctx, error):
    if not isinstance(error, commands.CheckFailure):
        embed = discord.Embed(title="Error!", url="https://moonball.io/", description="There was an Error while executing your command.", color=embed_color).set_author(name=embed_header).set_footer(text=embed_footer)
        embed.add_field(name="Here is your Error -", value=f"```ini\n[{str(error)}]```", inline=False)

        if "is not found" in str(error):    # Non-Existent Command
            embed.add_field(name="Here is the command you tried to execute -", value=f"```ini\n[{ctx.message.content}]```", inline=False)
            embed.add_field(name="What This Means", value=f"**Non-Existent Command** : The command you just tried to execute, does not exist!\nUse `{prefix}help` to learn about the available commands!", inline=False)
        elif str(error) == "Command raised an exception: IndexError: list index out of range":  # Bad Syntax
            embed.add_field(name="Here is the command you tried to execute -", value=f"```ini\n[{ctx.message.content}]```", inline=False)
            embed.add_field(name="What This Means", value=f"**Bad Syntax** : The Syntax for this specific command is not right. There may be arguments missing within the command.\nUse `{prefix}help` to learn about the commands and their syntaxes!", inline=False)
        else:
            embed.add_field(name="Here is the command you tried to execute -", value=f"```ini\n[{ctx.message.content}]```", inline=False)
            embed.add_field(name="What This Means", value=f"With so many possible errors, I do not know what the exact error is, without the error code. Please send this error code to the Developer, <@837584356988944396> in DMs for it to be resolved.\nThere is still a chance it may be a syntax error.\nUse `{prefix}help` to learn about the commands and their syntaxes!", inline=False)

        # await ctx.reply(f"**Error!** The command may not exist, The Syntax may be wrong or there was an Internal Error. Use `{prefix}help` to view all available commands.\nError - ```ini\n[{error}]```") # , delete_after=10.0
        await ctx.author.send(embed=embed)
        await ctx.message.add_reaction("<:cross_bot:953561649254649866>")
        await logger("h", f"Sent Error message to {ctx.author.name}#{ctx.author.discriminator}. Error - {error}", "help", f"Sent Error Embed to message of {ctx.author.name}#{ctx.author.discriminator}\nError - ```ini\n{error}```")


async def checkcommandchannel(ctx):  # Check if the channel in which a command is executed in is a command-channel
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


@client.event  # No reacting to both in suggestions
async def on_raw_reaction_add(payload):   # checks whenever a reaction is added to a message
    if payload.channel_id == 956806563950112848:  # check which channel the reaction was added in
        channel = await client.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        for r in message.reactions:  # iterating through each reaction in the message
            if payload.member in await r.users().flatten() and not payload.member.bot and str(r) != str(payload.emoji):
                await message.remove_reaction(r.emoji, payload.member)  # Removes the reaction

    # msg_author = await client.get_channel(payload.channel_id).fetch_message(payload.message_id).author
    # if payload.emoji.name == "❌" and msg_author == client.user.id:  # checks if the bot reacted with a check
    #     channel = await client.fetch_channel(payload.channel_id)
    #     message = await channel.fetch_message(payload.message_id)
    #     await message.delete()  # deletes the message




#
#   ===BACKEND===
#
# Do not touch this, other than putting in your API key and server list
# Trust me messing stuff up here can cause a lot of bad!
#


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
        server_status[guides[i][1]] = await stats(guides[i][1])

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

    # server =     #Gets server player-info from API
    try:
        playerCount = MinecraftServer.lookup(serv_ips.get(servername)).query().players.online
        # Try to get player info from server, only IF it is online
    except:
        playerCount = 0
        await ctx.send("There was an error trying to get the player count of the server. The panel is perhaps down. Anyways ill continue with it being 0")

    if power in ("stop", "kill", "restart"):
        if playerCount != 0:
            # await ctx.reply(f"There are {playerCount} online")
            await ctx.reply("There is more than one person online on that server. Are you sure you want to proceed with the distructive action, while the players are online. If you do wish to, say `yes`")
            # await ctx.send(type=InteractionType.ChannelMessageWithSource, content="There is more than one person online on that server. Are you sure you want to proceed with the distructive action, while the players are online", components= Button(style=ButtonStyle.red, label="Confirm", custom_id="confirm_power_action")])
            msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
            if msg.content == "yes" or "YES" or "Yes":
                await ctx.reply("Okay! As you wish, master. Here I begin!")
            else:
                await ctx.reply("You took to long to reply or did not say `yes`. I am aborting the power action on the server.")
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
    else: return "invalid_power"

    response = requests.request('POST', url, data=payload, headers=headers)
    return response.text


#
#   Send Command to Server BACKEND
#

async def sendcmd(ctx, servername, cmd):
    ptero_panel = "panel.moonball.io"  # Put your Pterodactyl Panel's URL here
    server_guide = {'proxy': 'fe5a4fe1', 'limbo': "d1e50e31", 'auth': 'e91b165c', 'lobby': 'b7b7c4b3', 'survival': '777f305b', 'skyblock': '33cbad29', 'duels': '04cc6bb3', 'bedwars': '583e6fbc', 'bot': '5426b68e', 'parkour': '10770164', 'prison': 'a321d8fa'}  # Change this part, Add your server name and the ptero identifier (example in https://panel.moonball.io/server/5426b68e "5426b68e" is the ID)
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
# Permission level system backend
#
async def get_permlvl(user, class_type=True):
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



async def checkperm(ctx, level):
    currentlvl = await get_permlvl(ctx.author, True)
    if int(currentlvl) < int(level):
        await ctx.reply(f"You don't have the required permissions to use this command. You have permission level `{currentlvl}`, but required level is `{level}`!", delete_after=10)
        return True
    else:
        return False


client.run(os.getenv("DISCORD_TOKEN"))