from discord.ext import commands
from discord.utils import get
import asyncio, discord

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="+", intents=intents, help_command=None)

@client.event
async def on_ready():
    print("Connected to Discord!")
    await client.change_presence(activity=discord.Game('on the Shenanigans Network'))


@client.event
async def on_message(ctx):
    if ctx.author.bot:
        return
    else:
        if "ip" in ctx.content:
            await ctx.channel.send("Since you're too lazy to check the Pins, I have to do the work for you <a:checkpins:930751586890842143>")
            ipembed = discord.Embed(title="Here's the Server ip!", url="https://moonball.io", color=0x0016bd)
            ipembed.set_thumbnail(url="https://media.discordapp.net/attachments/880368661104316459/950775364928561162/logo.png")
            ipembed.add_field(name="Java", value="play.moonball.io", inline=True)
            ipembed.add_field(name="Bedrock", value="play.moonball.io (Port 25565)", inline=False)
            ipembed.set_footer(text="Maybe check the pins next time? eh.")
            await ctx.channel.send(embed=ipembed)

client.run('x')