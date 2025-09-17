import discord
from discord import app_commands
from discord.ext import commands

from config import EMBED_COLOR, EMOJIS
from data import MOBS
from utils import Formulas


async def setup_dmg_command(bot: commands.Bot):
    """Configure the /dmg command"""
    
    @bot.tree.command(name="dmg", description="Calculates the auto-damage you do to a certain group of mobs")
    @app_commands.describe(
        attacktype="Type of attack",
        mob="Mob ID (0-40)",
        weaponatk="Weapon attack power",
        base="Base level (10-1000)",
        stat="Stat level (50-1000)",
        buff="Buff value (-80 to 100)"
    )
    @app_commands.choices(attacktype=[
        app_commands.Choice(name="Auto", value=0),
        app_commands.Choice(name="Special (Melee)", value=1),
        app_commands.Choice(name="Special (Distance)", value=2),
        app_commands.Choice(name="Special (Magic)", value=3)
    ])
    async def dmg_command(
        interaction: discord.Interaction,
        attacktype: int,
        mob: app_commands.Range[int, 0, 40],
        weaponatk: int,
        base: app_commands.Range[int, 10, 1000],
        stat: app_commands.Range[int, 50, 1000],
        buff: app_commands.Range[int, -80, 100] = 0
    ):
        """
        Calculate the damage dealt to a specific mob
        
        Args:
            interaction: The Discord interaction
            attacktype: Type of attack (0=Auto, 1=Special Melee, 2=Special Distance, 3=Special Magic)
            mob: Target mob ID
            weaponatk: Weapon attack power
            base: Player base level
            stat: Player stat level
            buff: Applied buffs
        """
    # Verify that the mob ID is valid
        if mob >= len(MOBS):
            embed = discord.Embed(
                title="Invalid Mob ID",
                description=f"Mob ID must be between 0 and {len(MOBS) - 1}!",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
    # Define attack types (as in the legacy version)
        attack_strings = ["Auto", "Special :crossed_swords:", "Special :bow_and_arrow:", "Special :fire:"]
        attack_string = attack_strings[attacktype]
        
        embed = discord.Embed(
            title=f"{attack_string} Damage Calculation",
            color=EMBED_COLOR
        )
        
    # Header with parameters
        header = f"Base: **{base}** {EMOJIS['slime_lord']} Stat: **{stat}** {EMOJIS['slime_lord']} Buffs: **+{buff}** {EMOJIS['slime_lord']} Weapon: **{weaponatk} Atk**\n"
        
    # Calculate total stats with buffs
        stat_total = stat + buff
        
    # Calculate raw damage based on the attack type
        if attacktype == 0:  # Auto
            min_raw_damage = Formulas.auto_min_raw_damage_calc(stat_total, weaponatk, base)
            max_raw_damage = Formulas.auto_max_raw_damage_calc(stat_total, weaponatk, base)
        elif attacktype == 3:  # Magic
            min_raw_damage = Formulas.special_magic_min_raw_damage_calc(stat_total, weaponatk, base)
            max_raw_damage = Formulas.special_magic_max_raw_damage_calc(stat_total, weaponatk, base)
        else:  # Melee/Distance (1 ou 2)
            min_raw_damage = Formulas.special_meldist_min_raw_damage_calc(stat_total, weaponatk, base)
            max_raw_damage = Formulas.special_meldist_max_raw_damage_calc(stat_total, weaponatk, base)
        
        max_raw_crit_damage = Formulas.max_raw_crit_damage_calc(max_raw_damage)
        
    # Get the target mob
        target_mob = MOBS[mob]
        
    # Calculate effective damage
        min_damage = Formulas.min_damage_calc(min_raw_damage, target_mob.defense)
        max_damage = Formulas.max_damage_calc(max_raw_damage, target_mob.defense)
        max_crit_damage = Formulas.max_crit_damage_calc(max_raw_crit_damage, target_mob.defense)
        
    # Calculate accuracy
        normal_accuracy = Formulas.normal_accuracy_calc(max_raw_damage, min_raw_damage, target_mob.defense)
        crit_accuracy = Formulas.crit_accuracy_calc(max_raw_crit_damage, max_raw_damage, target_mob.defense)
        
    # Build the message
        str0 = f"Mob: **{target_mob.name}{target_mob.emoji}**\n"
        
    # Show normal damage
        if normal_accuracy == 1.00:
            # Always hits
            str1 = f"Min. Damage ({attack_string}): **{int(min_damage)}** {EMOJIS['slime_lord']} Max. Damage ({attack_string}): **{int(max_damage)}**\n"
        elif normal_accuracy > 0:
            # Sometimes hits
            str1 = f"Max. Damage ({attack_string}): **{int(max_damage)}**\n"
        else:
            # Cannot deal normal damage
            str1 = "You aren't strong enough to deal normal damage to this mob.\n"
            
    # Show critical damage
        if crit_accuracy > 0:
            str2 = f"Maximum Critical Damage ({attack_string}): **{int(max_crit_damage)}**\n"
        else:
            str2 = "You aren't strong enough to deal critical damage to this mob.\n"
            
    # Assemble the description (simple original format)
        embed.description = header + str0 + str1 + str2
        
        await interaction.response.send_message(embed=embed)