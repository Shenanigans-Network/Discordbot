import discord, sqlite3
from discord.ext import commands
from bot import prefix, embed_header, embed_footer, embed_color, bot_version, embed_icon, guild_id
from bot import checkperm, logger, serverpower, sendcmd, get_permlvl, resetcount, status
from discord.commands import SlashCommandGroup


class Admin(commands.Cog):
    """Commands meant for server admins only."""
    def __init__(self, client):
        self.client = client
        self.embed_color = embed_color
        self.embed_icon = embed_icon
        self.embed_header = embed_header
        self.embed_footer = embed_footer
        self.prefix = prefix
        self.bot_version = bot_version

    admin = SlashCommandGroup("admin", "Various commands meant for server admins only.")

    @commands.Cog.listener()
    async def on_ready(self):
        global embed_log
        embed_log = self.client.get_channel(960204173989789736)
        print("Cog : Admin.py Loaded")


    # @commands.group(pass_context=True, invoke_without_command=True, aliases=['adminhelp'])
    # async def admin(self, ctx):
    #     if await checkperm(ctx, 0): return
    #     if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
    #     Base Admin-Help command embed
        # admin_help = discord.Embed(title="Admin Command", url="https://moonball.io", description=f"Use `{prefix}admin <module>` to execute the command\nModules Include - ```ini\n[changeServerState/css, resetcounter, helpcmd, helppw]```",color=embed_color)
        # admin_help.set_author(name=embed_header, icon_url=embed_icon)
        # admin_help.add_field(name="Prefix", value=f"The prefix is `{prefix}`", inline=True)
        # admin_help.add_field(name="Bot Version", value=f"{bot_version}", inline=True)
        # admin_help.add_field(name="Bot Dev", value="<@837584356988944396>", inline=True)
        # admin_help.add_field(name="Change Server State",value=f"Changes the state of the mentioned server, Can Start/Stop/Restart and Kill any server.\nTo learn more, do `{prefix}admin css`",inline=True)
        # admin_help.add_field(name="Send Command",value=f"Sends a command to any server mentioned with a simple syntax.\nTo learn more, do `{prefix}admin helpcmd`",inline=False)
        # admin_help.add_field(name="Add/Take Money",value=f"Give or Take money to/from a mentioned user (survival).\nTo learn more, do `{prefix}admin helptake/helpgive`",inline=False)
        # admin_help.add_field(name="Change Password",value=f"Changes the password of the user mentioned, right from Discord.\nTo learn more, do `{prefix}admin helppw`",inline=False)
        # admin_help.add_field(name="Permission Level", value=f"The permission level system allows easy management of giving specific command permissions to users.\n `{prefix}admin permlvl` to learn more! ",inline=True)
        # admin_help.add_field(name="Reset Command Counter",value=f"Resets a command counter from the 5 options with a single command.\n To learn more do `{prefix}admin resetcounter`",inline=False)
        # admin_help.set_footer(text=embed_footer)
        # await ctx.reply(embed=admin_help)
        # await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")



    # Send Command to Server
    @admin.command(name="sendcmd", description="ADMIN: Sends Command to the given Backend Server", guild_ids=[guild_id])
    async def sendcmd_admin(self, ctx, server: discord.Option(choices=[
                                                             discord.OptionChoice("Survival", value="survival"),
                                                             discord.OptionChoice("Bedwars", value="bedwars"),
                                                             discord.OptionChoice("Duels", value="duels"),
                                                             discord.OptionChoice("Skyblock", value="skyblock"),
                                                             discord.OptionChoice("Prison", value="prison"),
                                                             discord.OptionChoice("Parkour", value="parkour")
                                                             ]), command: str):
        if await checkperm(ctx, 4): return
        try:
            p = await sendcmd(ctx, server.lower(), command)
        except Exception as e:
            await ctx.respond(f"There was a error while sending the command to the given server\nError - {e}", ephemeral=True)
            return
        if p != "done":
            return
        embed = discord.Embed(title="Admin - Send Command", url="https://moonball.io", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Operation Successful!",value=f"Successfully Sent the Command. Issued by {ctx.author.name}#{ctx.author.discriminator} \n \n**Server** - `{server}` \n **Command** - `{command}`",inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.respond(embed=embed, ephemeral=True)
        await embed_log.send(embed=embed)
        await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} sent a command to `{server}`', "admin",f'{ctx.author.name}#{ctx.author.discriminator} sent a command to `{server}\nCommand - ```ini\n{command}```')



    #
    # == Economy ==
    #
    @admin.command(name="takemoney", description="ADMIN: Take Survival Money from a user", guild_ids=[guild_id])
    async def take_money_admin(self, ctx, user: str,amount: int):  # Take Money Admin Command
        if await checkperm(ctx, 3): return
        if len(user) <= 3 or len(user) >= 16:
            await ctx.send("Invalid Username"); return "invalid_username"
        try:
            p = await sendcmd(ctx, "survival", f"eco take {user} {amount}")
        except Exception as e:
            await ctx.respond(f"There was a error while sending the command\nError - {e}", ephemeral=True)
            return
        if p != "done": return
        embed = discord.Embed(title="Admin - Take Money", url="https://moonball.io", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Operation Successful!",value=f"Successfully executed the command! \n \n**User** - `{user}` \n **Amount** - `{amount}`",inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.respond(embed=embed, ephemeral=True)
        await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} took ${amount} from {user}', "admin",f'{ctx.author.name}#{ctx.author.discriminator} took ${amount} from {user}')


    @admin.command(name="givemoney", description="ADMIN: Give Survival Money to a user", guild_ids=[guild_id])
    async def give_money_admin(self, ctx, user: str, amount: int):  # Take Money Admin Command
        if await checkperm(ctx, 3): return
        if len(user) < 3 or len(user) > 16:
            await ctx.send("Invalid User Name"); return
        try:
            p = await sendcmd(ctx, "survival", f"eco give {user} {amount}")
        except Exception as e:
            await ctx.respond(f"There was a error in sending the command\nError - {e}", ephemeral=True)
            return
        if p != "done": return
        embed = discord.Embed(title="Admin - Take Money", url="https://moonball.io", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Operation Successful!",value=f"Successfully executed the command! \n \n**User** - `{user}` \n **Amount** - `{amount}`",inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.respond(embed=embed, ephemeral=True)
        await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} gave ${amount} to {user}', "admin",f'{ctx.author.name}#{ctx.author.discriminator} gave ${amount} to {user}')


    #
    # == Player Commands ==
    #
    @admin.command(name="changeuserpw", description="ADMIN: Change the password of a given Minecraft User", guild_ids=[guild_id])
    async def changepw_admin(self, ctx, user: str, pw: str):  # Change Password Command
        if await checkperm(ctx, 4): return
        if len(user) <= 3 or len(user) >= 16:
            await ctx.respond("Invalid Username | Username must be between 3 and 16 characters", ephemeral=True)
            return "invalid_username"
        if len(pw) <= 5 or len(pw) >= 30:
            await ctx.respond("Invalid Password | Password must be between 6 and 30 characters", ephemeral=True)
            return "invalid_password"
        cmd = f"authme cp {user} {pw}"
        try:
            p = await sendcmd(ctx, "auth", cmd)
        except:
            await ctx.respond("There was a error in sending the command", ephemeral=True)
            return
        if p != "done": return
        embed = discord.Embed(title="Admin - Change Password", url="https://moonball.io", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Operation Successful!",value=f"Successfully Changed the Password. Issued by {ctx.author.name}#{ctx.author.discriminator} \n \n**Player** - `{user}` \n **Password** - ||{pw}||", inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.respond(embed=embed, ephemeral=True)
        await embed_log.send(embed=embed)  # Sending it to the Logs channel
        await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} changed the password of {user}', "admin",f'{ctx.author.name}#{ctx.author.discriminator} changed the password of {user}')


    @admin.command(name="unreg", description="ADMIN: Unregister the Given User (AuthMe)", guild_ids=[guild_id])
    async def unreg_admin(self, ctx, user: str):  # Change Password Command
        if await checkperm(ctx, 4): return
        if len(user) <= 3 or len(user) >= 16:
            await ctx.send("Invalid Username | Username must be between 3 and 16 characters")
            return "invalid_username"
        try:
            p = await sendcmd(ctx, "auth", f"authme unreg {user}")
        except Exception as e:
            await ctx.respond(f"There was a error in sending the command\nError - {e}", ephemeral=True)
            return
        if p != "done":
            return
        embed = discord.Embed(title="Admin - Change Password", url="https://moonball.io", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Operation Successful!", value=f"Successfully Unregistered User. Issued by {ctx.author.name}#{ctx.author.discriminator} \n \n**Player** - `{user}`", inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.respond(embed=embed, ephemeral=True)
        await embed_log.send(embed=embed)  # Sending it to the Logs channel
        await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} Unregistered {user}', "admin",f'{ctx.author.name}#{ctx.author.discriminator} unregistered {user}')



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
                          server: discord.Option(choices=[
                                                          discord.OptionChoice("Survival", value="survival"),
                                                          discord.OptionChoice("Bedwars", value="bedwars"),
                                                          discord.OptionChoice("Duels", value="duels"),
                                                          discord.OptionChoice("Skyblock", value="skyblock"),
                                                          discord.OptionChoice("Prison", value="prison"),
                                                          discord.OptionChoice("Parkour", value="parkour")
                                                          ]),
                          ):  # Start Server Command
        if await checkperm(ctx, 2): return
        msg = await ctx.respond(embed=discord.Embed(title=f"Power | {server.capitalize()}", description="*Server Power is being changed...*\nPlease hold on!", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)

        e = await status(server)
        serverstatus = e["state"]  # Gets its state

        # Checks if specific conditions are true
        if serverstatus == "running" and power == "start":
            await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}", description=f"**The Server, {server.capitalize()} is already running!**", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        elif serverstatus == "offline" and power == "stop":
            await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}", description=f"**The Server, {server.capitalize()} is already offline!**", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        elif serverstatus == "offline" and power == "kill":
            await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}", description=f"**The Server, {server.capitalize()} is already offline!**", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        elif serverstatus == "starting" and power == "start":
            await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}", description=f"**The Server, {server.capitalize()} is already starting!**", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        elif serverstatus == "stopping" and power == "stop":
            await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}", description=f"**The Server, {server.capitalize()} is already stopping!**", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return

        # Creating button class
        # class View(discord.ui.View):  # Create a class called View that subclasses discord.ui.View
        #     def __init__(self, author):
        #         self.author = author
        #         super().__init__()
        #     @discord.ui.button(label="Confirm!", style=discord.ButtonStyle.red,
        #                        emoji="❗")
        #     async def button_callback(self, button, interaction):
        #         await interaction.response.send_message("You have confirmed the action, beginning")  # Send a message when the button is clicked
        #         try:
        #             await serverpower(server, power)
        #         except Exception as e:
        #             await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}",
        #                                                                 description=f"**There was an error!**\nError - {e}",
        #                                                                 color=embed_color))
        #             return
        #     async def interaction_check(self, interaction: discord.Interaction):
        #         return interaction.user.id == self.author.id
        #
        # playerCount = 0
        # server =     #Gets server player-info from API
        # if power in ["stop", "restart", "kill"]:
        #     if not server in ["proxy", "auth", "limbo", "lobby"]:
        #         try:
        #             playerCount = JavaServer.lookup(serv_ips.get(server)).query().players.online
        #         except Exception as e:
        #             print(f"There was an error trying to get the player count of the server. The panel is perhaps down. I'll continue with it being 0. Error - {e}")
        #
        #     if playerCount != 0:
        #         await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}", description=f"**Warning** - There are {playerCount} players on the server.\nIf you continue, they will be kicked.", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), view=View(ctx.author))
        # else:
        #     try:
        #         a = await serverpower(server, power)
        #     except Exception as e:
        #         await msg.edit_original_message(embed=discord.Embed(title=f"Power | {server.capitalize()}",
        #                                                         description=f"**There was an error!**\nError - {e}",
        #                                                         color=embed_color))
        #         return
        # if e == "exception":
        #     return
        await serverpower(server, power)

        embed = discord.Embed(title="Server Power", url="https://moonball.io/", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name=f'Operation Successful!', value=f'Successfully Started the {server.capitalize()} Server!',inline=False)
        embed.set_footer(text=embed_footer)
        await msg.edit_original_message(embed=embed)
        await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} started server {server}', "admin",f'{ctx.author.name}#{ctx.author.discriminator} started server {server}')




    #
    # == Permission Level ==
    #

    @admin.command(name="setlvl", description="ADMIN: Set the permission level of the mentioned user", guild_ids=[guild_id])
    async def set_level(self, ctx, user: discord.Member, level: int):  # Set Level Command
        if await checkperm(ctx, 4): return
        msg = await ctx.respond(embed=discord.Embed(title="Set Level", description=f"*Setting the level*\nPlease hold on!", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)
        if -1 < int(level) > 5:
            await msg.edit(embed=discord.Embed(title="Set Level - Error", description=f"**Error : Invalid Level**\nThe level of a user may be between `-1` and `5`! or {prefix}admin permlvl", color=embed_color))
            return
        con = sqlite3.connect('./data/data.db')
        cur = con.cursor()
        old_level = await get_permlvl(user.id, class_type=False)
        cur.execute(f"UPDATE perms SET lvl = {level} WHERE user_id = '{user}';")
        con.commit()
        con.close()
        perm_embed = discord.Embed(title="Permission Level", description=f"Permission Level successfully changed!",color=embed_color)
        perm_embed.set_author(name=embed_header, icon_url=embed_icon)
        perm_embed.set_footer(text=embed_footer)
        perm_embed.add_field(name="User",value=f"`{user.name}#{user.discriminator}`", inline=False)
        perm_embed.add_field(name="Old Level", value=f"`{old_level}`", inline=True)
        perm_embed.add_field(name="New Level", value=f"`{level}`", inline=True)
        await msg.edit_original_message(embed=perm_embed)
        await logger("a", f"{user.name}#{user.discriminator}'s permission level has been set to {level} from {old_level}", "admin", f"{user.name}#{user.discriminator}'s permission level has been set to {level} from {old_level}")  # Logs to Log channel


    @commands.slash_command(name="getlvl", description="Get the permission level of the mentioned user", guild_ids=[guild_id])
    async def get_level(self, ctx, user: discord.Member):  # Get Level Command
        if await checkperm(ctx, 0): return
        level_embed = discord.Embed(title="Permission Level", description=f"Got the Permission Level!", color=embed_color)
        level_embed.set_author(name=embed_header, icon_url=embed_icon)
        level_embed.set_footer(text=embed_footer)
        level_embed.add_field(name="User",value=f"`{user.name}#{user.discriminator}`", inline=False)
        level_embed.add_field(name="Level", value=f"`{await get_permlvl(user.id, class_type=False)}`", inline=True)
        await ctx.respond(embed=level_embed, ephemeral=True)
        await logger("a", f"{ctx.author.name}#{ctx.author.discriminator} requested the Permission Level of {user.name}#{user.discriminator}","admin",f"{ctx.author.name}#{ctx.author.discriminator} requested the Permission Level of {user.name}#{user.discriminator}")  # Logs to Log channel


    #
    #   == Connection Commands ==
    #

    @admin.command(name="disconnectuser", description="ADMIN: Disconnect a Minecraft Account", guild_ids=[guild_id])
    async def disconnect(self, ctx, username: str):
        if await checkperm(ctx, 3): return
        msg = await ctx.respond(embed=discord.Embed(title="Disconnect MC Account", description=f"*Disconnecting Account, Please hold on...*", color=embed_color), ephemeral=True)
        con = sqlite3.connect('./data/data.db')
        c = con.cursor()
        c.execute(f"SELECT disc_id FROM connection WHERE mc_username = '{username}';")
        result = c.fetchone()
        if not result:
            await msg.edit_original_message(embed=discord.Embed(title="Disconnect MC Account", description="**There was an Error!**\nYou didn't connect your Minecraft account to your Discord account.", color=discord.colour.Color.red()))
            return
        c.execute(f"DELETE FROM connection WHERE mc_username = '{username}';")
        con.commit()
        con.close()
        discon_embed = discord.Embed(title="Disconnect MC Account", description=f"**Success!**\nThe Minecraft account has been disconnected from the Discord account.", color=embed_color)
        discon_embed.set_footer(text=embed_footer)
        discon_embed.set_author(name=embed_header, icon_url=embed_icon)
        discon_embed.add_field(name="Username", value=f"`{username}`", inline=True)
        await msg.edit_original_message(embed=discon_embed)

    #
    #   == Other ==
    #

    @admin.command(name="resetcount", description="ADMIN: Reset a bot command counter", guild_ids=[guild_id])
    async def reset_admin(self, ctx, counter: discord.Option(choices=[
                                     discord.OptionChoice("All", value="all"),
                                     discord.OptionChoice("Suggestion", value="suggestion"),
                                     discord.OptionChoice("Help", value="help"),
                                     discord.OptionChoice("Info", value="info"),
                                     discord.OptionChoice("Fun", value="fun"),
                                     discord.OptionChoice("Admin", value="admin")
                                     ])
                          ):  # Reset Counter Command
        if await checkperm(ctx, 5): return
        if counter == "all":
            await resetcount(ctx, "all", "all")
        elif counter == "suggestion" or counter == "s":
            await resetcount(ctx, "s", "suggestion")
        elif counter == "help" or counter == "h":
            await resetcount(ctx, "h", "help")
        elif counter == "info" or counter == "i":
            await resetcount(ctx, "i", "info")
        elif counter == "fun" or counter == "f":
            await resetcount(ctx, "f", "fun")
        elif counter == "admin" or counter == "a":
            await resetcount(ctx, "a", "admin")
        emb = discord.Embed(title="Reset Counter", description=f"**Success!**\nThe counter has been reset!", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon)
        await ctx.respond(embed=emb, ephemeral=True)


    @admin.command(name="changepresence", description="ADMIN: Change the bot's Presence", guild_ids=[guild_id])
    async def change_presence(self, ctx, new_presence: str):
        if await checkperm(ctx, 3): return
        await self.client.change_presence(activity=discord.Game(new_presence))  # Set Presence
        await ctx.respond(embed=discord.Embed(title="Change Presence", description="**Success!**\nThe status has been changed.", color=embed_color), ephemeral=True)



#
#
#   Admin Help
#
    """
    @admin.command(aliases=['resetcounter'])  # Help reset counter
    async def resetcounter_admin(self, ctx):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        # Base Admin-Help command embed
        bothelp = discord.Embed(title="Admin Help - Reset Counter", url="https://moonball.io", description=f"Use `{prefix}admin [suffix]` to execute the command.\nResets a specific command counter",color=embed_color)
        bothelp.set_author(name=embed_header, icon_url=embed_icon)
        bothelp.add_field(name="Description", value=f"This command resets one of the 5 total command use counters`",inline=True)
        bothelp.add_field(name="Counter Names", value=f"```ini\n[suggestion, help, info, fun, admin]```", inline=True)
        bothelp.add_field(name="Valid suffixes", value=f"```ini\n[s, h, i, f, a]```", inline=True)
        bothelp.set_footer(text=embed_footer)
        await ctx.reply(embed=bothelp)
        await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")


    @admin.command(aliases=['css', 'changeserverstate'])
    async def changeserverpower_admin(self, ctx):  # Help changeserverstate
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        # Base Admin-Help command embed
        bothelp = discord.Embed(title="Admin Help - Change Server State", url="https://moonball.io", description=f"Use `{prefix}admin [state] [servername]` to execute the command.\nChanges the status of a specific mentioned server ",color=embed_color)
        bothelp.set_author(name=embed_header, icon_url=embed_icon)
        bothelp.add_field(name="Description", value=f"This command changes the power/state of any server", inline=True)
        bothelp.add_field(name="Features",value=f"Start/Stop/Restart or Kill a server just with one single command here on Discord, using a conveniently easy command!",inline=False)
        bothelp.add_field(name="Valid States", value=f"```ini\n[start, stop, restart, kill]```", inline=False)
        bothelp.add_field(name="Valid Servers",value="```ini\n[proxy, limbo, auth, lobby, survival, skyblock, duels, bedwars, parkour]```",inline=False)
        bothelp.set_footer(text=embed_footer)
        await ctx.reply(embed=bothelp)
        await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")  # Logs to Log channel


    @admin.command(aliases=['helpcmd'])
    async def sendcmd_admin_help(self, ctx):  # Help sendcmd
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        # Base Admin-Help command embed
        bothelp = discord.Embed(title="Admin Help - Send Command", url="https://moonball.io", description=f"Use `{prefix}admin cmd [server] | [command]` to execute the command.\nSends a command to the mentioned server ",color=embed_color)
        bothelp.set_author(name=embed_header, icon_url=embed_icon)
        bothelp.add_field(name="Description", value=f"This command can send a command to the mentioned server",inline=True)
        bothelp.add_field(name="Features",value=f"Send a in-game command to any mentioned server here on Discord, using a conveniently easy command and easy syntax!",inline=False)
        bothelp.add_field(name="Valid Servers",value="```ini\n[proxy, limbo, auth, lobby, survival, skyblock, duels, bedwars, parkour]```",inline=False)
        bothelp.add_field(name="Syntax", value=f"```ini\n{prefix}admin cmd [server] | [command here]```", inline=False)
        bothelp.set_footer(text=embed_footer)
        await ctx.reply(embed=bothelp)
        await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")  # Logs to Log channel


    @admin.command(aliases=['helppw'])
    async def password_admin(self, ctx):  # Help password
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        # Base Admin-Help command embed
        bothelp = discord.Embed(title="Admin Help - Change Password", url="https://moonball.io", description=f"Use `{prefix}admin pw [username] [new-password]` to execute the command.\nChanges the password of the mentioned user ",color=embed_color)
        bothelp.set_author(name=embed_header, icon_url=embed_icon)
        bothelp.add_field(name="Description", value=f"This command can change the password of a user", inline=True)
        bothelp.add_field(name="Features",value=f"Change the password of any mentioned user with a simple and easy command, here from Discord.",inline=False)
        bothelp.add_field(name="Syntax", value=f"```ini\n{prefix}admin pw Username NewPassword```", inline=False)
        bothelp.set_footer(text=embed_footer)
        await ctx.reply(embed=bothelp)
        await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")  # Logs to Log channel


    @admin.command(aliases=['helpgive', 'helptake'])
    async def helptg_admin(self, ctx):  # Help password
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        # Base Admin-Help command embed
        bothelp = discord.Embed(title="Admin Help - Give/Take Money", url="https://moonball.io", description=f"Use `{prefix}admin give/take [username] [money]` to execute the command.\nGive or take money from a user",color=embed_color)
        bothelp.set_author(name=embed_header, icon_url=embed_icon)
        bothelp.add_field(name="Description", value=f"This command can give or take money from a user", inline=True)
        bothelp.add_field(name="Features", value=f"Gives or takes money from a specific user.", inline=False)
        bothelp.add_field(name="Syntax", value=f"```ini\n{prefix}admin give/take Username Money```", inline=False)
        bothelp.set_footer(text=embed_footer)
        await ctx.reply(embed=bothelp)
        await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")  # Logs to Log channel


    @admin.command(aliases=['permlvl'])
    async def permlevel_admin(self, ctx):  # Help password
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        # Base Admin-Help command embed
        bothelp = discord.Embed(title="Admin Help - Permission Level", url="https://moonball.io",
                                description=f"For permission level hierarchy list, do `{prefix}admin permlist`\n Use `{prefix}admin setlvl [@mention] [level]` or `{prefix}admin getlvl [@mention]` to execute the command.\nSet/Get the permission level of a user",color=embed_color)
        bothelp.add_field(name="Description",value=f"This command can set or get the permission level of a user. Permission levels are used to give specific command access to different levels of permissions a user can have. Permissions vary between `-1` and `5`, -1 disabling access to all commands and 5 giving access to all.",inline=True)
        bothelp.add_field(name="Features",value=f"Manage usage of commands easily with one command giving a permission level to a user",inline=False)
        bothelp.add_field(name="Syntax",value=f"```ini\n{prefix}admin setlvl [@mention] [level]\n{prefix}admin getlvl [@mention]```",inline=False)
        bothelp.set_footer(text=embed_footer)
        bothelp.set_author(name=embed_header, icon_url=embed_icon)
        await ctx.reply(embed=bothelp)
        await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")  # Logs to Log channel


    @admin.command(aliases=['permlist'])
    async def permlist_admin(self, ctx):  # Help password
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        # Base Admin-Help command embed
        bothelp = discord.Embed(title="Admin Help - Permission Level", url="https://moonball.io",description=f"This command gives the permission list and what commands it lets you use.",color=embed_color)
        bothelp.add_field(name="5 | Developer", value=f"Gives access to all commands", inline=True)
        bothelp.add_field(name="4 | Owner", value=f"Gives access to all commands except\n►Bot Backend/Database",inline=False)
        bothelp.add_field(name="3 | Admin",value=f"Gives access to all commands except\n►affecting Permission Levels\n►Bot Backend/Database",inline=False)
        bothelp.add_field(name="2 | Moderator",value=f"Gives access to all commands except\n►►affecting Permission Levels\n►Bot Backend/Database\n►Kill/Stop Servers\n►Give/Take Money",inline=False)
        bothelp.add_field(name="1 | Helper", value=f"Gives access to\n►Execute command in any channel", inline=False)
        bothelp.add_field(name="0 | User", value=f"Gives access to normal user commands", inline=False)
        bothelp.add_field(name="-1 | Disabled", value=f"Gives access to no command", inline=False)
        bothelp.set_footer(text=embed_footer)
        bothelp.set_author(name=embed_header, icon_url=embed_icon)
        await ctx.reply(embed=bothelp)
        await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")  # Logs to Log channel
"""

def setup(client):
    client.add_cog(Admin(client))

