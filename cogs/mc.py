import discord, hashlib, mysql.connector, sqlite3, os
from discord.ext import commands
from bot import prefix, embed_header, embed_footer, embed_color, bot_version, embed_icon, guild_id    # Import bot variables
from bot import logger, checkperm, get_mc, sendcmd, bad_char
from dotenv import load_dotenv
from pathlib import Path
from discord.commands import SlashCommandGroup

load_dotenv(dotenv_path=Path('./data/.env'))
db_user = os.getenv("DB_USER")
db_pw = os.getenv("DB_PW")


# Import bot functions


class Sha256:
    def __init__(self, usersalt):
        self.usersalt = usersalt

    def realHash(self, pw):
        return hashlib.sha256(pw.encode('utf-8')).hexdigest()

    def hash(self, password):
        salt = self.usersalt  # Get salt from database
        return str(str('$SHA$' + str(salt)) + '$') + self.realHash((self.realHash(password) + str(salt)))

mc = discord.SlashCommandGroup("mc", "Minecraft Related Commands")

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
        self.mc = mc

    mc = SlashCommandGroup("mc", "Various commands meant for users that have connected their MC account.")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog : MC.py Loaded")


    @mc.command(name="connect", description="Connects your Discord account to your Minecraft Account", guild_ids=[guild_id])
    async def con(self, ctx, username: str):
        if await checkperm(ctx, 0): return
        msg = await ctx.respond(embed=discord.Embed(title="Connect MC Account", description="*Processing Request, Please hold on...*", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)
        charsfound = await bad_char(username)
        if charsfound:
            await msg.edit_original_message(embed=discord.Embed(title="Connect MC Account", description=f"**There was an error!**\nThe username contains illegal character(s)!\n{charsfound}", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        con = sqlite3.connect('./data/data.db') # Connect to the database
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM connection WHERE disc_id = '{ctx.author.id}';")  # Get the discord user from the database
        id_result = cursor.fetchone()
        if id_result:   # If the user is in the database
            await msg.edit_original_message(embed=discord.Embed(title="Connect MC Account", description="**There was an Error!**\nYour Discord account is already connected.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        cursor.execute(f"SELECT * FROM connection WHERE mc_username = '{username}';") # Get the mc user from the database
        mc_result = cursor.fetchone()
        if mc_result:   # If the mc user is in the database
            await msg.edit_original_message(embed=discord.Embed(title="Connect MC Account", description="**There was an Error!**\nYour Minecraft account is already connected.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        try:    # Try to connect to the Authme MYSQL database
            mydb = mysql.connector.connect(
                host="192.168.100.70",
                user=db_user,
                password=db_pw,
                database='s21_authme'
            )
        except mysql.connector.Error as err:    # If there is an error
            await msg.edit_original_message(embed=discord.Embed(title="Connect MC Account", description=f"**There was an error!**\nCouldn't Connect to the Database.\n`{err}`", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        cur = mydb.cursor()
        cur.execute(f"SELECT password FROM authme WHERE realname = '{username}';")  # Get the Hashed Password from the Authme database
        result = cur.fetchone()
        if result is None:   # If the user doesn't exist in the Authme database
            await msg.edit_original_message(embed=discord.Embed(title="Connect MC Account", description=f"**There was an error!**\nThe username `{username}` does not exist in the database. Have you registered?", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        mydb.close()
        db_password = result[0]
        await msg.edit_original_message(embed=discord.Embed(title="Connect MC Account", description="Please DM me your password.", color=embed_color))
        dm = await ctx.author.send(embed=discord.Embed(title="Connect MC Account", description="Please DM me your Moonball *Minecraft* password.\nNote : You have 60 seconds to respond!", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
        try:    # Try to get the password from the DM
            password = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
        except:  # If the user didn't respond in time
            await dm.edit(embed=discord.Embed(title="Connect MC Account", description="**There was an Error!**\n You didn't send your password in DMs in time!", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            await msg.edit_original_message(embed=discord.Embed(title="Connect MC Account", description="**There was an Error!**\n You didn't send your password in DMs in time!", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        user_salt = db_password.split('$')[2]
        sha256 = Sha256(user_salt)
        hashed_pw = sha256.hash(password.content)
        if hashed_pw != db_password:    # If the password is incorrect
            await dm.edit(embed=discord.Embed(title="Connect MC Account", description="*Incorrect Password!*", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            await msg.edit_original_message(embed=discord.Embed(title="Connect MC Account", description="*Incorrect Password!*", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
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
        await msg.edit_original_message(embed=con_embed)   # Edit the message to show the success message
        # give them the "connected" role
        role = discord.utils.get(ctx.guild.roles, name="Connected")
        try:
            await ctx.author.add_roles(role)
        except Exception as e:
            print("Couldn't add role. Error:", e)
        await logger("m", f"{ctx.author.name}#{ctx.author.discriminator} connected their Minecraft account to their Discord account.", "Minecraft", f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) connected their Minecraft account to their Discord account.")



    @mc.command(name="disconnect", description="Disconnects your Discord account from your Minecraft Account", guild_ids=[guild_id])
    async def discon(self, ctx):
        if await checkperm(ctx, 0): return
        iscon = await get_mc(ctx.author.id)
        if iscon is None:
            await ctx.respond(embed=discord.Embed(title="Disconnect MC Account", description="**There was an Error!**\nThere is no Minecraft Account connected to your Discord.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)
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
        await ctx.respond(embed=discon_embed, ephemeral=True)
        # remove the "connected" role
        role = discord.utils.get(ctx.guild.roles, name="Connected")
        try:
            await ctx.author.remove_roles(role)
        except Exception as e:
            print("Couldn't remove role. Error:", e)
        await logger("m", f"{ctx.author.name}#{ctx.author.discriminator} disconnected their Minecraft account from their Discord account.", "Minecraft", f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) disconnected their Minecraft account from their Discord account.")



    @mc.command(name="changepassword", description="Changes your Moonball Minecraft account Password", guild_ids=[guild_id])
    async def changepassword_mc(self, ctx):
        emb = await ctx.respond(embed=discord.Embed(title="Change Password", description=f"*Processing Request, Please wait!*", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)
        username = await get_mc(ctx.author.id)
        if username is None:
            await emb.edit_original_message(embed=discord.Embed(title="Change Password Command",description="**There was an Error!**\nThere is no Minecraft Account connected to your Discord.", color=discord.colour.Color.red()))
            return
        await ctx.author.send(f"Please send your new password for your Minecraft account `{username}`")
        try:
            pw = (await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)).content
        except:
            await emb.edit_original_message(embed=discord.Embed(title="Change Password Command", description="**There was an Error!**\nYou took too long to send your password.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        if 3 < len(pw) > 16:
            await emb.edit_original_message(embed=discord.Embed(title="Change Password Command", description=f"**Error!**\nYour password must be between 3 and 16 characters.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        elif " " in pw:
            await emb.edit_original_message(embed=discord.Embed(title="Change Password Command", description=f"**Error!**\nYour password cannot contain spaces.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        cmd = f"authme cp {username} {pw}"
        try:
            cmdout = await sendcmd(ctx, "auth", cmd)
        except:
            await emb.edit_original_message(embed=discord.Embed(title="Change Password Command", description="**There was an Error!**\nThere was an error while trying to change your password.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        if cmdout != "done": return
        pw_embed = discord.Embed(title="Change Password Command", description=f"**Success!**\nYour password has been changed.", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon)
        pw_embed.add_field(name="Username", value=username)
        pw_embed.set_footer(text=embed_footer)
        pw_embed.set_author(name=embed_header, icon_url=embed_icon)
        await emb.edit_original_message(embed=pw_embed)
        pw_embed.add_field(name="Password", value=f"||{pw}||")
        await ctx.author.send(embed=pw_embed)



    @mc.command(name="pay", description="MC : Pay Someone a given amount of money (Survival)", guild_ids=[guild_id])
    async def pay(self, ctx, user: discord.Member, amount: int):
        await checkperm(ctx, 0)
        emb = await ctx.respond(embed=discord.Embed(title="Pay Command", description="*Sending the Money, Please wait...*", color=embed_color).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)
        user1 = await get_mc(ctx.author.id) # Get the username of the payer
        user2 = await get_mc(user.id)    # Get the username of the payee
        if user2 is None:
            await emb.edit_original_message(embed=discord.Embed(title="Pay Command",description=f"**Error!**\nThe user, <@{user.id}> has no Minecraft account connected!\nPlease ask the owner of the account to connect their MC account to their Discord, with `{prefix}connect` to enable this feature.",color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        if user1 == user2:  # If the payer and payee are the same person
            await emb.edit_original_message(embed=discord.Embed(title="Pay Command", description="**Error!**\nYou cannot pay yourself.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        try:
            await sendcmd(ctx, "survival", f"eco take {user1} {amount}")
            await sendcmd(ctx, "survival", f"eco give {user2} {amount}")
            await sendcmd(ctx, "survival", f"msg {user2} Greetings!, {user1} has paid you ${amount}")
            await sendcmd(ctx, "survival", f"mail {user2} Greetings!, {user1} has paid you ${amount}")
        except:
            await emb.edit_original_message(embed=discord.Embed(title="Pay Command", description="**There was an Error!**\nThere was an error while sending the command to the server. Please contact the mods.", color=discord.colour.Color.red()).set_footer(text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
            return
        embd = discord.Embed(title="Pay Command", description=f"The operation was successful.", color=embed_color)
        embd.add_field(name="Payer", value=f"`{user1}`")
        embd.add_field(name="Payee", value=f"`{user2}`")
        embd.add_field(name="Amount", value=f"`{amount}`")
        await emb.edit_original_message(embed=embd)
        await user.send(f"You have received a payment of ${amount} from {user1}!")


def setup(client):
    client.add_cog(MC(client))


