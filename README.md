# Discord Music Bot

## Description

Discord Music Bot is a powerful and versatile bot designed to bring music and entertainment to your Discord server. This bot allows users to search for songs, play them in voice channels, and control playback with various commands. Built with Python and utilizing the discord.py library, this bot provides a seamless music experience for your server members.

## Features

- **Join and Leave Voice Channels**: The bot can join and leave voice channels based on user commands.
- **Search and Play Music**: Users can search for songs by name, select from a list of results, and play their choice.
- **Playback Controls**: Commands to pause, resume, stop, and skip tracks, ensuring full control over the music experience.
- **Queue Management**: The bot maintains a queue of songs, allowing multiple tracks to be lined up for continuous playback.
- **Volume Control**: Adjust the playback volume to suit your preferences.
- **Rich Embeds**: Provides visually appealing embeds with details about the currently playing track.

## Commands

- `!join`: Joins the bot to the user's current voice channel.
- `!leave`: Makes the bot leave the voice channel.
- `!play <url>`: Plays a song from a URL or searches for and plays a song by name.
- `!search <query>`: Searches for songs matching the query and lets the user select from a list.
- `!pause`: Pauses the currently playing track.
- `!resume`: Resumes the paused track.
- `!stop`: Stops the current track and clears the queue.
- `!skip`: Skips the current track.
- `!queue`: Displays the current song queue.
- `!volume <value>`: Sets the playback volume (0-100).
- `!testaudio`: Plays a test audio file to verify bot functionality (for development and troubleshooting).

## Installation

### Prerequisites

- Python 3.8 or higher
- `ffmpeg` installed and added to your system PATH

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
