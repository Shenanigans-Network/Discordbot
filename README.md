# Moonball Discord Bot #
This Discord Bot was originally made to improve user experience on the Moonball Network's Discord server, But now it has turned to something very big  
It has Many Features, Spread into multiple cogs for easy readability and higher performance.

# Contents #
`/` The root directory contains the bot.py file and the config file, has all the code required to run the bot's framework  
`/cogs` The actual bot code, split to multiple .py python files, each containing many commands and features of the respective category  
`/data` Containing all data stored by the bot. Includes a SQLITE3 Database file and a .ENV file  

## Requirements ##
This Bot requires many components to function properly, and for you, the end user to make the most out of it. 

##### Packages #####

- Discord
- Requests
- Json
- Sqlite3
- os
- Asyncio
- mcstatus
- Hashlib
- Mysql.connector
- datetime
- random
- Aiohttp
- configparser
- logging
- time
- re

##### Other Requirements #####
- Minecraft Plugins
  - **Essentials**: Managing money and sending mail/msg
  - **AuthMe**: Connection System, Un-register, Change-password
- The **Pterodactyl** Panel
  - One of the core features of this Bot includes the ability to interact with backend servers, sending commands, getting status and much more, thought the Pterodactyl API, which requires you, the end user; to use the Pterodactyl Panel
- Basic knowledge of Python and Troubleshooting
  - Basic knowledge of Python is needed with the ability to troubleshoot any error the bot produces, other than known errors. Which will later be fixed me in a future update. There can be any error within any part of the code, sometimes not even an error with the code but with an API we are using. You must know how to troubleshoot it, because I will not be providing support. I will fix bugs within the code, if you find any.

## Installation ##
1. Ensure you have a `requirements.txt` file, upon downloading the bot's code from GitHub Releases. Run the line of code below to install the required packages, while CMD is open in the bot's directory.  

```bash
$ pip3 install -r requirements.txt
```

2. Go to https://github.com/Shenanigans-Network/Discordbot/releases and download the latest version's .zip file.
3. Download the .zip file and extract it to the bot's directory.
4. Head on to https://discord.com/developers/applications, Make sure you're logged into your Discord Account and create an Application (New Application Button)
5. After Setting its name and details, proceed to the `Bot` tab. Ignore what it says and click on the `Add Bot` button, further clicking `Confirm` when prompted.  
6. In the `Bot` Tab, scroll down, and you can find three Indents, `Privileged Gateway Intents`, `Server Members Intent` and `Message Content Intent`. Click on the tick boxes to enable all three.
7. There's a Token on the top of the Bot Tab too, in the top of the Bot tab. Click on the `Reset Token` button and click confirm. 
8. Copy it and put it in the `/data/config.ini` file, within the Moonball Bot files. Make sure to _not_ give the token to anyone else, since they can use it to log into your bot and do anything!
9. Go in the `/data/config.ini` file and customise everything to you liking. Input every variable required. 
10. When you feel everything is customised to your liking, execute the bot with Python 3.
```shell
  $ python bot.py
  ```
There you go, your bot should now be running, 
11. Now, to add your bot go to `OAuth2` ⟶ `URL Generator`. There, Tick the `Bot` and `applications.commands` checkboxes.
12. Now copy the URL generated and use it to add the bot to your server

```
/joke
```



## Features ##

A list of features can be found at the bot Wiki  
https://github.com/Shenanigans-Network/Discordbot/wiki


## Development ##
The discord Bot is built in `Python`, using the `discord.py` library.
To add your custom code, it must be in the pycord cog format.  

```python
import discord
from discord.ext import commands

class Example(commands.Cog):
  def __init__(self, client):
    self.client = client

    # Use @command.Cog.listener() for listeners
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog : Example.py Loaded")
    
    # Use @commands.command() for a command
    @commands.command()
    async def ping(self, ctx):
      await ctx.reply("pong!")

def setup(client):
    client.add_cog(Example(client))
```

Add the `.py` file into the `/cogs` folder, and restart your bot.
There will be no support, to what ever you try to add on your own to the bot, You must know basic Python and discord.py before trying to attempt this  

## Contact Me ##
If you have any issue, find a bug within my code or just want to talk, You can contact me on my Discord or Instagram  

Discord - `Raj Dave#3215`  
[Website](https://raj.moonball.io) |
[Instagram](https://www.instagram.com/raj_clicks25/) |
[Reddit](https://www.reddit.com/user/itz_raj69_/) |
[Github](https://github.com/rajdave69) 

