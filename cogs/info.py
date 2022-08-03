#   ╔═╗╔═╗            ╔╗       ╔╗ ╔╗     ╔══╗      ╔╗              ╔═══╗╔═══╗╔═══╗
#   ║║╚╝║║            ║║       ║║ ║║     ║╔╗║     ╔╝╚╗             ║╔═╗║║╔═╗║║╔═╗║
#   ║╔╗╔╗║╔══╗╔══╗╔═╗ ║╚═╗╔══╗ ║║ ║║     ║╚╝╚╗╔══╗╚╗╔╝             ║║ ╚╝║║ ║║║║ ╚╝
#   ║║║║║║║╔╗║║╔╗║║╔╗╗║╔╗║╚ ╗║ ║║ ║║     ║╔═╗║║╔╗║ ║║     ╔═══╗    ║║ ╔╗║║ ║║║║╔═╗
#   ║║║║║║║╚╝║║╚╝║║║║║║╚╝║║╚╝╚╗║╚╗║╚╗    ║╚═╝║║╚╝║ ║╚╗    ╚═══╝    ║╚═╝║║╚═╝║║╚╩═║
#   ╚╝╚╝╚╝╚══╝╚══╝╚╝╚╝╚══╝╚═══╝╚═╝╚═╝    ╚═══╝╚══╝ ╚═╝             ╚═══╝╚═══╝╚═══╝
#
#
#   This is a cog belonging to the Moonball Bot.
#   We are Open Source => https://moonball.io/opensource
#
#   This cog (info) must be edited to fit your bot's needs.
#   You can find more info about how to do this on the GitHub page.
#

import discord
from discord.ext import commands
from backend import embed_header, embed_footer, embed_color, bot_version, embed_icon, guild_id, embed_url     # Import bot variables
from backend import checkperm, logger, ip_embed, version_embed, log # Import functions


class Info(commands.Cog):
    """Commands which provide information relating to Servers and our Network"""
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog : Info.py Loaded")



    @commands.slash_command(name="ip", description="Sends the Server IP", guild_ids=[guild_id])
    async def getip(self, ctx): await ip_embed(ctx, isslash=True)

    @commands.slash_command(name="version", description="Sends the Server Version",guild_ids=[guild_id])
    async def getversion(self, ctx): await version_embed(ctx, isslash=True)

    @commands.slash_command(name="shop", description="Sends a URL to the Moonball Shop", guild_ids=[guild_id])
    async def shop(self, ctx):
        if await checkperm(ctx, 0): return
        await ctx.respond("Visit our shop here!- \nhttps://shop.moonball.io")
        await logger("i", f"Sent Shop link to message of `{ctx.author.name}#{ctx.author.discriminator}`", self.client)

    @commands.slash_command(name="opensource", description="Sends a link to the Moonball Network's Discord Bot's Open Source Repository", guild_ids=[guild_id])
    async def opensource(self, ctx):
        if await checkperm(ctx, 0): return
        await ctx.respond(f"This Discord Bot is opensource and made with py-cord in Python.\nIf you would like to check out the source code, Visit the GitHub Repo here - https://moonball.io/opensource", ephemeral=True)
        await logger("i", f"Sent Bot GitHub URL to message of `{ctx.author.name}#{ctx.author.discriminator}`", self.client)

    @commands.slash_command(name="botversion", description="Sends the current version of the bot", guild_ids=[guild_id])
    async def botversion(self, ctx):
        if await checkperm(ctx, 0): return
        await ctx.respond(f"I am currently on Version `{bot_version}`!", ephemeral=True)
        await logger("i", f"Sent Bot Version to message of `{ctx.author.name}#{ctx.author.discriminator}`", self.client)


    @commands.slash_command(name="socials", description="Sends a link to the Moonball Network's Social Media", guild_ids=[guild_id])
    async def socials(self, ctx):
        if await checkperm(ctx, 0): return
        embed = discord.Embed(title="Social Media", description="Here are the links to our Socials!", url=embed_url, color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header,icon_url=embed_icon).set_thumbnail(url=embed_icon)
        embed.add_field(name="<:discordlogo:1003979264846204938> Discord", value="https://moonball.io/discord", inline=True)
        embed.add_field(name="<:twitterlogo:985601023995441202> Twitter", value="https://moonball.io/twitter", inline=False)
        embed.add_field(name="<:youtubelogo:985600997541961779> YouTube", value="https://moonball.io/youtube", inline=False)
        embed.add_field(name="<:instagram:985601063509979256> Instagram", value="https://moonball.io/instagram", inline=False)
        embed.add_field(name="<:redditlogo:1003978205021077606> Reddit", value="https://moonball.io/reddit", inline=False)
        await ctx.respond(embed=embed)
        await logger("i", f"Sent Socials to message of `{ctx.author.name}#{ctx.author.discriminator}`", self.client)


def setup(client):
    client.add_cog(Info(client))
