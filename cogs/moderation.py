from discord.ext import commands
from discord.utils import get
import asyncio, discord

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.manual_lock = [] 

    def convert_time(self, t):
        if t[-1] not in ['m', 'h', 's', 'd']:
            return False
        val = {'m': 60, 's': 1, 'h': 3600, 'd': 86400}
        return int(t[:-1]) * val[t[-1]]

    # Command to lock a channel
    @commands.command(aliases=['lockdown'])
    @commands.has_permissions(administrator=True)
    async def lock(self, ctx, time="1d", channel: discord.TextChannel = None):
        sec = self.convert_time(time)
        if not sec:
            await ctx.send('Please pass in a valid time metric. (s, m, h, d)')
            return

        channel = channel or ctx.channel
        full = {'d': "day(s)", 's': "seconds", 'm': "minute(s)", 'h': "hour(s)"}

        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await channel.send(f'<#{channel.id}> locked for {time[:-1]} {full[time[-1]]}.')

        self.manual_lock.append([channel.id, True])

        await asyncio.sleep(sec)

        rec = [chan for chan in self.manual_lock if chan[0] == channel.id][0]
        if rec[1]:
            overwrite.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await channel.send(f'<#{channel.id}> is now unlocked!')

            self.manual_lock.remove(rec)

    # channel un-lockdown command
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx, channel=None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True

        for chan in self.manual_lock:
            if chan[0] == channel.id:
                self.manual_lock.remove(chan)
                self.manual_lock.append([channel.id, False])

        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await channel.send(f'<#{channel.id}> is now unlocked!')

    # temp-mute command
    @commands.command(aliases=['temp-mute'])
    @commands.has_permissions(administrator=True)
    async def temp_mute(self, ctx, person: discord.Member, t="1h", reason="Not specified"):
        sec = self.convert_time(t)
        if not sec:
            await ctx.send('Please provide a valid time')
            return

        muted = discord.utils.find(lambda r: r.name == 'Muted', ctx.guild.roles)
        await person.add_roles(muted)

        embed = discord.Embed(colour=discord.Color.from_rgb(255, 0, 0), description=f"**Reason:** {reason}")
        embed.set_author(name=f"{person} Has Been Muted", icon_url=f"{person.avatar_url}")
        embed.set_footer(text='seriously?')

        await ctx.send(embed=embed)
        await asyncio.sleep(sec)

        await person.remove_roles(muted)

        unmuted_embed = discord.Embed(color=discord.Color.from_rgb(0, 0, 225), description="Better be good now")
        unmuted_embed.set_author(name=f'{person} Has Now Been Unmuted! YAY')
        unmuted_embed.set_footer(text='IKR it took forever')

        await ctx.send(embed=unmuted_embed)

    # temp-purg command
    @commands.command(aliases=['temp-purg', 'tpurg', 'temppurg', 'purg'])
    @commands.has_permissions(administrator=True)
    async def temp_purg(self, ctx, person: discord.Member, t="1h", reason="Not specified"):
        sec = self.convert_time(t)
        if not sec:
            await ctx.send('Please provide a valid time')
            return

        purg = get(ctx.guild.roles, name='Purg')
        await person.add_roles(purg)

        embed = discord.Embed(colour=discord.Color.from_rgb(255, 0, 0), description=f"**Reason:** {reason}")
        embed.set_author(name=f"{person} Has Been added to Purgatory", icon_url=f"{person.avatar_url}")
        embed.set_footer(text='Go tell your mom about it')

        await ctx.send(embed=embed)
        await asyncio.sleep(sec)

        await person.remove_roles(purg)

        unpurg_embed = discord.Embed(color=discord.Color.from_rgb(0, 0, 225), description="Better be good hooman now")
        unpurg_embed.set_author(name=f"{person} has Now been removed from Purgatory! YAY")
        unpurg_embed.set_footer(text='IKR it took forever')

        await ctx.send(embed=unpurg_embed)

    # unmute command
    @commands.command(aliases=['umute', 'un-mute', 'unm'])
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        await member.send(f" you have unmuted from: - {ctx.guild.name}")
        unmute_embed = discord.Embed(color=discord.Color.from_rgb(0, 0, 225), description="Better be good now")
        unmute_embed.set_author(name=f'{member} Has Now Been Unmuted! YAY')
        unmute_embed.set_footer(text='IKR it took forever')
        await ctx.send(embed=unmute_embed)

    # unpurg command
    @commands.command(aliases=['upurg', 'un-purg'])
    @commands.has_permissions(manage_messages=True)
    async def unpurg(self, ctx, member: discord.Member):

        purgrole = discord.utils.get(ctx.guild.roles, name="Purg")

        await member.remove_roles(purgrole)
        await member.send(f" you have been removed from Purgatory from: - {ctx.guild.name}")
        upurg_embed = discord.Embed(color=discord.Color.from_rgb(0, 0, 225), description="Better be good hooman now")
        upurg_embed.set_author(name=f"{member} has Now been removed from Purgatory! YAY")
        upurg_embed.set_footer(text='IKR it took forever')
        await ctx.send(embed=upurg_embed)


def setup(client):
    client.add_cog(Moderation(client))
