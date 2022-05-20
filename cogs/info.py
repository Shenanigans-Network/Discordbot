import discord
from discord.ext import commands
from bot import prefix, embed_header, embed_footer, embed_color, bot_version, embed_icon    # Import bot variables
from bot import checkcommandchannel, checkperm, logger                                      # Import functions


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.embed_color = embed_color
        self.embed_icon = embed_icon
        self.embed_header = embed_header
        self.embed_footer = embed_footer
        self.prefix = prefix
        self.bot_version = bot_version


    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog : Info.py Loaded")


    @commands.command()
    async def shop(self, ctx):
        if await checkperm(ctx, 0): return
        await ctx.reply("Visit our shop here!- \nhttps://shop.moonball.io")
        await logger("i", f"Sent Shop link to message of {ctx.author.name}#{ctx.author.discriminator}", "info", f"Sent Shop link to message of {ctx.author.name}#{ctx.author.discriminator}")


    @commands.command()
    async def opensource(self, ctx):
        if await checkperm(ctx, 0): return
        await checkcommandchannel(ctx)
        await ctx.reply(f"This Discord Bot is opensource and made with discord.py.\nIf you would like to check out the source code, Visit the GitHub Repo here - https://moonball.io/opensource")
        await logger("i", f"Sent Bot GitHub URL to message of {ctx.author.name}#{ctx.author.discriminator}", "info", f"Sent Bot GitHub URL to message of {ctx.author.name}#{ctx.author.discriminator}")


    @commands.command()
    async def botversion(self, ctx):
        if await checkperm(ctx, 0): return
        await checkcommandchannel(ctx)
        ctx.reply(f"I am currently on Version `{bot_version}`!")
        await logger("i", f"Sent Bot Version to message of {ctx.author.name}#{ctx.author.discriminator}", "info",f"Sent Bot Version to message of {ctx.author.name}#{ctx.author.discriminator}")


    @commands.command()
    async def invite(self, ctx):
        if await checkperm(ctx, 0): return
        await checkcommandchannel(ctx)
        await ctx.reply("To invite me to your server, Click on the link below\nhttps://moonball.io/bot")
        await logger("i", f"Sent Bot invite URL to message of {ctx.author.name}#{ctx.author.discriminator}", "info",f"Sent Bot invite URL to message of {ctx.author.name}#{ctx.author.discriminator}")



    @commands.command()
    async def socials(self, ctx):
        if await checkperm(ctx, 0): return
        await checkcommandchannel(ctx)
        embed = discord.Embed(title="Social Media", description="Here are the links to our Socials!", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header,icon_url=embed_icon).set_thumbnail(url=embed_icon)
        embed.add_field(name="<:discordlogo:972789364981661716> Discord", value="https://moonball.io/discord", inline=True)
        embed.add_field(name="<:twitterlogo:972789038727708712> Twitter", value="https://moonball.io/twitter", inline=False)
        embed.add_field(name="<:youtubelogo:972789038677385226> YouTube", value="https://moonball.io/youtube", inline=False)
        embed.add_field(name="<:instagramlogo:972789038572527657> Instagram", value="https://moonball.io/instagram", inline=False)
        embed.add_field(name="<:redditlogo:972789038731886603> Reddit", value="https://moonball.io/reddit", inline=False)
        await ctx.reply(embed=embed)
        await logger("i", f"Sent Bot Socials to message of {ctx.author.name}#{ctx.author.discriminator}", "info",f"Sent Bot Socials to message of {ctx.author.name}#{ctx.author.discriminator}")


def setup(client):
    client.add_cog(Info(client))
