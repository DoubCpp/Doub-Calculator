import asyncio
import discord
from discord.ext import commands
import os
import sys

from config import BOT_TOKEN, COMMAND_PREFIX

from commands.help import HelpCog
from commands.listservers import ListServersCog

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')

    await bot.change_presence(activity=discord.Game(name="Use /help for commands"))

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

async def load_cogs():
    await bot.add_cog(HelpCog(bot))
    await bot.add_cog(ListServersCog(bot))

    from commands.calc import setup_slash_commands
    await setup_slash_commands(bot)

async def main():
    async with bot:
        await load_cogs()
        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user")
    except Exception as e:
        import traceback
        print(f"Error starting bot: {e}")
        print("Full traceback:")
        traceback.print_exc()
        sys.exit(1)
