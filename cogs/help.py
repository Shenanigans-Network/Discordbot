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
#   This code is not intended to be edited but feel free to do so
#   More info can be found on the GitHub page:
#

import discord
from discord.ext import commands
from backend import bot_version, prefix, embed_color, embed_footer, embed_header, embed_icon
from backend import log, logger


async def send_embed(ctx, embed):
    try:
        await ctx.reply(embed=embed)
        await logger("h", f"Sent help Embed to {ctx.author.name}#{ctx.author.discriminator}", f"Sent help Embed to {ctx.author.name}#{ctx.author.discriminator}", ctx.client)
    except Exception as e:
        log.error(f"Unable to send help Embed. Error: {e}")


class Help(commands.Cog, description="Help and Admin Help Commands for the Bot"):

    def __init__(self, client):
        self.client = client
        self.bot_version = bot_version
        self.prefix = prefix

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog : Help.py Loaded")


    @commands.command(aliass=["h", "help"])
    async def help(self, ctx):
        emb = discord.Embed(title="Help", description="", color=embed_color)
        emb.set_thumbnail(url=embed_icon)
        emb.set_footer(text=embed_footer)
        emb.set_author(name=embed_header, icon_url=embed_icon)
        emb.add_field(name="Version", value=self.bot_version, inline=True)
        emb.add_field(name="Prefix", value="`/` (Slash Commands)", inline=True)
        emb.add_field(name="Dev", value="<@929411943738015764>", inline=True)
        emb.add_field(name="There is no help required!", value="Do `/` and view all the Moonball Bot slash commands!", inline=False)

        # sending reply embed using our own function defined above
        await send_embed(ctx, emb)


def setup(client):
    client.add_cog(Help(client))