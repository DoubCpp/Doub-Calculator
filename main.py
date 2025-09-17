import asyncio
import discord
from discord.ext import commands
import os
import sys
import traceback

# Import config
from config import BOT_TOKEN, COMMAND_PREFIX

# Import setup_all_commands()
from commands import setup_all_commands


# Configure Discord intents
intents = discord.Intents.default()
intents.message_content = True  # Required for prefix commands

# Initialize the bot
bot = commands.Bot(
    command_prefix=COMMAND_PREFIX,
    intents=intents,
    help_command=None  # We use our own help command
)


@bot.event
async def on_ready():
    """
    Event triggered when the bot is ready
    """
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    
    # Set bot presence
    await bot.change_presence(
        activity=discord.Game(name="Use /help for commands")
    )
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.event
async def on_guild_join(guild):
    """
    Event triggered when the bot joins a new server
    """
    print(f"Joined new guild: {guild.name} (ID: {guild.id})")
    print(f"Total guilds: {len(bot.guilds)}")


@bot.event
async def on_guild_remove(guild):
    """
    Event triggered when the bot is removed from a server
    """
    print(f"Removed from guild: {guild.name} (ID: {guild.id})")
    print(f"Total guilds: {len(bot.guilds)}")


@bot.event
async def on_command_error(ctx, error):
    """
    Global error handler for prefix commands
    """
    if isinstance(error, commands.CommandNotFound):
        # Ignore unknown commands
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ Bad argument: {error}")
    else:
        # Log full error
        print(f"Error in command {ctx.command}: {error}")
        traceback.print_exception(type(error), error, error.__traceback__)


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    """
    Global error handler for slash commands
    """
    if isinstance(error, discord.app_commands.CommandOnCooldown):
        await interaction.response.send_message(
            f"❌ Command on cooldown. Try again in {error.retry_after:.2f} seconds.",
            ephemeral=True
        )
    else:
        # Log full error
        print(f"Error in slash command: {error}")
        traceback.print_exception(type(error), error, error.__traceback__)
        
        # Send a generic error message to the user
        if not interaction.response.is_done():
            await interaction.response.send_message(
                "❌ An error occurred while processing this command.",
                ephemeral=True
            )


async def main():
    """
    Main function to start the bot
    """
    async with bot:
        # Load all commands
        print("Loading commands...")
        await setup_all_commands(bot)
        print("Commands loaded successfully!")
        
        # Start the bot
        print("Starting bot...")
        await bot.start(BOT_TOKEN)


if __name__ == "__main__":
    """
    Program entry point
    """
    try:
        # Check that the token is set
        if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            print("ERROR: Bot token not configured!")
            print("Please set your bot token in config/settings.py")
            sys.exit(1)
        
        # Run the bot
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\nBot stopped by user")
        
    except Exception as e:
        print(f"Error starting bot: {e}")
        print("Full traceback:")
        traceback.print_exc()
        sys.exit(1)
