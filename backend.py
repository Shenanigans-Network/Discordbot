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
#       WARNING: DO NOT EDIT THIS FILE IF YOU DO NOT KNOW WHAT YOU ARE DOING

try:
    import discord, requests, json, sqlite3, mysql.connector, configparser, logging
    from mcstatus import JavaServer
    from discord.ext import commands
except Exception as errr:
    print("Unable to import modules. Please make sure you have the required modules installed. Error: ", errr)
    exit()

bot_version = "0.6.0"
intents = discord.Intents.all()

# Loading config.ini
config = configparser.ConfigParser()

try:
    config.read('data/config.ini')
except Exception as e:
    print("Error reading the config.ini file. Error: " + str(e))
    exit()

#  ==Getting variables from config file==
try:
    prefix: str = config.get('general', 'prefix')
    log_level: str = config.get('general', 'log_level')
    presence: str = config.get('general', 'presence')
    roles_synced: list = (config.get('general', 'roles_synced')).split(' ')
    s_list: str = config.get('general', 'server_list')
    ptero_panel: str = config.get('general', 'panel_url')

    guild_id: int = config.getint('discord', 'guild_id')
    cmd_channel: int = config.getint('discord', 'cmd_channel')
    welcome_channel: int = config.getint('discord', 'welcome_channel')
    suggestion_channel: int = config.getint('discord', 'suggestion_channel')
    log_channel: int = config.getint('discord', 'log_channel')
    embed_log: int = config.getint('discord', 'embed_log')
    member_role: int = config.getint('discord', 'member_role_id')
    general_channel: int = config.getint('discord', 'general_channel')
    music_channel: int = config.getint('discord', 'music_channel')
    music_vc: int = config.getint('discord', 'music_vc')

    embed_footer: str = config.get('discord', 'embed_footer').replace("$bot_version", bot_version)
    embed_header: str = config.get('discord', 'embed_header').replace("$bot_version", bot_version)
    embed_color: int = int(config.get('discord', 'embed_color'), base=16)
    embed_icon: str = config.get('discord', 'embed_icon')
    embed_url: str = config.get('discord', 'embed_url')

    ptero_apikey: str = config.get('secret', 'pterodactyl_apikey')
    db_host: str = config.get('secret', 'db_host')
    db_name: str = config.get('secret', 'db_name')
    db_user: str = config.get('secret', 'db_user')
    db_pw: str = config.get('secret', 'db_pw')

    tick_emoji: str = config.get('emoji', 'tick_emoji')
    cross_emoji: str = config.get('emoji', 'cross_emoji')
    one_emoji: str = config.get('emoji', 'one_emoji')
    two_emoji: str = config.get('emoji', 'two_emoji')
    three_emoji: str = config.get('emoji', 'three_emoji')
    four_emoji: str = config.get('emoji', 'four_emoji')

    music_save: str = config.get('emoji', 'music_save')
    music_loop: str = config.get('emoji', 'music_loop')
    music_pause: str = config.get('emoji', 'music_pause')
    music_stop: str = config.get('emoji', 'music_stop')
    music_skip: str = config.get('emoji', 'music_skip')
    music_vol_down: str = config.get('emoji', 'music_vol_down')
    music_vol_up: str = config.get('emoji', 'music_vol_up')


except Exception as err:
    print("Error getting variables from the config file. Error: " + str(err))
    exit(1)


# Initializing the logger
def colorlogger(name='moonball'):
    from colorlog import ColoredFormatter
    # disabler loggers
    for logger in logging.Logger.manager.loggerDict:
        logging.getLogger(logger).disabled = True
    logger = logging.getLogger(name)
    stream = logging.StreamHandler()
    LogFormat = "%(reset)s%(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s"
    stream.setFormatter(ColoredFormatter(LogFormat))
    logger.addHandler(stream)
    # Set logger level
    if log_level.upper() in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        logger.setLevel(log_level.upper())
    else:
        log.warning(f"Invalid log level {log_level}. Defaulting to INFO.")
        logger.setLevel("INFO")
    return logger  # Return the logger


