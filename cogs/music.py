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
import time

from discord.utils import get
from discord.ext import commands
from discord import SlashCommandGroup
import discord, os, sqlite3, random, yt_dlp, re
from youtube_search import YoutubeSearch
from backend import embed_icon, embed_color, embed_footer, embed_header, embed_url, client, music_channel, guild_id  # , music_vc
from backend import checkperm, log


class ReplayButton(discord.ui.View):
    def __init__(self, ctx, video_url, msg):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.url = video_url
        self.client = client
        self.message = msg

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

    @discord.ui.button(label="Replay", style=discord.ButtonStyle.gray, custom_id="replay")
    async def button_callback(self, button, interaction):  # Don't remove the unused variable
        await interaction.response.send_message("Added song to queue.", ephemeral=True)
        await self.client.cogs.get('Music').player(self.ctx, self.url)


class DedicatedButtons(discord.ui.View):
    def __init__(self, voice):
        super().__init__(timeout=None)
        self.voice = voice
        self.queues = Queue()

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.gray, custom_id="music_playpause")
    async def play_pause_button(self, button, interaction):
        # play pause button
        if self.voice.is_playing():
            self.voice.pause()
            await interaction.response.send_message("Paused the current song.", ephemeral=True)
        else:
            self.voice.resume()
            await interaction.response.send_message("Resumed the current song.", ephemeral=True)

    @discord.ui.button(label="⏭️", style=discord.ButtonStyle.gray, custom_id="music_skip")
    async def skip_button(self, button, interaction):
        # skip button
        await interaction.response.send_message("Skip button pressed", ephemeral=True)
        self.voice.stop()

    @discord.ui.button(label="⏹️", style=discord.ButtonStyle.red, custom_id="music_stop")
    async def stop_button(self, button, interaction):
        # stop button
        if self.voice.is_playing():
            self.voice.stop()
            self.voice.channel.disconnect()
        await interaction.response.send_message("Stop button pressed", ephemeral=True)

    @discord.ui.button(label="🔁", style=discord.ButtonStyle.gray, custom_id="music_loop")
    async def loop_button(self, button, interaction):
        # loop button
        await interaction.response.send_message("Loop button pressed", ephemeral=True)
        self.queues.loop_song()

    @discord.ui.button(label="🔀", style=discord.ButtonStyle.gray, custom_id="music_shuffle")
    async def shuffle_button(self, button, interaction):
        await interaction.response.send_message("Shuffle button pressed", ephemeral=True)
        self.queues.shuffle = True


class Queue:
    def __init__(self):
        self.song_list = []
        self.current_song = None  # [id, title, loop]
        self.shuffle = False

    def get_next_song(self, override=False) -> list | None:
        if self.shuffle:
            self.current_song = random.choice(self.song_list)
            return self.current_song

        if not (self.current_song is None) and self.current_song[2] and not override:
            return self.current_song
        elif len(self.song_list):
            self.current_song = self.song_list.pop()
            return self.current_song
        else:
            return None

    def add_song(self, song_id, title):
        self.song_list.insert(0, [song_id, title, False])

    def loop_song(self):
        self.current_song = [self.current_song[0], self.current_song[1], not self.current_song[2]]

    def skip_song(self):
        return self.get_next_song(override=True)




