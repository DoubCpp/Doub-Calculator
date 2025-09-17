import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

from config import EMBED_COLOR, EMOJIS
from utils import Formulas, format_number, format_float


async def setup_stat_command(bot: commands.Bot):
    """Configure the /stat command"""
    
    @bot.tree.command(name="stat", description="Calculates the amount of ticks and time needed to reach a certain stat level")
    @app_commands.describe(
        stat1="Initial stat level (50-1000)",
        stat2="Goal stat level (50-1000)",
        statrate="Experience rate per hour (optional, for custom calculation)"
    )
    async def stat_command(
        interaction: discord.Interaction,
        stat1: app_commands.Range[int, 50, 1000],
        stat2: app_commands.Range[int, 50, 1000],
        statrate: Optional[int] = None
    ):
        """
        Calculates the time and potions needed to reach a stat level
        
        Args:
            interaction: The Discord interaction
            stat1: Initial stat level
            stat2: Target stat level
            statrate: Custom exp rate (optional)
        """
        # Ensure stat2 > stat1 (same as original)
        if stat1 >= stat2:
            return
            
        embed = discord.Embed(
            title="Stat Calculation",
            color=EMBED_COLOR
        )
        
        # Calculate the required ticks
        if stat1 <= 54:
            ticks1 = Formulas.stat0to54_calc(stat1)
        else:
            ticks1 = Formulas.stat55to99_calc(stat1)
            
        if stat2 <= 54:
            ticks2 = Formulas.stat0to54_calc(stat2)
        else:
            ticks2 = Formulas.stat55to99_calc(stat2)
            
        total_ticks = ticks2 - ticks1
        
        if statrate is not None:
            # Custom calculation with the provided rate
            hours_needed = total_ticks / statrate
            minutes_needed = hours_needed * 60
            
            embed.description = (
                f"Initial Stat: **{format_number(stat1)}** {EMOJIS['slime_lord']} Goal Stat: **{format_number(stat2)}**\n"
                f"You need approximately **{format_number(int(total_ticks))}** ticks until you reach stat level **{format_number(stat2)}**!\n"
                f"This is around **{format_float(minutes_needed)}** minutes, or **{format_float(hours_needed)}** hours of training at a rate of **{format_number(statrate)}** exp/hr!"
            )
        else:
            # Detailed calculation with different exp bonuses
            # Calculations for different power training rates (4-tick)
            mana_1 = int(50 * total_ticks / 4)      # Standard 4-tick powertrain
            mana_1_5 = int(50 * total_ticks / 6)    # 1.5x exp 4-tick powertrain
            mana_2 = int(50 * total_ticks / 8)      # 2x exp 4-tick powertrain
            mana_2_5 = int(50 * total_ticks / 10)   # 2.5x exp 4-tick powertrain
            
            embed.description = (
                f"Initial Stat: **{format_number(stat1)}** {EMOJIS['slime_lord']} Goal Stat: **{format_number(stat2)}**\n"
                f"You need approximately **{format_number(int(total_ticks))}** ticks until you reach stat level **{format_number(stat2)}**!\n\n"
                
                # AFK training without bonuses
                f"This is around **{format_float(total_ticks * 60 / 3600)}** minutes, or **{format_float(total_ticks / 3600)}** hours of afk training without bonuses!\n"
                f"This is around **{format_float(total_ticks * 60 / 14400)}** minutes, or **{format_float(total_ticks / 14400)}** hours of **4-tick** power training without bonuses!\n"
                f"Which will cost you around **{format_number(mana_1 // 100)}{EMOJIS['mana_potion']}**, **{format_number(mana_1 // 250)}{EMOJIS['greater_mana_potion']}**, **{format_number(mana_1 // 500)}{EMOJIS['super_mana_potion']}**, or **{format_number(mana_1 // 750)}{EMOJIS['ultimate_mana_potion']}**\n\n"
                
                # With 1.5x bonus
                f"This is around **{format_float(total_ticks * 60 / (3600 * 1.5))}** minutes, or **{format_float(total_ticks / (3600 * 1.5))}** hours of afk training with a **1.5x** bonus!\n"
                f"This is around **{format_float(total_ticks * 60 / (14400 * 1.5))}** minutes, or **{format_float(total_ticks / (14400 * 1.5))}** hours of **4-tick** power training with a **1.5x** bonus!\n"
                f"Which will cost you around **{format_number(mana_1_5 // 100)}{EMOJIS['mana_potion']}**, **{format_number(mana_1_5 // 250)}{EMOJIS['greater_mana_potion']}**, **{format_number(mana_1_5 // 500)}{EMOJIS['super_mana_potion']}**, or **{format_number(mana_1_5 // 750)}{EMOJIS['ultimate_mana_potion']}**\n\n"
                
                # With 2x bonus
                f"This is around **{format_float(total_ticks * 60 / (3600 * 2))}** minutes, or **{format_float(total_ticks / (3600 * 2))}** hours of afk training with a **2x** bonus!\n"
                f"This is around **{format_float(total_ticks * 60 / (14400 * 2))}** minutes, or **{format_float(total_ticks / (14400 * 2))}** hours of **4-tick** power training with a **2x** bonus!\n"
                f"Which will cost you around **{format_number(mana_2 // 100)}{EMOJIS['mana_potion']}**, **{format_number(mana_2 // 250)}{EMOJIS['greater_mana_potion']}**, **{format_number(mana_2 // 500)}{EMOJIS['super_mana_potion']}**, or **{format_number(mana_2 // 750)}{EMOJIS['ultimate_mana_potion']}**\n\n"
                
                # With 2.5x bonus
                f"This is around **{format_float(total_ticks * 60 / (3600 * 2.5))}** minutes, or **{format_float(total_ticks / (3600 * 2.5))}** hours of afk training with a **2.5x** bonus!\n"
                f"This is around **{format_float(total_ticks * 60 / (14400 * 2.5))}** minutes, or **{format_float(total_ticks / (14400 * 2.5))}** hours of **4-tick** power training with a **2.5x** bonus!\n"
                f"Which will cost you around **{format_number(mana_2_5 // 100)}{EMOJIS['mana_potion']}**, **{format_number(mana_2_5 // 250)}{EMOJIS['greater_mana_potion']}**, **{format_number(mana_2_5 // 500)}{EMOJIS['super_mana_potion']}**, or **{format_number(mana_2_5 // 750)}{EMOJIS['ultimate_mana_potion']}**\n"
            )
        
        await interaction.response.send_message(embed=embed)