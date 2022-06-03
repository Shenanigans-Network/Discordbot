import discord, hashlib, mysql.connector, sqlite3, os
from discord.ext import commands
from bot import prefix, embed_header, embed_footer, embed_color, bot_version, embed_icon    # Import bot variables
from bot import logger, checkperm, checkcommandchannel, get_mc, sendcmd, mc_exists, bad_char
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(dotenv_path=Path('./data/.env'))
db_user = os.getenv("DB_USER")
db_pw = os.getenv("DB_PW")


# Import bot functions


class Sha256:
    def __init__(self, usersalt):
        self.usersalt = usersalt

    def realHash(self, ignoreme, pw):
        return hashlib.sha256(pw.encode('utf-8')).hexdigest()

    def hash(self, password):
        salt = self.usersalt  # Get salt from database
        return str(str('$SHA$' + str(salt)) + '$') + self.realHash('sha256', (self.realHash('sha256', password) + str(salt)))



class MC(commands.Cog):
    """Commands interacting with the Minecraft server, meant for the general user."""
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

        print("Cog : Listeners.py Loaded")


    @commands.command(name="connect", help=f"Connects your Minecraft account to your Discord account. Requires you to have joined the Minecraft server at least once and your Moonball Minecraft password. Syntax - ```ini\n{prefix}connect [username]\n```")
    async def con(self, ctx, *data):
        if await checkperm(ctx, 0): return
        if await checkcommandchannel(ctx): return  # Checks if command was executed in the Command Channel
        msg = await ctx.reply(embed=discord.Embed(title="Connect MC Account", description="*Processing Request, Please hold on...*", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
        if len(data) != 1:  #Checks if there is only one argument
            await msg.edit(embed=discord.Embed(title="Connect MC Account", description=f"**There was an error!**\nInvalid Syntax! The correct syntax is `{prefix}connect <username>`.", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        charsfound = await bad_char(data[0])
        if charsfound:
            await msg.edit(embed=discord.Embed(title="Connect MC Account", description=f"**There was an error!**\nThe username contains illegal character(s)!\n{charsfound}", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        con = sqlite3.connect('./data/data.db') # Connect to the database
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM connection WHERE disc_id = '{ctx.author.id}';")  # Get the discord user from the database
        id_result = cursor.fetchone()
        if id_result:   # If the user is in the database
            await msg.edit(embed=discord.Embed(title="Connect MC Account", description="**There was an Error!**\nYour Discord account is already connected.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        cursor.execute(f"SELECT * FROM connection WHERE mc_username = '{data[0]}';") # Get the mc user from the database
        mc_result = cursor.fetchone()
        if mc_result:   # If the mc user is in the database
            await msg.edit(embed=discord.Embed(title="Connect MC Account", description="**There was an Error!**\nYour Minecraft account is already connected.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        username = data[0]
        try:    # Try to connect to the Authme MYSQL database
            mydb = mysql.connector.connect(
                host="192.168.100.70",
                user=db_user,
                password=db_pw,
                database='s21_authme'
            )
        except mysql.connector.Error as err:    # If there is an error
            await msg.edit(embed=discord.Embed(title="Connect MC Account", description=f"**There was an error!**\nCouldn't Connect to the Database.\n`{err}`", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        cur = mydb.cursor()
        cur.execute(f"SELECT password FROM authme WHERE realname = '{username}';")  # Get the Hashed Password from the Authme database
        result = cur.fetchone()
        if result is None:   # If the user doesn't exist in the Authme database
            await msg.edit(embed=discord.Embed(title="Connect MC Account", description=f"**There was an error!**\nThe username `{username}` does not exist in the database. Have you registered?", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        mydb.close()
        db_password = result[0]
        await msg.edit(embed=discord.Embed(title="Connect MC Account", description="Please DM me your password.", color=embed_color))
        dm = await ctx.author.send(embed=discord.Embed(title="Connect MC Account", description="Please DM me your Moonball *Minecraft* password.\nNote : You have 60 seconds to respond!", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
        try:    # Try to get the password from the DM
            password = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
        except:  # If the user didn't respond in time
            await dm.edit(embed=discord.Embed(title="Connect MC Account", description="**There was an Error!**\n You didn't send your password in DMs in time!", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            await msg.edit(embed=discord.Embed(title="Connect MC Account", description="**There was an Error!**\n You didn't send your password in DMs in time!", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        user_salt = db_password.split('$')[2]
        sha256 = Sha256(user_salt)
        hashed_pw = sha256.hash(password.content)
        if hashed_pw != db_password:    # If the password is incorrect
            await dm.edit(embed=discord.Embed(title="Connect MC Account", description="*Incorrect Password!*", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            await msg.edit(embed=discord.Embed(title="Connect MC Account", description="*Incorrect Password!*", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        con = sqlite3.connect('./data/data.db')
        c = con.cursor()
        c.execute(f"INSERT INTO connection (disc_id, mc_username, mc_pw) VALUES ({ctx.author.id}, '{username}', '{db_password}');")     # Insert the user into the database
        con.commit()
        con.close()
        con_embed = discord.Embed(title="Connect MC Account", description=f"**Success!**\nYour Minecraft account has been connected to your Discord account.", color=embed_color)
        con_embed.set_footer(text=embed_footer)
        con_embed.set_author(name=embed_header, icon_url=embed_icon)
        con_embed.add_field(name="Username", value=f"`{username}`", inline=True)
        con_embed.add_field(name="Discord", value=f"`{ctx.author.id}`", inline=True)
        await dm.edit(embed=con_embed)
        await msg.edit(embed=con_embed)   # Edit the message to show the success message
        await logger("m", f"{ctx.author.name}#{ctx.author.discriminator} connected their Minecraft account to their Discord account.", "Minecraft", f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) connected their Minecraft account to their Discord account.")



    @commands.command(name="disconnect", help=f"Disconnect your Minecraft account from your Discord account.\n Syntax - ```ini\n{prefix}disconnect```" ,)
    async def discon(self, ctx):
        if await checkperm(ctx, 0): return
        iscon = await get_mc(ctx.author.id)
        if iscon is None:
            await ctx.send(embed=discord.Embed(title="Disconnect MC Account",description="**There was an Error!**\nThere is no Minecraft Account connected to your Discord.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        mc = await get_mc(ctx.author.id)
        con = sqlite3.connect('./data/data.db')
        c = con.cursor()
        c.execute(f"DELETE FROM connection WHERE disc_id = '{ctx.author.id}';")
        con.commit()
        con.close()
        discon_embed = discord.Embed(title="Disconnect MC Account", description=f"**Success!**\nYour Minecraft account has been disconnected from your Discord account.", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon)
        discon_embed.set_footer(text=embed_footer)
        discon_embed.set_author(name=embed_header, icon_url=embed_icon)
        discon_embed.add_field(name="MC", value=f"`{mc}`", inline=True)
        discon_embed.add_field(name="Discord", value=f"`{ctx.author.id}`", inline=True)
        await ctx.send(embed=discon_embed)
        await logger("m", f"{ctx.author.name}#{ctx.author.discriminator} disconnected their Minecraft account from their Discord account.", "Minecraft", f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) disconnected their Minecraft account from their Discord account.")


    @commands.group(aliases=['minecraft'], pass_context=True, invoke_without_command=True)
    async def mc(self, ctx):
        mc_embed = discord.Embed(title="Minecraft Commands", description=f"The commands which interact with the Minecraft Server are prefixed by `{prefix}mc`\nMore info can be found at `{prefix}help mc`", color=embed_color)
        mc_embed.set_footer(text=embed_footer)
        mc_embed.set_author(name=embed_header, icon_url=embed_icon)
        await ctx.reply(embed=mc_embed)

    @mc.command(aliases=['connect'])
    async def connect_mc(self, ctx, *data):
        await self.con(ctx, data)

    @mc.command(aliases=['disconnect'])
    async def disconnect_mc(self, ctx):
        await self.discon(ctx)


    @mc.command(aliases=['changepw', "changepass", "changepassword"])
    async def changepassword_mc(self, ctx):
        if await checkperm(ctx, 0): return
        emb = await ctx.reply(embed=discord.Embed(title="Change Password", description=f"*Processing Request, Please wait!*", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
        username = await get_mc(ctx.author.id)
        if username is None:
            await emb.edit(embed=discord.Embed(title="Change Password Command",description="**There was an Error!**\nThere is no Minecraft Account connected to your Discord.", color=discord.colour.Color.red()))
            return
        await ctx.author.send(f"Please send your new password for your Minecraft account `{username}`")
        try:
            pw = (await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)).content
        except:
            await emb.edit(embed=discord.Embed(title="Change Password Command", description="**There was an Error!**\nYou took too long to send your password.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        if 3 < len(pw) > 16:
            await emb.edit(embed=discord.Embed(title="Change Password Command", description=f"**Error!**\nYour password must be between 3 and 16 characters.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        elif " " in pw:
            await emb.edit(embed=discord.Embed(title="Change Password Command", description=f"**Error!**\nYour password cannot contain spaces.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        # Anti SQL Injection
        if ";" in pw:
            await emb.edit(embed=discord.Embed(title="Change Password Command", description=f"**Error!**\nYour password cannot contain a `;`.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        cmd = f"authme cp {username} {pw}"
        try:
            cmdout = await sendcmd(ctx, "auth", cmd)
        except:
            await emb.edit(embed=discord.Embed(title="Change Password Command", description="**There was an Error!**\nThere was an error while trying to change your password.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        if cmdout != "done": return
        pw_embed = discord.Embed(title="Change Password Command", description=f"**Success!**\nYour password has been changed.", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon)
        pw_embed.add_field(name="Username", value=username)
        pw_embed.set_footer(text=embed_footer)
        pw_embed.set_author(name=embed_header, icon_url=embed_icon)
        await ctx.reply(embed=pw_embed)
        pw_embed.add_field(name="Password", value=f"||{pw}||")
        await ctx.author.send(embed=pw_embed)



    @mc.command()
    async def pay(self, ctx, *data):
        await checkperm(ctx, 0)
        await checkcommandchannel(ctx)
        emb = await ctx.reply(embed=discord.Embed(title="Pay Command", description="**Please wait...**", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
        charsfound = await bad_char(data[0])
        if charsfound:
            await emb.edit(embed=discord.Embed(title="Pay Command", description=f"**Error!**\nThe Minecraft Account, `{data[0]}` cannot contain {charsfound}.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        user1 = await get_mc(ctx.author.id)
        if user1 is None:
            await emb.edit(embed=discord.Embed(title="Change Password Command",description="**There was an Error!**\nThere is no Minecraft Account connected to your Discord.", color=discord.colour.Color.red()))
            return
        elif not len(data) == 2:
            await emb.edit(embed=discord.Embed(title="Pay Command", description=f"**Error!**\nInvalid number of arguments. Expected `2` got `{len(data)}`", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        elif not await mc_exists(data[0]):
            await emb.edit(embed=discord.Embed(title="Pay Command", description=f"**Error!**\nThe Minecraft Account `{data[0]}` is not connected!\nPlease ask the owner of the account to connect their MC account to their Discord, with `{prefix}connect` to enable this feature.",color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        elif not data[1].isnumeric():
            await emb.edit(embed=discord.Embed(title="Pay Command", description=f"**Error!**\nThe amount, `{data[1]}` is not a number.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        elif user1 == data[0]:
            await emb.edit(embed=discord.Embed(title="Pay Command", description="**Error!**\nYou cannot pay yourself.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        user2 = data[0]
        amount = int(data[1])

        try:
            await sendcmd(ctx, "survival", f"eco take {user1} {amount}")
            await sendcmd(ctx, "survival", f"eco give {user2} {amount}")
            await sendcmd(ctx, "survival", f"mail {user2} Hello, {user1} has paid you ${amount}")
        except:
            await emb.edit(embed=discord.Embed(title="Pay Command", description="**There was an Error!**\nThere was an error while sending the command to the server. Please contact the mods.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return

        embd = discord.Embed(title="Pay Command", description=f"The operation was successful.", color=embed_color)
        embd.add_field(name="Payer", value=f"`{user1}`")
        embd.add_field(name="Payee", value=f"`{user2}`")
        embd.add_field(name="Amount", value=f"`{amount}`")
        await emb.edit(embed=embd)

def setup(client):
    client.add_cog(MC(client))


