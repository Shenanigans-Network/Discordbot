#   ╔═╗╔═╗            ╔╗       ╔╗ ╔╗     ╔══╗      ╔╗
#   ║║╚╝║║            ║║       ║║ ║║     ║╔╗║     ╔╝╚╗
#   ║╔╗╔╗║╔══╗╔══╗╔═╗ ║╚═╗╔══╗ ║║ ║║     ║╚╝╚╗╔══╗╚╗╔╝
#   ║║║║║║║╔╗║║╔╗║║╔╗╗║╔╗║╚ ╗║ ║║ ║║     ║╔═╗║║╔╗║ ║║
#   ║║║║║║║╚╝║║╚╝║║║║║║╚╝║║╚╝╚╗║╚╗║╚╗    ║╚═╝║║╚╝║ ║╚╗
#   ╚╝╚╝╚╝╚══╝╚══╝╚╝╚╝╚══╝╚═══╝╚═╝╚═╝    ╚═══╝╚══╝ ╚═╝
#
#
# Made by RajDave69
#
# Contacts -
#   Raj Dave -
#       Instagram - raj_clicks25
#       Discord - Raj Dave#3215
#
#
#   Please Do not use this bot's files or code for your own projects without credit
#   Owner(s) include Raj Dave#3215 (discord)
#
#       Remember to edit the config.ini file to your liking.
#       Thank you for your time here, and I hope this code is useful to you =D
#
#   Github - https://moonball.io/opensource
#


# Importing Modules
try:
    from backend import log
    from backend import checkperm, client
    import discord, os, asyncio, configparser
except Exception as errr:
    print("Unable to import required modules. Please make sure you have all the modules installed." + f"Error: {errr}")
    exit()


#   Loading Config File
config = configparser.ConfigParser()
try:
   config.read('data/config.ini')
except Exception as e:
    log.critical("Error reading the config.ini file. Error: " + str(e))
    exit()



@client.event
async def on_ready():  # Stuff the bot does when it starts
    await client.change_presence(activity=discord.Game(f'on the Moonball Network'))  # Set Presence
    global log_channel
    try:
        log_channel = client.get_channel(config.getint('discord', 'log_channel'))  # Put your log channel's channel ID here
    except Exception as err:
        log.error("Couldn't get log_channel from config.ini. Error: " + str(err))


    await asyncio.sleep(2) # Waits for cogs to be loaded
    print("---------------------")
    print("Connected to Discord!")  # Print this when the bot starts
    log.info(f"Logged in as {client.user.name}. User ID: {client.user.id}")
    print("---------------------")



#
# == Cog Commands ==
#
@client.command()
async def loadcog(ctx, extention: str):
    if await checkperm(ctx, 5): return
    client.load_extension(f'cogs.{extention}')
    log.info(f"loadcog: Loaded {extention}")
    await ctx.respond(f'Loaded `{extention}`')

@client.command()
async def unloadcog(ctx, extention: str):
    if await checkperm(ctx, 5): return
    client.unload_extension(f'cogs.{extention}')
    log.debug(f'unloadcog: Unloaded `{extention}`')
    await ctx.respond(f'Unloaded `{extention}`')

@client.slash_command()
async def reloadcog(ctx, extention: str):
    if await checkperm(ctx, 5): return
    if extention == "all":
        for _filename in os.listdir('./cogs'):
            if _filename.endswith('.py'):
                client.unload_extension(f'cogs.{_filename[:-3]}')
                client.load_extension(f'cogs.{_filename[:-3]}')
        await ctx.respond(f'Reloaded all cogs', ephemeral=True)
        return
    client.unload_extension(f'cogs.{extention}')
    client.load_extension(f'cogs.{extention}')
    log.debug(f"reloadcog: Reloaded {extention}")
    await ctx.respond(f'Reloaded `{extention}`', ephemeral=True)



print("---------------------")

cog_list = []
# Loading the cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        cog_list.append(filename[:-3])
log.debug(f"Loaded {len(cog_list)} cogs. List: {cog_list}")



client.run(config.get("secret", "discord_token"))
