import discord
from discord import app_commands
from discord.ext import commands

from config import EMBED_COLOR, EMOJIS
from data import MOBS, WEAPONS
from utils import Formulas, format_time


async def setup_weapon_command(bot: commands.Bot):
    """Configure the /weapon command"""
    
    @bot.tree.command(name="weapon", description="Calculates the weapon needed to train on a certain mob")
    @app_commands.describe(
        attacktype="Type of training",
        mob="Mob ID (0-40)",
        base="Base level (10-1000)",
        stat="Stat level (50-1000)",
        buff="Buff value (-80 to 100)"
    )
    @app_commands.choices(attacktype=[
        app_commands.Choice(name="Afk Train (Auto)", value=0),
        app_commands.Choice(name="Power Train (Melee)", value=1),
        app_commands.Choice(name="Power Train (Distance)", value=2),
        app_commands.Choice(name="Power Train (Magic)", value=3)
    ])
    async def weapon_command(
        interaction: discord.Interaction,
        attacktype: int,
        mob: app_commands.Range[int, 0, 40],
        base: app_commands.Range[int, 10, 1000],
        stat: app_commands.Range[int, 50, 1000],
        buff: app_commands.Range[int, -80, 100] = 0
    ):
        """
        Calculate the minimum weapon needed to train effectively on a mob
        
        Args:
            interaction: The Discord interaction
            attacktype: Training type (0=Auto/AFK, 1-3=Power training)
            mob: Target mob ID
            base: Player base level
            stat: Player stat level
            buff: Applied buffs
        """
        # Set parameters based on attack type
        tick = 1 if attacktype == 0 else 4
        
        if attacktype == 0:  # Auto
            threshold = 0.1749
            attack_strings = ["(Auto)", "train"]
        else:  # Special attacks
            threshold = Formulas.threshold_calc(tick)
            class_names = ["power train **Melee :crossed_swords:**", "power train **Distance :bow_and_arrow:**", "power train **Magic :fire:**"]
            attack_strings = ["(Spec)", class_names[attacktype - 1]]
        
        embed = discord.Embed(
            title="Weapon Calculation",
            color=EMBED_COLOR
        )
        
        target_mob = MOBS[mob]
        header = f"Mob: **{target_mob.name}{target_mob.emoji}** {EMOJIS['slime_lord']} Base: **{base}** {EMOJIS['slime_lord']} Stat: **{stat}** {EMOJIS['slime_lord']} Buffs: **+{buff}**\n"
        
        # Find the minimum weapon needed
        pos = 0
        stat_total = stat + buff
        
        for i, weapon in enumerate(WEAPONS):
            effective_stat = stat_total + weapon.buffs
            
            if attacktype == 0:  # Auto
                min_raw_damage = Formulas.auto_min_raw_damage_calc(effective_stat, weapon.attack, base)
                max_raw_damage = Formulas.auto_max_raw_damage_calc(effective_stat, weapon.attack, base)
            elif attacktype == 3:  # Magic
                min_raw_damage = Formulas.special_magic_min_raw_damage_calc(effective_stat, weapon.attack, base)
                max_raw_damage = Formulas.special_magic_max_raw_damage_calc(effective_stat, weapon.attack, base)
            else:  # Melee/Distance
                min_raw_damage = Formulas.special_meldist_min_raw_damage_calc(effective_stat, weapon.attack, base)
                max_raw_damage = Formulas.special_meldist_max_raw_damage_calc(effective_stat, weapon.attack, base)
            
            max_raw_crit_damage = Formulas.max_raw_crit_damage_calc(max_raw_damage)
            accuracy = Formulas.accuracy_calc(max_raw_crit_damage, max_raw_damage, min_raw_damage, target_mob.defense)
            
            if accuracy >= threshold:
                pos = i
                break
        
        weapon = WEAPONS[pos]
        effective_stat = stat_total + weapon.buffs
        
        # Recalculate with the selected weapon
        if attacktype == 0:  # Auto
            min_raw_damage = Formulas.auto_min_raw_damage_calc(effective_stat, weapon.attack, base)
            max_raw_damage = Formulas.auto_max_raw_damage_calc(effective_stat, weapon.attack, base)
        elif attacktype == 3:  # Magic
            min_raw_damage = Formulas.special_magic_min_raw_damage_calc(effective_stat, weapon.attack, base)
            max_raw_damage = Formulas.special_magic_max_raw_damage_calc(effective_stat, weapon.attack, base)
        else:  # Melee/Distance
            min_raw_damage = Formulas.special_meldist_min_raw_damage_calc(effective_stat, weapon.attack, base)
            max_raw_damage = Formulas.special_meldist_max_raw_damage_calc(effective_stat, weapon.attack, base)
        
        max_raw_crit_damage = Formulas.max_raw_crit_damage_calc(max_raw_damage)
        min_damage = Formulas.min_damage_calc(min_raw_damage, target_mob.defense)
        max_damage = Formulas.max_damage_calc(max_raw_damage, target_mob.defense)
        max_crit_damage = Formulas.max_crit_damage_calc(max_raw_crit_damage, target_mob.defense)
        accuracy = Formulas.accuracy_calc(max_raw_crit_damage, max_raw_damage, min_raw_damage, target_mob.defense)
        avgdmg = Formulas.average_damage_calc(accuracy, max_damage, min_damage, max_crit_damage)
        max_tickrate = Formulas.max_tickrate_calc(tick)
        
        if attacktype == 0:
            all_tickrate = Formulas.tickrate_calc(accuracy, 3600)
        else:
            total_accuracy = Formulas.total_accuracy_calc(accuracy, tick)
            all_tickrate = Formulas.powertickrate_calc(total_accuracy, max_tickrate)
        
        time = Formulas.time_to_kill_calc(avgdmg, target_mob.health)
        
        str0 = f"You can {attack_strings[1]} effectively on **{target_mob.name}{target_mob.emoji}** with a **{weapon.name}{weapon.get_emoji()}**!\n"
        str2 = f"Average time to kill **{target_mob.name}{target_mob.emoji}**: **{format_time(time)}**\n"
        
        # Calculate stats needed for next weapon
        check_next_weapon = 0 < pos < len(WEAPONS) - 1
        stat_add = 0
        new_accuracy = 0
        str1 = ""
        str3 = ""
        
        if check_next_weapon:
            next_weapon = WEAPONS[pos - 1]  # Better weapon (lower index = better)
            
            # Add safety limit to prevent infinite loops
            max_iterations = 1000
            iterations = 0
            
            while new_accuracy < threshold and iterations < max_iterations:
                stat_needed = effective_stat + stat_add
                
                new_min_raw_damage = Formulas.auto_min_raw_damage_calc(stat_needed, next_weapon.attack, base)
                new_max_raw_damage = Formulas.auto_max_raw_damage_calc(stat_needed, next_weapon.attack, base)
                new_max_raw_crit_damage = Formulas.max_raw_crit_damage_calc(new_max_raw_damage)
                new_accuracy = Formulas.accuracy_calc(new_max_raw_crit_damage, new_max_raw_damage, new_min_raw_damage, target_mob.defense)
                stat_add += 1
                iterations += 1
                
            str1 = f"Max. Damage {attack_strings[0]}: **{int(max_damage)}** {EMOJIS['slime_lord']} Tickrate: **{int(all_tickrate)} / {int(max_tickrate)}**\n"
            
            if iterations < max_iterations:
                str3 = f"You need **{stat_add}** stats to {attack_strings[1]} effectively on **{target_mob.name}{target_mob.emoji}** with a **{next_weapon.name}{next_weapon.get_emoji()}**!\n"
            else:
                str3 = f"The stat requirement for **{next_weapon.name}{next_weapon.get_emoji()}** is too high to calculate!\n"
        else:
            str1 = f"Min. Damage {attack_strings[0]}: **{int(min_damage)}** {EMOJIS['slime_lord']} Max. Damage {attack_strings[0]}: **{int(max_damage)}**\n"
        
        embed.description = header + str0 + str1 + str2 + str3
        await interaction.response.send_message(embed=embed)