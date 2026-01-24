"""Discord bot entry point."""

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Called when the bot is ready."""
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command()
async def ping(ctx: commands.Context):
    """Simple ping command to test bot responsiveness."""
    await ctx.send(f"Pong! Latency: {round(bot.latency * 1000)}ms")


def main():
    """Run the Discord bot."""
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise ValueError("DISCORD_BOT_TOKEN environment variable not set")
    bot.run(token)


if __name__ == "__main__":
    main()