log = colorlogger()

try:
    con = sqlite3.connect('./data/data.db')
except Exception as err:
    log.error("Error: Could not connect to data.db." + str(err))
    exit(1)
# noinspection PyUnboundLocalVariable
cur = con.cursor()

# noinspection PyUnboundLocalVariable
client = commands.Bot(command_prefix=prefix, intents=intents, help_command=None,
                      case_insensitive=True)  # Setting prefix

# Getting Server Names into a List
server_list: list = []
try:
    # noinspection PyUnboundLocalVariable
    for server in s_list.split(' '):
        server = f" {server} "
        server_list.append(server)
    log.debug(f"Server List: {server_list}")
except Exception as error:
    log.error(f"Error getting server list from config. Error: {error}")

# Getting Server IPs to a Dictionary
ip_cat = config['ips']
try:
    serv_ips: dict = {}
    for key in ip_cat:
        serv_ips[key] = config.get('ips', key)
    log.debug(f"Server IPs: {serv_ips}")
except Exception as error:
    log.error(f"Error getting server IPs from config. Error: {error}")

# Getting Pterodactyl Identifies to a Dictionary
ip_cat = config['server guide']
try:
    server_guide: dict = {}
    for key in ip_cat:
        server_guide[key] = config.get('server guide', key)
    # reverse the dictionary
    server_guide_r = {v: k for k, v in server_guide.items()}
    log.debug(f"Ptero IDs: {server_guide}")
    log.debug(f"Ptero IDs Reverse: {server_guide_r}")
except Exception as error:
    log.error(f"Error getting server IPs from config. Error: {error}")


#
# === Embeds ===
#

async def ip_embed(ctx, isslash: bool = False):
    if await checkperm(ctx, 0): return
    ipembed = discord.Embed(title="Here's the Server IP!", url="https://moonball.io", color=embed_color)
    ipembed.set_author(name=embed_header, icon_url=embed_icon)
    ipembed.add_field(name="Java ", value="play.moonball.io", inline=True)
    ipembed.add_field(name="Bedrock ", value="play.moonball.io (Port 25565)", inline=False)
    ipembed.set_footer(text=embed_footer)
    if isslash:
        await ctx.respond(embed=ipembed)
    else:
        msg = await ctx.reply(embed=ipembed)
        await msg.edit(embed=ipembed, view=DeleteButton(msg))

    await logger("i", f'Sent IP Embed to message of `{ctx.author.name}#{ctx.author.discriminator}`', client)


async def version_embed(ctx, isslash: bool = False):
    if await checkperm(ctx, 0): return
    vembed = discord.Embed(title="Here's the Server Version!", url="https://moonball.io", color=embed_color).set_footer(
        text=embed_footer)
    vembed.set_author(name=embed_header, icon_url=embed_icon)
    vembed.add_field(name="Java ", value="1.13 - 1.19", inline=True)
    vembed.add_field(name="Bedrock ", value="1.17.40 - 1.19.0", inline=False)
    if isslash:
        await ctx.respond(embed=vembed)
    else:
        msg = await ctx.reply(embed=vembed)
        await msg.edit(embed=vembed, view=DeleteButton(msg))
    await logger("i", f'Sent Version Embed to message of `{ctx.author.name}#{ctx.author.discriminator}`', client)


async def input_sanitizer(input_str):
    # Sanitize input
    cleaned = input_str.replace("'", "").replace('"', "").replace("`", "").replace("\\", "").replace("\n", "").replace(
        "\r", "").replace(";", '')
    return cleaned


#
# === Server Status ===
#

