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
import random

import discord, sqlite3, time
from discord.ext import commands
from backend import prefix, embed_header, embed_footer, embed_color, embed_icon, guild_id, serv_ips, embed_log, server_list, embed_url
from backend import checkperm, logger, serverpower, sendcmd, get_permlvl, resetcount, status, mc_exists, log
from discord.commands import SlashCommandGroup
from mcstatus import JavaServer


choices = []
for i in server_list:
    choices.append(discord.OptionChoice(i.capitalize().strip(), value=i.strip().lower()))

class Admin(commands.Cog):
    """Commands meant for server admins only."""
    def __init__(self, client):
        self.client = client


        try:
            self.con = sqlite3.connect('./data/data.db')
        except Exception as e:
            log.critical(f"[ADMIN]: Error while connecting to database. Error: {str(e)}")
            exit(2)
        self.cur = self.con.cursor()





    admin = SlashCommandGroup("admin", "Various commands meant for server admins only.")
    giveaway = SlashCommandGroup("giveaway", "Giveaway commands.")


    @commands.Cog.listener()
    async def on_ready(self):
        global _embed_log
        _embed_log = self.client.get_channel(embed_log)
        log.info("Cog : Admin.py Loaded")



    # Send Command to Server
    @admin.command(name="sendcmd", description="ADMIN: Sends Command to the given Backend Server", guild_ids=[guild_id])
    async def sendcmd_admin(self, ctx, server: discord.Option(choices=choices), command: str):
        if await checkperm(ctx, 4): return
        # Check if the corresponding server is online
        server_status = await status(server)
        state = server_status["state"]
        if state != "running":  # If the server is not online, return
            await ctx.respond(f"The `{server}` Server is not online!", ephemeral=True)
            return
        try:    # Send the command to the server
            p = await sendcmd(server.lower(), command)
        except Exception as e:  # If the command fails, return
            await ctx.respond(f"There was a error while sending the command to the given server\nError - {e}", ephemeral=True)
            log.error(f"[ADMIN]: Unable to send command to server. Error: {e}")
            return
        if not p:   # If the sending the command was not successful, return
            await ctx.respond(f"There was a error while sending the command to the given server", ephemeral=True)
            return
        embed = discord.Embed(title="Admin - Send Command", url=embed_url, color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Operation Successful!",value=f"Successfully Sent the Command. Issued by {ctx.author.name}#{ctx.author.discriminator} \n \n**Server** - `{server}` \n **Command** - `{command}`",inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.respond(embed=embed, ephemeral=True)
        await _embed_log.send(embed=embed)
        await logger("a", f'`{ctx.author.name}#{ctx.author.discriminator}` sent a command to `{server}`\nCommand `{command}`', self.client)



    #
    # == Economy ==
    #
    @admin.command(name="takemoney", description="ADMIN: Take Survival Money from a user", guild_ids=[guild_id])
    async def take_money_admin(self, ctx, user: str, amount: int):  # Take Money Admin Command
        if await checkperm(ctx, 3): return
        if not await mc_exists(user): # check if user exists
            await ctx.respond(f"The `{user}` User does not exist!", ephemeral=True)
            return
        server_status = await status("survival")    # check if server is on
        state = server_status["state"]
        if state != "running":  # If the server is not online, return
            await ctx.respond(f"The Survival Server is not online!", ephemeral=True)
            return
        if len(user) <= 3 or len(user) >= 16:   # username validation
            await ctx.send("Invalid Username")
            return
        try:    # Take the money from the user
            p = await sendcmd("survival", f"eco take {user} {amount}")
        except Exception as e:  # If the command fails, return
            await ctx.respond(f"There was a error while sending the command\nError - {e}", ephemeral=True)
            log.error(f"[ADMIN]: Unable to send command to server. Error: {e}")
            return
        if not p: return    # If the sending the command was not successful, return
        embed = discord.Embed(title="Admin - Take Money", url=embed_url, color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Operation Successful!",value=f"Successfully executed the command! \n \n**User** - `{user}` \n **Amount** - `{amount}`",inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.respond(embed=embed, ephemeral=True)
        await logger("a", f'`{ctx.author.name}#{ctx.author.discriminator}` took $`{amount}` from `{user}`', self.client)


    @admin.command(name="givemoney", description="ADMIN: Give Survival Money to a user", guild_ids=[guild_id])
    async def give_money_admin(self, ctx, user: str, amount: int):  # Take Money Admin Command
        if await checkperm(ctx, 3): return
        if not await mc_exists(user): # check if user exists
            await ctx.respond(f"The `{user}` User does not exist!", ephemeral=True)
            return
        server_status = await status("survival")    # check if server is on
        state = server_status["state"]
        if state != "running":
            await ctx.respond(f"The Survival Server is not online!", ephemeral=True)
            return
        if len(user) < 3 or len(user) > 16:  # username validation
            await ctx.send("Invalid User Name")
            return
        try:    # Give the money to the user
            p = await sendcmd("survival", f"eco give {user} {amount}")
        except Exception as e:  # If the command fails, return
            await ctx.respond(f"There was a error in sending the command\nError - {e}", ephemeral=True)
            log.error(f"[ADMIN]: Unable to send command to server. Error: {e}")
            return
        if not p: return    # If the sending the command was not successful, return
        embed = discord.Embed(title="Admin - Take Money", url=embed_url, color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Operation Successful!",value=f"Successfully executed the command! \n \n**User** - `{user}` \n **Amount** - `{amount}`",inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.respond(embed=embed, ephemeral=True)
        await logger("a", f'`{ctx.author.name}#{ctx.author.discriminator}` gave $`{amount}` to `{user}`', self.client)


    #
    # == Player Commands ==
    #
    # Changes a given user's Minecraft AuthMe Password
    @admin.command(name="changeuserpw", description="ADMIN: Change the password of a given Minecraft User", guild_ids=[guild_id])
    async def changepw_admin(self, ctx, user: str, new_password: str):  # Change Password Command
        if await checkperm(ctx, 4): return
        if not await mc_exists(user):   # check if user exists
            await ctx.respond(f"The Minecraft User `{user}` does not exist", ephemeral=True)
            return
        server_status = await status("auth")    # check if server is online
        state = server_status["state"]
        if state != "running":  # If the server is not online, return
            await ctx.respond(f"The Auth Server is not online!", ephemeral=True)
            return
        if len(user) <= 3 or len(user) >= 16:   # username validation
            await ctx.respond("Invalid Username | Username must be between 3 and 16 characters", ephemeral=True)
            return "invalid_username"
        if len(new_password) <= 5 or len(new_password) >= 30:   # password validation
            await ctx.respond("Invalid Password | Password must be between 6 and 30 characters", ephemeral=True)
            return "invalid_password"
        cmd = f"authme cp {user} {new_password}"
        try:    # Change the password of the user
            p = await sendcmd("auth", cmd)
        except Exception as e:  # If the command fails, return
            await ctx.respond("There was a error in sending the command", ephemeral=True)
            log.error(f"[ADMIN]: Error while sending command to Auth Server. Error - {str(e)}")
            return
        if not p: return    # If the sending the command was not successful, return
        embed = discord.Embed(title="Admin - Change Password", url=embed_url, color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Operation Successful!", value=f"Successfully Changed the Password. Issued by {ctx.author.name}#{ctx.author.discriminator} \n \n**Player** - `{user}` \n **Password** - ||`{new_password}`||", inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.respond(embed=embed, ephemeral=True)
        await _embed_log.send(embed=embed)  # Sending it to the Logs channel
        await logger("a", f'`{ctx.author.name}#{ctx.author.discriminator}` changed the password of `{user}`', self.client)


    @admin.command(name="unreg", description="ADMIN: Unregister the Given User (AuthMe)", guild_ids=[guild_id])
    async def unreg_admin(self, ctx, user: str):  # Change Password Command
        if await checkperm(ctx, 4): return
        if not await mc_exists(user):   # check if user exists
            await ctx.respond(f"The Minecraft User `{user}` does not exist", ephemeral=True)
            return
        server_status = await status("auth")    # check if server is online
        state = server_status["state"]
        if state != "running":  # If the server is not online, return
            await ctx.respond(f"The Auth Server is not online!", ephemeral=True)
            return
        if len(user) < 3 or len(user) > 16:   # username validation
            await ctx.send("Invalid Username | Username must be between 3 and 16 characters")
            return "invalid_username"
        try:    # Change the password of the user
            p = await sendcmd("auth", f"authme unreg {user}")
        except Exception as e:  # If the command fails, return
            await ctx.respond(f"There was a error in sending the command\nError - {e}", ephemeral=True)
            log.error(f"[ADMIN]: Error while sending command to Auth Server. Error - {str(e)}")
            return
        if not p:   # If the sending the command was not successful, return
            return
        embed = discord.Embed(title="Admin - Change Password", url=embed_url, color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Operation Successful!", value=f"Successfully Unregistered User. Issued by {ctx.author.name}#{ctx.author.discriminator} \n \n**Player** - `{user}`", inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.respond(embed=embed, ephemeral=True)
        await _embed_log.send(embed=embed)  # Sending it to the Logs channel
        await logger("a", f'`{ctx.author.name}#{ctx.author.discriminator}` Unregistered `{user}`', self.client)



    #
    # == Power Commands ==
    #
    @admin.command(name="power", description="ADMIN: Start/Stop/Restart or kill a given backend server.", guild_ids=[guild_id])
    async def power_admin(self, ctx,
                          power: discord.Option(choices=[
                                                        discord.OptionChoice("Start", value="start"),
                                                        discord.OptionChoice("Stop", value="stop"),
                                                        discord.OptionChoice("Restart", value="restart"),
                                                        discord.OptionChoice("Kill", value="kill"),
                                                        ]),
                          server: discord.Option(choices=choices)):  # Start Server Command
        if await checkperm(ctx, 2): return
        # There are retarded long 1-line embeds have fun editing those.
        msg = await ctx.respond(embed=discord.Embed(title=f"Power | {server.capitalize()}", description="*Server Power is being changed...*\nPlease hold on!", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)
        e = await status(server)
        serverstatus = e["state"]  # Gets its state
        # Checks if specific conditions are true
        if serverstatus == "running" and power == "start":  # Exception 1/4
            await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}", description=f"**The Server, {server.capitalize()} is already running!**", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        elif (serverstatus == "offline" and power == "stop") or (serverstatus == "offline" and power == "kill"):    # Exception 2/4
            await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}", description=f"**The Server, {server.capitalize()} is already offline!**", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        elif serverstatus == "starting" and power == "start":   # Exception 3/4
            await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}", description=f"**The Server, {server.capitalize()} is already starting!**", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        elif serverstatus == "stopping" and power == "stop":    # Exception 4/4
            await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}", description=f"**The Server, {server.capitalize()} is already stopping!**", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return

        class Confirm(discord.ui.View): # Confirm Button Class
            def __init__(self):
                super().__init__()
                self.value = None
                self.author = ctx.author

            # When the confirm button is pressed, set the inner value
            # to `True` and stop the View from listening to more input.
            # We also send the user an ephemeral message that we're confirming their choice.
            @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
            async def confirm_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
                if not interaction.user.id == self.author.id:
                    return await interaction.response.send_message("This button is not for you", ephemeral=True)
                self.value = True
                for child in self.children: # Disable all buttons
                    child.disabled = True
                await interaction.response.edit_message(view=self)
                self.stop()

            # This one is similar to the confirmation button except sets the inner value to `False`.
            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
            async def cancel_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
                if not interaction.user.id == self.author.id:
                    return await interaction.response.send_message("This button is not for you", ephemeral=True)
                self.value = False

                for child in self.children:
                    child.disabled = True

                await interaction.response.edit_message(view=self)
                self.stop()



        embed = discord.Embed(title="Server Power", url="https://moonball.io/", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name=f'Operation Successful!',value=f'Successfully performed the power action on the {server.capitalize()} Server!', inline=False)
        embed.set_footer(text=embed_footer)


        if not power == "start":    # If power is not start
            if not server in ["proxy", "auth", "limbo", "lobby"]:   # If server is not proxy, auth, limbo, lobby, which do not support viewing player count
                try:    # Try to get the player count
                    player_count = JavaServer.lookup(serv_ips[server]).query().players.online  # Gets player count from API

                except Exception as e:  # If it fails, print the error
                    log.warning(f"[ADMIN]: Error while getting player count for {server} in Admin Power command. Error: {e}")
                    player_count = 0

                if not player_count == 0:    # If the player count is not 0
                    view = Confirm()
                    await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}", description=f"**Warning** - There are `{player_count}` players on the server.\nIf you wish to continue, press the button below to confirm", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), view=view)

                    # Wait for the user to confirm their choice
                    await view.wait()
                    if view.value is None:  # Timeout
                        await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}", description=f"Timed out waiting for confirmation, Aborting.", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), view=view)
                        return
                    elif not view.value:    # Cancel
                        await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}", description=f"Cancelled, Aborting.", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), view=view)
                        return
                    elif view.value:        # Confirm
                        await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}", description=f"Confirmed, continuing with the operation.",color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), view=view)

        try:
            res = await serverpower(server, power)
        except Exception as e:
            await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}",description=f"**There was an error!**\nError - {e}",color=embed_color))
            log.error(f"[ADMIN]: Error while trying to change server power. Error: {e}")
            return

        if not res:
            return
        await msg.edit_original_message(embed=embed)
        await logger("a", f'`{ctx.author.name}#{ctx.author.discriminator}` performed a power action on `{server.capitalize()}`', self.client)




    #
    # == Permission Level ==
    #

    @admin.command(name="setlvl", description="ADMIN: Set the permission level of the mentioned user", guild_ids=[guild_id])
    async def set_level(self, ctx, user: discord.Member, level: int):  # Set Level Command
        if await checkperm(ctx, 4): return
        msg = await ctx.respond(embed=discord.Embed(title="Set Level", description=f"*Setting the level*\nPlease hold on!", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)
        if -1 <= int(level) <= 5:   # Level is between -1 and 5
            await msg.edit(embed=discord.Embed(title="Set Level - Error", description=f"**Error : Invalid Level**\nThe level of a user may be between `-1` and `5`! or {prefix}admin permlvl", color=embed_color))
            return
        cur = self.con.cursor()
        old_level = await get_permlvl(user.id, class_type=False)
        cur.execute(f"UPDATE perms SET lvl = {level} WHERE user_id = '{user}';")
        self.con.commit()
        perm_embed = discord.Embed(title="Permission Level", description=f"Permission Level successfully changed!",color=embed_color)
        perm_embed.set_author(name=embed_header, icon_url=embed_icon)
        perm_embed.set_footer(text=embed_footer)
        perm_embed.add_field(name="User",value=f"`{user.name}#{user.discriminator}`", inline=False)
        perm_embed.add_field(name="Old Level", value=f"`{old_level}`", inline=True)
        perm_embed.add_field(name="New Level", value=f"`{level}`", inline=True)
        await msg.edit_original_message(embed=perm_embed)
        await logger("a", f"`{user.name}#{user.discriminator}`'s permission level has been set to `{level}` from `{old_level}`", self.client)  # Logs to Log channel


    @commands.slash_command(name="getlvl", description="Get the permission level of the mentioned user", guild_ids=[guild_id])
    async def get_level(self, ctx, user: discord.Member):  # Get Level Command
        if await checkperm(ctx, 0): return
        level_embed = discord.Embed(title="Permission Level", description=f"Got the Permission Level!", color=embed_color)
        level_embed.set_author(name=embed_header, icon_url=embed_icon)
        level_embed.set_footer(text=embed_footer)
        level_embed.add_field(name="User",value=f"`{user.name}#{user.discriminator}`", inline=False)
        level_embed.add_field(name="Level", value=f"`{await get_permlvl(user.id, class_type=False)}`", inline=True)
        await ctx.respond(embed=level_embed, ephemeral=True)
        await logger("a", f"`{ctx.author.name}#{ctx.author.discriminator}` requested the Permission Level of `{user.name}#{user.discriminator}`", self.client)  # Logs to Log channel


    #
    #   == Connection Commands ==
    #

    @admin.command(name="disconnectuser", description="ADMIN: Disconnect a Minecraft Account", guild_ids=[guild_id])
    async def disconnect(self, ctx, username: str):
        if await checkperm(ctx, 3): return
        msg = await ctx.respond(embed=discord.Embed(title="Disconnect MC Account", description=f"*Disconnecting Account, Please hold on...*", color=embed_color), ephemeral=True)
        self.cur.execute(f"SELECT disc_id FROM connection WHERE mc_username = '{username}';")
        result = self.cur.fetchone()
        if not result:  # If the result is None, the user is not connected
            await msg.edit_original_message(embed=discord.Embed(title="Disconnect MC Account", description="**There was an Error!**\nThere is no Discord account connected to that Minecraft Account.", color=discord.colour.Color.red()))
            return
        self.cur.execute(f"DELETE FROM connection WHERE mc_username = '{username}';")
        self.con.commit()
        discon_embed = discord.Embed(title="Disconnect MC Account", description=f"**Success!**\nThe Minecraft account has been disconnected from the Discord account.", color=embed_color)
        discon_embed.set_footer(text=embed_footer)
        discon_embed.set_author(name=embed_header, icon_url=embed_icon)
        discon_embed.add_field(name="Username", value=f"`{username}`", inline=True)
        await logger("a", f"`{ctx.author.name}#{ctx.author.discriminator}` disconnected `{username}`'s Minecraft Account from Discord", self.client)  # Logs to Log channel
        await msg.edit_original_message(embed=discon_embed)


    @admin.command(name="getconnection", description="ADMIN: Get the Discord Account connected to a Minecraft Account", guild_ids=[guild_id])
    async def get_connection(self, ctx, username: str):
        if await checkperm(ctx, 3): return
        self.cur.execute(f"SELECT disc_id FROM connection WHERE mc_username = '{username}';")
        result = self.cur.fetchone()
        if not result:  # If the result is None, the user is not connected
            await ctx.respond(embed=discord.Embed(title="Get Connection", description="**There was an Error!**\nThere is no Discord account connected to that Minecraft Account.", color=discord.colour.Color.red()))
            return
        self.con.commit()
        get_con_embed = discord.Embed(title="Get Connection", description=f"**Success!**\nGot the account connected.", color=embed_color)
        get_con_embed.set_footer(text=embed_footer)
        get_con_embed.set_author(name=embed_header, icon_url=embed_icon)
        get_con_embed.add_field(name="Discord", value=f"`{result[0]}`", inline=True)
        get_con_embed.add_field(name="Minecraft", value=f"`{username}`", inline=True)
        await ctx.respond(embed=get_con_embed)
        await logger("a", f"`{ctx.author.name}#{ctx.author.discriminator}` requested the Discord account connected to `{username}`", self.client)  # Logs to Log channel

    #
    #   == Other ==
    #

    @admin.command(name="resetcount", description="ADMIN: Reset a bot command counter", guild_ids=[guild_id])
    async def reset_admin(self, ctx, counter: discord.Option(choices=[
                                     discord.OptionChoice("All", value="all"),
                                     discord.OptionChoice("Suggestion", value="s"),
                                     discord.OptionChoice("Help", value="h"),
                                     discord.OptionChoice("Info", value="i"),
                                     discord.OptionChoice("Fun", value="f"),
                                     discord.OptionChoice("Admin", value="a"),
                                     discord.OptionChoice("Minecraft", value="m"),
                                     discord.OptionChoice("Other", value="o"),
                                     ]) ):  # Reset Counter Command
        if await checkperm(ctx, 5): return
        await resetcount(ctx, counter)
        emb = discord.Embed(title="Reset Counter", description=f"**Success!**\nThe counter has been reset!", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon)
        await ctx.respond(embed=emb, ephemeral=True)



    @admin.command(name="changepresence", description="ADMIN: Change the bot's Presence", guild_ids=[guild_id])
    async def change_presence(self, ctx, new_presence: str):
        if await checkperm(ctx, 3): return
        await self.client.change_presence(activity=discord.Game(new_presence))  # Set Presence
        await logger("a", f"`{ctx.author.name}#{ctx.author.discriminator}` changed the bot's presence to `{new_presence}`", self.client)  # Logs to Log channel
        await ctx.respond(embed=discord.Embed(title="Change Presence", description="**Success!**\nThe presence has been changed.", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)


    @admin.command(name="giverole", description="ADMIN: Give a role to a user", guild_ids=[guild_id])
    async def give_role(self, ctx, user: discord.Member, role: discord.Role):
        if await checkperm(ctx, 3): return
        if role.position > ctx.author.top_role.position:  # if the role is above users top role it sends error
            await ctx.respond(embed=discord.Embed(title="Give Role", description="**Error!**\nThe role is above your top role.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)
            return
        elif role in user.roles:
            await ctx.respond(embed=discord.Embed(title="Give Role", description="**Error!**\nThat user already has that role.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)
            return
        await user.add_roles(role)
        embed = discord.Embed(title="Give Role", description=f"**Success!**\nThe role has been given to {user.mention}.", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon)
        await ctx.respond(embed=embed, ephemeral=True)
        await logger("a", f"`{ctx.author.name}#{ctx.author.discriminator}` gave `{user.name}` the role `{role.name}`", self.client)


    @admin.command(name="takerole", description="ADMIN: Take a role from a user", guild_ids=[guild_id])
    async def take_role(self, ctx, user: discord.Member, role: discord.Role):
        if await checkperm(ctx, 3): return
        if not role in user.roles:
            await ctx.respond(embed=discord.Embed(title="Take Role", description="**Error!**\nThat user does not have that role.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)
            return
        if role.id == "894902529039687720": # @everyone
            await ctx.respond(embed=discord.Embed(title="Take Role", description="**Error!**\nYou cannot take the @everyone role.", color=discord.colour.Color.red()), ephemeral=True)
            return
        await user.remove_roles(role)
        embed = discord.Embed(title="Take Role", description=f"**Success!**\nThe role has been taken from {user.mention}.", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon)
        await ctx.respond(embed=embed, ephemeral=True)
        await logger("a", f"`{ctx.author.name}#{ctx.author.discriminator}` took `{user.name}` the role `{role.name}`", self.client)



    @admin.command(name="execsql", description="ADMIN: Execute SQL", guild_ids=[guild_id])
    async def exec_sql(self, ctx, database:
    discord.Option(choices=[
                            discord.OptionChoice("data.db", value="./data/data.db"),
                            discord.OptionChoice("music.db", value="./data/music.db")
                            ]),        sql: str):
        if await checkperm(ctx, 5): return
        db = sqlite3.connect(database)
        _cursor = db.cursor()
        try:
            _cursor.execute(sql)
        except Exception as e:
            await ctx.respond(embed=discord.Embed(title="Execute SQL", description=f"**Error!**\n{e}", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)
            return
        res = _cursor.fetchall()
        if len(res) == 0:
            embed = discord.Embed(title="Execute SQL", description="**Success!**\nNo results found.", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon)
        else:
            embed = discord.Embed(title="Execute SQL", description="**Success!**\nResults found.", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon)
            for i in res:
                embed.add_field(name=str(i[0]), value=str(i[1]), inline=False)
        db.commit()
        db.close()
        await ctx.respond(embed=embed, ephemeral=True)







    # Giveaway Commands
    @giveaway.command(name="start", description="Start a giveaway", guild_ids=[guild_id])
    async def start_giveaway(self, ctx, amount: int,
                       unit: discord.Option(choices=
                       [
                            discord.OptionChoice("Minute(s)", value="m"),
                            discord.OptionChoice("Hour(s)", value="h"),
                            discord.OptionChoice("Day(s)", value="d"),
                            discord.OptionChoice("Week(s)", value="w"),
                            discord.OptionChoice("Month(s)", value="mo"),
                           ]),
                       prize: str):

        if await checkperm(ctx, 1): return
        units = {"m" : 60, "h" : 3600, "d" : 86400, "w": 604800, "mo": 2592000}
        if not amount > 0:
            await ctx.respond("Quantity must be a positive number.", ephemeral=True)
            return
        seconds = units[unit] * amount

        g_embed = discord.Embed(title="Giveaway", description=f"There's a giveaway!", color=embed_color)
        g_embed.add_field(name="Host", value=f"{ctx.author.mention}")
        g_embed.add_field(name="Prize", value=f"`{prize}`")
        g_embed.set_footer(text=embed_footer)
        g_embed.set_author(name=embed_header, icon_url=embed_icon)

        class Confirm(discord.ui.View): # Confirm Button Class
            def __init__(self):
                super().__init__()
                self.value = None
                self.author = ctx.author

            @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
            async def confirm_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
                if not interaction.user.id == self.author.id:
                    return await interaction.response.send_message("This button is not for you", ephemeral=True)
                self.value = True
                for child in self.children: # Disable all buttons
                    child.disabled = True
                await interaction.response.edit_message(view=self)
                self.stop()

            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
            async def cancel_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
                if not interaction.user.id == self.author.id:
                    return await interaction.response.send_message("This button is not for you", ephemeral=True)
                self.value = False
                for child in self.children:
                    child.disabled = True
                await interaction.response.edit_message(view=self)
                self.stop()

        _view = Confirm()
        g_embed.add_field(name="Duration", value=f"`{seconds}s`")

        await ctx.respond("Here is the giveaway, Do you want to post it?", embed=g_embed, ephemeral=True, view=_view)
        g_embed.remove_field(2)
        await _view.wait()
        if _view.value is None:  # timeout
            await ctx.respond("Giveaway Cancelled. Didn't respond in time", ephemeral=True)
            return
        if not _view.value:    # cancel
            await ctx.respond("Giveaway Cancelled", ephemeral=True)
            return
        # await ctx.respond("Confirmed :  Giveaway Starting", ephemeral=True)
        g_embed.add_field(name="Duration", value=f"<t:{int(time.time()) + seconds}:R>")
        g_msg = await ctx.channel.send(embed=g_embed)

        duration = int(time.time()) + seconds

        cur = self.con.cursor()
        r_id = random.randint(1000000000, 9999999999)
        # Database Format => id, host_id, channel_id, duration, prize, selected_id, winner_id
        #                     0     1       2           3           4         5          6
        cur.execute(f'INSERT INTO giveaways VALUES({r_id}, {ctx.author.id}, {ctx.channel.id}, {duration}, "{prize}", " ", "") ;')
        self.con.commit()
        await g_msg.add_reaction("🎉")
        await logger("a", f"`{ctx.author.name}#{ctx.author.discriminator}` started a giveaway for `{prize}`", self.client)






    @giveaway.command(name="redeem", description="Redeem a giveaway", guild_ids=[guild_id])
    async def redeem_giveaway(self, ctx, code: str):
        if await checkperm(ctx, 0): return
        self.cur.execute(f'SELECT * FROM giveaways WHERE id="{code}" ;')
        data = self.cur.fetchone()
        if data is None:
            await ctx.respond("Invalid Code", ephemeral=True)
            return
        if data[6] is not None:
            if data[5] == data[6]:
                await ctx.respond("Giveaway Already Redeemed", ephemeral=True)
                return
        if not ctx.user.id == data[5]:
            await ctx.respond("You are not the winner of this giveaway", ephemeral=True)
            return
        self.cur.execute(f'DELETE FROM giveaways WHERE id={code};')
        self.con.commit()
        await ctx.respond("Giveaway Redeemed", ephemeral=True)
        g_embed = discord.Embed(title="Giveaway", description=f"We have a Winner!", color=embed_color)
        g_embed.add_field(name="Host", value=data[1].mention, inline=True)
        g_embed.add_field(name="Winner", value=ctx.author.mention, inline=True)
        g_embed.add_field(name="Prize", value=f"`{data[4]}`", inline=False)
        g_embed.set_footer(text=embed_footer)
        await self.client.get_channel(data[2]).send(embed=g_embed)
        await logger("a", f"`{ctx.author.name}#{ctx.author.discriminator}` redeemed a giveaway for `{data[4]}`", self.client)




def setup(client):
    client.add_cog(Admin(client))
