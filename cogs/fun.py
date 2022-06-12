import discord, random, asyncio, sqlite3, datetime, aiohttp, time
from discord.ext import commands
from bot import prefix, embed_header, embed_footer, embed_color, bot_version, embed_icon, guild_id    # Import bot variables
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


    @commands.slash_command(name="embed", description="Sends a nice looking customisable embed", guild_ids=[guild_id])
    async def sendembed(self, ctx, title: str, content: str):
        if await checkperm(ctx, 0): return
        announcement = discord.Embed(title=f"Embed by {ctx.author.name}#{ctx.author.discriminator}", url="https://moonball.io", color=embed_color)
        announcement.add_field(name=title, value=content.replace(" nl", "\n"), inline=True)
        announcement.set_footer(text=embed_footer)
        try:  # Try to send the embed
            await ctx.respond(embed=announcement)
            await embed_log.send(embed=announcement)
        except:
            await ctx.send(f"Could not send the Embed. An error occurred. Re-Check the syntax or read the embed help page with `{prefix}help embed`")
            return
        await logger("f", f"Sent Embed (Embed Creator) to message of {ctx.author.name}#{ctx.author.discriminator}","fun",f"Sent Embed (Embed Creator) to message of {ctx.author.name}#{ctx.author.discriminator}")  # Logs to Log channel


    @commands.slash_command(name="poll", description="Sends a nice looking customisable poll", guild_ids=[guild_id])
    async def poll(self, ctx, options: int, content: str):
        if await checkperm(ctx, 0): return
            # The embed
        p_embed = discord.Embed(title=f"Poll", url="https://moonball.io", color=embed_color)
        p_embed.add_field(name=f"Poll by {ctx.author.name}#{ctx.author.discriminator}", value=content.replace(" nl", "\n"), inline=True)
        p_embed.set_footer(text=f"{embed_footer}")
        if options > 4:  # Check if number of reactions is more than 4
            await ctx.send("Sorry, You can't have more than 4 options in a Poll")
            return
        elif options < 2:  # Check if number of reactions is less than 2
            await ctx.send("Sorry, You can't have less than 2 options in a Poll")
            return

        p = await ctx.send(embed=p_embed)  # Sending the Embed
        await ctx.respond("Your poll was sent!", ephemeral=True)
        await p.add_reaction("<:1_bot:957922958502952981>")  # Adding 1 reaction
        await p.add_reaction("<:2_bot:957922954119888917>")  # Adding 2 reaction
        if int(options) == 3:
            await p.add_reaction("<:3_bot:957922953893384192>")  # Checking if number is 3, if yes add 3 reaction
        elif int(options) == 4:  # Checking of the number is 4
            await p.add_reaction("<:3_bot:957922953893384192>")  # Adding 3 reaction
            await p.add_reaction("<:4_bot:957922953381707797>")  # Adding 4 reaction

        await logger("f", f"Sent Poll embed to message of {ctx.author.name}#{ctx.author.discriminator}", "fun", f"Sent Poll embed to message of {ctx.author.name}#{ctx.author.discriminator}")  # Logs to Log channel

    @commands.slash_command(name="coinflip", description="Flips a coin", guild_ids=[guild_id])
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
        await ctx.respond(embed=embed, ephemeral=True)
        await logger("f", f'Sent Coin Flip result to message of {ctx.author.name}#{ctx.author.discriminator}', "fun",f'Sent Coin Flip result to message of {ctx.author.name}#{ctx.author.discriminator}')


    @commands.slash_command(name="avatar", description="Gets your avatar", guild_ids=[guild_id])
    async def av(self, ctx):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        emb = discord.Embed(title="Avatar", color=embed_color, description=f"This is {ctx.author.name}#{ctx.author.discriminator}'s avatar!")
        emb.set_image(url=ctx.author.avatar_url)
        await ctx.respond(embed=emb)
        await logger("f", f"Sent {ctx.author.name}'s avatar to message of {ctx.author.name}#{ctx.author.discriminator}","fun",f"Sent {ctx.author.name}'s avatar to message of {ctx.author.name}#{ctx.author.discriminator}")

    
    @commands.slash_command(name="suggest", description="Send a suggestion to the official Suggestion Channel", guild_ids=[guild_id])
    async def sendsuggestion(self, ctx, suggestion: str, image_url: discord.Option(str, "Image Link", required=False, default=None)):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        cat = "s"
        s = suggestion.replace(" nl ", " \n")  # Replacing nl with \n
        s_embed = discord.Embed(title=f"Suggestion", url="https://moonball.io", color=embed_color)
        s_embed.add_field(name=f"Submitted by {ctx.author.name}#{ctx.author.discriminator}",
                          value=f"Suggestion #{countadd(cat)}\n{s} ", inline=True)
        if image_url:
            s_embed.set_image(url=image_url)  # Setting image
        s_embed.set_footer(text=embed_footer)
        s = await suggestion_channel.send(embed=s_embed)
        # Adding reactions
        await s.add_reaction("<:tick_bot:953561636566863903>")  # Adding tick reaction
        await s.add_reaction("<:cross_bot:953561649254649866>")  # Adding cross reaction
        await embed_log.send(embed=s_embed)  # Sending it to the Logs channel
        await ctx.respond(f"Your Suggestion was sent! Check <#960203053103972403> to see how its doing!", ephemeral=True)
        print(f"Sent {ctx.author.name}'s suggestion to the suggestion channel!")



    @commands.slash_command(name="addbirthday", description="Sets your birthday", guild_ids=[guild_id])
    async def setbirthday(self, ctx, day: int, month: int):
        disc_id = ctx.author.id
        if not (0 < int(day) < 32 and 0 < int(month) < 13):
            await ctx.respond("Invalid Date. Please use DD/MM format.", ephemeral=True)
            return
        con = sqlite3.connect('./data/data.db')
        cur = con.cursor()
        cur.execute(f"SELECT * FROM birthdays WHERE disc_id = {disc_id}")
        data = cur.fetchone()
        action = "set"
        if data is None:
            cur.execute(f"INSERT INTO birthdays VALUES ({disc_id}, {day}, {month})")
        else:
            action = "updated"
            cur.execute(f"UPDATE birthdays SET day = {day}, month = {month} WHERE disc_id = {disc_id}")
        con.commit()
        con.close()
        emb = discord.Embed(title="Birthday", color=embed_color, description=f"Successfully {action} your birthday!")
        emb.add_field(name="User", value=f"`{ctx.author.name}#{ctx.author.discriminator}`", inline=True)
        emb.add_field(name="Birthday", value=f"`{day}/{month}`", inline=True)
        emb.set_footer(text=embed_footer)
        emb.set_author(name=embed_header, icon_url=embed_icon)
        await ctx.respond(embed=emb, ephemeral=True)
        await logger("f", f"Set {ctx.author.name}'s birthday to {day}/{month}", "fun", f"Set {ctx.author.name}'s birthday to {day}/{month}")


    @commands.slash_command(name="removebirthday", description="Removes your birthday", guild_ids=[guild_id])
    async def removebirthday(self, ctx):
        # Removes the birthday from the database
        disc_id = ctx.author.id
        con = sqlite3.connect('./data/data.db')
        cur = con.cursor()
        cur.execute(f"SELECT * FROM birthdays WHERE disc_id = {disc_id}")
        data = cur.fetchone()
        if data is None:
            await ctx.respond("You don't have a birthday set!", ephemeral=True)
            return
        else:
            cur.execute(f"DELETE FROM birthdays WHERE disc_id = {disc_id}")
            con.commit()
            await ctx.respond("Birthday removed!", ephemeral=True)


    # if __name__ == "__main__":
    #     self.bg_task = self.loop.create_task(self.check_for_birthday())

    # Upcoming birthdays cmd
    @commands.slash_command(name="upcomingbirthdays", description="Shows all upcoming birthdays", guild_ids=[guild_id])
    async def upcomingbirthdays(self, ctx):
        con = sqlite3.connect('./data/data.db')
        c = con.cursor()
        c.execute("SELECT * FROM birthdays")
        bdays = c.fetchall()

        this_month, upcoming_months, next_year = [], [], []
        current_time = (int(time.strftime("%d")), int(time.strftime("%m")))
        for bday in bdays:
            if current_time[1] == bday[2]:
                if current_time[0] < bday[1]:
                    this_month.append(bday)
                elif current_time[0] > bday[1]:
                    next_year.append(bday)
            elif current_time[1] < bday[2]:
                upcoming_months.append(bday)
            else:
                next_year.append(bday)

        bdays = this_month
        if not this_month:
            bdays = upcoming_months
            if not upcoming_months:
                bdays = next_year
                if not next_year:
                    await ctx.respond("There are no upcoming birthdays!", ephemeral=True)
                    return
        print(bdays)
        # bdays = '\n'.join(bdays)
        # seperates bdays list to two lists, one for the int and another for the day and date
        bdays_int = [bday[0] for bday in bdays]
        bdays_day = [bday[1] for bday in bdays]
        bdays_date = [bday[2] for bday in bdays]

        # merge day and date lists with / seperating them
        bdays_day_date = [f"{day}/{date}" for day, date in zip(bdays_day, bdays_date)]
        for i in bdays:
            print(i)

        emb = discord.Embed(title="Upcoming Birthdays", color=embed_color, description="These are the upcoming birthdays!")
        emb.add_field(name="Birthdays", value=bdays, inline=True)
        emb.set_footer(text=embed_footer)
        emb.set_author(name=embed_header, icon_url=embed_icon)
        await ctx.respond(embed=emb, ephemeral=True)


    @commands.slash_command(name="joke", description="Gets you a joke", guild_ids=[guild_id])
    async def getjoke(self, ctx):
        if await checkperm(ctx, 0): return
        async with aiohttp.ClientSession() as session:
            async with session.get("https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist") as resp: #&type=single
                data = await resp.json()
        if data["type"] == "single":
            emb = discord.Embed(title="Random Joke", color=embed_color, description=f"{data['joke']}")
            emb.set_footer(text=embed_footer)
            emb.set_author(name=embed_header, icon_url=embed_icon)
            await ctx.respond(embed=emb, ephemeral=True)
            await logger("f", f"Sent {ctx.author.name}#{ctx.author.discriminator} a joke", "fun", f"Sent {ctx.author.name}#{ctx.author.discriminator} a joke")
        elif data["type"] == "twopart":
            emb = discord.Embed(title="Random Joke", color=embed_color, description=f"{data['setup']}\n||{data['delivery']}||")
            emb.set_footer(text=embed_footer)
            emb.set_author(name=embed_header, icon_url=embed_icon)
            await ctx.respond(embed=emb, ephemeral=True)
            await logger("f", f"Sent {ctx.author.name}#{ctx.author.discriminator} a joke", "fun", f"Sent {ctx.author.name}#{ctx.author.discriminator} a joke")
        else:
            await ctx.respond("Something went wrong!", ephemeral=True)

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
                    except Exception as e:
                        print(f"There was an error sending a birthday message to {member[0]}\n{e}")
            await asyncio.sleep(86400)  # task runs every day


    @commands.slash_command(name="timestamp", description="Generates you a timestamp", guild_ids=[guild_id])
    async def timestamp(self, ctx, seconds: int):
        if await checkperm(ctx, 0): return
        emb = discord.Embed(title="Timestamp", color=embed_color, description=f"Sends you a custom, variable Discord timestamp.")
        emb.add_field(name="Timestamp", value=f"<t:{int(time.time())+seconds}:R>", inline=False)
        emb.add_field(name="Raw Code", value=f"`<t:{int(time.time())+seconds}:R>`", inline=False)
        await ctx.respond(embed=emb, ephemeral=True)


def setup(client):
    client.add_cog(Fun(client))
