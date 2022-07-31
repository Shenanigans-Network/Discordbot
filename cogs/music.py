import random
from discord.utils import get
from discord.ext import commands
import discord, os, sqlite3
import yt_dlp, re
from discord import SlashCommandGroup
from backend import embed_icon, embed_color, embed_footer, embed_header, embed_url, client
from backend import checkperm, log
from youtube_search import YoutubeSearch



class ReplayButton(discord.ui.View):
    def __init__(self, ctx, video_url):
        super().__init__()
        self.ctx = ctx
        self.url = video_url
        self.client = client

    @discord.ui.button(label="Replay", style=discord.ButtonStyle.gray)
    async def button_callback(self, button, interaction):  # Don't remove the two unused variables
        await interaction.response.send_message("Added song to queue.", ephemeral=True)
        await self.client.cogs.get('Music').player(self.ctx, self.url)

"""
class DedicatedButtons(discord.ui.View):
    def __init__(self, voice):
        super().__init__()
        self.voice = voice

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.gray)
    async def play_pause_button(self, button, interaction):
        # play pause button
        if self.voice.is_playing():
            self.voice.pause()
            await interaction.response.send_message("Paused the current song.", ephemeral=True)
        else:
            self.voice.resume()
            await interaction.response.send_message("Resumed the current song.", ephemeral=True)

    @discord.ui.button(label="⏭️", style=discord.ButtonStyle.gray)
    async def skip_button(self, button, interaction):
        # skip button
        await interaction.response.send_message("Skip button pressed", ephemeral=True)

    @discord.ui.button(label="⏹️", style=discord.ButtonStyle.gray)
    async def stop_button(self, button, interaction):
        # stop button
        await interaction.response.send_message("Stop button pressed", ephemeral=True)
        self.voice.stop()

    @discord.ui.button(label="🔁", style=discord.ButtonStyle.gray)
    async def loop_button(self, button, interaction):
        # loop button
        await interaction.response.send_message("Loop button pressed", ephemeral=True)
        if self.voice.is_looping():
            self.voice.set_loop(False)
        else:
            self.voice.set_loop(True)

    @discord.ui.button(label="⏭️", style=discord.ButtonStyle.gray)
    async def shuffle_button(self):
        pass
"""

class Queue:
    def __init__(self):
        self.song_list = []
        self.current_song = None  # [id, title, loop]

        self.shuffle = False

    def get_next_song(self, overide=False):

        if self.shuffle:
            self.current_song = random.choice(self.song_list)
            return self.current_song

        if not (self.current_song is None) and self.current_song[2] and not overide:
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
        return self.get_next_song(overide=True)


class Music(commands.Cog):
    music = SlashCommandGroup("music", "Music related commands")

    def __init__(self, client):
        self.client = client

        self.db = sqlite3.connect('./data/data.db')
        self.c = self.db.cursor()

        self.ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
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


    def next_song(self, voice):

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
                return
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




    @music.command()
    async def play(self, ctx, song: str):
        if await checkperm(ctx, 0): return

        m_embed = discord.Embed(title="Music", color=embed_color, url=embed_url)
        m_embed.set_footer(text=embed_footer)
        m_embed.set_author(name=embed_header, icon_url=embed_icon)
        m_embed.add_field(name="Please hold on!", value="*We are fetching the song...*", inline=False)
        msg = await ctx.respond(embed=m_embed)
        m_embed.remove_field(0)

        # check valid YouTube url with regex
        if not re.search(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\n]*)', song):
            results = YoutubeSearch(song, max_results=1).to_dict()
            log.debug(results[0]['id'])
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
        video_duration = round((int(res[3]) / 60), 2)

        if status == "now_playing":
            m_embed.add_field(name="Now Playing", value=f"{video_title}")
            m_embed.add_field(name="Duration", value=f"{video_duration}")
            await msg.edit_original_message(embed=m_embed, view=ReplayButton(ctx, song))
        elif status == "added_to_queue":
            m_embed.add_field(name="Song added to queue!", value=f"*{video_title}*", inline=False)
            m_embed.add_field(name="Duration", value=f"{video_duration}")
            await msg.edit_original_message(embed=m_embed, view=ReplayButton(ctx, song))



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

        q = "\n".join(f"{i + 1}. {self.queues.song_list[i][1]}" for i in range(len(self.queues.song_list)))
        q = q.replace("[", "").replace("]", "").replace("'", "")

        m_embed = discord.Embed(title="Music", color=embed_color, url=embed_url)
        m_embed.set_footer(text=embed_footer)
        m_embed.set_author(name=embed_header, icon_url=embed_icon)
        m_embed.add_field(name="Queue", value=q, inline=False)
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


def setup(client):
    client.add_cog(Music(client))