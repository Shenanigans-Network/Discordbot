import discord
from discord.ext import commands
from bot import prefix, embed_header, embed_footer, embed_color, bot_version, embed_icon    # Import bot variables
from bot import checkcommandchannel, checkperm, logger                                      # Import functions

class Help(commands.Cog):
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
        print("Cog : Help.py Loaded")



    @commands.group(pass_context=True, aliases=['info', 'help'], invoke_without_command=True)  # Help Command
    async def bothelp(self, ctx):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        # Base Help command embed
        bothelp = discord.Embed(title="Help Command", url="https://moonball.io",description=f"Use `{prefix}help <module>` to learn more about that specific module\nModules Include - ```ini\n[ping, status, suggestion, ip/version, embed, poll, admin]```", color=embed_color)
        bothelp.set_author(name=embed_header, icon_url=embed_icon)
        bothelp.add_field(name="Prefix", value=f"The prefix is `{prefix}`", inline=True)
        bothelp.add_field(name="Bot Version", value=f"{bot_version}", inline=True)
        bothelp.add_field(name="Bot Dev", value="<@837584356988944396>", inline=True)
        bothelp.add_field(name="Info", value=f"Get info about the Server/Bot with this category of commands.\n Commands include ```ini\n{prefix}[ip, version, ping, status, playerlist]```",inline=True)
        bothelp.add_field(name="Help", value=f"Commands assisting the usage of this Discord Bot or our Minecraft Server can be found in this category. Commands include ```ini\n{prefix}help [ping, status, suggestion, ip/version, embed, poll, coinflip]```",inline=False)
        bothelp.add_field(name="Fun", value=f"The commands which enrich the user experience of being in this Discord Server.\n Commands include ```ini\n{prefix}[suggest, embed, coinflip, poll, avatar)]``` \n", inline=False)
        bothelp.add_field(name="Admin", value=f"Functions and Commands made to modify details about the bot/server are within this category. Only server Staff can access/use them. Commands include ```ini\n{prefix}admin [changeServerState\css, resetcounter, changepassword, unregister, sendCommand, set/get-Level, give/take-Money]```", inline=False)
        bothelp.add_field(name="MC", value=f"Commands that interact with the Minecraft Server can be found in this category.\n Commands include ```ini\n{prefix}mc [connect, password, balance, unregister, pay]```", inline=False)
        bothelp.set_footer(text=embed_footer)
        await ctx.reply(embed=bothelp)
        await logger("h", f"Sent Base Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent Base Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")

    #
    #  == INFO HELP ==
    #

    @bothelp.command(aliases=['ping', 'stats', 'mem', 'stat', 'cpu'])  # Sub-command for help.
    async def ping_bothelp(self, ctx):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        embed = discord.Embed(title="Help Command - Ping", url="https://moonball.io",description="This is the Help category for the `ping` command.", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Description",value="The `ping` Command sends information relating to the bot's status.  ", inline=False)
        embed.add_field(name="Features", value="Can be used to check Latency, CPU Usage, RAM Usage and Uptime.",inline=False)
        embed.add_field(name="Version introduced in", value="\>0.05", inline=False)
        embed.add_field(name="Aliases", value="```ini\n[mem, memory, cpu, ram, lag, ping, stats]```", inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.reply(embed=embed)
        await logger("h", f"Sent Ping-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent Ping-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")


    @bothelp.command(aliases=['status'])  # Sub-command for help.
    async def status_bothelp(self, ctx):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        embed = discord.Embed(title="Help Command - Status", url="https://moonball.io",description="This is the Help category for the `status` command.", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Description",value=f"The `status` command sends info about a specific mentioned server. It can be triggered in 2 ways.\n►**Auto Trigger** - When user says 'up'/'down' and (servername) in the same message.\n►**Manual Trigger** - Using the command `{prefix}servername`", inline=False)
        embed.add_field(name="Features",value="Can be used to check the Status, Players Online, CPU/RAM/Disk and Uptime information for a specific server",inline=False)
        embed.add_field(name="Version introduced in", value="\>0.1", inline=False)
        embed.add_field(name="Aliases",value=f"```ini\n[Proxy/Velocity, Limbo, Auth/AuthServer, Lobby/Hub, Survival, Skyblock, Bedwars/Bedwar/bw, Duels/Duel, Parkour, Prison]```",inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.reply(embed=embed)
        await logger("h", f"Sent Status-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent Status-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")


    @bothelp.command(aliases=['ip', 'version'])  # Sub-command for help.
    async def ip_bothelp(self, ctx):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        embed = discord.Embed(title="Help Command - IP", url="https://moonball.io",description="This is the Help category for the `IP`/`version` command.",color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Description",value=f"The `IP`/`version` Command sends a nice-looking embed to the user.\nCan be triggered in 2 ways\n►**Automatic Trigger** - Any message with the word `ip` or `version` in it will trigger the embed\n**Manual Trigger** - Doing `{prefix}ip` or `{prefix}version` will also send the embed",inline=False)
        embed.add_field(name="Features",value="Posts the IPs/Versions of both Java and Bedrock in a convenient Embed. Reducing the manual work to post the ip message again and again.",inline=False)
        embed.add_field(name="Version introduced in", value="0.01", inline=False)
        embed.add_field(name="Aliases", value="```ini\n[ip, java, bedrock / version]```", inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.reply(embed=embed)
        await logger("h", f"Sent IP-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help", f"Sent IP-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")


    @bothelp.command(aliases=['playerlist', "players"])  # Sub-command for help.
    async def playerlist_bothelp(self, ctx):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        embed = discord.Embed(title="Help Command - Playerlist", url="https://moonball.io",description="This is the Help category for the `playerlist` command.", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Description",
                        value=f"The `playerlist` command sends a nice-looking embed to the user.\nSyntax - `{prefix}players [servername]`",inline=False)
        embed.add_field(name="Version introduced in", value="0.3.9", inline=False)
        embed.add_field(name="Valid Servers",
                        value="```ini\n[limbo, auth, lobby, survival, skyblock, duels, bedwars, parkour]```",inline=False)
        embed.add_field(name="Aliases", value="```ini\n[playerlist, players]```", inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.reply(embed=embed)


    @bothelp.command(aliases=['suggest', 'suggestion'])  # Sub-command for help.
    async def suggest_bothelp(self, ctx):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        embed = discord.Embed(title="Help Command - Suggestion", url="https://moonball.io",description="This is the Help category for the `Suggestion` command.", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Description",value=f"The `Suggest` Command sends a user's suggestion to the <#{self.suggestion_channel}> channel. Reacts to it with <:tick_bot:953561636566863903> and <:cross_bot:953561649254649866> so that it can be voted on and implemented! You can also add a image (jpg, png or jpeg) into the suggestion.\n Syntax - ```ini\n{prefix}suggest [Line 1 nl line 2] | [https://image.link.png]```",inline=False)
        embed.add_field(name="Features",value="It posts your suggestion to the official suggestion channel of the server. Say `nl` within the embed to put the proceeding text in the next line.",inline=False)
        embed.add_field(name="Version introduced in", value="0.2", inline=False)
        embed.add_field(name="Aliases", value="```ini\n[suggest, suggestion, createsuggestion]```", inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.reply(embed=embed)
        await logger("h", f"Sent Suggest-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent Suggest-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")

    #
    #   == FUN HELP ==
    #

    @bothelp.command(aliases=['embed', 'announce', 'ann'])  # Sub-command for help.
    async def embed_bothelp(self, ctx):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        embed = discord.Embed(title="Help Command - Embed", url="https://moonball.io",
                              description="This is the Help category for the `Embed` command.", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Description",
                        value=f"The `Embed` Command creates a nice embed with a simple syntax ```ini\n{prefix}embed [The Embed Title] | [The Embed Content]```\n Use `|` to separate all the 2 arguments.",inline=False)
        embed.add_field(name="Features",
                        value="Posts a Embed with the user's liking's content to any channel Say `nl` within the embed to put the proceeding text in the next line.",inline=False)
        embed.add_field(name="Version introduced in", value="0.0.5", inline=False)
        embed.add_field(name="Aliases", value="```ini\n[ann, announce, embed]```", inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.reply(embed=embed)
        await logger("h", f"Sent Embed-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",
                     f"Sent Embed-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")


    @bothelp.command(aliases=['poll', 'cpoll', 'spoll', 'createpoll', 'sendpoll'])  # Sub-command for help.
    async def poll_bothelp(self, ctx):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        embed = discord.Embed(title="Help Command - Poll", url="https://moonball.io", description="This is the Help category for the `Poll` command.", color=embed_color)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.add_field(name="Description", value=f"The `Poll` Command Sends a multiple option poll with up to 4 options", inline=False)
        embed.add_field(name="Features", value=f"The Poll Command sends a poll with the user's input with up to 4 reactions/options. It has a simple syntax - \n```ini\n{prefix}poll [number of options] | [Your poll Text here]```\nUse `|` to seperate the 2 arguments. Say `nl` within the poll to put the proceeding text in the next line.",inline=False)
        embed.add_field(name="Version introduced in", value="0.2.3", inline=False)
        embed.add_field(name="Aliases", value="```ini\n[cpoll, spoll, createpoll, sendpoll]```", inline=False)
        embed.set_footer(text=embed_footer)
        await ctx.reply(embed=embed)
        await logger("h", f"Sent Poll-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent Poll-Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")


    #
    #
    #   == ADMIN HELP ==
    #
    #

    @bothelp.group(aliases=['resetcounter', 'rc'])  # Help reset counter
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


    @bothelp.group(aliases=['css', 'changeserverstate'])
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


    @bothelp.group(aliases=['helpcmd'])
    async def changecmd_admin(self, ctx):  # Help sendcmd
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        # Base Admin-Help command embed
        bothelp = discord.Embed(title="Admin Help - Send Command", url="https://moonball.io", description=f"Use `{prefix}admin cmd [server] | [command]` to execute the command.\nSends a command to the mentioned server ",color=embed_color)
        bothelp.set_author(name=embed_header, icon_url=embed_icon)
        bothelp.add_field(name="Description", value=f"This command can send a command to the mentioned server",inline=True)
        bothelp.add_field(name="Features",value=f"Send a in-game command to any mentioned server here on Discord, using a conveniently easy command and easy syntax!",inline=False)
        bothelp.add_field(name="Valid Servers",value="```ini\n[proxy, limbo, auth, lobby, survival, skyblock, duels, bedwars, parkour]```",inline=False)
        bothelp.add_field(name="Syntax", value=f"```ini\n{prefix}admin cmd server | command here!```", inline=False)
        bothelp.set_footer(text=embed_footer)
        await ctx.reply(embed=bothelp)
        await logger("h", f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent Admin Help Embed to message of {ctx.author.name}#{ctx.author.discriminator}")  # Logs to Log channel


    @bothelp.group(aliases=['helppw'])
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


    @bothelp.group(aliases=['helpgive', 'helptake'])
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


    @bothelp.group(aliases=['permlvl'])
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


    @bothelp.group(aliases=['permlist'])
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



def setup(client):
    client.add_cog(Help(client))