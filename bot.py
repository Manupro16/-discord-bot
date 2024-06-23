import os
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
import discord

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX', '!')

# Define intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# Remove default help command
bot.remove_command('help')

# Initialize discord-components
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command does not exist. Please use a valid command.")
    else:
        print(error)
        await ctx.send(f"An error occurred while processing the command.")

# List of initial cogs to load
initial_extensions = ['cogs.music', 'cogs.general']

# Load cogs asynchronously
async def load_extensions():
    for extension in initial_extensions:
        await bot.load_extension(extension)

# Run the bot
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

# Entry point for the async event loop
if __name__ == '__main__':
    asyncio.run(main())
