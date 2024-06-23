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
            embed = discord.Embed(
                title="Joined Voice Channel",
                description=f"Joined {channel.name}.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="You are not connected to a voice channel.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    async def leave(self, ctx):
        self.queue.clear()
        await ctx.voice_client.disconnect()
        embed = discord.Embed(
            title="Left Voice Channel",
            description="Disconnected from the voice channel.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    async def search_and_play(self, ctx, query):
        if ctx.author.voice is None:
            embed = discord.Embed(
                title="Error",
                description="You need to be in a voice channel to search for and play songs.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        async with ctx.typing():
            self.song_search_results = await YTDLSource.search(query, loop=self.bot.loop)
            if not self.song_search_results:
                embed = discord.Embed(
                    title="No Results Found",
                    description=f"No results found for `{query}`.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return

            search_list = "\n".join([f"{idx + 1}. {entry['title']}" for idx, entry in enumerate(self.song_search_results)])
            embed = discord.Embed(
                title="Search Results",
                description=f"Select a song by clicking its number:\n{search_list}",
                color=discord.Color.blue()
            )
            view = discord.ui.View()
            for idx in range(len(self.song_search_results)):
                view.add_item(discord.ui.Button(label=str(idx + 1), style=discord.ButtonStyle.primary, custom_id=str(idx)))

            message = await ctx.send(embed=embed, view=view)

            def check(interaction):
                return interaction.message.id == message.id and interaction.user == ctx.author

            try:
                interaction = await self.bot.wait_for('interaction', check=check, timeout=30.0)
                selected_idx = int(interaction.data['custom_id'])
                await interaction.response.send_message(f"You selected: {self.song_search_results[selected_idx]['title']}")
                await self.play(ctx, self.song_search_results[selected_idx]['url'])
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title="Timeout",
                    description="You took too long to respond.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                await message.delete()

    async def play(self, ctx, url):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            self.queue.append(player)

            embed = discord.Embed(
                title="Now Playing",
                description=player.title,
                color=discord.Color.green()
            )
            embed.add_field(name="Duration", value=str(player.data.get('duration')), inline=True)
            embed.add_field(name="Uploader", value=player.data.get('uploader'), inline=True)
            embed.set_thumbnail(url=player.data.get('thumbnail'))

            await ctx.send(embed=embed)

            if not ctx.voice_client.is_playing():
                await self.start_playing(ctx)

    async def start_playing(self, ctx):
        if self.queue:
            player = self.queue.pop(0)
            ctx.voice_client.play(player, after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))
            embed = discord.Embed(
                title="Now Playing",
                description=player.title,
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

    async def play_next(self, ctx):
        if self.queue:
            player = self.queue.pop(0)
            ctx.voice_client.play(player, after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))
            embed = discord.Embed(
                title="Now Playing",
                description=player.title,
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Queue Empty",
                description="No more songs in the queue.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

    async def pause(self, ctx):
        ctx.voice_client.pause()
        embed = discord.Embed(
            title="Paused",
            description="Music playback has been paused.",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    async def resume(self, ctx):
        ctx.voice_client.resume()
        embed = discord.Embed(
            title="Resumed",
            description="Music playback has been resumed.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    async def stop(self, ctx):
        self.queue.clear()
        ctx.voice_client.stop()
        embed = discord.Embed(
            title="Stopped",
            description="Music playback has been stopped and the queue has been cleared.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    async def skip(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            embed = discord.Embed(
                title="Skipped",
                description="Current track has been skipped.",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)

    async def queue(self, ctx):
        if self.queue:
            queue_titles = [player.title for player in self.queue]
            embed = discord.Embed(
                title="Current Queue",
                description="\n".join(queue_titles),
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Queue Empty",
                description="The queue is empty.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

