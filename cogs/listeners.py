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
#   More info can be found on the GitHub page
#
import random
import discord, datetime, sqlite3, asyncio, time
from discord.ext import commands, tasks
from backend import embed_header, embed_footer, embed_color, embed_icon, server_list, welcome_channel, embed_url, suggestion_channel, roles_synced, guild_id, member_role, general_channel  # Import bot variables
from backend import logger, serverstatus, get_con, sendcmd, ip_embed, version_embed, log    # Import bot functions


class Listeners(commands.Cog):
    """Event Listeners for the Bot."""
    def __init__(self, client):
        self.client = client
        self.guild_id = int(guild_id)

        try:
            self.con = sqlite3.connect('./data/data.db')
        except Exception as err:
            log.error("Error: Could not connect to data.db." + str(err))
            return
        self.cur = self.con.cursor()

        self.check_reminders.start()
        self.check_giveaway.start()
        self.check_for_birthday.start()


    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog : Listeners.py Loaded")



    # On-Message
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot: return  # Checks if message author is a bot.
        if " ip " in f" {ctx.content.lower()} ":
                await ip_embed(ctx)

        if any(word in f" {ctx.content.lower()} " for word in [" version ", " 1.8.9 ", " 1.8 ", " 1.19 "]):
                await version_embed(ctx)

        # On message containing => [on|off|down|up][server]
        if any(word in f" {ctx.content.lower()} " for word in [" up ", " down ", " on ", " off "]): # Checks if the message contains the trigger words
            server = None
            for i in server_list:
                if i in f" {ctx.content.lower()} ":
                    server = i.strip()
                    break
            if server is None:
                return
            await serverstatus(ctx, server, isslash=False)


    # Welcome Announcement
    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_embed = discord.Embed(title=f'Welcome to the Discord Server!', url=embed_url,color=embed_color)
        welcome_embed.add_field(name=embed_header,value=f"<a:malconfetti:910127223791554570> Welcome {member.mention} to the Server! <a:malconfetti:910127223791554570>\n<a:Read_Rules:910128684751544330> Please check out the Server Rules here <#960196761656385546> <a:Read_Rules:910128684751544330>\n <a:hypelove:901476784204288070> Take your Self Roles at <#960196767251570749> <a:hypelove:901476784204288070>\n <:02cool:910128856550244352> Head over to <#960196776579719278> to talk with others! <:02cool:910128856550244352> \n<a:Hearts:952919562846875650> Server info and IP can be found here <#960212885332705290> <a:Hearts:952919562846875650>",inline=True)
        welcome_embed.set_image(url="https://cdn.discordapp.com/attachments/988082459658813490/988083938952093736/welcome-minecraft.gif")
        welcome_embed.set_footer(text=embed_footer)
        # get the welcome channel
        channel = self.client.get_guild(guild_id).get_channel(int(welcome_channel))
        try:
            await channel.send(embed=welcome_embed)
            role = discord.utils.get(self.client.get_guild(self.guild_id).roles, id=member_role)
            await member.add_roles(role)
        except Exception as e:
            log.error(f"[listeners.py] Error in Welcome Announcement: {e}")
            return
        await logger("o", f"Sent Welcome Embed to `{member.name}#{member.discriminator}`", self.client)


    # Disables reacting to both options in the suggestion channel
    @commands.Cog.listener()  # No reacting to both in suggestions
    async def on_raw_reaction_add(self, payload):  # checks whenever a reaction is added to a message
        if payload.channel_id == suggestion_channel:  # check which channel the reaction was added in Suggestion Channel
            channel = await self.client.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            for r in message.reactions:  # iterating through each reaction in the message
                if payload.member in await r.users().flatten() and not payload.member.bot and str(r) != str(payload.emoji):
                    await message.remove_reaction(r.emoji, payload.member)  # Removes the reaction
                    await logger("o", f"Removed Reaction `{r.emoji}` from `{payload.member.name}#{payload.member.discriminator}`", self.client)



    # Rank Sync
    @commands.Cog.listener()    # On role given
    async def on_member_update(self, before, after):

        # If the user is given a role
        if len(before.roles) < len(after.roles):
            new_role = next(role for role in after.roles if role not in before.roles)   # Gets the role that the user just got

            if new_role.name in roles_synced:    # If the user just got a Rank Role
                mc_user = await get_con(int(after.id))  # Gets the user's MC account, if exists
                if mc_user is None: # If the user is not connected
                    return

                role = new_role.name.lower()
                cmd = f"lp user {mc_user} parent add {role}" # Command to give the user the rank
                await sendcmd("auth", cmd)  # Sends the command to LuckPerms server
                await after.send(f"Greetings, You have been given the `{new_role.name.capitalize()}` rank, in-game.") # DMs the user on Discord
                await logger("m", f"Gave `{after.name}#{after.discriminator}` the `{new_role.name.capitalize()}` rank!", self.client)


        # If a role is removed from the user
        if len(before.roles) > len(after.roles):
            removed_role = next(role for role in before.roles if role not in after.roles)   # Gets the role that the user just lost
            if removed_role.name in roles_synced:    # If the user just lost a Rank Role
                mc_user = await get_con(int(before.id))  # Gets the user's MC account, if exists
                if mc_user is None: # If the user is not connected
                    return

                role = removed_role.name.lower()
                cmd = f"lp user {mc_user} parent remove {role}" # Command to remove the rank
                await sendcmd("auth", cmd)  # Sends the command to LuckPerms server
                await before.send(f"Greetings, The `{removed_role.name.capitalize()}` rank has been taken from you, in-game.") # DMs the user on Discord
                await logger("m", f"Removed `{removed_role.name.capitalize()}` Role from `{before.name}#{before.discriminator}`", self.client)


def setup(client):
    client.add_cog(Listeners(client))

