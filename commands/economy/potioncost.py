import discord
from discord import app_commands
from discord.ext import commands

from config import EMBED_COLOR, EMOJIS
from utils import format_number


async def setup_potioncost_command(bot: commands.Bot):
    """Configure the /potioncost command"""
    
    @bot.tree.command(name="potioncost", description="Calculates the amount of gold needed for potions")
    @app_commands.describe(
        numpotions="Number of potions to calculate cost for"
    )
    async def potioncost_command(interaction: discord.Interaction, numpotions: app_commands.Range[int, 1, 10000]):
        """
        Calculates the gold cost for different types of potions
        
        Args:
            interaction: The Discord interaction
            numpotions: The number of potions
        """
        embed = discord.Embed(
            title="Potion Gold Calculation",
            color=EMBED_COLOR
        )
        
    # Potion prices
    # Regular Potion = 50 gold
    # Greater Potion = 150 gold
    # Super Potion = 350 gold
    # Ultimate Potion = 650 gold
        
        normal_cost = numpotions * 50
        greater_cost = numpotions * 150
        super_cost = numpotions * 350
        ultimate_cost = numpotions * 650
        
        embed.description = (
            f"Potion Number: **{format_number(numpotions)}**\n"
            f"Gold Needed for **Potion**{EMOJIS['mana_potion']}{EMOJIS['health_potion']}: **{format_number(numpotions * 50)}** {EMOJIS['gold']}\n"
            f"Gold Needed for **Greater Potion**{EMOJIS['greater_mana_potion']}{EMOJIS['greater_health_potion']}: **{format_number(numpotions * 150)}** {EMOJIS['gold']}\n"
            f"Gold Needed for **Super Potion**{EMOJIS['super_mana_potion']}{EMOJIS['super_health_potion']}: **{format_number(numpotions * 350)}** {EMOJIS['gold']}\n"
            f"Gold Needed for **Ultimate Potion**{EMOJIS['ultimate_mana_potion']}{EMOJIS['ultimate_health_potion']}: **{format_number(numpotions * 650)}** {EMOJIS['gold']}"
        )
        
        await interaction.response.send_message(embed=embed)