async def serverstatus(ctx, server: str, isslash: bool = True):
    if await checkperm(ctx, 0): return
    if isslash:
        msg = await ctx.respond(embed=discord.Embed(title=f"Server Status | {server.capitalize()}",
                                                    description=f"*Please hold on, Command Content is loading*",
                                                    color=embed_color, url="https://moonball.io").set_footer(
            text=embed_footer).set_author(name=embed_header, icon_url=embed_icon), ephemeral=True)
    else:
        msg = await ctx.reply(embed=discord.Embed(title=f"Server Status | {server.capitalize()}",
                                                  description=f"*Please hold on, Command Content is loading*",
                                                  color=embed_color, url="https://moonball.io").set_footer(
            text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
    try:
        server_info = await status(server.lower())  # Gets server info from Pterodactyl API
    except Exception as error:
        if isslash:
            msg.edit_original_response(embed=discord.Embed(title=f"Server Status | {server.capitalize()}",
                                                           description=f"**Error**: Couldn't get Status\n{e}",
                                                           color=embed_color, url="https://moonball.io").set_footer(
                text=embed_footer).set_author(name=embed_header, icon_url=embed_icon))
        else:
            msg.edit(embed=discord.Embed(title=f"Server Status | {server.capitalize()}",
                                         description=f"**Error**: Couldn't get Status\n{e}", color=embed_color,
                                         url="https://moonball.io").set_footer(text=embed_footer).set_author(
                name=embed_header, icon_url=embed_icon))
        log.error(f"Error while trying to get Server Status. Error: {str(error)}")
        return
    serverstatus = server_info["state"]  # Setting this as placeholder state
    player_count = 0
    online = False
    if serverstatus == "offline":  # If server is offline
        serverstatus = "Offline <:offline:915916197797715979>"
    elif serverstatus == "running":
        online = True
        serverstatus = "Online <:online:915916197973864449>"
        if not server in ["proxy", "bot", "auth", "lobby", "limbo"]:  # If not one of these servers
            try:
                player_count = JavaServer.lookup(serv_ips[server]).query().players.online  # Gets player count from API
            except Exception as error:
                log.warning(f"Error while getting playercount of {server}. Error: {str(error)}")
    elif serverstatus == "starting":  # If server is starting
        serverstatus = "Starting <:partial:915916197848047646>"
    elif serverstatus == "stopping":  # If server is stopping
        serverstatus = "Stopping <:outage:915916198032588800>"
    # Embed
    server_embed = discord.Embed(title=f"Status | {server.capitalize()}", url="https://moonball.io",
                                 description=f"Live Status for the {server.capitalize()} Server.\nTriggered by {ctx.author.name}#{ctx.author.discriminator}",
                                 color=embed_color)
    server_embed.set_author(name=embed_header, icon_url=embed_icon)
    server_embed.set_thumbnail(url=embed_icon)
    server_embed.add_field(name="Status", value=f'{serverstatus}', inline=True)
    server_embed.add_field(name="Players", value=f'{player_count} Online', inline=False)
    server_embed.add_field(name="CPU Usage", value=f'{server_info["cpuUsage"]}%', inline=False)
    server_embed.add_field(name="Memory Usage", value=f'{server_info["memUsage"]}', inline=False)
    server_embed.add_field(name="Disk Space", value=f'{server_info["spaceOccupied"]}', inline=False)
    if online:
        server_embed.add_field(name="Uptime", value=f'{server_info["uptime"]}', inline=False)
    server_embed.set_footer(text=embed_footer)
    if isslash:
        await msg.edit_original_response(embed=server_embed)
    else:
        await msg.edit(embed=server_embed, view=DeleteButton(msg))
    await logger("i",
                 f'Server Status : Sent Server `{server.capitalize()}` embed to message of `{ctx.author.name}#{ctx.author.discriminator}`',
                 client)


# This function gets the corresponding connected Minecraft account of the user from their Discord ID
async def get_con(disc_id: int) -> str | None:
    cur.execute(f"SELECT mc_username FROM connection WHERE disc_id = '{disc_id}';")
    result = cur.fetchone()
    log.debug(f"get_con: {result}")
    if result:
        return result[0]
    else:
        return None


# This function is used to check if a Minecraft Account is in the AuthMe Database.
# So basically checking if they've ever logged in before and their profile exists.
async def mc_exists(username: str) -> bool:
    #
    try:  # Try to connect to the Authme MYSQL database
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pw,
            database=db_name
        )
    except mysql.connector.Error as e:  # If there is an error
        log.error(
            f"Unable to connect to the Authme MYSQL database. Are the credentials within config.ini correct? Error: {e}")
        return False
    c = mydb.cursor()
    c.execute(f"SELECT username FROM authme WHERE username = '{username}';")
    result = c.fetchone()
    mydb.close()
    log.debug(f"mc_exists: {result}")
    if result:
        return True
    else:
        return False


# This function is to check if there are any illegal characters in a string.
async def bad_char(input_str: str, preset: list | str = None) -> str | None:
    if preset is None:
        illegal_chars = [";", "'", '"', ".", ",", ":", "!", "?", "`", "~", "@", "#", "$", "%", "^", "&", "*", "(", ")",
                         "-", "=", "[", "]", "{", "}", "|", "\\", "/", ">", "<", "`", "+"]
    elif preset == "username":
        illegal_chars = [";", "'", '"', ".", ",", ":", "!", "?", "`", "~", "@", "#", "$", "%", "^", "&", "*", "(", ")",
                         "-", "=", "[", "]", "{", "}", "|", "\\", "/", ">", "<", "`"]
    elif preset == "password":
        illegal_chars = [";", "'", '"']
    else:
        illegal_chars = list(preset)
    chars_found = []
    # username_regex = r'^[a-zA-Z0-9_+]{2,16}$'
    # special_chars_regex = r'[^a-zA-Z0-9_+]'
    # sql_regex = r'[\x00-\x1F\x7F-\x9F]'
    for i in illegal_chars:
        if i in input_str:
            chars_found.append(i)
    log.debug(f"bad_char: {chars_found}")
    if not chars_found:
        return None
    else:
        return f"`{'`, `'.join(chars_found)}`"  # Converts list to string with Discord ` formatting


async def logger(cat, msg, client):  # Logs to Log channel
    logtype = {"s": "Suggestion", "f": "Fun", "h": "Help", "i": "Info", "a": "Admin", "m": "Minecraft", "o": "other"}
    logchannel = client.get_channel(log_channel)
    await logchannel.send(f'**{logtype[cat]}** : ' + f'#{countadd(cat)} ' + msg)  # Logs to Log channel
    log.info(msg.replace("`", ""))


async def resetcount(ctx, kw: str) -> bool:  # Counter Add Function

    name_dict = {"s": "suggestion", "f": "fun", "h": "help", "i": "info", "a": "admin", "m": "minecraft", "o": "other",
                 "all": "all"}
    if kw == "all":
        for cat in ["a", "s", "f", "i", "h", "m", "o"]:
            cur.execute(f'UPDATE counters SET count=:c WHERE cname=:n', {"c": 0, "n": cat})
    else:
        cur.execute(f'UPDATE counters SET count=:c WHERE cname=:n', {"c": 0, "n": kw})
    con.commit()
    log.debug(f"resetcount: {kw}")
    await logger("a", f"`{name_dict[kw]}` Counter was reset by `{ctx.author.name}#{ctx.author.discriminator}`",
                 client)  # Logs to Log channel
    return True


def countadd(cat: str) -> int | None:  # Counter Add Function
    cur.execute(f'SELECT count FROM counters WHERE cname=:n', {"n": cat})
    count = cur.fetchone()[0]
    count += 1
    cur.execute(f'UPDATE counters SET count=:c WHERE cname=:n', {"c": count, "n": cat})
    con.commit()
    return count


#
# === Pterodactyl Interacting ===
#

def form_dict(stats):  # Takes raw data from the Pterodactyl API and converts it into usable variables
    placeholders = {}
    ph_keys = ["state", "memUsage", "cpuUsage", "spaceOccupied", "uptime"]
    ph_values = [
        stats["attributes"]["current_state"],
        str(round(stats["attributes"]["resources"]["memory_bytes"] / 1073741824, 2)) + " GB",
        str(round(stats["attributes"]["resources"]["cpu_absolute"], 2)),
        str(round(stats["attributes"]["resources"]["disk_bytes"] / 1073741824, 2)) + " GB",
        str(round(stats["attributes"]["resources"]["uptime"] / 3600000, 2)) + " hour(s)"
    ]
    for ind, ph_key in enumerate(ph_keys): placeholders[ph_key] = ph_values[ind]
    return placeholders


# This function get the status of a server from the Pterodactyl API.
async def status(server: str):  # Gets the status of a server
    headers = {"Authorization": f"Bearer {ptero_apikey}", "Accept": "application/json",
               "Content-Type": "application/json"}
    if server == "all":
        servers = {}
        for server_id in list(server_guide_r.keys()):
            url = f"https://{ptero_panel}/api/client/servers/{server_id}/resources"
            servers[server_guide_r[server_id]] = form_dict(requests.request('GET', url, headers=headers).json())
        return servers
    if server not in list(server_guide_r.values()): return "Invalid server name"
    return form_dict(requests.request('GET',
                                      f"https://{ptero_panel}/api/client/servers/{[x[0] for x in server_guide_r.items() if x[1] == server][0]}/resources",
                                      headers=headers).json())


# This function changes the power of a server from the Pterodactyl API.
async def serverpower(server: str, power: str) -> bool:  # Sets the power of a server
    ptero_panel = "panel.moonball.io"  # Put your Pterodactyl Panel's URL here
    url = f'https://{ptero_panel}/api/client/servers/{server_guide[server]}/power'
    headers = {"Authorization": f"Bearer {ptero_apikey}", "Accept": "application/json",
               "Content-Type": "application/json"}
    if power == "start":
        payload = '{"signal": "start"}'
    elif power == "stop":
        payload = '{"signal": "stop"}'
    elif power == "restart":
        payload = '{"signal": "restart"}'
    elif power == "kill":
        payload = '{"signal": "kill"}'
    else:
        return False

    response = requests.request('POST', url, data=payload, headers=headers)
    log.debug("serverpower: " + str(response))
    return True


# This function sends a Console Command to a server from the Pterodactyl API.
async def sendcmd(server_name: str, command: str) -> bool:
    url = f'https://{ptero_panel}/api/client/servers/{server_guide[server_name]}/command'
    headers = {"Authorization": f"Bearer {ptero_apikey}", "Accept": "application/json",
               "Content-Type": "application/json"}
    payload = json.dumps({"command": command})
    response = ''
    try:
        response = requests.request('POST', url, data=payload, headers=headers)
        log.debug(f"sendcmd: {response}")
        return True
    except Exception as err:
        log.error("Unable to send command to Pterodactyl. Error:" + str(err))
        log.error(response.text)
        return False


#
# === Permission Level System ===
#

async def get_permlvl(user, class_type=True) -> -1 | 0 | 1 | 2 | 3 | 4 | 5:
    user = user.id if class_type else user
    cur.execute(f"SELECT * FROM perms WHERE user_id={user}")
    result = cur.fetchone()
    if result is None:
        cur.execute(f"INSERT INTO perms (user_id, lvl) VALUES ({user}, 0)")
        con.commit()
        cur.execute(f"SELECT * FROM perms WHERE user_id={user}")
        result = cur.fetchone()
    log.debug(f"get_permlvl: {result[1]}")
    return result[1]


async def checkperm(ctx, level, isslash: bool = True) -> bool:
    currentlvl = await get_permlvl(ctx.author, True)
    log.debug(f"checkperm: current-{currentlvl}, req-{level}")
    if int(currentlvl) < int(level):
        if isslash:
            await ctx.respond(
                f"You don't have the required permissions to use this command. You have permission level `{currentlvl}`, but required level is `{level}`!",
                ephemeral=True)
        else:
            await ctx.reply(
                f"You don't have the required permissions to use this command. You have permission level `{currentlvl}`, but required level is `{level}`!",
                delete_after=10)
        return True
    else:
        return False


class DeleteButton(discord.ui.View):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red)
    async def button_callback(self, button,
                              interaction):  # I have no idea why there are 2 unused variables, removing them breaks the code
        await self.msg.delete()
