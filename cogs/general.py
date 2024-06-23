import discord
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Responds with 'Pong!'"""
        await ctx.send('Pong!')

    @commands.command(name='custom_help')
    async def custom_help(self, ctx):
        """Provides help information for commands"""
        help_text = """
        **Commands:**
        !ping - Responds with 'Pong!'
        !join - Joins a voice channel
        !play [url] - Plays audio from a URL
        !queue - Displays the current queue
        !skip - Skips the current track
        !pause - Pauses the current track
        !resume - Resumes the current track
        !stop - Stops the current track
        !leave - Leaves the voice channel
        """
        await ctx.send(help_text)

    @commands.command(name='admin')
    @commands.has_permissions(administrator=True)
    async def admin(self, ctx):
        """Admin-only command"""
        await ctx.send('You are an administrator!')

    @commands.command(name='userinfo')
    async def userinfo(self, ctx, member: commands.MemberConverter = None):
        """Displays information about a user"""
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f"{member.name}'s info", description=f"Here's what I found about {member.name}")
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Name", value=member.display_name, inline=True)
        embed.add_field(name="Status", value=member.status, inline=True)
        embed.add_field(name="Top Role", value=member.top_role, inline=True)
        embed.add_field(name="Joined At", value=member.joined_at, inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='is_dayton_gay?')
    async def is_dayton_gay(self, ctx):
        await ctx.send('yes indeed he is homosexual ')


async def setup(bot):
    await bot.add_cog(General(bot))
