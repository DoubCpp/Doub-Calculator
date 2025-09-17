import discord
from discord import app_commands
from discord.ext import commands

from config import EMBED_COLOR, EMOJIS
from utils import Formulas, format_number, format_float


async def setup_offline_command(bot: commands.Bot):
    """Configure the /offline command"""
    
    @bot.tree.command(name="offline", description="Calculates the time needed between stat1 and stat2, or the stat gain from specified hours")
    @app_commands.describe(
        stat1="Initial stat level (50-1000)",
        stat2="Goal stat level (50-1000)"
    )
    async def offline_command(
        interaction: discord.Interaction,
        stat1: app_commands.Range[int, 50, 1000],
        stat2: app_commands.Range[int, 50, 1000]
    ):
        """
        Calculates the necessary offline training time
        
        Args:
            interaction: The Discord interaction
            stat1: Initial stat level
            stat2: Target stat level
        """
        # Ensure stat2 > stat1 (same as original)
        if stat1 >= stat2:
            return
            
        embed = discord.Embed(
            title="Offline Training Calculation",
            color=EMBED_COLOR
        )
        
        if stat1 <= 54:
            ticks1 = Formulas.stat0to54_calc(stat1)
        else:
            ticks1 = Formulas.stat55to99_calc(stat1)
            
        if stat2 <= 54:
            ticks2 = Formulas.stat0to54_calc(stat2)
        else:
            ticks2 = Formulas.stat55to99_calc(stat2)
            
        total_ticks = ticks2 - ticks1
        
        embed.description = (
            f"Initial Stat: **{format_number(stat1)}** {EMOJIS['slime_lord']} Goal Stat: **{format_number(stat2)}**\n"
            f"You need approximately **{format_number(int(total_ticks))}** ticks until you reach stat level **{format_number(stat2)}**!\n"
            f"This is around **{format_float(total_ticks * 60 / 600)}** minutes, or **{format_float(total_ticks / 600)}** hours of offline training at **600** exp/hr"
        )
        
        await interaction.response.send_message(embed=embed)