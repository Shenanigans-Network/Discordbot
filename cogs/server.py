import discord
from mcstatus import JavaServer
from discord.ext import commands
from bot import prefix, embed_header, embed_footer, embed_color, bot_version, embed_icon, serv_ips, guild_id      # Import bot variables
from bot import checkperm, logger, status, version_embed, ip_embed   # Import bot functions

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
        print("Cog : Server.py Loaded")


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
        await logger("s", f'Sent bot Stats to message of {ctx.author.name}#{ctx.author.discriminator}', "server", f"Sent Stats embed to message of {ctx.author.name}#{ctx.author.discriminator}")


    # Server Playercount Command
    @commands.slash_command(name="players", description="Sends the names of Players online on a Server", guild_ids=[guild_id])

    async def playercount(self, ctx, server: discord.Option(choices=[
                                                             discord.OptionChoice("Survival", value="survival"),
                                                             discord.OptionChoice("Bedwars", value="bedwars"),
                                                             discord.OptionChoice("Duels", value="duels"),
                                                             discord.OptionChoice("Skyblock", value="skyblock"),
                                                             discord.OptionChoice("Prison", value="prison"),
                                                             discord.OptionChoice("Parkour", value="parkour")
                                                             ])):
        if await checkperm(ctx, 0): return
        msg = await ctx.respond(embed=discord.Embed(title=f'Player List | {server.capitalize()}', description='*Please hold on, Command Content is loading*', color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)
        try:
            server_info = await status(server.lower())  # Gets server info from Pterodactyl API
        except Exception as e:
            await msg.edit_original_message(embed=discord.Embed(title=f"Server Status | {server.capitalize()}",description=f"**Error**: Couldn't get Status\n{e}",color=embed_color,url="https://moonball.io").set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            print(f"Couldn't get Server Status for {server.capitalize()}\n{e}")
            return
        server_status = server_info["state"]
        if server_status != "running":
            await msg.edit_original_message(embed=discord.Embed(title=f"Server Status | {server.capitalize()}",description=f"**Error**: Server is {server_status.capitalize()}",color=embed_color,url="https://moonball.io").set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        player_list = JavaServer.lookup(serv_ips.get(server)).query().players.names
        player_count = JavaServer.lookup(serv_ips.get(server)).query().players.online
        pc_embed = discord.Embed(title=f"Player List", description=f"Online player list for the server {server.capitalize()}.\n Requested by {ctx.author.name}#{ctx.author.discriminator}", color=embed_color, url="https://moonball.io")
        pc_embed.set_author(name=embed_header, icon_url=embed_icon)
        pc_embed.add_field(name="Player Count", value=player_count, inline=False)
        if player_count != 0:
            pc_embed.add_field(name=f"Player List | {server.capitalize()}", value='\n'.join(player_list), inline=False)
        await msg.edit_original_message(embed=pc_embed)
        await logger("s",f"{ctx.author.name}#{ctx.author.discriminator} used Player List Command for server {server.capitalize()}","server",f"{ctx.author.name}#{ctx.author.discriminator} used Player-Count Command for server {server.capitalize()}")

    @commands.slash_command(name="ip", description="Sends the Server IP", guild_ids=[guild_id])
    async def getip(self, ctx): await ip_embed(ctx)

    @commands.slash_command(name="version", description="Sends the Server Version",guild_ids=[guild_id])
    async def getversion(self, ctx): await version_embed(ctx)


    @commands.slash_command(name="status", description="Sends the status for a Minecraft Server", guild_ids=[guild_id])
    async def status(self, ctx, server: discord.Option(choices=[
                                                             discord.OptionChoice("Proxy", value="proxy"),
                                                             discord.OptionChoice("Limbo", value="limbo"),
                                                             discord.OptionChoice("Auth", value="auth"),
                                                             discord.OptionChoice("Lobby", value="lobby"),
                                                             discord.OptionChoice("Survival", value="survival"),
                                                             discord.OptionChoice("Bedwars", value="bedwars"),
                                                             discord.OptionChoice("Duels", value="duels"),
                                                             discord.OptionChoice("Skyblock", value="skyblock"),
                                                             discord.OptionChoice("Prison", value="prison"),
                                                             discord.OptionChoice("Parkour", value="parkour")
                                                             ] )):
            if await checkperm(ctx, 0): return
            msg = await ctx.respond(embed=discord.Embed(title=f"Server Status | {server.capitalize()}", description=f"*Please hold on, Command Content is loading*", color=embed_color, url="https://moonball.io").set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)
            try:
                server_info = await status(server.lower())  # Gets server info from Pterodactyl API
            except Exception as e:
                await msg.edit_original_message(embed=discord.Embed(title=f"Server Status | {server.capitalize()}", description=f"**Error**: Couldn't get Status\n{e}", color=embed_color, url="https://moonball.io").set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
                print(f"Couldn't get Server Status for {server.capitalize()}\n{e}")
                return
            server_status = server_info["state"]  # Setting this as placeholder state
            player_count = 0
            if server_status == "offline":  # If server is offline
                server_status = "Offline <:offline:915916197797715979>"
            elif server_status == "running":
                server_status = "Online <:online:915916197973864449>"
                if not server in ["proxy", "bot", "auth", "lobby", "limbo"]:  # If not one of these servers
                    try:
                        player_count = server.query().players.online  # Gets player count from API
                    except Exception as e:
                        print(f"Error getting player count, It is 0\n{e}")  # If error in getting Playercount
            elif server_status == "starting":  # If server is starting
                server_status = "Starting <:partial:915916197848047646>"
            elif server_status == "stopping":  # If server is stopping
                server_status = "Stopping <:outage:915916198032588800>"
            # Embed
            server_embed = discord.Embed(title=f"Status | {server.capitalize()}", url="https://moonball.io",description=f"Live Status for the {server.capitalize()} Server.\nTriggered by {ctx.author.name}#{ctx.author.discriminator}",color=embed_color)
            server_embed.set_author(name=embed_header, icon_url=embed_icon)
            server_embed.set_thumbnail(url=embed_icon)
            server_embed.add_field(name="<:load_bot:952580881367826542> Status", value=f'{server_status}', inline=True)
            server_embed.add_field(name="<:member_bot:953308738234748928> Players", value=f'{player_count} Online',inline=False)
            server_embed.add_field(name="<:cpu_bot:951055641395478568> CPU Usage", value=f'{server_info["cpuUsage"]}%',inline=False)
            server_embed.add_field(name="<:ram_bot:951055641332563988> Memory Usage",value=f'{server_info["memUsage"]}', inline=False)
            server_embed.add_field(name="<:disk_bot:952580881237803028> Disk Space",value=f'{server_info["spaceOccupied"]}', inline=False)
            server_embed.add_field(name="<:uptime_bot:951055640967675945> Uptime", value=f'{server_info["uptime"]}',inline=False)
            server_embed.set_footer(text=embed_footer)
            await msg.edit_original_message(embed=server_embed)
            await logger("s",f'Server Status : Sent Server {server.capitalize()} embed to message of {ctx.author.name}#{ctx.author.discriminator}',"server",f"Sent Server {server.capitalize()} embed to message of {ctx.author.name}#{ctx.author.discriminator}")



def setup(client):
    client.add_cog(Server(client))
