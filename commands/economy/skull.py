import discord
from discord import app_commands
from discord.ext import commands

from config import EMBED_COLOR, EMOJIS
from utils import format_number


async def setup_skull_command(bot: commands.Bot):
    """Configure the /skull command"""
    
    @bot.tree.command(name="skull", description="Calculates the amount of gold needed for skulling")
    @app_commands.describe(
        base="Base level (1-1000)"
    )
    async def skull_command(interaction: discord.Interaction, base: app_commands.Range[int, 1, 1000]):
        """
        Calculates the gold required to obtain each type of skull
        
        Args:
            interaction: The Discord interaction
            base: The player's base level
        """
        embed = discord.Embed(
            title="Skulling Gold Calculation",
            color=EMBED_COLOR
        )
        
    # Calculations for each skull type
        # Yellow skull = 150 * base
        # Orange skull = 150 * 4 * base = 600 * base
        # Red skull = 150 * 13 * base = 1950 * base
        # Black skull = 150 * 40 * base = 6000 * base
        
        yellow_gold = 150 * base
        orange_gold = 150 * 4 * base
        red_gold = 150 * 13 * base
        black_gold = 150 * 40 * base
        
        embed.description = (
            f"Base Level: **{format_number(base)}**\n"
            f"Gold Needed for **Yellow Skull**{EMOJIS['skull_yellow']}: **{format_number(150 * base)}** {EMOJIS['gold']}\n"
            f"Gold Needed for **Orange Skull**{EMOJIS['skull_orange']}: **{format_number(150 * 4 * base)}** {EMOJIS['gold']}\n"
            f"Gold Needed for **Red Skull**{EMOJIS['skull_red']}: **{format_number(150 * 13 * base)}** {EMOJIS['gold']}\n"
            f"Gold Needed for **Black Skull**{EMOJIS['skull_black']}: **{format_number(150 * 40 * base)}** {EMOJIS['gold']}"
        )
        
        await interaction.response.send_message(embed=embed)