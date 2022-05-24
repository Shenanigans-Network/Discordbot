import discord, random, aiohttp, io, asyncio
from discord.ext import commands
from bot import prefix, embed_header, embed_footer, embed_color, bot_version, embed_icon    # Import bot variables
from bot import checkcommandchannel, checkperm, logger, countadd                                     # Import functions


class Fun(commands.Cog):
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
        global embed_log, suggestion_channel
        embed_log = self.client.get_channel(960204173989789736)
        suggestion_channel = self.client.get_channel(960203053103972403)
        print("Cog : Fun.py Loaded")



    @commands.command(aliases=['announce, ann'])
    async def sendembed(self, ctx, *data):
        if await checkperm(ctx, 0): return
        try:
            data = " ".join(data).split(' | ')  # Input Splitter
            a = data[1].replace(" nl ", " \n")
            syntax_error = False
            if len(data) != 2:  # verifying complete syntax
                syntax_error = True
                await ctx.send(f"The syntax is as follows: `{prefix}embed <title> | <description>`")
                await ctx.add_reaction("<:cross_bot:953561649254649866>")
            if syntax_error:
                return
        except:
            await ctx.send(f"Could not send the Embed. An error occurred. Re-Check the syntax or read the embed help page with `{prefix}help embed`")
            return
            # Embed Builder
        announcement = discord.Embed(title=f"Embed by {ctx.author.name}#{ctx.author.discriminator}", url="https://moonball.io", color=embed_color)
        announcement.add_field(name=f"{data[0]}", value=f"{a}", inline=True)
        announcement.set_footer(text=embed_footer)
        try:  # Try to send the embed
            await ctx.send(embed=announcement)
            await embed_log.send(embed=announcement)
            await ctx.message.delete()  # delete original
        except:
            await ctx.send(f"Could not send the Embed. An error occurred. Re-Check the syntax or read the embed help page with `{prefix}help embed`")
            return
        await logger("f", f"Sent Embed (Embed Creator) to message of {ctx.author.name}#{ctx.author.discriminator}","fun",f"Sent Embed (Embed Creator) to message of {ctx.author.name}#{ctx.author.discriminator}")  # Logs to Log channel


    @commands.command(aliases=['cpoll', 'spoll', 'createpoll', 'sendpoll'])
    async def poll(self, ctx, *data):
        if await checkperm(ctx, 0): return
        try:
            data = " ".join(data).split(' | ')  # Input Splitter
            reaction_count = int(data[0])
            content = data[1].replace(" nl ", " \n")
        except:
            await ctx.send(f"There was an error! The Syntax is perhaps incorrect. The correct Syntax is ```ini\n{prefix}poll [number of options] | [Your poll Text here]```\n For more, check out `{prefix}help poll`.")
            return
            # The embed
        p_embed = discord.Embed(title=f"Poll", url="https://moonball.io", color=embed_color)
        p_embed.add_field(name=f"Poll by {ctx.author.name}#{ctx.author.discriminator}", value=f"{content}", inline=True)
        p_embed.set_footer(text=f"{embed_footer}")
        if reaction_count > 4:  # Check if number of reactions is more than 4
            await ctx.send("Sorry, You can't have more than 4 options in a Poll")
            return
        elif reaction_count < 2:  # Check if number of reactions is less than 2
            await ctx.send("Sorry, You can't have less than 2 options in a Poll")
            return

        p = await ctx.send(embed=p_embed)  # Sending the Embed
        await p.add_reaction("<:1_bot:957922958502952981>")  # Adding 1 reaction
        await p.add_reaction("<:2_bot:957922954119888917>")  # Adding 2 reaction
        if int(reaction_count) == 3:
            await p.add_reaction("<:3_bot:957922953893384192>")  # Checking if number is 3, if yes add 3 reaction
        elif int(reaction_count) == 4:  # Checking of the number is 4
            await p.add_reaction("<:3_bot:957922953893384192>")  # Adding 3 reaction
            await p.add_reaction("<:4_bot:957922953381707797>")  # Adding 4 reaction
        await ctx.author.send(f"Your Poll was sent!")
        await logger("f", f"Sent Poll embed to message of {ctx.author.name}#{ctx.author.discriminator}", "fun", f"Sent Poll embed to message of {ctx.author.name}#{ctx.author.discriminator}")  # Logs to Log channel


    @commands.command(aliases=['head', 'tail', 'flip', 'flipcoin'])
    async def coinflip(self, ctx):  # Coin Flip Command
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        value = random.choice(["heads", "tails"])
        embed = discord.Embed(title="Coin Flip", description=f"{ctx.author.mention} Flipped a coin!, They got **{value.capitalize()}**", color=embed_color)
        if value == "heads":
            embed.set_image(url="https://cdn.discordapp.com/attachments/951055432833695767/960211489254436935/head.png")  # Setting head image
        else:
            embed.set_image(url="https://cdn.discordapp.com/attachments/951055432833695767/960211488772083752/tail.png")  # Setting tails image
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.set_footer(text=embed_footer)
        await ctx.send(embed=embed)
        await logger("f", f'Sent Coin Flip result to message of {ctx.author.name}#{ctx.author.discriminator}', "fun",f'Sent Coin Flip result to message of {ctx.author.name}#{ctx.author.discriminator}')


    @commands.command(aliases=['pfp', 'avatar'])
    async def av(self, ctx, *, user: discord.User = None):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        pfp_format = "gif"
        user = user or ctx.author
        if not user.is_avatar_animated():
            pfp_format = "png"
        avatar = user.avatar_url_as(format=pfp_format if pfp_format != "gif" else None)
        async with aiohttp.ClientSession() as session:
            async with session.get(str(avatar)) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.reply(file=discord.File(file, f"Avatar.{pfp_format}"))
        await logger("i", f"Sent {ctx.author.name}'s avatar to message of {ctx.author.name}#{ctx.author.discriminator}","fun",f"Sent {ctx.author.name}'s avatar to message of {ctx.author.name}#{ctx.author.discriminator}")


    @commands.command(aliases=['suggestion', 'createsuggestion'])
    async def suggest(self, ctx, *data):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        data = " ".join(data).split(' | ')  # Input Splitter
        # if data[0] == " " or "": # Checks if the first input is empty
        #     await ctx.send("Please enter a suggestion!")
        #     return
        if len(data) != 1:  # Checks if there is more than one input
            if not data[1].startswith("https://") or data[1].startswith(
                    "http://"):  # Checks if the second input starts with https://
                await ctx.send("0- Please enter a valid image link!")
                return
            # elif not data[1].endswith(".png") or not data[1].endswith(".jpg") or not data[1].endswith(".jpeg"): # Checks if the second input ends with .png, .jpg or .jpeg
            #     await ctx.send("1- Please enter a valid image link!")
            #     return
        s = data[0].replace(" nl ", " \n")  # Replacing nl with \n
        # The embed
        cat = "s"
        s_embed = discord.Embed(title=f"Suggestion", url="https://moonball.io", color=embed_color)
        s_embed.add_field(name=f"Submitted by {ctx.author.name}#{ctx.author.discriminator}",
                          value=f"Suggestion #{countadd(cat)}\n{s}", inline=True)
        if len(data) > 1: s_embed.set_image(url=data[1])  # Setting image
        s_embed.set_footer(text=embed_footer)
        s = await suggestion_channel.send(embed=s_embed)
        # Adding reactions
        await s.add_reaction("<:tick_bot:953561636566863903>")  # Adding tick reaction
        await s.add_reaction("<:cross_bot:953561649254649866>")  # Adding cross reaction
        await embed_log.send(embed=s_embed)  # Sending it to the Logs channel
        await ctx.reply(f"Your Suggestion was sent! Check <#960203053103972403> to see how its doing!")
        print(f"Sent {ctx.author.name}'s suggestion to the suggestion channel!")


    # @commands.command(aliases=['cleardms'])
    # async def cleardm(self, ctx):
    #     messages_to_remove = 1000
    #
    #     async for message in self.client.get_user(ctx.user.id).history(limit=messages_to_remove):
    #         if message.author.id == self.client.user.id:
    #             await message.delete()
    #             await asyncio.sleep(0.5)

def setup(client):
    client.add_cog(Fun(client))
