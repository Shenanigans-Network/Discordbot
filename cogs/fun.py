import discord, random, asyncio, sqlite3, datetime
from discord.ext import commands
from bot import prefix, embed_header, embed_footer, embed_color, bot_version, embed_icon    # Import bot variables
from bot import checkcommandchannel, checkperm, logger, countadd                                     # Import functions


class Fun(commands.Cog):
    """Fun and Interactive Commands that enrich the server experience"""
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



    @commands.command(name="embed", aliases=['announce, ann'], help=f"Send a nice looking embed with a custom Title and Content. \nSyntax - ```ini\n{prefix}sendembed [title] | [content]```")
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


    @commands.command(name="poll", aliases=['cpoll', 'spoll', 'createpoll', 'sendpoll'], help=f"Create a poll with 2-4 options.\nSyntax - ```ini\n{prefix}poll [number of options] | [poll text]```")
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


    @commands.command(name="coinflip", aliases=['head', 'tail', 'flip', 'flipcoin'], help=f"Flip a coin and get either heads or tails.")
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


    @commands.command(name="avatar", aliases=['pfp'], help=f"Get a user's profile picture. \nSyntax - ```ini\n{prefix}avatar [@user]```")
    async def av(self, ctx):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        mentions = ctx.message.mentions[0] if ctx.message.mentions else ctx.author
        emb = discord.Embed(title="Avatar", color=embed_color, description=f"This is {mentions.name}#{mentions.discriminator}'s avatar!")
        emb.set_image(url=mentions.avatar_url)
        await ctx.reply(embed=emb)
        await logger("f", f"Sent {mentions.name}'s avatar to message of {ctx.author.name}#{ctx.author.discriminator}","fun",f"Sent {mentions.name}'s avatar to message of {ctx.author.name}#{ctx.author.discriminator}")



    @commands.command(name="suggest", aliases=['suggestion', 'createsuggestion'], help=f"Send a suggestion to the server's suggestion channel.\nSyntax - ```ini\n{prefix}suggest [suggestion] | [https://image.url.png (optional)]```")
    async def sendsuggestion(self, ctx, *data):
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

    async def check_for_birthday(self):
        now = datetime.datetime.now()
        curmonth = now.month
        curday = now.day
        e = True
        while e:
            # use db
            con = sqlite3.connect('./data/data.db')
            cur = con.cursor()
            cur.execute(f"SELECT * FROM birthdays WHERE month={curmonth} AND day={curday}")
            birthdays = cur.fetchall()
            con.close()
            if birthdays:
                for member in birthdays:
                    try:
                        await self.client.get_user(member).send("Happy birthday!")
                        # get birthday role
                        role = discord.utils.get(self.client.get_guild(894902529039687720).roles, name="🎉Happy Birthday!🎉")
                        await self.client.get_user(member).add_roles(role)
                    except:
                        pass
            await asyncio.sleep(86400)  # task runs every day


    @commands.command(name="set-birthday", aliases=["setbday"], help=f"Sets your Birthday. Syntax - \n```ini\n{prefix}set-birthday [day]/[month]```")
    async def setbirthday(self, ctx, *data):
        disc_id = ctx.message.author.id
        _list = " ".join(data).split('/')
        if 32 > int(_list[0]) < 1 < int(_list[1]) < 13:
            await ctx.send("Invalid Date. Please use DD/MM format.")
            return
        con = sqlite3.connect('./data/data.db')
        cur = con.cursor()
        cur.execute(f"SELECT * FROM birthdays WHERE disc_id = {disc_id}")
        data = cur.fetchone()
        action = "set"
        if data is None:
            cur.execute(f"INSERT INTO birthdays VALUES ({disc_id}, {_list[0]}, {_list[1]})")
        else:
            action = "updated"
            cur.execute(f"UPDATE birthdays SET day = {_list[0]}, month = {_list[1]} WHERE disc_id = {disc_id}")
        con.commit()
        con.close()

        emb = discord.Embed(title="Birthday", color=embed_color, description=f"Successfully {action} your birthday!")
        emb.add_field(name="User", value=f"`{ctx.author.name}#{ctx.author.discriminator}`", inline=True)
        emb.add_field(name="Birthday", value=f"`{_list[0]}/{_list[1]}`", inline=True)
        emb.set_footer(text=embed_footer)
        emb.set_author(name=embed_header, icon_url=embed_icon)
        await ctx.reply(embed=emb)
        await logger("f", f"Set {ctx.author.name}'s birthday to {_list[0]}/{_list[1]}", "fun", f"Set {ctx.author.name}'s birthday to {_list[0]}/{_list[1]}")




    @commands.command(name="remove-birthday", aliases=["removebday"], help=f"Removes your Birthday.")
    async def removebirthday(self, ctx):
        # Removes the birthday from the database
        disc_id = ctx.message.author.id
        con = sqlite3.connect('./data/data.db')
        cur = con.cursor()
        cur.execute(f"SELECT * FROM birthdays WHERE disc_id = {disc_id}")
        data = cur.fetchone()
        if data is None:
            await ctx.reply("You don't have a birthday set!")
            return
        else:
            cur.execute(f"DELETE FROM birthdays WHERE disc_id = {disc_id}")
            con.commit()
            await ctx.reply("Birthday removed!")


    # if __name__ == "__main__":
    #     self.bg_task = self.loop.create_task(self.check_for_birthday())


def setup(client):
    client.add_cog(Fun(client))
