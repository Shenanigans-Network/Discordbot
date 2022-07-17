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
from mcstatus import JavaServer
from discord.ext import commands
from backend import prefix, embed_header, embed_footer, embed_color, bot_version, embed_icon, serv_ips, guild_id, server_list       # Import bot variables
from backend import checkperm, logger, status, serverstatus, log   # Import bot functions

choices = []
for i in server_list:
    choices.append(discord.OptionChoice(i.capitalize().strip(), value=i.strip().lower()))

class Server(commands.Cog):
    """Commands that provide information about the Server meant for general users"""
    def __init__(self, client):
        self.client = client
        self.embed_color = embed_color
        self.embed_icon = embed_icon
        self.embed_header = embed_header
        self.embed_footer = embed_footer
        self.prefix = prefix
        self.bot_version = bot_version
        self.serv_ips = serv_ips


    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog : Server.py Loaded")


    @commands.slash_command(name="stats", description="Sends Bot Resource usage, etc.", guild_ids=[guild_id])
    async def stats(self, ctx):
        if await checkperm(ctx, 0): return
        server_info = await status("bot")
        stats_embed = discord.Embed(title='System Resource Usage', description='See Resource Usages of the Bot.', url="https://moonball.io", color=embed_color).set_footer(text=embed_footer)
        stats_embed.set_author(name=embed_header, icon_url=embed_icon)
        stats_embed.add_field(name='<:latency_bot:951055641307381770> Latency',value=f'{round(self.client.latency * 1000)}ms', inline=False)
        stats_embed.add_field(name='<:cpu_bot:951055641395478568> CPU Usage', value=f'{server_info["cpuUsage"]}%',inline=False)
        stats_embed.add_field(name='<:ram_bot:951055641332563988> Memory Usage', value=f'{server_info["memUsage"]}',inline=False)
        stats_embed.add_field(name='<:uptime_bot:951055640967675945> Uptime', value=f'{server_info["uptime"]}',inline=False)
        await ctx.respond(embed=stats_embed, ephemeral=True)
        await logger("i", f'Sent bot Stats to `{ctx.author.name}#{ctx.author.discriminator}`', self.client)



    # Server Playercount Command
    @commands.slash_command(name="players", description="Sends the names of Players online on a Server", guild_ids=[guild_id])
    async def playercount(self, ctx, server: discord.Option(choices=choices)):
        if await checkperm(ctx, 0): return
        msg = await ctx.respond(embed=discord.Embed(title=f'Player List | {server.capitalize()}', description='*Please hold on, Command Content is loading*', color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)
        try:
            server_info = await status(server.lower())  # Gets server info from Pterodactyl API
        except Exception as e:
            await msg.edit_original_message(embed=discord.Embed(title=f"Server Status | {server.capitalize()}",description=f"**Error**: Couldn't get Status\n{e}",color=embed_color,url="https://moonball.io").set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            log.warning(f"Error while trying to get Server Status. Error: {str(e)}")
            return
        server_status = server_info["state"]
        if server_status != "running":
            await msg.edit_original_message(embed=discord.Embed(title=f"Server Status | {server.capitalize()}",description=f"**Error**: Server is {server_status.capitalize()}",color=embed_color,url="https://moonball.io").set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        player_list = JavaServer.lookup(serv_ips.get(server)).query().players.names
        player_count = JavaServer.lookup(serv_ips.get(server)).query().players.online
        pc_embed = discord.Embed(title=f"Player List", description=f"Online player list for the server {server.capitalize()}.\n Requested by {ctx.author.name}#{ctx.author.discriminator}", color=embed_color, url="https://moonball.io").set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon)
        pc_embed.set_author(name=embed_header, icon_url=embed_icon)
        pc_embed.add_field(name="Player Count", value=player_count, inline=False)
        if player_count != 0:
            pc_embed.add_field(name=f"Player List | {server.capitalize()}", value='\n'.join(player_list), inline=False)
        await msg.edit_original_message(embed=pc_embed)
        await logger("i", f"Sent `{ctx.author.name}#{ctx.author.discriminator}` Player List of `{server.capitalize()}`", self.client)




    @commands.slash_command(name="status", description="Sends the status for a Minecraft Server", guild_ids=[guild_id])
    async def status(self, ctx, server: discord.Option(choices=choices)):
        await serverstatus(ctx, server, isslash=True)


def setup(client):
    client.add_cog(Server(client))
