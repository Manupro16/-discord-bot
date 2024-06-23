from discord.ext import commands
import discord
from services.music_service import MusicService

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_service = MusicService(bot)

    @commands.command(name='join')
    async def join(self, ctx):
        """Joins a voice channel"""
        await self.music_service.join(ctx)

    @commands.command(name='leave')
    async def leave(self, ctx):
        """Leaves a voice channel"""
        await self.music_service.leave(ctx)

    @commands.command(name='play')
    async def play(self, ctx, *, url):
        """Plays from a URL"""
        await self.music_service.play(ctx, url)

    @commands.command(name='search')
    async def search(self, ctx, *, query):
        """Searches for a song and lets the user pick from a list"""
        await self.music_service.search_and_play(ctx, query)

    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pauses the current track"""
        await self.music_service.pause(ctx)

    @commands.command(name='resume')
    async def resume(self, ctx):
        """Resumes the current track"""
        await self.music_service.resume(ctx)

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stops the current track"""
        await self.music_service.stop(ctx)

    @commands.command(name='skip')
    async def skip(self, ctx):
        """Skips the current track"""
        await self.music_service.skip(ctx)

    @commands.command(name='queue')
    async def queue(self, ctx):
        """Displays the current queue"""
        await self.music_service.queue(ctx)

    @commands.command(name='loop')
    async def loop(self, ctx):
        """Toggles looping of the current song"""
        await self.music_service.loop_song(ctx)

    @commands.command(name='loopqueue')
    async def loopqueue(self, ctx):
        """Toggles looping of the entire queue"""
        await self.music_service.loop_queue(ctx)

async def setup(bot):
    await bot.add_cog(Music(bot))
