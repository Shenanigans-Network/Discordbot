import discord
from discord.ext import commands
from bot import prefix, embed_header, embed_footer, embed_color, bot_version, embed_icon    # Import bot variables
from bot import logger, ip_embed, version_embed, serverstatus                               # Import bot functions

class Listeners(commands.Cog):
    """Event Listeners for the Bot."""
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
        global welcome_channel
        welcome_channel = self.client.get_channel(960196760565841941)
        print("Cog : Listeners.py Loaded")

    # On-Message
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot: return  # checks if author is a bot.
        else:
            if " ip " in f" {ctx.content.lower()} ": await ip_embed(ctx)                # On word IP send ip embed
            elif " version " in f" {ctx.content.lower()} ": await version_embed(ctx)    # On word "version" send the version embed

            # elif self.client.user in ctx.mentions:  # Replies to when the Bot in @mentioned
            #     await ctx.reply(f"Hello! my prefix is `{prefix}`. Use `{prefix}help` to view available commands.",delete_after=10.0)
            #     await logger("h", f"Sent Mention message to {ctx.author.name}#{ctx.author.discriminator}", "help",f"Sent mention-message to message of {ctx.author.name}#{ctx.author.discriminator}")

            elif " down " in f" {ctx.content.lower()} " or " up " in f" {ctx.content.lower()} " or " on " in f" {ctx.content.lower()} " or " off " in f" {ctx.content.lower()} ":
                if " proxy " in f" {ctx.content.lower()} ": await serverstatus(ctx, "proxy")
                elif " limbo " in f" {ctx.content.lower()} ": await serverstatus(ctx, "limbo")
                elif " auth " in f" {ctx.content.lower()} " : await serverstatus(ctx, "auth")
                elif " lobby " in f" {ctx.content.lower()} ": await serverstatus(ctx, "lobby")
                elif " survival " in f" {ctx.content.lower()} ": await serverstatus(ctx, "survival")
                elif " bedwars " in f" {ctx.content.lower()} ": await serverstatus(ctx, "bedwars")
                elif " duels " in f" {ctx.content.lower()} ": await serverstatus(ctx, "duels")
                elif " skyblock " in f" {ctx.content.lower()} ": await serverstatus(ctx, "skyblock")
                elif " prison " in f" {ctx.content.lower()} ": await serverstatus(ctx, "prison")
                elif " parkour " in f" {ctx.content.lower()} ": await serverstatus(ctx, "parkour")



    # Welcome Announcement
    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_embed = discord.Embed(title=f'Welcome to the Discord Server!', url="https://moonball.io",color=embed_color)
        welcome_embed.add_field(name="Moonball Network",value=f"<a:malconfetti:910127223791554570> Welcome {member.mention} to the Server! <a:malconfetti:910127223791554570>\n<a:Read_Rules:910128684751544330> Please check out the Server Rules here <#960196761656385546> <a:Read_Rules:910128684751544330>\n <a:hypelove:901476784204288070> Take your Self Roles at <#960196767251570749> <a:hypelove:901476784204288070>\n <:02cool:910128856550244352> Head over to <#960196776579719278> to talk with others! <:02cool:910128856550244352> \n<a:Hearts:952919562846875650> Server info and IP can be found here <#960212885332705290> <a:Hearts:952919562846875650>",inline=True)
        welcome_embed.set_image(url="https://media.discordapp.net/attachments/896348336972496936/952940944175554590/ezgif-1-e6eb713fa2.gif")
        welcome_embed.set_footer(text=embed_footer)
        await welcome_channel.send(embed=welcome_embed)
        role = discord.utils.get(self.client.get_guild(894902529039687720).roles, id=960196710766895134)
        await member.add_roles(role)
        await logger("i", f"Sent Welcome Embed to {member.name}#{member.discriminator}", "info",f"Sent Welcome Embed to {member.name}#{member.discriminator}")


    # Disables reacting to both options in the suggestion channel
    @commands.Cog.listener()  # No reacting to both in suggestions
    async def on_raw_reaction_add(self, payload):  # checks whenever a reaction is added to a message
        if payload.channel_id == 956806563950112848:  # check which channel the reaction was added in Suggestion Channel
            channel = await self.client.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            for r in message.reactions:  # iterating through each reaction in the message
                if payload.member in await r.users().flatten() and not payload.member.bot and str(r) != str(
                        payload.emoji):
                    await message.remove_reaction(r.emoji, payload.member)  # Removes the reaction


    # On command error
    @commands.Cog.listener()  # When user does an invalid command
    async def on_command_error(self, ctx, error):
        if not isinstance(error, commands.CheckFailure):
            embed = discord.Embed(title="Error!", url="https://moonball.io/",description="There was an Error while executing your command.",color=embed_color).set_author(name=embed_header).set_footer(text=embed_footer)
            embed.add_field(name="Here is your Error -", value=f"```ini\n[{str(error)}]```", inline=False)
            if "is not found" in str(error):  # Non-Existent Command
                embed.add_field(name="Here is the command you tried to execute -",value=f"```ini\n[{ctx.message.content}]```", inline=False)
                embed.add_field(name="What This Means",value=f"**Non-Existent Command** : The command you just tried to execute, does not exist!\nUse `{prefix}help` to learn about the available commands!",inline=False)
            elif str(error) == "Command raised an exception: IndexError: list index out of range":  # Bad Syntax
                embed.add_field(name="Here is the command you tried to execute -",value=f"```ini\n[{ctx.message.content}]```", inline=False)
                embed.add_field(name="What This Means",value=f"**Bad Syntax** : The Syntax for this specific command is not right. There may be arguments missing within the command.\nUse `{prefix}help` to learn about the commands and their syntaxes!",inline=False)
            else:
                embed.add_field(name="Here is the command you tried to execute -",value=f"```ini\n[{ctx.message.content}]```", inline=False)
                embed.add_field(name="What This Means",value=f"With so many possible errors, I do not know what the exact error is, without the error code. Please send this error code to the Developer, <@837584356988944396> in DMs for it to be resolved.\nThere is still a chance it may be a syntax error.\nUse `{prefix}help` to learn about the commands and their syntaxes!",inline=False)
            await ctx.author.send(embed=embed)
            await ctx.message.add_reaction("<:cross_bot:953561649254649866>")
            await logger("h", f"Sent Error message to {ctx.author.name}#{ctx.author.discriminator}. Error - {error}","help",f"Sent Error Embed to message of {ctx.author.name}#{ctx.author.discriminator}\nError - ```ini\n{error}```")


def setup(client):
    client.add_cog(Listeners(client))
