import discord
from mcstatus import MinecraftServer
from discord.ext import commands
from bot import prefix, embed_header, embed_footer, embed_color, bot_version, embed_icon, serv_ips      # Import bot variables
from bot import checkcommandchannel, checkperm, logger, serverstatus, status, version_embed, ip_embed   # Import bot functions

class Server(commands.Cog):
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
        global embed_log
        embed_log = self.client.get_channel(960204173989789736)
        print("Cog : Server.py Loaded")


    # Bot Ping Command
    @commands.command(aliases=['memory', 'mem', 'cpu', 'ram', 'lag', 'ping'])  # Bot Stats Command
    async def stats(self, ctx):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        server_info = await status("bot")
        stats_embed = discord.Embed(title='System Resource Usage', description='See Resource Usages of the Bot.', url="https://moonball.io", color=embed_color).set_footer(text=embed_footer)
        stats_embed.set_author(name=embed_header, icon_url=embed_icon)
        stats_embed.add_field(name='<:latency_bot:951055641307381770> Latency',value=f'{round(self.client.latency * 1000)}ms', inline=False)
        stats_embed.add_field(name='<:cpu_bot:951055641395478568> CPU Usage', value=f'{server_info["cpuUsage"]}%',inline=False)
        stats_embed.add_field(name='<:ram_bot:951055641332563988> Memory Usage', value=f'{server_info["memUsage"]}',inline=False)
        stats_embed.add_field(name='<:uptime_bot:951055640967675945> Uptime', value=f'{server_info["uptime"]}',inline=False)
        await ctx.reply(embed=stats_embed)
        await logger("i", f'Sent bot Stats to message of {ctx.author.name}#{ctx.author.discriminator}', "info", f"Sent Stats embed to message of {ctx.author.name}#{ctx.author.discriminator}")


    # Server Playercount Command
    @commands.command(aliases=["players"])
    async def playercount(self, ctx, st_server):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was used in a valid channel
        msg = await ctx.reply(embed=discord.Embed(title=f"{st_server.capitalize()} Server Status",description="*Server Status is loading*\nPlease hold on!",color=embed_color))
        if st_server.lower() in ["proxy", "lobby", "auth", "limbo"]:
            await msg.edit(embed=discord.Embed(title=f"{st_server.capitalize()} Server Status",description="**There was an error!**\nPlayer Count cannot be viewed for Proxy, Limbo, Auth and Lobby", color=embed_color))
            return
        elif not st_server.lower() in ["survival", "bedwars", "duels", "skyblock", "prison", "parkour"]:
            await msg.edit(embed=discord.Embed(title=f"{st_server.capitalize()} Server Status",description=f"**There was an error!**\n{st_server.capitalize()} is not a valid Server! `+help playercount` for Server List!",color=embed_color))
            return
        player_list = MinecraftServer.lookup(serv_ips.get(st_server)).query().players.names
        player_count = MinecraftServer.lookup(serv_ips.get(st_server)).query().players.online
        pc_embed = discord.Embed(title=f"Player List", description=f"Online player list for the server {st_server.capitalize()}.\n Requested by {ctx.author.name}#{ctx.author.discriminator}", color=embed_color, url="https://moonball.io")
        pc_embed.set_author(name=embed_header, icon_url=embed_icon)
        pc_embed.add_field(name="Player Count", value=player_count, inline=False)
        if player_count != 0:
            pc_embed.add_field(name="Players", value='\n'.join(player_list), inline=False)
        await msg.edit(embed=pc_embed)
        await logger("i",f"{ctx.author.name}#{ctx.author.discriminator} used Player List Command for server {st_server.capitalize()}","info",f"{ctx.author.name}#{ctx.author.discriminator} used Player-Count Command for server {st_server.capitalize()}")


    @commands.command(aliases=['bedrock', 'java'])  # The IP command
    async def ip(self, ctx): await ip_embed(ctx)

    @commands.command()
    async def version(self, ctx): await version_embed(ctx)

    # This part is making aliases for each server's status. Just copy-paste of code, but with server-name changed
    @commands.command(aliases=['proxy', 'velocity'])  # Status cmd for proxy
    async def statusproxy(self, ctx):
        await serverstatus(ctx, "proxy")

    @commands.command(aliases=['limbo'])  # Status cmd for limbo
    async def statuslimbo(self, ctx):
        await serverstatus(ctx, "limbo")

    @commands.command(aliases=['auth', 'authserver'])  # Status cmd for auth
    async def statusauth(self, ctx):
        await serverstatus(ctx, "auth")

    @commands.command(aliases=['lobby', 'hub'])  # Status cmd for lobby
    async def statuslobby(self, ctx):
        await serverstatus(ctx, "lobby")

    @commands.command(aliases=['survival'])  # Status cmd for survival
    async def statussurvival(self, ctx):
        await serverstatus(ctx, "survival")

    @commands.command(aliases=['bedwars', 'bedwar', 'bw'])  # Status cmd for Bedwars
    async def statusbedwars(self, ctx):
        await serverstatus(ctx, "bedwars")

    @commands.command(aliases=['duels', 'duel'])  # Status cmd for duels
    async def statusduels(self, ctx):
        await serverstatus(ctx, "duels")

    @commands.command(aliases=['skyblock'])  # Status cmd for Skyblock
    async def statusskyblock(self, ctx):
        await serverstatus(ctx, "skyblock")

    @commands.command(aliases=['parkour'])  # Status cmd for parkour
    async def statusparkour(self, ctx):
        await serverstatus(ctx, "parkour")

    @commands.command(aliases=['prison'])  # Status cmd for parkour
    async def statusprison(self, ctx):
        await serverstatus(ctx, "prison")

def setup(client):
    client.add_cog(Server(client))
