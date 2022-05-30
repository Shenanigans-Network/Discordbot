import discord
from discord.ext import commands
from discord.errors import Forbidden
from bot import bot_version, prefix, embed_color, embed_footer, embed_header, embed_icon


async def send_embed(ctx, embed):
    try:
        await ctx.reply(embed=embed)
    except Forbidden:
        try:
            await ctx.reply("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


class Help(commands.Cog, description="Help and Admin Help Commands for the Bot"):

    def __init__(self, client):
        self.client = client
        self.bot_version = bot_version
        self.prefix = prefix


    @commands.command()
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, ctx, *input):
        """Shows all modules of that bot"""

        owner =  123 # enter your name here
        # owner_name =  # ENTER YOUR USERNAME#1234

        # checks if cog parameter was given
        # if not: sending all modules and commands not associated with a cog
        if not input:
            # checks if owner is on this server - used to 'tag' owner
            try:
                owner = ctx.guild.get_member(owner).mention

            except AttributeError as e:
                owner = owner

            # starting to build embed
            emb = discord.Embed(title='Commands and modules', color=embed_color,
                                description=f'Use `{prefix}help <module>` to gain more information about that module '
                                            f':smiley:\n').set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon)


            # iterating trough cogs, gathering descriptions
            cogs_desc = ''
            for cog in self.client.cogs:
                cogs_desc += f'`{cog}` \n{self.client.cogs[cog].__doc__}\n'
            emb.add_field(name="Prefix", value=f"The prefix is `{prefix}`", inline=True)
            emb.add_field(name="Bot Version", value=f"{bot_version}", inline=True)
            emb.add_field(name="Bot Dev", value="<@837584356988944396>", inline=True)
            emb.add_field(name='Modules', value=cogs_desc, inline=False)

            # integrating trough uncategorized commands
            commands_desc = ''
            for command in self.client.walk_commands():
                # if cog not in a cog
                # listing command if cog name is None and command isn't hidden
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            # adding those commands to embed
            if commands_desc:
                emb.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

            # setting information about author
            emb.add_field(name="About", value="The Moonball bot is a Discord bot made to assist on The Moonball Network's Discord server.")
            emb.set_footer(text=embed_footer)
            emb.set_author(name=embed_header, icon_url=embed_icon)

        # block called when one cog-name is given
        # trying to find matching cog and it's commands
        elif len(input) == 1:

            # iterating trough cogs
            for cog in self.client.cogs:
                # check if cog is the matching one
                if cog.lower() == input[0].lower():

                    # making title - getting description from doc-string below class
                    emb = discord.Embed(title=f'{cog} - Commands', description=self.client.cogs[cog].__doc__,
                                        color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon)

                    # getting commands from cog
                    for command in self.client.get_cog(cog).get_commands():
                        # if cog is not hidden
                        if not command.hidden:
                            emb.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                    # found cog - breaking loop
                    break

            # if input not found
            # yes, for-loops have an else statement, it's called when no 'break' was issued
            else:
                emb = discord.Embed(title="What's that?!",
                                    description=f"I've never heard from a module called `{input[0]}` before :scream:",
                                    color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon)

        # too many cogs requested - only one at a time allowed
        elif len(input) > 1:
            emb = discord.Embed(title="That's too much.",
                                description="Please request only one module at once :sweat_smile:",
                                color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon)

        else:
            emb = discord.Embed(title="It's a magical place.",
                                description="AN ERROR HAS OCCURRED :scream:",
                                color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon)

        # sending reply embed using our own function defined above
        await send_embed(ctx, emb)


def setup(client):
    client.add_cog(Help(client))