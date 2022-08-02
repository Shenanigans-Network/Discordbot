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

import discord, random, sqlite3, aiohttp, time, re, datetime
from discord.ext import commands
from backend import embed_header, embed_footer, embed_color, embed_icon, guild_id, embed_log, suggestion_channel, tick_emoji, cross_emoji, one_emoji, two_emoji, three_emoji, four_emoji   # Import bot variables
from backend import checkperm, logger, countadd, log                                     # Import functions
from discord.commands import SlashCommandGroup



class Fun(commands.Cog):
    """Fun and Interactive Commands that enriches the server experience"""
    def __init__(self, client):
        self.client = client

        try:
            self.con = sqlite3.connect('./data/data.db')
        except Exception as e:
            log.critical(f"[FUN]: Error while connecting to database. Error: {str(e)}")
            exit(2)
        self.cur = self.con.cursor()

    reminder = SlashCommandGroup("reminder", "Reminder related commands.")

    @commands.Cog.listener()
    async def on_ready(self):
        global _embed_log, _suggestion_channel
        _embed_log = self.client.get_channel(embed_log)
        _suggestion_channel = self.client.get_channel(suggestion_channel)
        log.info("Cog : Fun.py Loaded")


    @commands.slash_command(name="embed", description="Sends a nice looking customisable embed", guild_ids=[guild_id])
    async def sendembed(self, ctx,
                        # Title
                        title: discord.Option(description="Title of the Embed", type=str),

                        color: discord.Option(choices=[
                                                    discord.OptionChoice("Blue"),
                                                    discord.OptionChoice("Red"),
                                                    discord.OptionChoice("Yellow"),
                                                    discord.OptionChoice("Green"),
                                                    discord.OptionChoice("Purple"),
                                                    discord.OptionChoice("Pink"),
                                                    discord.OptionChoice("Blurple"),
                                                    discord.OptionChoice("Orange"),
                                                    discord.OptionChoice("Default")
                                                    ]),

                        # Field
                        field_name1: discord.Option(description="Name of the first Field", type=str, default=None),
                        field_value1: discord.Option(description="Value of the first Field", type=str, default=None),

                        description: discord.Option(description="Description of the Embed", type=str, default=None, optional=True),

                        footer: discord.Option(description="Text in the Footer", type=str, default=None, optional=True),

                        # Author
                        author: discord.Option(description="Author of the Embed", type=str, default=None, optional=True),
                        thumbnail: discord.Option(description="URL of the Thumbnail", type=str, default=None, optional=True),

                        # Field 2
                        field_name2: discord.Option(description="Name of the second Field", type=str, default=None, optional=True),
                        field_value2: discord.Option(description="Value of the second Field", type=str, default=None, optional=True),

                        # Field 3
                        field_name3: discord.Option(description="Name of the third Field", type=str, default=None, optional=True),
                        field_value3: discord.Option(description="Value of the third Field", type=str, default=None, optional=True),

                        # Field 4
                        field_name4: discord.Option(description="Name of the fourth Field", type=str, default=None, optional=True),
                        field_value4: discord.Option(description="Value of the fourth Field", type=str, default=None, optional=True),

                        # Footer
                        url: discord.Option(description="URL in the Embed Title", type=str, default=None, optional=True),
                        author_url: discord.Option(description="URL in the Embed Author", type=str, default=None, optional=True),
                        ):

        if await checkperm(ctx, 0): return

        # Colorizer
        color_list = {"Blue": discord.Color.blue(), "Red": discord.Color.red(), "Yellow": discord.Color.yellow(), "Green": discord.Color.green(), "Purple": discord.Color.purple(), "Pink": discord.Color.magenta(), "Blurple": discord.Color.blurple(), "Orange": discord.Color.orange(), "Default": discord.Color.default()}
        color = color_list[color]

        embed = discord.Embed(title=title, color=color)
        if description is not None:
            embed.description = description

        if url is not None:
            # check it is a valid image url with regex
            regex_img = r'^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=.]+(.jpg|.jpeg|.png|.gif|.webp)$'
            if re.match(regex_img, url):
                embed.url = url
        if author is not None:
            if author_url is not None and author is not None:
                # check it is a valid url with regex
                regex = r'^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=.]+$'
                if re.match(regex, author_url):
                    embed.set_author(name=author, url=author_url)
                else:
                    embed.set_author(name=author)
            else:
                embed.set_author(name=author)

        if thumbnail is not None:
            embed.set_thumbnail(url=thumbnail)
        if field_name1 is not None and field_value1 is not None:
            embed.add_field(name=field_name1, value=field_value1, inline=False)
        if field_name2 is not None and field_value2 is not None:
            embed.add_field(name=field_name2, value=field_value2, inline=False)
        if field_name3 is not None and field_value3 is not None:
            embed.add_field(name=field_name3, value=field_value3, inline=False)
        if field_name4 is not None and field_value4 is not None:
            embed.add_field(name=field_name4, value=field_value4, inline=False)
        if footer is not None:
            embed.set_footer(text=footer)
        await ctx.send(embed=embed)
        await ctx.respond("Embed Sent", ephemeral=True)



    @commands.slash_command(name="poll", description="Sends a nice looking customisable poll", guild_ids=[guild_id])
    async def poll(self, ctx,
                    option1: discord.Option(description="First Option", type=str, optional=False, default=None),
                    option2: discord.Option(description="Second Option", type=str, optional=False, default=None),
                    option3: discord.Option(description="Third Option", type=str, optional=True, default=None),
                    option4: discord.Option(description="Fourth Option", type=str, optional=True, default=None)
        ):
        if await checkperm(ctx, 0): return
        if option1 is None and option2 is None:
            await ctx.respond("You need to specify at least two options")
            return
        if option3 is None:
            number = 2
            value = f"{one_emoji} : `{option1}`\n {two_emoji} : `{option2}`"
        elif option4 is None:
            number = 3
            value = f"{one_emoji} : `{option1}`\n {two_emoji} : `{option2}`\n {three_emoji} : `{option3}`"
        else:
            number = 4
            value = f"{one_emoji} : `{option1}`\n {two_emoji} : `{option2}`\n {three_emoji} : `{option3}`\n{four_emoji} : `{option4}`"

        p_embed = discord.Embed(title=f"Poll", url="https://moonball.io", color=embed_color)
        p_embed.add_field(name=f"Poll by {ctx.author.name}#{ctx.author.discriminator}", value=value, inline=True)
        p_embed.set_footer(text=f"{embed_footer}")
        p = await ctx.send(embed=p_embed)  # Sending the Embed
        await ctx.respond("Your poll was sent!", ephemeral=True)
        await p.add_reaction(one_emoji)  # Adding 1 reaction
        await p.add_reaction(two_emoji)  # Adding 2 reaction
        if number > 2:
            await p.add_reaction(three_emoji)  # Checking if number is 3, if yes add 3 reaction
            if number == 4:  # Checking of the number is 4
                await p.add_reaction(four_emoji)  # Adding 4 reaction
        await logger("f", f"Sent Poll embed to message of `{ctx.author.name}#{ctx.author.discriminator}`", self.client)  # Logs to Log channel



    @commands.slash_command(name="coinflip", description="Flips a coin", guild_ids=[guild_id])
    async def coinflip(self, ctx):  # Coin Flip Command
        if await checkperm(ctx, 0): return
        value = random.choice(["heads", "tails"])
        embed = discord.Embed(title="Coin Flip", description=f"{ctx.author.mention} Flipped a coin!, They got **{value.capitalize()}**", color=embed_color)
        if value == "heads":
            embed.set_image(url="https://cdn.discordapp.com/attachments/951055432833695767/960211489254436935/head.png")  # Setting head image
        else:
            embed.set_image(url="https://cdn.discordapp.com/attachments/951055432833695767/960211488772083752/tail.png")  # Setting tails image
        embed.set_author(name=embed_header, icon_url=embed_icon)
        embed.set_footer(text=embed_footer)
        await ctx.respond(embed=embed)
        await logger("f", f'Sent Coin Flip result to message of `{ctx.author.name}#{ctx.author.discriminator}`', self.client)


    @commands.slash_command(name="avatar", description="Gets your avatar", guild_ids=[guild_id])
    async def av(self, ctx, user: discord.Member):
        emb = discord.Embed(title="Avatar", color=embed_color,
                            description=f"This is {user.mention}'s avatar!")
        emb.set_image(url=user.avatar.url)
        await logger("f", f'Sent Avatar to message of `{ctx.author.name}#{ctx.author.discriminator}`', self.client)
        await ctx.respond(embed=emb, ephemeral=True)

    
    @commands.slash_command(name="suggest", description="Send a suggestion to the official Suggestion Channel", guild_ids=[guild_id])
    async def sendsuggestion(self, ctx, suggestion: str, image_url: discord.Option(str, "Image Link", required=False, default=None)):
        if await checkperm(ctx, 0): return
        s = suggestion.replace(" nl ", " \n")  # Replacing nl with \n
        s_embed = discord.Embed(title=f"Suggestion", url="https://moonball.io", color=embed_color)
        s_embed.add_field(name=f"Submitted by {ctx.author.name}#{ctx.author.discriminator}",
                          value=f"Suggestion #{countadd('s')}\n{s} ", inline=True)
        if image_url:
            s_embed.set_image(url=image_url)  # Setting image
        s_embed.set_footer(text=embed_footer)
        s = await _suggestion_channel.send(embed=s_embed)
        # Adding reactions
        await s.add_reaction(tick_emoji)  # Adding tick reaction
        await s.add_reaction(cross_emoji)  # Adding cross reaction
        await _embed_log.send(embed=s_embed)  # Sending it to the Logs channel
        await ctx.respond(f"Your Suggestion was sent! Check <#{suggestion_channel}> to see how its doing!", ephemeral=True)
        log.info(f"Sent `{ctx.author.name}`'s suggestion to the suggestion channel!")



    @commands.slash_command(name="addbirthday", description="Sets your birthday", guild_ids=[guild_id])
    async def setbirthday(self, ctx, day: int, month: int):
        disc_id = ctx.author.id
        if not (0 < int(day) < 32 and 0 < int(month) < 13):
            await ctx.respond("Invalid Date. Please use DD/MM format.", ephemeral=True)
            return
        self.cur.execute(f"SELECT * FROM birthdays WHERE disc_id = {disc_id}")
        data = self.cur.fetchone()
        action = "set"
        if data is None:
            self.cur.execute(f"INSERT INTO birthdays VALUES ({disc_id}, {day}, {month})")
        else:
            action = "updated"
            self.cur.execute(f"UPDATE birthdays SET day = {day}, month = {month} WHERE disc_id = {disc_id}")
        self.con.commit()
        emb = discord.Embed(title="Birthday", color=embed_color, description=f"Successfully {action} your birthday!")
        emb.add_field(name="User", value=f"`{ctx.author.name}#{ctx.author.discriminator}`", inline=True)
        emb.add_field(name="Birthday", value=f"`{day}/{month}`", inline=True)
        emb.set_footer(text=embed_footer)
        emb.set_author(name=embed_header, icon_url=embed_icon)
        await ctx.respond(embed=emb, ephemeral=True)
        await logger("f", f"Set `{ctx.author.name}`'s birthday to `{day}`/`{month}`", self.client)


    @commands.slash_command(name="removebirthday", description="Removes your birthday", guild_ids=[guild_id])
    async def removebirthday(self, ctx):
        # Removes the birthday from the database
        disc_id = ctx.author.id
        self.cur.execute(f"SELECT * FROM birthdays WHERE disc_id = {disc_id}")
        data = self.cur.fetchone()
        if data is None:
            await ctx.respond("You don't have a birthday set!", ephemeral=True)
            return
        self.cur.execute(f"DELETE FROM birthdays WHERE disc_id = {disc_id}")
        self.con.commit()
        await logger("f", f"Removed `{ctx.author.name}`'s birthday", self.client)
        await ctx.respond("Birthday removed!", ephemeral=True)



    # Upcoming birthdays cmd
    @commands.slash_command(name="upcomingbirthdays", description="Shows all upcoming birthdays", guild_ids=[guild_id])
    async def upcomingbirthdays(self, ctx):
        self.cur.execute("SELECT * FROM birthdays")
        bdays = self.cur.fetchall()
        if not bdays:
            await ctx.respond("No birthdays set!", ephemeral=True)
            return
        emb = discord.Embed(title="Upcoming Birthdays", color=embed_color)

        def upcoming_bdays(no: int, bdays: list) -> str:
            """
            Return a string with the upcoming birthdays of the users.
            """
            class DiscordBday():
                def __init__(self, day, month, ID):
                    self.day = day
                    self.month = month
                    self.id = ID

                    # calculate no. of days from jan 1st
                    self.days = self.day + (self.month - 1) * 30
            days = []
            for bday in bdays:
                days.append(DiscordBday(bday[1], bday[2], bday[0]))
            # Sort the days by their days from jan 1st
            days.sort(key=lambda x: x.days)
            # Get the upcoming birthdays
            upcoming = []
            i = 0
            while True:
                if days[i].month >= datetime.date.today().month:
                    upcoming.append(days[i])
                if len(upcoming) == no:
                    break
                if i >= len(days) - 1:
                    break
                i += 1
            output = ""
            for day in upcoming:
                output += f"{day.day}/{day.month} **|** <@{day.id}>\n"
            return output

        upcomingbirthdays = upcoming_bdays(5, bdays)

        emb.add_field(name="Upcoming Birthdays", value=upcomingbirthdays, inline=True)
        emb.set_footer(text=embed_footer)
        emb.set_author(name=embed_header, icon_url=embed_icon)
        await ctx.respond(embed=emb, ephemeral=True)





    @commands.slash_command(name="joke", description="Gets you a joke", guild_ids=[guild_id])
    async def getjoke(self, ctx):
        if await checkperm(ctx, 0): return
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist") as resp: #&type=single
                    data = await resp.json()
        except Exception as e:
            await ctx.respond(f"There was an error! Error: {str(e)}", ephemeral=True)
            log.error(f"[FUN]: Error while getting joke from API. Error: {str(e)}")
            return

        if data["type"] == "single":
            emb = discord.Embed(title="Random Joke", color=embed_color, description=f"{data['joke']}")
        elif data["type"] == "twopart":
            emb = discord.Embed(title="Random Joke", color=embed_color, description=f"{data['setup']}\n||{data['delivery']}||")
        else:
            return
        emb.set_footer(text=embed_footer)
        emb.set_author(name=embed_header, icon_url=embed_icon)
        await ctx.respond(embed=emb, ephemeral=True)
        await logger("f", f"Sent `{ctx.author.name}#{ctx.author.discriminator}` a joke", self.client)



    @commands.slash_command(name="timestamp", description="Generates you a timestamp", guild_ids=[guild_id])
    async def timestamp(self, ctx, seconds: int):
        if await checkperm(ctx, 0): return
        emb = discord.Embed(title="Timestamp", color=embed_color, description=f"Sends you a custom, variable Discord timestamp.")
        emb.add_field(name="Timestamp", value=f"<t:{int(time.time())+seconds}:R>", inline=False)
        emb.add_field(name="Raw Code", value=f"`<t:{int(time.time())+seconds}:R>`", inline=False)
        emb.set_footer(text=embed_footer)
        emb.set_author(name=embed_header, icon_url=embed_icon)
        await logger("f", f"Sent `{ctx.author.name}#{ctx.author.discriminator}` a timestamp", self.client)
        await ctx.respond(embed=emb, ephemeral=True)




    @commands.slash_command(name="8ball", description="Gets you a random answer", guild_ids=[guild_id])
    async def eightball(self, ctx, question: str):
        if await checkperm(ctx, 0): return
        answers = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.",
                   "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
                   "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
        embed = discord.Embed(title="8Ball", color=embed_color, description=f"{ctx.author.name}'s 8Ball Answer")
        embed.add_field(name="Question", value=f"`{question}`", inline=False)
        embed.add_field(name="Answer", value=f"||`{random.choice(answers)}`||", inline=False)
        embed.set_footer(text=embed_footer)
        embed.set_author(name=embed_header, icon_url=embed_icon)
        await ctx.respond(embed=embed)
        await logger("f", f"Sent `{ctx.author.name}#{ctx.author.discriminator}` a 8Ball answer", self.client)



    @reminder.command(name="create", description="Sets a reminder for you", guild_ids=[guild_id])
    async def reminder_create(self, ctx, quantity: int,
                       unit: discord.Option(choices=
                       [
                            discord.OptionChoice("Minute(s)", value="m"),
                            discord.OptionChoice("Hour(s)", value="h"),
                            discord.OptionChoice("Day(s)", value="d"),
                            discord.OptionChoice("Week(s)", value="w"),
                            discord.OptionChoice("Month(s)", value="mo"),
                           ]),
                       message: str=None,
                       user: discord.User=None):

        if await checkperm(ctx, 0): return
        units = {"m" : 60, "h" : 3600, "d" : 86400, "w": 604800, "mo": 2592000}
        if not quantity > 0:
            await ctx.respond("Quantity must be a positive number.", ephemeral=True)
            return
        if message:
            if len(message) > 1900:
                await ctx.respond("Your message is too long!", ephemeral=True)
                return
        if not user:
            user = ctx.author
        seconds = units[unit] * quantity
        duration = int(time.time())+seconds
        rem_id = random.randint(1000000000,9999999999)
        # Database Format => id, user_id, time, author_id, message
        #                     0    1        2      3           4
        if message: # If there is a message to send
            message = message.replace('"', '')
            self.cur.execute(f'INSERT INTO reminders VALUES({rem_id}, {user.id}, {duration}, {ctx.author.id}, "{message}");')
        else:   # If there is no message to send
            self.cur.execute(f'INSERT INTO reminders VALUES({rem_id},{user.id}, {duration}, {ctx.author.id}, "");')
        self.con.commit()
        r_embed = discord.Embed(title="Reminder", color=embed_color, description=f"{user.name} will be reminded in <t:{duration}:R>.")
        if message:
            r_embed.add_field(name="Message", value=f"`{message}`", inline=False)
        r_embed.add_field(name="ID", value=f"`{rem_id}`", inline=False)
        r_embed.set_footer(text=embed_footer)
        r_embed.set_author(name=embed_header, icon_url=embed_icon)
        await ctx.respond(embed=r_embed)
        await logger("f", f"`{ctx.author.name}#{ctx.author.discriminator}` set a reminder for `{user.id}`", self.client)



    @reminder.command(name="upcoming", description="Gets all your reminders", guild_ids=[guild_id])
    async def upcoming_reminders(self, ctx):
        if await checkperm(ctx, 0): return
        self.cur.execute(f'SELECT * FROM reminders WHERE user_id = {ctx.author.id};')
        reminders = self.cur.fetchall()
        r_embed = discord.Embed(title="Reminders", color=embed_color, description="Here are your upcoming reminders")
        r_embed.set_footer(text=embed_footer)
        r_embed.set_author(name=embed_header, icon_url=embed_icon)
        # Database Format => id, user_id, time, author_id, message
        #                     0    1        2      3           4
        if reminders:
            output = ""
            for reminder in reminders:
                output += f"`{reminder[0]}` <t:{reminder[2]}:R> `{reminder[4]}`\n"
            r_embed.add_field(name="Upcoming Reminders", value=output, inline=False)

        else:
            r_embed.add_field(name="Upcoming Reminders", value="You have no upcoming reminders.", inline=False)

        await ctx.respond(embed=r_embed)
        await logger("f", f"`{ctx.author.name}#{ctx.author.discriminator}` got their reminders", self.client)


    @reminder.command(name="delete", description="Deletes your reminder(s)", guild_ids=[guild_id])
    async def delete_reminder(self, ctx, id: int):
        if await checkperm(ctx, 0): return
        # check if reminder exists
        self.cur.execute(f'SELECT * FROM reminders WHERE user_id = {ctx.author.id} AND id = {id};')
        reminder = self.cur.fetchone()
        if not reminder:
            await ctx.respond("You have no reminder with that ID.", ephemeral=True)
            return
        self.cur.execute(f'DELETE FROM reminders WHERE id = {id} AND user_id = {ctx.author.id};')
        self.con.commit()
        await ctx.respond(f"I've successfully deleted reminder `{id}`", ephemeral=True)
        await logger("f", f"`{ctx.author.name}#{ctx.author.discriminator}` deleted a reminder `{id}`", self.client)



    # delete all reminders for a user
    @reminder.command(name="deleteall", description="Deletes all your reminders", guild_ids=[guild_id])
    async def delete_all_reminders(self, ctx):
        if await checkperm(ctx, 0): return
        self.cur.execute(f'SELECT * FROM reminders WHERE user_id = {ctx.author.id};')
        reminders = self.cur.fetchall()
        if reminders:
            num = len(reminders)
        else:
            await ctx.respond("You have no reminders.", ephemeral=True)
            return

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
        await ctx.respond(f"You have `{num}` reminders. Are you sure you want to delete all of your reminders?", ephemeral=True, view=_view)
        await _view.wait()
        if _view.value is None:  # timeout
            await ctx.respond("Deletion Cancelled. Didn't respond in time", ephemeral=True)
            return
        if not _view.value:    # cancel
            await ctx.respond("Deletion Cancelled", ephemeral=True)
            return

        self.cur.execute(f'DELETE FROM reminders WHERE user_id = {ctx.author.id};')
        self.con.commit()
        await ctx.respond(f"I've successfully deleted all reminders for you", ephemeral=True)
        await logger("f", f"`{ctx.author.name}#{ctx.author.discriminator}` deleted all reminders", self.client)

def setup(client):
    client.add_cog(Fun(client))
