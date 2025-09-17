import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

from config import EMBED_COLOR, EMOJIS
from data import MOBS
from utils import Formulas, format_number, format_time


async def setup_train_command(bot: commands.Bot):
    """Configure the /train command"""
    
    @bot.tree.command(name="train", description="Calculates the mob that you can train effectively on")
    @app_commands.describe(
        base="Base level (10-1000)",
        stat="Stat level (50-1000)",
        buff="Buff value (-80 to 100)",
        weaponatk="Weapon attack power (default: 5)"
    )
    async def train_command(
        interaction: discord.Interaction,
        base: app_commands.Range[int, 10, 1000],
        stat: app_commands.Range[int, 50, 1000],
        buff: app_commands.Range[int, -80, 100] = 0,
        weaponatk: Optional[int] = 5
    ):
        """
        Calculate the best mob for normal (AFK) training
        
        Args:
            interaction: The Discord interaction
            base: Player base level
            stat: Player stat level
            buff: Applied buffs
            weaponatk: Weapon attack power
        """
        embed = discord.Embed(
            title="Training Calculation",
            color=EMBED_COLOR
        )
        
        # Header with parameters
        header = f"Base: **{base}** {EMOJIS['slime_lord']} Stat: **{stat}** {EMOJIS['slime_lord']} Buffs: **+{buff}** {EMOJIS['slime_lord']} Weapon: **{weaponatk} Atk**\n"
        
        # Calculate total stats with buffs
        stat_total = stat + buff
        
        # Calculate raw damage
        min_raw_damage = Formulas.auto_min_raw_damage_calc(stat_total, weaponatk, base)
        max_raw_damage = Formulas.auto_max_raw_damage_calc(stat_total, weaponatk, base)
        max_raw_crit_damage = Formulas.max_raw_crit_damage_calc(max_raw_damage)
        
        # Find the best mob to train on
        # We look for the strongest mob where we have at least 17.49% accuracy
        pos = 0
        for i in range(len(MOBS) - 1, -1, -1):
            # Ignore certain special mobs
            if i == 26 or i == 31:  # Dead Eyes and Dragon Hatchling
                continue
            
            accuracy = Formulas.accuracy_calc(max_raw_crit_damage, max_raw_damage, min_raw_damage, MOBS[i].defense)
            if accuracy >= 0.1749:  # 17.49% minimum for effective training
                pos = i
                break
        
        mob = MOBS[pos]
        
        # Calculate combat statistics
        min_damage = Formulas.min_damage_calc(min_raw_damage, mob.defense)
        max_damage = Formulas.max_damage_calc(max_raw_damage, mob.defense)
        max_crit_damage = Formulas.max_crit_damage_calc(max_raw_crit_damage, mob.defense)
        accuracy = Formulas.accuracy_calc(max_raw_crit_damage, max_raw_damage, min_raw_damage, mob.defense)
        avgdmg = Formulas.average_damage_calc(accuracy, max_damage, min_damage, max_crit_damage)
        tickrate = Formulas.tickrate_calc(accuracy, 3600)
        
        time = Formulas.time_to_kill_calc(avgdmg, mob.health)
        
        # Check double-mob training scenarios
        one_mob = True
        check_next_mob = True
        new_pos = pos + 1
        
        # Some mobs come in pairs
        if pos in [5, 20, 22, 28, 30]:  # Cobra/Worm, Drow Ranger/Mage, etc.
            pos -= 1
            one_mob = False
            
        if new_pos > 40:
            check_next_mob = False
        if new_pos in [26, 31]:  # Skip Dead Eyes and Dragon Hatchling
            new_pos += 1
            
        # Build the main message
        str0 = f"You can train effectively on **{MOBS[pos].name}{MOBS[pos].emoji}**!\n"
        if not one_mob and pos + 1 < len(MOBS):
            time2 = Formulas.time_to_kill_calc(avgdmg, MOBS[pos + 1].health)
            str0 = f"You can train effectively on **{MOBS[pos].name}{MOBS[pos].emoji} & {MOBS[pos + 1].name}{MOBS[pos + 1].emoji}**!\n"
            str3 = f"Average time to kill **{MOBS[pos + 1].name}{MOBS[pos + 1].emoji}**: **{format_time(time2)}**\n"
        else:
            str3 = ""
        
        # Calculate stats needed for the next mob
        stat_add = 0
        checked = False
        already_deal_damage = False
        deal_damage = False
        new_accuracy = 0
        str4 = ""
        str5 = ""
        
        if check_next_mob and new_pos < len(MOBS):
            # Limit iterations to avoid infinite loops
            max_iterations = 1000
            iterations = 0
            
            while new_accuracy < 0.1749 and iterations < max_iterations:
                stat_needed = stat_total + stat_add
                new_min_raw_damage = Formulas.auto_min_raw_damage_calc(stat_needed, weaponatk, base)
                new_max_raw_damage = Formulas.auto_max_raw_damage_calc(stat_needed, weaponatk, base)
                new_max_raw_crit_damage = Formulas.max_raw_crit_damage_calc(new_max_raw_damage)
                
                new_max_damage = Formulas.max_damage_calc(new_max_raw_damage, MOBS[new_pos].defense)
                new_accuracy = Formulas.accuracy_calc(new_max_raw_crit_damage, new_max_raw_damage, new_min_raw_damage, MOBS[new_pos].defense)
                
                if new_max_damage >= 1 and not checked:
                    str5 = f"You can deal **{int(new_max_damage)}** max damage to **{MOBS[new_pos].name}{MOBS[new_pos].emoji}**!"
                    already_deal_damage = True
                elif new_max_damage > 1 and not already_deal_damage and not deal_damage:
                    str5 = f"You can deal **{int(new_max_damage)}** max damage to **{MOBS[new_pos].name}{MOBS[new_pos].emoji}** in **{stat_add}** stats!"
                    deal_damage = True
                    checked = True
                stat_add += 1
                iterations += 1
                
            str1 = f"Max. Damage: **{int(max_damage)}** {EMOJIS['slime_lord']} Tickrate: **{int(tickrate)} / 3600**\n"
            str2 = f"Average time to kill **{MOBS[pos].name}{MOBS[pos].emoji}**: **{format_time(time)}**\n"
            
            if iterations < max_iterations:
                str4 = f"You need **{stat_add}** stats to train effectively on **{MOBS[new_pos].name}{MOBS[new_pos].emoji}**!\n"
            else:
                str4 = f"The stat requirement for **{MOBS[new_pos].name}{MOBS[new_pos].emoji}** is too high to calculate!\n"
        else:
            str1 = f"Min. Damage (Auto): **{int(min_damage)}** {EMOJIS['slime_lord']} Max. Damage (Auto): **{int(max_damage)}**\n"
            str2 = f"Average time to kill **{MOBS[pos].name}{MOBS[pos].emoji}**: **{format_time(time)}**\n"
        
        # Assemble the final description
        embed.description = header + str0 + str1 + str2 + str3 + str4 + str5
        
        await interaction.response.send_message(embed=embed)