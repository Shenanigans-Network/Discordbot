from easy_pil import Editor, Font, load_image_async
from discord.ext import commands
import discord, sqlite3, os
from table import init

db = sqlite3.connect('./data/data.db')
c = db.cursor()

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix="+", intents=intents, help_command=None)
init(db, c, guild=client.guilds)

# cogs
extensions = []
for cog in os.listdir('./cogs'):
    if cog.endswith('.py'):
        client.load_extension(f'cogs.{cog[:-3]}')


@client.event
async def on_ready():
    print("Connected to Discord!")
    await client.change_presence(activity=discord.Game('Online classes :/'))


# welcome-announcement
@client.event
async def on_member_join(member):
    bg = Editor('welcome_banner.png').resize((900, 260))
    profile = await load_image_async(str(member.avatar_url))
    profile = Editor(profile).resize((150, 150)).circle_image()
    poppins_big = Font.poppins(variant="bold", size=60)
    poppins_norm = Font.poppins(variant='light', size=30)

    bg.paste(profile.image, (30, 30))
    bg.text((250, 40), f"{member.name}#{member.discriminator}", color='white', font=poppins_big)
    bg.text((260, 150), 'welcome to the server!', color='lightgrey', font=poppins_norm)

    file = discord.File(bg.image_bytes, filename='welcome_card.png')

    c.execute(f'SELECT * FROM {member.guild}')
    guild_info = c.fetchall()

    channel = 0
    for info in guild_info:
        if info[0] == 'welcome_channel':
            channel += int(info[1])

    if not channel: return

    channel = client.get_channel(channel)
    await channel.send(file=file)
    await channel.send(f'Hope you have a good time here, {member.mention}!')


@client.command()
async def spam(ctx, no, *args):
    for i in range(int(no)):
        await ctx.send(args)
    
@client.command(aliases=['welc-channel', 'welcome-channel'])
@commands.has_permissions(administrator=True)
async def welcome_channel(ctx, channel: discord.TextChannel):
    channel = channel or ctx.channel
    try:
        c.execute(f'UPDATE {ctx.guild} SET col2=:c2 WHERE col1=:c1', {
            "c2": channel.id,
            "c1": 'welcome_channel'
        })
        db.commit()
        await ctx.send(f'<#{channel.id}> is now the announcement channel!')
        return

    except sqlite3.OperationalError:

        c.execute(f'INSERT INTO {ctx.guild} values(?,?)', ('welcome_channel', channel.id))
        db.commit()
        await ctx.send(f'<#{channel.id}> is now the announcement channel!')
        return
    
@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} has been loaded!')

@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} has been unloaded!')

@client.command()
async def pfp(ctx, member:discord.Member):
    profile = await load_image_async(str(member.avatar_url))
    profile = Editor(profile).resize((150, 150)).circle_image()
    file = discord.File(profile.image_bytes, filename='pfp.png')

    await ctx.send(file=file)

@client.command()
async def grey(ctx, member:discord.Member):
    profile = await load_image_async(str(member.avatar_url))
    profile = ImageOps.grayscale(profile)
    profile = Editor(profile).resize((150, 150)).circle_image()

    file = discord.File(profile.image_bytes, filename='pfp.png')

    await ctx.send(file=file)


client.run("OTMxODc5NDQwMTUyMTMzNjMz.YeK2XA.Gcqq-QlQALqQVqhkHKVXQjpTos8")
