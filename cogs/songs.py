from discord.utils import get
from discord.ext import commands
import discord, os, sqlite3
from table import init
import yt_dlp
from discord_components import DiscordComponents, Button


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.db = sqlite3.connect('data/data.db')
        self.c = self.db.cursor()
        init(self.db, self.c)

        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        self.queues = {}
        self.current_song, self.current_title = {}, {}
        self.current_loop = {}
        self.song_titles = {}
        self.volume = 0.5

    def queue(self, ctx, voice):
        g = ctx.guild.id

        del self.song_titles[g][0], self.queues[g][0]
        if len(self.queues[g]) < 1:
            return

        if not voice.is_playing():
            self.current_song[g] = None
            self.current_title[g] = None

        new_song = self.current_loop[g] or self.queues[g][0]
        if new_song:
            voice.play(discord.FFmpegPCMAudio(f'./data/songs/{new_song}.mp3'), after=lambda x: self.queue(ctx, voice))

    @commands.command()
    async def play(self, ctx, url: str = None):

        if not url:
            ctx.send('Please gimme a url smh')
            return

        song_id = []
        if "=" in url:
            song_id.append(url.split("=")[1])
        elif "/" in url:
            song_id.append(url.split("/")[3])
        else:
            song_id.append(None)

        song_id = song_id[0]
        song_id.strip('=')
        song_id.strip('&list')

        vc = get(ctx.guild.voice_channels, name="music")
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice is None:
            await vc.connect()
            voice = get(self.client.voice_clients, guild=ctx.guild)

        else:
            if not voice.is_connected():
                await vc.connect()

        if ctx.guild.id not in self.queues:
            self.queues[ctx.guild.id] = []
            self.song_titles[ctx.guild.id] = []

        self.c.execute('SELECT * FROM songs_cache')
        songs = self.c.fetchall()
        video_title = []
        if song_id not in [s[0] for s in songs]:

            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                video = ydl.extract_info(url, download=True)
                video_title.append(video.get('title', None))

            for file in os.listdir('./'):
                if file.endswith('.mp3'):
                    try:
                        os.rename(file, f'./data/songs/{song_id}.mp3')
                    except:
                        pass

            self.c.execute('INSERT INTO songs_cache values(?,?)', (song_id, video_title[0]))
            self.db.commit()

        if not video_title:
            for s in songs:
                if s[0] == song_id:
                    video_title.append(s[1])

        print(video_title)

        if not voice.is_playing():

            self.queues[ctx.guild.id].append(song_id)
            self.song_titles[ctx.guild.id].append(video_title[0])

            self.current_song[ctx.guild.id] = song_id
            self.current_title[ctx.guild.id] = video_title[0]

            voice.play(discord.FFmpegPCMAudio(f'./data/songs/{song_id}.mp3'), after=lambda x: self.queue(ctx, voice))
            voice.source = discord.PCMVolumeTransformer(voice.source, volume=self.volume)
        else:
            self.queues[ctx.guild.id].append(song_id)
            self.song_titles[ctx.guild.id].append(video_title[0])
            await ctx.send('Song should have been added to the queue.')

    @commands.command()
    async def volume(self, ctx, *, volume):

        if not isinstance(volume, int):
            if volume == "max":
                volume = 100
            elif volume == "min":
                volume = 0

        volume = int(volume)

        voice = get(self.client.voice_clients, guild=ctx.guild)
        if (not voice) or (not voice.is_playing()):
            ctx.send('Currently not connected to a voice channel or is not playing anything')
            return

        if 0 > volume > 100:
            ctx.send('Please provide volume as a number between 1 and 100.')
            return
        voice.source.volume = volume / 100
        self.volume = volume / 100

    @commands.command()
    async def loop(self, ctx):
        self.current_loop[ctx.guild.id] = self.current_song
        await ctx.send('Song will be looped! (until +stop-loop)')

    @commands.command(aliases=['sloop', 'stop-loop'])
    async def unloop(self, ctx):
        try:
            del self.current_loop[ctx.guild.id]
        except KeyError:
            await ctx.send('No song was currently in loop...')
            return
        else:
            await ctx.send('The song is not gonna play in loop anymore!')

    @commands.command()
    async def leave(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("I am not connected to a voice channel")

    @commands.command()
    async def pause(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()
        elif voice.is_paused():
            voice.resume()
        else:
            await ctx.send("Currently no music is playing")

    @commands.command()
    async def stop(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.stop()

    @commands.command(aliases=['queue-list', 'qlist', 'q-list'])
    async def q_list(self, ctx):

        new_song, others = "", []
        if len(self.song_titles[ctx.guild.id]) >= 2:
            new_song = self.song_titles[ctx.guild.id][1]
        else:
            new_song = 'No Song'
        if len(self.song_titles[ctx.guild.id]) >= 3:
            others = self.song_titles[ctx.guild.id][2:]
        else:
            others.append('No Song')
        print(others)
        other_songs = ""
        for s in others:
            other_songs += s + '\n'

        embed = discord.Embed(title="Queue List", description="songs in queue", color=discord.Color.from_rgb(0, 0, 225))
        embed.add_field(name="Currently Playing", value=self.current_title, inline=True)
        embed.add_field(name="Next Up", value=new_song, inline=False)
        embed.add_field(name="Other", value=other_songs, inline=False)
        embed.set_footer(text="ooo songs")

        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.stop()
            self.queue(ctx, voice, self.song_id[1])

    # rajs half broken code

    """commands.command()

    async def setup(ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        guild = ctx.message.guild

        msg = await client.wait_for("message", check=check)  # timeout is None by default
        channel_id = msg.channel_mentions[0].id

        await ctx.send("the stuf u wan sya", components=[
            Button(label=":play_pause:"),
            Button(label=":stop_button:"),
            Button(label=":track_next:"),
            Button(label=":repeat:"),
            Button(label=":twisted_rightwards_arrows:"),
            Button(label=":star:"),

        ])



#half broken class
class MusicView(View):
    def ___init__(self, ctx):
      super().__init()
      self.ctx = ctx

    @button(label=':play_pause:', style=discord.ButtonStyle.success)
    async def play_callback(self, button, interaction):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice.is_playing():
            voice.pause()
        elif voice.is_paused():
            voice.resume()
        else:
            await self.ctx("Currently no music is playing")

    @button(label=':stop_button:', style=discord.ButtonStyle.danger)
    async def stop_callback(self, button, interaction):
        pass

    @button(label=':track_next:', style=discord.ButtonStyle.secondary)
    async def next_callback(self, button, interaction):
        pass

    @button(label=':repeat:', style=discord.ButtonStyle.primary)
    async def repeat_callback(self, button, interaction):
        pass

    @button(label=':twisted_rightwards_arrows:', style=discord.ButtonStyle.primary)
    async def mix_callback(self, button, interaction):
        pass

    @button(label=':star:', style=discord.ButtonStyle.primary)
    async def save_callback(self, button, interaction):
        pass

"""



def setup(client):
    client.add_cog(Music(client))