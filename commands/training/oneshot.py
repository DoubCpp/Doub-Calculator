import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

from config import EMBED_COLOR, EMOJIS
from data import MOBS
from utils import Formulas, format_number


async def setup_oneshot_command(bot: commands.Bot):
    """Configure the /oneshot command"""
    
    @bot.tree.command(name="oneshot", description="Calculates the stat needed to one-shot a certain mob")
    @app_commands.describe(
        attacktype="Type of attack",
        mob="Mob ID (0-40)",
        base="Base level (10-1000)",
        weaponatk="Weapon attack power",
        stat="Stat level (50-1000)",
        buff="Buff value (-80 to 100)",
        consistency="Consistency percentage (1-100)"
    )
    @app_commands.choices(attacktype=[
        app_commands.Choice(name="Auto", value=0),
        app_commands.Choice(name="Special (Melee)", value=1),
        app_commands.Choice(name="Special (Distance)", value=2),
        app_commands.Choice(name="Special (Magic)", value=3)
    ])
    async def oneshot_command(
        interaction: discord.Interaction,
        attacktype: int,
        mob: app_commands.Range[int, 0, 40],
        base: app_commands.Range[int, 10, 1000],
        weaponatk: int,
        stat: app_commands.Range[int, 50, 1000],
        buff: app_commands.Range[int, -80, 100] = 0,
        consistency: Optional[int] = 80
    ):
        """
        Calculate whether you can one-shot a mob or the stat level needed
        
        Args:
            interaction: The Discord interaction
            attacktype: Type of attack
            mob: Target mob ID
            base: Player base level
            weaponatk: Weapon attack power
            stat: Player stat level
            buff: Applied buffs
            consistency: Desired consistency percentage
        """
    # Define attack types and their display (as in the original)
        attack_strings = [
            ["(Auto)", "**Auto Attack**"],
            ["(Special :crossed_swords:)", "**Melee Special :crossed_swords:**"],
            ["(Special :bow_and_arrow:)", "**Distance Special :bow_and_arrow:**"],
            ["(Special :fire:)", "**Magic Special :fire:**"]
        ]
        attack_string = attack_strings[attacktype]
        
        embed = discord.Embed(
            title=f"{attack_string[1]} One-shot Calculation",
            color=EMBED_COLOR
        )
        
        target_mob = MOBS[mob]
        
    # Header with parameters
        if stat is not None and stat >= 5:
            header = f"Base: **{base}** {EMOJIS['slime_lord']} Stat: **{stat}** {EMOJIS['slime_lord']} Buffs: **+{buff}** {EMOJIS['slime_lord']} Weapon: **{weaponatk} Atk** {EMOJIS['slime_lord']} Consistency: **{consistency}%**\n"
        else:
            header = f"Base: **{base}** {EMOJIS['slime_lord']} Weapon: **{weaponatk} Atk** {EMOJIS['slime_lord']} Consistency: **{consistency}%**\n"
        
        mob_info = f"Mob: **{target_mob.name}{target_mob.emoji}** Health: **{target_mob.health}**\n"
        
        str0 = ""
        str1 = ""
        str2 = ""
        str3 = ""
        current_consistency = 0
        
    # Calculate with current stats
        if stat is not None and stat >= 5:
            stat_total = stat + buff
            
            # Calculate raw damage based on attack type
            if attacktype == 0:  # Auto
                min_raw_damage = Formulas.auto_min_raw_damage_calc(stat_total, weaponatk, base)
                max_raw_damage = Formulas.auto_max_raw_damage_calc(stat_total, weaponatk, base)
            elif attacktype == 3:  # Magic
                min_raw_damage = Formulas.special_magic_min_raw_damage_calc(stat_total, weaponatk, base)
                max_raw_damage = Formulas.special_magic_max_raw_damage_calc(stat_total, weaponatk, base)
            else:  # Melee/Distance
                min_raw_damage = Formulas.special_meldist_min_raw_damage_calc(stat_total, weaponatk, base)
                max_raw_damage = Formulas.special_meldist_max_raw_damage_calc(stat_total, weaponatk, base)
            
            max_raw_crit_damage = Formulas.max_raw_crit_damage_calc(max_raw_damage)
            
            # Calculate the current consistency
            current_consistency = Formulas.consistency_calc(max_raw_crit_damage, max_raw_damage, min_raw_damage, target_mob.health, target_mob.defense)
            
            if current_consistency > 0:
                str0 = f"You **can** already one-shot a **{target_mob.name}{target_mob.emoji}** with {attack_string[0]} at **{int(current_consistency * 100)}%** consistency!\n"
            else:
                str0 = f"You **cannot** one-shot a **{target_mob.name}{target_mob.emoji}** with {attack_string[0]} yet!\n"
            
            min_damage = Formulas.min_damage_calc(min_raw_damage, target_mob.defense)
            max_damage = Formulas.max_damage_calc(max_raw_damage, target_mob.defense)
            max_crit_damage = Formulas.max_crit_damage_calc(max_raw_crit_damage, target_mob.defense)
            
            normal_accuracy = Formulas.normal_accuracy_calc(max_raw_damage, min_raw_damage, target_mob.defense)
            crit_accuracy = Formulas.crit_accuracy_calc(max_raw_crit_damage, max_raw_damage, target_mob.defense)
            
            if normal_accuracy == 1.00:
                str1 = f"Min. Damage {attack_string[0]}: **{int(min_damage)}** {EMOJIS['slime_lord']} Max. Damage {attack_string[0]}: **{int(max_damage)}**\n"
            elif normal_accuracy > 0:
                str1 = f"Max. Damage {attack_string[0]}: **{int(max_damage)}**\n"
            else:
                str1 = "You aren't strong enough to deal normal damage to this mob!\n"
                
            if crit_accuracy > 0:
                str2 = f"Maximum Critical Damage {attack_string[0]}: **{int(max_crit_damage)}**\n"
            else:
                str2 = "You aren't strong enough to deal critical damage to this mob!\n"
        
    # Calculate the stat level needed for the desired consistency
        if current_consistency * 100 < consistency:
            stat_needed = 5
            stat_found = False
            
            while not stat_found and stat_needed < 1000:
                if attacktype == 0:  # Auto
                    new_min_raw_damage = Formulas.auto_min_raw_damage_calc(stat_needed, weaponatk, base)
                    new_max_raw_damage = Formulas.auto_max_raw_damage_calc(stat_needed, weaponatk, base)
                elif attacktype == 3:  # Magic
                    new_min_raw_damage = Formulas.special_magic_min_raw_damage_calc(stat_needed, weaponatk, base)
                    new_max_raw_damage = Formulas.special_magic_max_raw_damage_calc(stat_needed, weaponatk, base)
                else:  # Melee/Distance
                    new_min_raw_damage = Formulas.special_meldist_min_raw_damage_calc(stat_needed, weaponatk, base)
                    new_max_raw_damage = Formulas.special_meldist_max_raw_damage_calc(stat_needed, weaponatk, base)
                
                new_max_raw_crit_damage = Formulas.max_raw_crit_damage_calc(new_max_raw_damage)
                
                if Formulas.consistency_calc(new_max_raw_crit_damage, new_max_raw_damage, new_min_raw_damage, target_mob.health, target_mob.defense) * 100 >= consistency:
                    stat_found = True
                else:
                    stat_needed += 1
            
            if not stat_found:
                str3 = f"We could not find the necessary stat level for you to one-shot a **{target_mob.name}{target_mob.emoji}** because it is too high!\n"
            else:
                str3 = f"You need stat **level {stat_needed}** to one-shot a **{target_mob.name}{target_mob.emoji}** with **{consistency}%** consistency\n"
        
        embed.description = header + mob_info + str0 + str1 + str2 + str3
        await interaction.response.send_message(embed=embed)