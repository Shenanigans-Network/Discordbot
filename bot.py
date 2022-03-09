# Made by RajDave69 on Github
# Contacts -
#       Instagram - raj_clicks25
#       Discord - Raj Dave#3215
#       Reddit - Itz_Raj69_
#
#   Do not use this bot's files or codes for your own projects without credits
#   Owners include 𝓡𝓸𝓬𝓴𝔂_𝓡𝓾𝓽𝔀𝓲𝓴#5333 Raj Dave#3215 and Kabashi-Kun#5099 (discord)
#
#               Thank you for your time here, and I hope this code is useful to you =D

from discord.ext import commands #Imports required Modules
import discord, datetime, time
import psutil

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="+", intents=intents, help_command=None) #Setting prefix

#Stuff the bot does when it starts
@client.event
async def on_ready():
    print("Connected to Discord!")
    await client.change_presence(activity=discord.Game('on the Shenanigans Network')) #Set Presence
    global startTime #Set bot start time for the `Stats` Uptime monitor
    startTime = time.time()


#On word "ip" send the IP embed
@client.event
async def on_message(message):
    #checks if author is a bot.
    if message.author.bot: return
    else:
        if "ip" in message.content:
            # Sends main IP embed
            ipembed = discord.Embed(title="Here's the Server ip!", url="https://moonball.io", color=0xff0000)
            ipembed.set_thumbnail(url="https://media.discordapp.net/attachments/880368661104316459/950775364928561162/logo.png")
            ipembed.add_field(name="Java", value="play.moonball.io", inline=True)
            ipembed.add_field(name="Bedrock", value="play.moonball.io (Port 25565)", inline=False)
            ipembed.set_footer(text="Maybe check the pins next time? eh.")
            await message.channel.send(embed=ipembed)


    await client.process_commands(message)
    #Bot Stats Command
@client.command(aliases=['memory, mem, cpu, ram, lag'])
async def stats(ctx):
    #Uptime Calculator
    current_time = time.time()
    difference = int(round(current_time - startTime))
    uptime = str(datetime.timedelta(seconds=difference))
    w = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    availablemem = round(w, 2)

    #Stats Embed
    stats = discord.Embed(title = 'System Resource Usage', description = 'See CPU and memory usage of the system.')
    stats.add_field(name='<:latency_bot:951055641307381770> Latency' , value=f'{round(client.latency * 1000)}ms', inline=False)
    stats.add_field(name = '<:cpu_bot:951055641395478568> CPU Usage', value = f'{psutil.cpu_percent()}%', inline = False)
    stats.add_field(name = '<:ram_bot:951055641332563988> Memory Usage', value = f'{psutil.virtual_memory().percent}%', inline = False)
    stats.add_field(name = '<:shard_bot:951055641697456128> Available Memory', value = f'{availablemem}%', inline = False)
    stats.add_field(name = '<:uptime_bot:951055640967675945> Uptime', value=f'{uptime}', inline=False)
    await ctx.send(embed = stats)


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
    announcement = discord.Embed(title="Visit Our Website", url="https://moonball.io", color=0xff0000)
    announcement.set_thumbnail(url=f"{data[2]}")
    announcement.add_field(name=f"{data[0]}", value=f"{data[1]}", inline=True)
    announcement.set_footer(text=f"Announcement by {ctx.author.name}")
    await ctx.send(embed=announcement)
    return

client.run('your-token')