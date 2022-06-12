import discord
from discord.ext import commands
from discord.errors import Forbidden
from bot import bot_version, prefix, embed_color, embed_footer, embed_header, embed_icon
from bot import logger


async def send_embed(ctx, embed):
    try:
        await ctx.reply(embed=embed)
        await logger("h", f"Sent help Embed to {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent help Embed to {ctx.author.name}#{ctx.author.discriminator}")
    except Forbidden:
        try:
            await ctx.reply("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


class Help(commands.Cog, description="Help and Admin Help Commands for the Bot"):

    def __init__(self, client):
        self.client = client
        self.bot_version = bot_version
        self.prefix = prefix

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog : Help.py Loaded")


    @commands.command(aliass=["h", "help"])
    async def help(self, ctx):
        emb = discord.Embed(title="Help", description="", color=embed_color)
        emb.set_thumbnail(url=embed_icon)
        emb.set_footer(text=embed_footer)
        emb.set_author(name=embed_header, icon_url=embed_icon)
        emb.add_field(name="Version", value=self.bot_version, inline=True)
        emb.add_field(name="Prefix", value="`/` (Slash Commands)", inline=True)
        emb.add_field(name="Dev", value="<@929411943738015764>", inline=True)
        emb.add_field(name="There is no help required!", value="Do `/` and view al the Moonball Bot slash commands!", inline=False)

        # sending reply embed using our own function defined above
        await send_embed(ctx, emb)


def setup(client):
    client.add_cog(Help(client))