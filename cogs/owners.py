from discord.ext import commands
from discord.utils import get
import discord

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.owners = [828970752647626812, 837584356988944396, 869580247832600576]
    
    @commands.command(aliases=['get-id'])
    async def get_id(self, ctx, member:discord.Member=None):
        if int(ctx.author.id) in self.owners:
            member = member or ctx.author
            await ctx.send(member.id)
        else:
            await ctx.send("You've got to be a bot dev to use this command smh")

    @commands.command(aliases=['list-servers', 'lservers', 'servers'])
    async def list_servers(self, ctx):
        if int(ctx.author.id) in self.owners:
            servers = self.client.guilds
            message = "Here are the Servers I am in: ```\n"
            
            for serv in servers:
                message += serv.name+"\n"
            message += "```"
            await ctx.send(message)
        else:
            await ctx.send("You've got to be a bot dev to use this command smh")
    
    @commands.command(aliases=['exit-server', 'leave-server', 'lserver', 'ls'])
    async def leave_server(self, ctx, *server):
        e = " "
        server = e.join(server)

        if int(ctx.author.id) in self.owners:
            guild = get(self.client.guilds, name=server)
            if guild is None:
                await ctx.send(f'No server found with the name: {server}')
                return
            await guild.leave()
            await ctx.send(f'Left the server: {server}')
        else:
            await ctx.send("You've got to be a bot dev to use this command smh")
        





    
    

def setup(client):
    client.add_cog(Owner(client))


