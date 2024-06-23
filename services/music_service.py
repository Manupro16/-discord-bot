import asyncio

import discord
from utils.ytdl import YTDLSource

class MusicService:
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.song_search_results = []

    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")

    async def leave(self, ctx):
        self.queue.clear()
        await ctx.voice_client.disconnect()

    async def search_and_play(self, ctx, query):
        async with ctx.typing():
            self.song_search_results = await YTDLSource.search(query, loop=self.bot.loop)
            if not self.song_search_results:
                await ctx.send("No results found.")
                return

            search_list = "\n".join([f"{idx + 1}. {entry['title']}" for idx, entry in enumerate(self.song_search_results)])
            view = discord.ui.View()
            for idx in range(len(self.song_search_results)):
                view.add_item(discord.ui.Button(label=str(idx + 1), style=discord.ButtonStyle.primary, custom_id=str(idx)))

            message = await ctx.send(f"Select a song by clicking its number:\n{search_list}", view=view)

            def check(interaction):
                return interaction.message.id == message.id and interaction.user == ctx.author

            try:
                interaction = await self.bot.wait_for('interaction', check=check, timeout=30.0)
                selected_idx = int(interaction.data['custom_id'])
                await interaction.response.send_message(f"You selected: {self.song_search_results[selected_idx]['title']}")
                await self.play(ctx, self.song_search_results[selected_idx]['url'])
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond.")
                await message.delete()

    async def play(self, ctx, url):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            self.queue.append(player)
            await ctx.send(f'Queued: {player.title}')

            if not ctx.voice_client.is_playing():
                await self.start_playing(ctx)

    async def start_playing(self, ctx):
        if self.queue:
            player = self.queue.pop(0)
            ctx.voice_client.play(player, after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))
            await ctx.send(f'Now playing: {player.title}')

    async def play_next(self, ctx):
        if self.queue:
            player = self.queue.pop(0)
            ctx.voice_client.play(player, after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))
            await ctx.send(f'Now playing: {player.title}')
        else:
            await ctx.send('Queue is empty.')

    async def pause(self, ctx):
        ctx.voice_client.pause()

    async def resume(self, ctx):
        ctx.voice_client.resume()

    async def stop(self, ctx):
        self.queue.clear()
        ctx.voice_client.stop()

    async def skip(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    async def queue(self, ctx):
        if self.queue:
            queue_titles = [player.title for player in self.queue]
            await ctx.send('\n'.join(queue_titles))
        else:
            await ctx.send('The queue is empty.')
