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
from backend import prefix, embed_header, embed_footer, embed_color, bot_version, embed_icon, server_list, welcome_channel, embed_url, suggestion_channel, roles_synced, guild_id, member_role, general_channel  # Import bot variables
from backend import logger, serverstatus, get_con, sendcmd, ip_embed, version_embed, log    # Import bot functions


class Listeners(commands.Cog):
    """Event Listeners for the Bot."""
    def __init__(self, client):
        self.client = client
        self.embed_icon = embed_icon
        self.embed_header = embed_header
        self.embed_footer = embed_footer
        self.prefix = prefix
        self.bot_version = bot_version
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
        # await self.call_functions()



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





    # Runs every 1 day
    @tasks.loop(seconds=86400)
    async def check_for_birthday(self):
        log.debug("Birthday Checker Started")
        now = datetime.datetime.now()
        curmonth = now.month
        curday = now.day
        self.cur.execute(f"SELECT * FROM birthdays WHERE month={curmonth} AND day={curday}")
        birthdays = self.cur.fetchall()
        if birthdays:
            for birthday in birthdays:
                user = self.client.get_user(int(birthday[0]))
                log.debug(f"Today is {curmonth}/{curday} and {user.id} has a birthday!")
                try:
                    await user.send("Happy birthday! :tada:")
                    log.debug("Sent birthday message to " + str(user))
                    await self.client.get_channel(int(welcome_channel)).send(f"<@{int(birthday[0])}> has had their birthday today! :tada:")
                except Exception as e:
                    log.error(f"Error while sending birthday message and Giving role to {user.id}. Error: {str(e)}")
        else:
            log.debug("No birthdays today.")


    @tasks.loop(seconds=100)
    async def check_reminders(self):
        log.debug("Reminder Check Started")

        self.cur.execute(f"SELECT * FROM reminders")
        for r in self.cur.fetchall():    # For each reminder
            if round(int(r[2]), -2) <= round(int(time.time()), -2): # Round to nearest 10s place, and compare to current time
                log.debug(f"Found an upcoming reminder in these 100 seconds.")
                for i in range(100):    # For each second
                    await self.remind()
                    await asyncio.sleep(1)  # task runs every second
                continue


    # Database Format => id, user_id, time, author_id, message
    #                     0    1        2      3           4

    async def remind(self):
        self.cur.execute(f"SELECT * FROM reminders WHERE time <= {int(time.time())}")
        reminders = self.cur.fetchall()
        if not reminders:   # If there are no reminders
            return

        r_embed = discord.Embed(title="Reminder", description="This is a reminder!", color=embed_color)
        r_embed.set_footer(text=embed_footer)
        r_embed.set_author(name=embed_header, icon_url=embed_icon)

        for reminder in reminders:  # For each reminder
            if not int(reminder[3]) == int(reminder[1]):    # If the reminder has been sent from someone else
                r_embed.add_field(name="Sender", value=f"<@{reminder[3]}>", inline=False)
            user = self.client.get_user(int(reminder[1]))

            if reminder[4]: # If the reminder has a message
                r_embed.add_field(name="Message", value=f"`{reminder[4]}`", inline=False) # Adds the message to the embed

            try:    # Send the reminder
                await user.send(embed=r_embed) # Sends the reminder to the user
            except Exception as e:  # If I couldn't DM the user
                await self.client.get_guild(int(guild_id)).get_channel(int(general_channel)).send(f"Hey {user.mention}! Couldn't DM you your reminder.", embed=r_embed)
                log.error(f"Error while DMing reminder to {user.id}. Error: {str(e)}")

            await logger("f", f"Sent reminder from `{reminder[3]}` to `{user}`", self.client)
            self.cur.execute(f"DELETE FROM reminders WHERE id={reminder[0]}")
            self.con.commit()










    @tasks.loop(seconds=100)
    async def check_giveaway(self):
        log.debug("Giveaway Checker Started.")

        self.cur.execute(f"SELECT * FROM giveaways")
        giveaways = self.cur.fetchall()
        log.debug("Upcoming Giveaways" + str(giveaways))
        for g in giveaways:    # For each reminder
            if round(int(g[3]), -2) <= round(int(time.time()), -2): # Round to nearest 10s place, and compare to current time
                log.debug(f"Found an upcoming giveaway in these 100 seconds.")
                for i in range(100):    # For each second
                    await self.giveaway()
                    await asyncio.sleep(1)  # task runs every second
                continue


    async def giveaway(self):
        self.cur.execute(f"SELECT * FROM giveaways WHERE end_time <= {int(time.time())}")
        giveaways = self.cur.fetchall()
        if giveaways:   # If there are giveaways
            for g in giveaways:         # For each giveaway that has ended
                await self.get_winner(g)




    async def get_winner(self, g):
        self.cur.execute(f"SELECT * FROM giveaways WHERE id={g[0]}")
        d = self.cur.fetchone()
        if d[5] == d[6]:
            return
        # Database Format => id, host_id, channel_id, duration, prize, selected_id, winner_id
        #                     0     1       2           3           4         5          6
        channel = self.client.get_channel(int(g[2]))  # Gets the channel from the giveaway
        async for message in channel.history(limit=1):  # Gets the last message in the channel

            if message.author.id != self.client.user.id:  # If the (giveaway)message is from the bot\
                self.cur.execute(f"DELETE FROM giveaways WHERE id={g[0]}")
                self.con.commit()
                return "giveaway_not_found"

            if not message.reactions:  # If the message has reactions
                self.cur.execute(f"DELETE FROM giveaways WHERE id={g[0]}")
                self.con.commit()
                return "no_reactions"

            for reaction in message.reactions:  # For each reaction
                if reaction.emoji == "🎉":  # If the reaction is the "🎉" emoji
                    users = await reaction.users().flatten()  # Gets all the users that have reacted to the message
                    if not len(users) > 1:  # If there are users that have reacted to the message
                        return "only_one_react"

                    self.cur.execute(f"SELECT * FROM giveaways WHERE id={g[0]}")
                    giveaway = self.cur.fetchone()
                    if not giveaway:  # If the giveaway doesn't exist
                        return "giveaway_not_found"

                    if giveaway[5] == giveaway[6]:  # If the giveaway has not been selected
                        self.cur.execute(f"UPDATE giveaways SET selected_id={users[0].id} WHERE id={g[0]}")
                        self.con.commit()
                        return "giveaway_winner_already_selected"

                    while True:   # While the selected has not redeemed
                        self.cur.execute(f"SELECT * FROM giveaways WHERE id={g[0]}")
                        giveaway = self.cur.fetchone()
                        if giveaway[5] == giveaway[6]:  # If the selected has redeemed the giveaway
                            self.cur.execute(f"DELETE FROM giveaways WHERE id={g[0]}")
                            self.con.commit()
                            return "giveaway_winner_selected"

                        winner = random.choice(users)
                        while (winner.id == self.client.user.id) and not (str(winner.id) == giveaway[5]):    # If the winner is not the bot
                            winner = random.choice(users)

                        cur_time = int(time.time())
                        self.cur.execute(f"UPDATE giveaways SET selected={winner.id} WHERE id={g[0]}")
                        self.con.commit()
                        await channel.send(f"{winner.mention} you have won the giveaway! To redeem the prize, type `/giveaway redeem {g[0]}`. Your time ends  <t:{cur_time + 7200}:R>")
                        await asyncio.sleep(7200)   # Sleep for 2 hours


    @check_reminders.before_loop
    @check_for_birthday.before_loop
    @check_giveaway.before_loop
    async def before_my_task(self):
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(Listeners(client))

