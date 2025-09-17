import discord
from discord import app_commands
from discord.ext import commands

from config import EMBED_COLOR, EMOJIS


async def setup_info_command(bot: commands.Bot):
    """Configure the /info command"""
    
    @bot.tree.command(name="info", description="Shows more information about the bot")
    async def info_command(interaction: discord.Interaction):
        """
        Displays detailed information about the bot and its features
        
        Args:
            interaction: The Discord interaction
        """
        embed = discord.Embed(
            title=f"Info and Credits {EMOJIS['slime_lord']}{EMOJIS['slime']}",
            color=EMBED_COLOR
        )
        
    # Full information message
        message = (
            "**Doub' Rucoy Calculator v1.2** - Upload on **29/06/2025**\n"
            "Made by **Doub** (doub.cpp)\n\n"
            
            "I'm a Rucoy Calculator with a variety of features/commands such as:\n"
            f"{EMOJIS['slime']} /train and /ptrain commands, which tells you the best mob for effective training!\n"
            f"{EMOJIS['slime']} /dmg command, which tells you the damage you do to a certain mob!\n"
            f"{EMOJIS['slime']} /weapon command, which tells you the best weapon to train with!\n"
            f"{EMOJIS['slime']} /oneshot command, which tells you the stat level needed to one-shot a certain mob!\n"
            f"{EMOJIS['slime']} /offline command, which tells you the amount of offline training you need to reach the next level\n"
            f"{EMOJIS['slime']} + much more!\n\n"
          
            "**Technologies Used:**\n"
            "• Python with discord.py\n"
            "• Web scraping API for real-time data\n\n"
            
            "*If you have any suggestions, tips, or if there are any bugs, please let me know on discord: **doub.cpp***\n"
        )
        
        embed.description = message
        
        # Add additional information in fields
        embed.add_field(
            name="Servers",
            value=f"Present in **{len(bot.guilds)}** servers",
            inline=True
        )
        embed.add_field(
            name="Users",
            value=f"Serving **{sum(guild.member_count for guild in bot.guilds)}** users",
            inline=True
        )
        embed.add_field(
            name="Uptime",
            value="Online 24/7",
            inline=True
        )
        
        # Footer with credits
        embed.set_footer(
            text="Made by Doub | doub.cpp",
            icon_url=bot.user.avatar.url if bot.user.avatar else None
        )
        
        await interaction.response.send_message(embed=embed)