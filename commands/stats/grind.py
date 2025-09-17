import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

from config import EMBED_COLOR, EMOJIS
from utils import Formulas, format_number, format_float


async def setup_grind_command(bot: commands.Bot):
    """Configure the /grind command"""
    
    @bot.tree.command(name="grind", description="Calculates the experience needed to reach a certain base level")
    @app_commands.describe(
        base1="Initial base level (1-1000)",
        base2="Goal base level (1-1000)",
        grindrate="Experience per hour (default: 2000000)"
    )
    async def grind_command(
        interaction: discord.Interaction, 
        base1: app_commands.Range[int, 1, 1000],
        base2: app_commands.Range[int, 1, 1000],
        grindrate: Optional[int] = 2000000
    ):
        """
        Calculates the time and experience required to reach a level
        
        Args:
            interaction: The Discord interaction
            base1: Starting level
            base2: Target level
            grindrate: Experience rate per hour
        """
        # Ensure base2 > base1 (same as original)
        if base1 >= base2:
            return
            
        embed = discord.Embed(
            title="Grinding Calculation",
            color=EMBED_COLOR
        )
        
    # Calculate required experience
        exp1 = Formulas.exp_calc(base1)
        exp2 = Formulas.exp_calc(base2)
        exp_needed = exp2 - exp1
        hours_needed = exp_needed / grindrate
        minutes_needed = hours_needed * 60
        
        embed.description = (
            f"Initial Level: **{format_number(base1)}** {EMOJIS['slime_lord']} Goal Level: **{format_number(base2)}** {EMOJIS['slime_lord']} Grindrate: **{format_number(grindrate)}** Exp/Hour\n"
            f"You need **{format_number(int(exp_needed))}** experience until you reach base level **{format_number(base2)}**!\n"
            f"This is around **{format_float(minutes_needed)}** minutes, or **{format_float(hours_needed)}** hours of grinding at a rate of **{format_number(grindrate)}** exp/hr!"
        )
        
        await interaction.response.send_message(embed=embed)