import discord, sqlite3
from discord.ext import commands
from bot import prefix, embed_header, embed_footer, embed_color, bot_version, embed_icon
from bot import checkcommandchannel, checkperm, logger, serverpower, sendcmd, get_permlvl, resetcount

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.embed_color = embed_color
        self.embed_icon = embed_icon
        self.embed_header = embed_header
        self.embed_footer = embed_footer
        self.prefix = prefix
        self.bot_version = bot_version


    @commands.Cog.listener()
    async def on_ready(self):
        global embed_log
        embed_log = self.client.get_channel(960204173989789736)
        print("Cog : Admin.py Loaded")



    @commands.group(pass_context=True, invoke_without_command=True, aliases=['adminhelp'])
    async def admin(self, ctx):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        # Base Admin-Help command embed
        admin_help = discord.Embed(title="Admin Command", url="https://moonball.io", description=f"Use `{prefix}admin <module>` to execute the command\nModules Include - ```ini\n[changeServerState/css, resetcounter, helpcmd, helppw]```",color=embed_color)
        admin_help.set_author(name=embed_header, icon_url=embed_icon)
        admin_help.add_field(name="Prefix", value=f"The prefix is `{prefix}`", inline=True)
        admin_help.add_field(name="Bot Version", value=f"{bot_version}", inline=True)
        admin_help.add_field(name="Bot Dev", value="<@837584356988944396>", inline=True)
        admin_help.add_field(name="Change Server State",value=f"Changes the state of the mentioned server, Can Start/Stop/Restart and Kill any server.\nTo learn more, do `{prefix}admin css`",inline=True)
        admin_help.add_field(name="Send Command",value=f"Sends a command to any server mentioned with a simple syntax.\nTo learn more, do `{prefix}admin helpcmd`",inline=False)
        admin_help.add_field(name="Add/Take Money",value=f"Give or Take money to/from a mentioned user (survival).\nTo learn more, do `{prefix}admin helptake/helpgive`",inline=False)
        admin_help.add_field(name="Change Password",value=f"Changes the password of the user mentioned, right from Discord.\nTo learn more, do `{prefix}admin helppw`",inline=False)
        admin_help.add_field(name="Permission Level", value=f"The permission level system allows easy management of giving specific command permissions to users.\n `{prefix}admin permlvl` to learn more! ",inline=True)
        admin_help.add_field(name="Reset Command Counter",value=f"Resets a command counter from the 5 options with a single command.\n To learn more do `{prefix}admin resetcounter`",inline=False)
        admin_help.set_footer(text=embed_footer)
        await ctx.reply(embed=admin_help)
        await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")




    # Send Command to Server
    @admin.command(aliases=['cmd', 'send', 'sendcmd'])
    async def sendcmd_admin(self, ctx, *data):  # Send Command Admin Command
        if await checkperm(ctx, 4): return
        data = " ".join(data).split(' | ')  # Input Splitter
        valid_names = ["proxy", "limbo", "parkour", "auth", "lobby", "survival", "skyblock", "duels", "bedwars", "bot"]
        if data[0] not in valid_names:
            await ctx.send("Invalid Name")
            return "invalid_name"
        if data[1] == "":
            await ctx.send("Invalid command to send")
            return "invalid_cmd"
        try:
            p = await sendcmd(ctx, data[0], data[1])
        except:
            await ctx.reply("There was a error in sending the command")
            return
        if p != "done": return
        embed = discord.Embed(title="Admin - Send Command", url="https://moonball.io", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Operation Successful!",value=f"Successfully Sent the Command. Issued by {ctx.author.name}#{ctx.author.discriminator} \n \n**Server** - `{data[0]}` \n **Command** - `{data[1]}`",inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.reply(embed=embed)
        await embed_log.send(embed=embed)
        await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} sent a command to `{data[0]}`', "admin",f'{ctx.author.name}#{ctx.author.discriminator} sent a command to `{data[0]}\nCommand - ```ini\n{data[1]}```')



    #
    # == Economy ==
    #

    @admin.command(aliases=['takemoney', 'take', 'take_money'])
    async def take_money_admin(self, ctx, *data):  # Take Money Admin Command
        if await checkperm(ctx, 3): return
        if len(data[0]) <= 3 or len(data[0]) >= 16:
            await ctx.send("Invalid Username"); return "invalid_username"
        elif not data[1].isnumeric():
            await ctx.send("Invalid Amount"); return "invalid_amount"
        try:
            p = await sendcmd(ctx, "survival", f"eco take {data[0]} {data[1]}")
        except:
            await ctx.reply("There was a error in sending the command")
            return
        if p != "done": return
        embed = discord.Embed(title="Admin - Take Money", url="https://moonball.io", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Operation Successful!",value=f"Successfully took {data[1]} from {data[0]} \n \n**User** - `{data[0]}` \n **Amount** - `{data[1]}`",inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.reply(embed=embed)
        await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} took ${data[1]} from {data[0]}', "admin",f'{ctx.author.name}#{ctx.author.discriminator} took ${data[1]} from {data[0]}')


    @admin.command(aliases=['givemoney', 'give', 'give_money'])
    async def give_money_admin(self, ctx, *data):  # Take Money Admin Command
        if await checkperm(ctx, 3): return
        if len(data[0]) <= 3 or len(data[0]) >= 16:
            await ctx.send("Invalid User Name"); return
        elif not data[1].isnumeric():
            await ctx.send("Invalid Amount"); return
        try:
            p = await sendcmd(ctx, "survival", f"eco give {data[0]} {data[1]}")
        except:
            await ctx.reply("There was a error in sending the command")
            return
        if p != "done": return
        embed = discord.Embed(title="Admin - Take Money", url="https://moonball.io", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Operation Successful!",value=f"Successfully gave {data[1]} from {data[0]} \n \n**User** - `{data[0]}` \n **Amount** - `{data[1]}`",inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.reply(embed=embed)
        await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} gave ${data[1]} to {data[0]}', "admin",f'{ctx.author.name}#{ctx.author.discriminator} gave ${data[1]} to {data[0]}')


    #
    # == Player Commands ==
    #

    @admin.command(aliases=['changepw', 'changepassword', 'pw', 'password'])
    async def changepw_admin(self, ctx, *data):  # Change Password Command
        if await checkperm(ctx, 4): return
        if len(data[0]) <= 3 or len(data[0]) >= 16:
            await ctx.send("Invalid Username | Username must be between 3 and 16 characters")
            return "invalid_username"
        # Format = +admin changepw | username | password
        if len(data[1]) <= 5 or len(data[1]) >= 30:
            await ctx.send("Invalid Password | Password must be between 6 and 30 characters")
            return "invalid_password"
        cmd = f"authme cp {data[0]} {data[1]}"
        try:
            p = await sendcmd(ctx, "auth", cmd)
        except:
            await ctx.reply("There was a error in sending the command")
            return
        if p != "done": return
        embed = discord.Embed(title="Admin - Change Password", url="https://moonball.io", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Operation Successful!",value=f"Successfully Changed the Password. Issued by {ctx.author.name}#{ctx.author.discriminator} \n \n**Player** - `{data[0]}` \n **Password** - ||{data[1]}||",inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.reply(embed=embed)
        await embed_log.send(embed=embed)  # Sending it to the Logs channel
        await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} changed the password of {data[0]}', "admin",f'{ctx.author.name}#{ctx.author.discriminator} changed the password of {data[0]}')


    @admin.command(aliases=['unreg', 'ureg', 'unregister'])
    async def unreg_admin(self, ctx, *data):  # Change Password Command
        if await checkperm(ctx, 4): return
        if len(data[0]) <= 3 or len(data[0]) >= 16:
            await ctx.send("Invalid Username | Username must be between 3 and 16 characters")
            return "invalid_username"
        try:
            p = await sendcmd(ctx, "auth", f"authme unreg {data[0]}")
        except:
            await ctx.reply("There was a error in sending the command")
            return
        if p != "done":
            return
        embed = discord.Embed(title="Admin - Change Password", url="https://moonball.io", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Operation Successful!", value=f"Successfully Unregistered User. Issued by {ctx.author.name}#{ctx.author.discriminator} \n \n**Player** - `{data[0]}`", inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.reply(embed=embed)
        await embed_log.send(embed=embed)  # Sending it to the Logs channel
        await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} Unregistered {data[0]}', "admin",f'{ctx.author.name}#{ctx.author.discriminator} unregistered {data[0]}')



    #
    # == Power Commands ==
    #

    @admin.command(aliases=['startserver', 'serverstart', 'ss', 'start'])
    async def start_admin(self, ctx, *data):  # Start Server Command
        if await checkperm(ctx, 2): return
        msg = await ctx.reply(embed=discord.Embed(title=f"{data[0].capitalize()} Power", description="*Server Power is being changed*\nPlease hold on!", color=embed_color))
        valid_names = ["proxy", "limbo", "auth", "lobby", "survival", "skyblock", "duels", "bedwars", "bot", "parkour"]
        if data[0] not in valid_names:
            await msg.edit(embed=discord.Embed(title=f"{data[0].capitalize()} Power", description=f"**There was an error!**\nInvalid Server name!. `{prefix}help css` to learn more!", color=embed_color))
            return
        try:
            e = await serverpower(data[0], "start", ctx)
        except:
            await msg.edit(embed=discord.Embed(title=f"{data[0].capitalize()} Power - Error", description=f"**There was an error!**\nUse `{prefix}admin css` to learn more~", color=embed_color))
            return
        if e == "exception":
            return
        embed = discord.Embed(title="Server Power", url="https://moonball.io/", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name=f'Operation Successful!', value=f'Successfully Started the {data[0].capitalize()} Server!',inline=False)
        embed.set_footer(text=embed_footer)
        await msg.edit(embed=embed)
        await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} started server {data[0]}', "admin",f'{ctx.author.name}#{ctx.author.discriminator} started server {data[0]}')


    @admin.command(aliases=['stopserver', 'serverstop', 'sts', 'stop'])
    async def stop_admin(self, ctx, *data):  # Stop Server Command
        if await checkperm(ctx, 3): return
        msg = await ctx.reply(embed=discord.Embed(title=f"{data[0].capitalize()} Power",description="*Server Power is being changed*\nPlease hold on!",color=embed_color))
        valid_names = ["proxy", "limbo", "auth", "lobby", "survival", "skyblock", "duels", "bedwars", "bot", "parkour"]
        if data[0] not in valid_names:
            await msg.edit(embed=discord.Embed(title=f"{data[0].capitalize()} Power", description=f"**There was an error!**\nInvalid Server name!. `{prefix}help css` to learn more!", color=embed_color))
            return
        try:
            e = await serverpower(data[0], "stop", ctx)
        except:
            await msg.edit(embed=discord.Embed(title=f"{data[0].capitalize()} Power - Error", description=f"**There was an error!**\nUse `{prefix}admin css` to learn more~", color=embed_color))
            return
        if e == "exception":
            return
        embed = discord.Embed(title="Server Power", url="https://moonball.io/", color=embed_color)
        embed.set_author(name=f"{embed_header}")
        embed.add_field(name=f'Operation Successful!', value=f'Successfully Stopped the {data[0].capitalize()} Server!',inline=False)
        embed.set_footer(text=f"{embed_footer}")
        await msg.edit(embed=embed)
        await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} stopped server {data[0]}', "admin",f'{ctx.author.name}#{ctx.author.discriminator} stopped server {data[0]}')


    @admin.command(aliases=['restartserver', 'serverrestart', 'rs', 'restart'])
    async def restart_admin(self, ctx, *data):  # Restart Server Command
        if await checkperm(ctx, 2): return
        msg = await ctx.reply(embed=discord.Embed(title=f"{data[0].capitalize()} Power",description="*Server Power is being changed*\nPlease hold on!",color=embed_color))
        valid_names = ["proxy", "limbo", "auth", "lobby", "survival", "skyblock", "duels", "bedwars", "bot", "parkour"]
        if data[0] not in valid_names:
            await msg.edit(embed=discord.Embed(title=f"{data[0].capitalize()} Power", description=f"**There was an error!**\nInvalid Server name!. `{prefix}help css` to learn more!", color=embed_color))
            return
        try:
            e = await serverpower(data[0], "restart", ctx)
        except:
            await msg.edit(embed=discord.Embed(title=f"{data[0].capitalize()} Power - Error", description=f"**There was an error!**\nUse `{prefix}admin css` to learn more~", color=embed_color))
            return
        if e == "exception":
            return
        embed = discord.Embed(title="Server Power", url="https://moonball.io/", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name=f'Operation Successful!',value=f'Successfully Restarted the {data[0].capitalize()} Server!', inline=False)
        embed.set_footer(text=embed_footer)
        await msg.edit(embed=embed)
        await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} restarted server {data[0]}', "admin",f'{ctx.author.name}#{ctx.author.discriminator} restarted server {data[0]}')


    @admin.command(aliases=['killserver', 'serverkill', 'sk', 'kill'])
    async def kill_admin(self, ctx, *data):  # Kill Server Command
        if await checkperm(ctx, 3): return
        msg = await ctx.reply(embed=discord.Embed(title=f"{data[0].capitalize()} Power", description="*Server Power is being changed*\nPlease hold on!", color=embed_color))
        valid_names = ["proxy", "limbo", "auth", "lobby", "survival", "skyblock", "duels", "bedwars", "bot", "parkour"]
        if data[0] not in valid_names:
            await msg.edit(embed=discord.Embed(title=f"{data[0].capitalize()} Power", description=f"**There was an error!**\nInvalid Server name!. `{prefix}help css` to learn more!", color=embed_color))
            return
        try:
            e = await serverpower(data[0], "kill", ctx)
        except:
            await msg.edit(embed=discord.Embed(title=f"{data[0].capitalize()} Power - Error", description=f"**There was an error!**\nUse `{prefix}admin css` to learn more~", color=embed_color))
            return
        if e == "exception": return
        killembed = discord.Embed(title="Server Power", url="https://moonball.io/", color=embed_color)
        killembed.set_author(name=embed_header, icon_url=embed_icon)
        killembed.add_field(name=f'Operation Successful!',value=f"Successfully Killed the {data[0].capitalize()} Server!", inline=False)
        killembed.set_footer(text=embed_footer)
        await msg.edit(embed=killembed)
        await logger("a", f'{ctx.author.name}#{ctx.author.discriminator} killed server {data[0]}', "admin",f'{ctx.author.name}#{ctx.author.discriminator} killed server {data[0]}')



    #
    # == Permission Level ==
    #

    @admin.command(aliases=['setlvl', "setlevel", "sl"])
    async def set_level(self, ctx, *data):  # Set Level Command
        if await checkperm(ctx, 4): return
        msg = await ctx.reply(embed=discord.Embed(title="Set Level", description=f"*Setting the level*\nPlease hold on!", color=embed_color))
        # User = ctx.message.mentions[0].id
        # Level = data[0]
        if len(data) != 2:
            await msg.edit(embed=discord.Embed(title="Set Level - Error", description=f"**Error : Missing/Extra Argument**\nUse `{prefix}admin setlvl <user> <level>` to set a user's level or {prefix}admin permlvl", color=embed_color))
            return
        elif not ctx.message.mentions:
            await msg.edit(embed=discord.Embed(title="Set Level - Error", description=f"**Error : Missing @Mention**\nPlease @mention a user too! or {prefix}admin permlvl", color=embed_color))
            return
        elif -1 < int(data[1]) > 5:
            await msg.edit(embed=discord.Embed(title="Set Level - Error", description=f"**Error : Invalid Level**\nThe level of a user may be between `-1` and `5`! or {prefix}admin permlvl", color=embed_color))
            return
        con = sqlite3.connect('./data/data.db')
        cur = con.cursor()
        old_level = await get_permlvl(ctx.message.mentions[0])
        cur.execute(f"UPDATE perms SET lvl = {data[1]} WHERE user_id = {ctx.message.mentions[0].id}")
        con.commit()
        con.close()
        perm_embed = discord.Embed(title="Permission Level", description=f"Permission Level successfully changed!",color=embed_color)
        perm_embed.set_author(name=embed_header, icon_url=embed_icon)
        perm_embed.set_footer(text=embed_footer)
        perm_embed.add_field(name="User",value=f"`{ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator}`", inline=False)
        perm_embed.add_field(name="Old Level", value=f"`{old_level}`", inline=True)
        perm_embed.add_field(name="New Level", value=f"`{data[1]}`", inline=True)
        await msg.edit(embed=perm_embed)
        await logger("a",f"{ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator}'s permission level has been set to {data[1]} from {old_level}","admin",f"{ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator}'s permission level has been set to {data[1]} from {old_level}")  # Logs to Log channel


    @admin.command(aliases=['getlvl', "getlevel", "gl"])
    async def get_level(self, ctx):  # Get Level Command
        level_embed = discord.Embed(title="Permission Level", description=f"Got the Permission Level!", color=embed_color)
        level_embed.set_author(name=embed_header, icon_url=embed_icon)
        level_embed.set_footer(text=embed_footer)
        level_embed.add_field(name="User",value=f"`{ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator}`", inline=False)
        level_embed.add_field(name="Level", value=f"`{await get_permlvl(ctx.message.mentions[0])}`", inline=True)
        await ctx.reply(embed=level_embed)
        await logger("a",f"{ctx.author.name}#{ctx.author.discriminator} requested the Permission Level of {ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator}","admin",f"{ctx.author.name}#{ctx.author.discriminator} requested the Permission Level of {ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator}")  # Logs to Log channel


    #
    #   == Other ==
    #
    @admin.command(aliases=['reset', 'resetcount', "rc"])
    async def reset_admin(self, ctx, *data):  # Reset Counter Command
        if await checkperm(ctx, 5): return
        if data[0] == "all":
            await resetcount(ctx, "all", "all")
        elif data[0] == "suggestion" or data[0] == "s":
            await resetcount(ctx, "s", "suggestion")
        elif data[0] == "help" or data[0] == "h":
            await resetcount(ctx, "h", "help")
        elif data[0] == "info" or data[0] == "i":
            await resetcount(ctx, "i", "info")
        elif data[0] == "fun" or data[0] == "f":
            await resetcount(ctx, "f", "fun")
        elif data[0] == "admin" or data[0] == "a":
            await resetcount(ctx, "a", "admin")


def setup(client):
    client.add_cog(Admin(client))
