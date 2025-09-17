import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

from config import EMBED_COLOR, EMOJIS
from data import MOBS
from utils import Formulas, format_number, format_time


async def setup_ptrain_command(bot: commands.Bot):
    """Configure the /ptrain command"""
    
    @bot.tree.command(name="ptrain", description="Calculates the mob that you can power-train effectively on")
    @app_commands.describe(
        class_type="Choose your class",
        base="Base level (10-1000)",
        stat="Stat level (50-1000)", 
        buff="Buff value (-80 to 100)",
        weaponatk="Weapon attack power (default: 5)",
        tick="Number of ticks (default: 4)"
    )
    @app_commands.choices(class_type=[
        app_commands.Choice(name="Melee", value=0),
        app_commands.Choice(name="Dist", value=1),
        app_commands.Choice(name="Mage", value=2)
    ])
    @app_commands.rename(class_type="class")
    async def ptrain_command(
        interaction: discord.Interaction,
        class_type: int,
        base: app_commands.Range[int, 10, 1000],
        stat: app_commands.Range[int, 50, 1000],
        buff: app_commands.Range[int, -80, 100] = 0,
        weaponatk: Optional[int] = 5,
        tick: Optional[int] = 4
    ):
        """
        Calculate the best mob for power training (special attacks)
        
        Args:
            interaction: The Discord interaction
            class_type: Class type (0=Melee, 1=Distance, 2=Magic)
            base: Player base level
            stat: Player stat level
            buff: Applied buffs
            weaponatk: Weapon attack power
            tick: Number of ticks for power training
        """
        embed = discord.Embed(
            title="Power Training Calculation",
            color=EMBED_COLOR
        )
        
        # Class names (preserving legacy labels)
        class_emojis = ["Melee", "Distance", "Magic"]
        class_emoji = class_emojis[class_type]
        
        # Header with parameters
        header = (
            f"Base: **{base}** {EMOJIS['slime_lord']} "
            f"Stat: **{stat}** {EMOJIS['slime_lord']} "
            f"Buffs: **+{buff}** {EMOJIS['slime_lord']} "
            f"Weapon: **{weaponatk} Atk** {EMOJIS['slime_lord']} "
            f"Tick: **{tick}**\n"
        )
        
        # Calculate total stats with buffs
        stat_total = stat + buff
        
        # Calculate raw damage based on class
        if class_type == 2:  # Magic
            min_raw_damage = Formulas.special_magic_min_raw_damage_calc(stat_total, weaponatk, base)
            max_raw_damage = Formulas.special_magic_max_raw_damage_calc(stat_total, weaponatk, base)
        else:  # Melee/Distance
            min_raw_damage = Formulas.special_meldist_min_raw_damage_calc(stat_total, weaponatk, base)
            max_raw_damage = Formulas.special_meldist_max_raw_damage_calc(stat_total, weaponatk, base)
        
        max_raw_crit_damage = Formulas.max_raw_crit_damage_calc(max_raw_damage)
        threshold = Formulas.threshold_calc(tick)
        
        # Find the best mob that can be power-trained (using legacy logic)
        pos = 0
        non_power_trainable = [13, 19, 20, 22, 24, 25, 26, 29, 31, 33, 36, 37] + list(range(39, len(MOBS)))
        
        # Iterate mobs from strongest to weakest
        for i in range(len(MOBS) - 1, -1, -1):
            # Check if the mob is power-trainable
            if i in non_power_trainable:
                continue
            
            accuracy = Formulas.accuracy_calc(
                max_raw_crit_damage, max_raw_damage, min_raw_damage, MOBS[i].defense
            )
            if accuracy >= threshold:
                pos = i
                break
        
        mob = MOBS[pos]
        
        # Calculate combat statistics
        min_damage = Formulas.min_damage_calc(min_raw_damage, mob.defense)
        max_damage = Formulas.max_damage_calc(max_raw_damage, mob.defense)
        max_crit_damage = Formulas.max_crit_damage_calc(max_raw_crit_damage, mob.defense)
        accuracy = Formulas.accuracy_calc(max_raw_crit_damage, max_raw_damage, min_raw_damage, mob.defense)
        avgdmg = Formulas.average_damage_calc(accuracy, max_damage, min_damage, max_crit_damage)
        total_accuracy = Formulas.total_accuracy_calc(accuracy, tick)
        max_tickrate = Formulas.max_tickrate_calc(tick)
        power_tickrate = Formulas.powertickrate_calc(total_accuracy, max_tickrate)
        time = Formulas.time_to_kill_calc(avgdmg, mob.health)
        
        str0 = f"You can power train **{class_emoji}** on **{mob.name}{mob.emoji}**!\n"
        
        # Calculate stats needed for the next power-trainable mob
        new_pos = pos + 1
        
        # Find the next power-trainable mob (using legacy logic)
        while new_pos < len(MOBS) and new_pos in non_power_trainable:
            new_pos += 1
        
        check_next_mob = new_pos < len(MOBS) and pos != 38  # 38 is the last power-trainable mob
        stat_add = 0
        checked = False
        already_deal_damage = False
        deal_damage = False
        new_accuracy = 0
        new_max_damage = 0
        str3 = ""
        str4 = ""
        
        if check_next_mob:
            # Limit iterations to avoid infinite loops
            max_iterations = 1000
            iterations = 0
            
            while new_accuracy < threshold and iterations < max_iterations:
                stat_needed = stat_total + stat_add
                
                if class_type == 2:  # Magic
                    new_min_raw_damage = Formulas.special_magic_min_raw_damage_calc(stat_needed, weaponatk, base)
                    new_max_raw_damage = Formulas.special_magic_max_raw_damage_calc(stat_needed, weaponatk, base)
                else:  # Melee/Distance
                    new_min_raw_damage = Formulas.special_meldist_min_raw_damage_calc(stat_needed, weaponatk, base)
                    new_max_raw_damage = Formulas.special_meldist_max_raw_damage_calc(stat_needed, weaponatk, base)
                
                new_max_raw_crit_damage = Formulas.max_raw_crit_damage_calc(new_max_raw_damage)
                new_max_damage = Formulas.max_damage_calc(new_max_raw_damage, MOBS[new_pos].defense)
                new_accuracy = Formulas.accuracy_calc(
                    new_max_raw_crit_damage, new_max_raw_damage, new_min_raw_damage, MOBS[new_pos].defense
                )
                
                if new_max_damage >= 1 and not checked:
                    str4 = (
                        f"You can deal **{int(new_max_damage)}** max damage to "
                        f"**{MOBS[new_pos].name}{MOBS[new_pos].emoji}**!"
                    )
                    already_deal_damage = True
                elif new_max_damage > 1 and not already_deal_damage and not deal_damage:
                    str4 = (
                        f"You can deal **{int(new_max_damage)}** max damage to "
                        f"**{MOBS[new_pos].name}{MOBS[new_pos].emoji}** in **{stat_add}** stats!"
                    )
                    deal_damage = True
                
                checked = True
                stat_add += 1
                iterations += 1
            
            str1 = (
                f"Max. Damage: **{int(max_damage)}** {EMOJIS['slime_lord']} "
                f"Tickrate: **{int(power_tickrate)} / {int(max_tickrate)}**\n"
            )
            str2 = f"Average time to kill **{mob.name}{mob.emoji}**: **{format_time(time)}**\n"
            
            if iterations < max_iterations:
                str3 = (
                    f"You need **{stat_add}** stats to power train effectively on "
                    f"**{MOBS[new_pos].name}{MOBS[new_pos].emoji}**!\n"
                )
            else:
                str3 = (
                    f"The stat requirement for **{MOBS[new_pos].name}{MOBS[new_pos].emoji}** "
                    f"is too high to calculate!\n"
                )
        else:
            str1 = (
                f"Min. Damage (Auto): **{int(min_damage)}** {EMOJIS['slime_lord']} "
                f"Max. Damage (Auto): **{int(max_damage)}**\n"
            )
            str2 = f"Average time to kill **{mob.name}{mob.emoji}**: **{format_time(time)}**\n"
        
        # Assemble the final description
        embed.description = header + str0 + str1 + str2 + str3 + str4
        
        await interaction.response.send_message(embed=embed)
