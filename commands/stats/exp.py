import discord
from discord import app_commands
from discord.ext import commands

from config import EMBED_COLOR, EMOJIS
from utils import Formulas, format_number


async def setup_exp_command(bot: commands.Bot):
    """Configure the /exp command"""
    
    @bot.tree.command(name="exp", description="Calculates the experience at the current base level")
    @app_commands.describe(
        level="Base level to calculate experience for (1-1000)"
    )
    async def exp_command(interaction: discord.Interaction, level: app_commands.Range[int, 1, 1000]):
        """
        Calculates the total and required experience for a level
        
        Args:
            interaction: The Discord interaction
            level: The base level
        """
        embed = discord.Embed(
            title="Experience Calculation",
            color=EMBED_COLOR
        )
        
    # Calculate experience for the current and next level
        current_exp = Formulas.exp_calc(level)
        next_exp = Formulas.exp_calc(level + 1)
        exp_needed = next_exp - current_exp
        
        embed.description = (
            f"Level **{format_number(level)}** is at **{format_number(int(current_exp))}** exp!\n"
            f"You need **{format_number(int(exp_needed))}** experience to reach Level **{format_number(level + 1)}**!"
        )
        
        await interaction.response.send_message(embed=embed)