class Music(commands.Cog):
    music = SlashCommandGroup("music", "Music related commands")

    def __init__(self, client):
        self.client = client

        self.db = sqlite3.connect('./data/music.db')
        self.c = self.db.cursor()

        self.ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        self.queues = Queue()
        self.volume = 0.5

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog : Music.py Loaded")


    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.id == self.client.user.id: return
        if ctx.channel.id != music_channel: return

        content = ctx.content
        await ctx.delete()

        if not re.search(
                r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\n]*)',
                content):
            results = YoutubeSearch(content, max_results=1).to_dict()
            log.debug(results[0]['id'])
            content = f"https://www.youtube.com/watch?v={results[0]['id']}"
            log.debug(content)

        # key | title | song_id | duration
        res = await self.player(ctx, content)

        if res == "length_too_long":
            return
        log.debug(res)



    def next_song(self, voice) -> None:

        song = self.queues.get_next_song()
        if song: voice.play(discord.FFmpegPCMAudio(f'./data/songs/{song[0]}.mp3'),
                            after=lambda x: self.next_song(voice))

    async def player(self, ctx, song_url):
        vc = get(ctx.guild.voice_channels, name="Music")
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice is None:
            await vc.connect()
            voice = get(self.client.voice_clients, guild=ctx.guild)

        else:
            if not voice.is_connected():
                await vc.connect()

        self.c.execute('SELECT * FROM songs_cache')
        songs = self.c.fetchall()
        video_title = []

        # get video id
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                vid_info = ydl.extract_info(song_url, download=False)
                song_id = vid_info['id']
                video_duration = vid_info['duration']
                video_title.append(vid_info['title'])

            except Exception as e:
                log.error(e)
                return "vid_not_found"
            if video_duration > 599:
                return "length_too_long"

        if song_id not in [s[0] for s in songs]:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.extract_info(song_url, download=True)

            for file in os.listdir('./'):
                if file.endswith('.mp3'):
                    try:
                        os.rename(file, f'./data/songs/{song_id}.mp3')
                    except FileExistsError:
                        log.warning(f"File {song_id} already exists in ./data/songs/")

            self.c.execute(f'INSERT INTO songs_cache values("{song_id}","{video_title[0]}")')
            self.db.commit()

        if not video_title:
            for s in songs:
                if s[0] == song_id:
                    video_title.append(s[1])

        if voice:
            if not voice.is_playing():

                self.queues.add_song(song_id, video_title)
                self.next_song(voice)
                voice.source = discord.PCMVolumeTransformer(voice.source, volume=self.volume)
                return f"now_playing|{video_title[0]}|{song_id}|{video_duration}"
            else:
                self.queues.add_song(song_id, video_title)
                return f"added_to_queue|{video_title[0]}|{song_id}|{video_duration}"



    @music.command(name="setup", description="Setup the music channel")
    async def m_setup(self, ctx):
        if await checkperm(ctx, 3): return
        voice = get(self.client.voice_clients, guild=ctx.guild)
        m_embed = discord.Embed(title="Music",
                                description="Paste a **YouTube URL** or **Song Name** into this Channel.",
                                color=embed_color, url=embed_url)
        m_embed.set_image(url="https://miro.medium.com/max/1400/1*zOshpZng8plvNt3pPv6KIA.png")
        m_embed.set_footer(text=embed_footer)
        m_embed.set_author(name=embed_header, icon_url=embed_icon)
        await self.client.get_guild(guild_id).get_channel(music_channel).send(embed=m_embed,

                                                                              view=DedicatedButtons(voice))

    @music.command()
    async def play(self, ctx, song: str):
        if await checkperm(ctx, 0): return
        start_time = time.time()

        m_embed = discord.Embed(title="Music", color=embed_color, url=embed_url)
        m_embed.set_footer(text=embed_footer)
        m_embed.set_author(name=embed_header, icon_url=embed_icon)
        m_embed.add_field(name="Please hold on!", value="*We are fetching the song...*", inline=False)
        msg = await ctx.respond(embed=m_embed)
        m_embed.remove_field(0)

        # check valid YouTube url with regex
        if not re.search(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\n]*)',song):
            results = YoutubeSearch(song, max_results=1).to_dict()
            if not results:
                m_embed.add_field(name="Error", value="No results found!", inline=False)
                await msg.edit(embed=m_embed)
                return
            song = f"https://www.youtube.com/watch?v={results[0]['id']}"
            log.debug(song)

        # key | title | song_id | duration
        res = await self.player(ctx, song)

        if res == "length_too_long":
            m_embed.add_field(name="Error", value="Song is too long!", inline=False)
            await msg.edit_original_message(embed=m_embed)
            return

        res = res.split("|")
        status = res[0]
        video_title = res[1]
        video_duration = round(int(res[3]) / 60, 2)

        log.debug(f"Took {round(time.time() - start_time, 2)} seconds to fetch and play song")
        if status == "now_playing":
            m_embed.add_field(name="Now Playing", value=f"{video_title}")
            m_embed.add_field(name="Duration", value=f"{video_duration}")
            await msg.edit_original_message(embed=m_embed, view=ReplayButton(ctx, song, msg))
        elif status == "added_to_queue":
            m_embed.add_field(name="Song added to queue!", value=f"*{video_title}*", inline=False)
            m_embed.add_field(name="Duration", value=f"{video_duration}")
            await msg.edit_original_message(embed=m_embed, view=ReplayButton(ctx, song, msg))



    @music.command()
    async def volume(self, ctx, volume: int):
        if await checkperm(ctx, 0): return

        voice = get(self.client.voice_clients, guild=ctx.guild)
        if (not voice) or (not voice.is_playing()):
            await ctx.respond("I'm not playing anything right now!")
            return

        if 0 > volume > 100:
            await ctx.respond('Please provide volume as a number between 1 and 100.')
            return
        voice.source.volume = volume / 100
        self.volume = volume / 100
        await ctx.respond(f"Volume set to {volume}%")



    @music.command()
    async def loop(self, ctx):
        if await checkperm(ctx, 0): return

        self.queues.loop_song()
        song = self.queues.current_song[1].replace("[", "").replace("'", "").replace("]", "")
        await ctx.respond(f'{song} will be looped!')



    @music.command()
    async def unloop(self, ctx):
        if await checkperm(ctx, 0): return

        self.queues.loop_song()
        song = self.queues.current_song[1].replace("[", "").replace("'", "").replace("]", "")
        await ctx.respond(f'{song} will no longer be looped!')



    @music.command()
    async def leave(self, ctx):
        if await checkperm(ctx, 1): return

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.respond("I am not connected to a voice channel")



    @music.command()
    async def pause(self, ctx):
        if await checkperm(ctx, 0): return
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()
            await ctx.respond("Paused!", ephemeral=True)
        else:
            await ctx.respond("Currently no music is playing!", ephemeral=True)



    @music.command()
    async def resume(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_paused():
            voice.resume()
            await ctx.respond("Resumed!", ephemeral=True)
        else:
            await ctx.respond("The music is not paused!", ephemeral=True)



    @music.command()
    async def stop(self, ctx):
        if await checkperm(ctx, 1): return
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
            await ctx.respond("Stopped!", ephemeral=True)



    @music.command()
    async def queuelist(self, ctx):
        if await checkperm(ctx, 0): return
        if not self.queues.song_list:
            await ctx.respond("No songs in queue")
            return

        queue_list = "\n".join(f"{i + 1}. {self.queues.song_list[i][1]}" for i in range(len(self.queues.song_list)))
        queue_list = (queue_list.replace("[", "").replace("]", "").replace("'", ""))[::-1]    # get rid of []' and reverse

        m_embed = discord.Embed(title="Music", color=embed_color, url=embed_url)
        m_embed.set_footer(text=embed_footer)
        m_embed.set_author(name=embed_header, icon_url=embed_icon)
        m_embed.add_field(name="Queue", value=queue_list, inline=False)
        await ctx.respond(embed=m_embed)



    @music.command()
    async def skip(self, ctx):
        if await checkperm(ctx, 0): return

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.stop()
            song = self.queues.skip_song()
            if song: voice.play(discord.FFmpegPCMAudio(f'./data/songs/{song[0]}.mp3'),
                                after=lambda x: self.next_song(voice))
            await ctx.respond("Skipped current song!")
        else:
            await ctx.respond("No music is playing")


    @music.command()
    async def add_song(self, ctx, playlist: str):

        self.c.execute(f"CREATE TABLE IF NOT EXISTS playlists_{ctx.author.id} (playlist TEXT, song_id TEXT, titles TEXT)")
        self.db.commit()

        if not self.queues.current_song[0]:
            await ctx.respond("No song is currently playing")
            return

        self.c.execute(f'SELECT song_id FROM playlists_{ctx.author.id} WHERE song_id="{self.queues.current_song[0]}" AND playlist="{playlist}"')
        res = self.c.fetchone()
        if res is not None:
            log.debug(res)
            await ctx.respond("Already added!")
            return

        # remove special characters from playlist name
        playlist = playlist.replace(";", "").replace('"', '').replace("'", "").replace("`", "")


        self.c.execute(f'INSERT INTO playlists_{ctx.author.id} (playlist, song_id, titles) values("{playlist}", "{self.queues.current_song[0]}", "{self.queues.current_song[1][0]}")')
        self.db.commit()

        await ctx.respond(f"Added `{self.queues.current_song[1]}` to your `{playlist}` Playlist!")



    @music.command()
    async def play_playlist(self, ctx, playlist: str):
        self.c.execute(f"SELECT song_id FROM playlists_{ctx.author.id} WHERE playlist='{playlist}'")
        songs = self.c.fetchall()

        if not songs:
            await ctx.respond("No songs in your songs playlist! Try again.")
            return

        log.debug(songs)
        for song in songs:
            self.queues.add_song(song[0], song[1])

def setup(client):
    client.add_cog(Music(client))