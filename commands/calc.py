import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

from config import EMBED_COLOR, EMOJIS
from utils import Formulas, format_number, format_float, format_time
from data import MOBS, WEAPONS, get_mob, get_weapon, is_power_trainable


async def setup_slash_commands(bot: commands.Bot):

    @bot.tree.command(name="help", description="Returns a list of commands")
    async def help_command(interaction: discord.Interaction):
            
        embed = discord.Embed(
            title=f"Commands {EMOJIS['slime_lord']}{EMOJIS['slime']}",
            color=EMBED_COLOR
        )
        
        message = (
            "**/train [base] [stat] [buffs] [weapon atk]**\n"
            "Calculates the mob that you can train effectively on.\n"
            "Buff default is 0. Weapon atk default is 5.\n\n"

            "**/ptrain [class] [base] [stat] [buffs] [weapon atk] [ticks]**\n"
            "Calculates the mob that you can power-train effectively on.\n"
            "Buff default is 0. Weapon atk default is 5. Ticks default is 4.\n\n"

            "**/moblist**\n"
            "Shows the list of mob IDs.\n\n"

            "**/oneshot [attacktype] [mobID] [base] [weaponatk] [stat] [buffs] [consistency]**\n"
            "Calculates whether you already one-shot a mob, or the stat level needed to one-shot a certain mob.\n"
            "Buff default is 0. Consistency default is 80%.\n"
            "Do /moblist for the list of mob IDs.\n\n"

            "**/weapon [attacktype] [mobID] [base] [stat] [buffs]**\n"
            "Calculates the weapon needed to train on a certain mob.\n"
            "Buff default is 0.\n"
            "Do /moblist for the list of mob IDs.\n\n"

            "**/dmg [attacktype] [mobID] [base] [stat] [buffs] [weapon atk]**\n"
            "Calculates the damage you do to certain mobs.\n"
            "Do /moblist for the list of mob IDs.\n\n"

            "**/stat [stat1] [stat2] [statrate]**\n"
            "Calculates the time, amount of experience, and potions needed to reach a certain stat level.\n"
            "Statrate default is 3600.\n\n"

            "**/offline [stat1] [stat2] [hours]**\n"
            "Calculates the offline training time needed for stat2, or stat gain from hours of offline training.\n\n"

            "**/exp [base]**\n"
            "Calculates the experience at a certain base level.\n\n"

            "**/grind [base1] [base2] [grindrate]**\n"
            "Calculates the time and amount of experience needed to reach a certain base level.\n"
            "Grindrate default is 2000000.\n\n"

            "**/skull [base]**\n"
            "Calculates the amount of gold needed to skull for a certain base level.\n\n"

            "**/potioncost [numpotions]**\n"
            "Calculates the amount of gold needed for a certain number potions.\n\n"

            "**/help**\n"
            "Displays the command list, but it looks like you already know how to use this!\n\n"

            "**/changelog**\n"
            "Shows the changelog.\n\n"

            "**/info**\n"
            "Shows more information about the bot.\n\n"

            "\n*If you have suggestions or bugs to report, message me!*: ***doub.cpp***\n"
        )
        
        embed.description = message
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="info", description="Shows more information about the bot")
    async def info_command(interaction: discord.Interaction):
            
        embed = discord.Embed(
            title=f"Info and Credits {EMOJIS['slime_lord']}{EMOJIS['slime']}",
            color=EMBED_COLOR
        )
        
        message = (
            "**Doub' Rucoy Calculator v1.0** - Upload on **29/06/2025**\n"
            "Made by **Doub** (doub.cpp)\n\n"
            
            "I'm a Rucoy Calculator with a variety of features/commands such as:\n"
            f"{EMOJIS['slime']} /train and /ptrain commands, which tells you the best mob for effective training!\n"
            f"{EMOJIS['slime']} /dmg command, which tells you the damage you do to a certain mob!\n"
            f"{EMOJIS['slime']} /weapon command, which tells you the best weapon to train with!\n"
            f"{EMOJIS['slime']} /oneshot command, which tells you the stat level needed to one-shot a certain mob!\n"
            f"{EMOJIS['slime']} /offline command, which tells you the amount of offline training you need to reach the next level\n"
            f"{EMOJIS['slime']} + much more!\n"
            
            "*If you have any suggestions, tips, or if there are any bugs, please let me know on discord: **doub.cpp***\n"
        )
        
        embed.description = message
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="changelog", description="Shows the changelog")
    async def changelog_command(interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Changelog {EMOJIS['slime_lord']}{EMOJIS['slime']}",
            color=EMBED_COLOR
        )
        
        message = (
            f"{EMOJIS['slime']} **28/06/2025 v1.0** - Start of the bot. \n"
        )
        
        embed.description = message
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="exp", description="Calculates the experience at the current base level")
    async def exp_command(interaction: discord.Interaction, level: int):
            
        embed = discord.Embed(
            title="Experience Calculation",
            color=EMBED_COLOR
        )
        
        current_exp = Formulas.exp_calc(level)
        next_exp = Formulas.exp_calc(level + 1)
        exp_needed = next_exp - current_exp
        
        embed.description = (
            f"Level **{format_number(level)}** is at **{format_number(int(current_exp))}** exp!\n"
            f"You need **{format_number(int(exp_needed))}** experience to reach Level **{format_number(level + 1)}**!"
        )
        
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="skull", description="Calculates the amount of gold needed for skulling")
    async def skull_command(interaction: discord.Interaction, base: int):
            
        embed = discord.Embed(
            title="Skulling Gold Calculation",
            color=EMBED_COLOR
        )
        
        embed.description = (
            f"Base Level: **{format_number(base)}**\n"
            f"Gold Needed for **Yellow Skull**{EMOJIS['skull_yellow']}: **{format_number(150 * base)}** {EMOJIS['gold']}\n"
            f"Gold Needed for **Orange Skull**{EMOJIS['skull_orange']}: **{format_number(150 * 4 * base)}** {EMOJIS['gold']}\n"
            f"Gold Needed for **Red Skull**{EMOJIS['skull_red']}: **{format_number(150 * 13 * base)}** {EMOJIS['gold']}\n"
            f"Gold Needed for **Black Skull**{EMOJIS['skull_black']}: **{format_number(150 * 40 * base)}** {EMOJIS['gold']}"
        )
        
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="potioncost", description="Calculates the amount of gold needed for potions")
    async def potioncost_command(interaction: discord.Interaction, numpotions: int):
            
        embed = discord.Embed(
            title="Potion Gold Calculation",
            color=EMBED_COLOR
        )
        
        embed.description = (
            f"Potion Number: **{format_number(numpotions)}**\n"
            f"Gold Needed for **Potion**{EMOJIS['mana_potion']}{EMOJIS['health_potion']}: **{format_number(numpotions * 50)}** {EMOJIS['gold']}\n"
            f"Gold Needed for **Greater Potion**{EMOJIS['greater_mana_potion']}{EMOJIS['greater_health_potion']}: **{format_number(numpotions * 150)}** {EMOJIS['gold']}\n"
            f"Gold Needed for **Super Potion**{EMOJIS['super_mana_potion']}{EMOJIS['super_health_potion']}: **{format_number(numpotions * 350)}** {EMOJIS['gold']}\n"
            f"Gold Needed for **Ultimate Potion**{EMOJIS['ultimate_mana_potion']}{EMOJIS['ultimate_health_potion']}: **{format_number(numpotions * 650)}** {EMOJIS['gold']}"
        )
        
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="moblist", description="Returns a list of mob IDs")
    async def moblist_command(interaction: discord.Interaction):
            
        embed = discord.Embed(
            title="Moblist",
            color=EMBED_COLOR
        )
        
        mob_list = []
        for i, mob in enumerate(MOBS):
            mob_list.append(f"Mob ID: **{i}** - **{mob.name} {mob.emoji}**")
        
        embed.description = "\n".join(mob_list)
        await interaction.response.send_message(embed=embed)

    # Continue with more commands in the next part...

    @bot.tree.command(name="grind", description="Calculates the experience needed to reach a certain base level")
    async def grind_command(interaction: discord.Interaction, base1: int, base2: int, grindrate: Optional[int] = 2000000):
            
        if base1 >= base2:
            embed = discord.Embed(
                title="❌ Invalid Input",
                description="Goal level must be greater than current level",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
            
        embed = discord.Embed(
            title="Grinding Calculation",
            color=EMBED_COLOR
        )
        
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

    @bot.tree.command(name="train", description="Calculates the mob that you can train effectively on")
    async def train_command(interaction: discord.Interaction, base: int, stat: int, buff: Optional[int] = 0, weaponatk: Optional[int] = 5):
            
        embed = discord.Embed(
            title="Training Calculation",
            color=EMBED_COLOR
        )
        
        header = f"Base: **{base}** {EMOJIS['slime_lord']} Stat: **{stat}** {EMOJIS['slime_lord']} Buffs: **+{buff}** {EMOJIS['slime_lord']} Weapon: **{weaponatk} Atk**\n"
        
        stat_total = stat + buff
        min_raw_damage = Formulas.auto_min_raw_damage_calc(stat_total, weaponatk, base)
        max_raw_damage = Formulas.auto_max_raw_damage_calc(stat_total, weaponatk, base)
        max_raw_crit_damage = Formulas.max_raw_crit_damage_calc(max_raw_damage)
        
        # Find the best mob to train on
        pos = 0
        for i in range(len(MOBS) - 1, -1, -1):
            if i == 26 or i == 31:  # Skip certain mobs
                continue
            accuracy = Formulas.accuracy_calc(max_raw_crit_damage, max_raw_damage, min_raw_damage, MOBS[i].defense)
            if accuracy >= 0.1749:
                pos = i
                break
        
        mob = MOBS[pos]
        min_damage = Formulas.min_damage_calc(min_raw_damage, mob.defense)
        max_damage = Formulas.max_damage_calc(max_raw_damage, mob.defense)
        max_crit_damage = Formulas.max_crit_damage_calc(max_raw_crit_damage, mob.defense)
        accuracy = Formulas.accuracy_calc(max_raw_crit_damage, max_raw_damage, min_raw_damage, mob.defense)
        avgdmg = Formulas.average_damage_calc(accuracy, max_damage, min_damage, max_crit_damage)
        tickrate = Formulas.tickrate_calc(accuracy, 3600)
        
        time = Formulas.time_to_kill_calc(avgdmg, mob.health)
        
        # Check for dual mob training scenarios
        one_mob = True
        check_next_mob = True
        new_pos = pos + 1
        
        if pos in [5, 20, 22, 28, 30]:
            pos -= 1
            one_mob = False
            
        if new_pos > 40:
            check_next_mob = False
        if new_pos in [26, 31]:
            new_pos += 1
            
        str0 = f"You can train effectively on **{MOBS[pos].name}{MOBS[pos].emoji}**!\n"
        if not one_mob and pos + 1 < len(MOBS):
            time2 = Formulas.time_to_kill_calc(avgdmg, MOBS[pos + 1].health)
            str0 = f"You can train effectively on **{MOBS[pos].name}{MOBS[pos].emoji} & {MOBS[pos + 1].name}{MOBS[pos + 1].emoji}**!\n"
            str3 = f"Average time to kill **{MOBS[pos + 1].name}{MOBS[pos + 1].emoji}**: **{format_time(time2)}**\n"
        else:
            str3 = ""
        
        # Calculate stats needed for next mob
        stat_add = 0
        checked = False
        already_deal_damage = False
        deal_damage = False
        new_accuracy = 0
        str4 = ""
        str5 = ""
        
        if check_next_mob and new_pos < len(MOBS):
            # Add safety limit to prevent infinite loops
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
        
        embed.description = header + str0 + str1 + str2 + str3 + str4 + str5
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="ptrain", description="Calculates the mob that you can power train effectively on")
    @discord.app_commands.describe(class_type="Choose your class")
    @discord.app_commands.choices(class_type=[
        discord.app_commands.Choice(name="Melee", value=0),
        discord.app_commands.Choice(name="Dist", value=1),
        discord.app_commands.Choice(name="Mage", value=2)
    ])
    @discord.app_commands.rename(class_type="class")
    async def ptrain_command(interaction: discord.Interaction, class_type: int, base: int, stat: int, buff: Optional[int] = 0, weaponatk: Optional[int] = 5, tick: Optional[int] = 4):
            
        embed = discord.Embed(
            title="Power Training Calculation",
            color=EMBED_COLOR
        )
        class_emojis = ["Melee", "Distance", "Magic"]
        class_emoji = class_emojis[class_type]
        
        header = f"Base: **{base}** {EMOJIS['slime_lord']} Stat: **{stat}** {EMOJIS['slime_lord']} Buffs: **+{buff}** {EMOJIS['slime_lord']} Weapon: **{weaponatk} Atk** {EMOJIS['slime_lord']} Tick: **{tick}**\n"
        
        stat_total = stat + buff
        
        if class_type == 2:  # Magic
            min_raw_damage = Formulas.special_magic_min_raw_damage_calc(stat_total, weaponatk, base)
            max_raw_damage = Formulas.special_magic_max_raw_damage_calc(stat_total, weaponatk, base)
        else:  # Melee/Distance
            min_raw_damage = Formulas.special_meldist_min_raw_damage_calc(stat_total, weaponatk, base)
            max_raw_damage = Formulas.special_meldist_max_raw_damage_calc(stat_total, weaponatk, base)
        
        max_raw_crit_damage = Formulas.max_raw_crit_damage_calc(max_raw_damage)
        threshold = Formulas.threshold_calc(tick)
        
        # Find power trainable mob
        pos = 0
        non_power_trainable = [13, 19, 20, 22, 24, 25, 26, 29, 31, 33, 36, 37] + list(range(39, len(MOBS)))
        
        for i in range(len(MOBS) - 1, -1, -1):
            if i in non_power_trainable:
                continue
            accuracy = Formulas.accuracy_calc(max_raw_crit_damage, max_raw_damage, min_raw_damage, MOBS[i].defense)
            if accuracy >= threshold:
                pos = i
                break
        
        mob = MOBS[pos]
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

        new_pos = pos + 1
        while new_pos < len(MOBS) and new_pos in non_power_trainable:
            new_pos += 1
            
        check_next_mob = new_pos < len(MOBS) and pos != 38
        stat_add = 0
        checked = False
        already_deal_damage = False
        deal_damage = False
        new_accuracy = 0
        str3 = ""
        str4 = ""
        
        if check_next_mob:
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
                new_accuracy = Formulas.accuracy_calc(new_max_raw_crit_damage, new_max_raw_damage, new_min_raw_damage, MOBS[new_pos].defense)
                
                if new_max_damage >= 1 and not checked:
                    str4 = f"You can deal **{int(new_max_damage)}** max damage to **{MOBS[new_pos].name}{MOBS[new_pos].emoji}**!"
                    already_deal_damage = True
                elif new_max_damage > 1 and not already_deal_damage and not deal_damage:
                    str4 = f"You can deal **{int(new_max_damage)}** max damage to **{MOBS[new_pos].name}{MOBS[new_pos].emoji}** in **{stat_add}** stats!"
                    deal_damage = True
                
                checked = True
                stat_add += 1
                iterations += 1
                
            str1 = f"Max. Damage: **{int(max_damage)}** {EMOJIS['slime_lord']} Tickrate: **{int(power_tickrate)} / {int(max_tickrate)}**\n"
            str2 = f"Average time to kill **{mob.name}{mob.emoji}**: **{format_time(time)}**\n"
            
            if iterations < max_iterations:
                str3 = f"You need **{stat_add}** stats to power train effectively on **{MOBS[new_pos].name}{MOBS[new_pos].emoji}**!\n"
            else:
                str3 = f"The stat requirement for **{MOBS[new_pos].name}{MOBS[new_pos].emoji}** is too high to calculate!\n"
        else:
            str1 = f"Min. Damage (Auto): **{int(min_damage)}** {EMOJIS['slime_lord']} Max. Damage (Auto): **{int(max_damage)}**\n"
            str2 = f"Average time to kill **{mob.name}{mob.emoji}**: **{format_time(time)}**\n"
        embed.description = header + str0 + str1 + str2 + str3 + str4
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="dmg", description="Calculates the auto-damage you do to a certain group of mobs")
    @discord.app_commands.choices(attacktype=[
        discord.app_commands.Choice(name="Auto", value=0),
        discord.app_commands.Choice(name="Special (Melee)", value=1),
        discord.app_commands.Choice(name="Special (Distance)", value=2),
        discord.app_commands.Choice(name="Special (Magic)", value=3)
    ])
    async def dmg_command(interaction: discord.Interaction, attacktype: int, mob: int, weaponatk: int, base: int, stat: int, buff: Optional[int] = 0):
            
        if mob < 0 or mob >= len(MOBS):
            embed = discord.Embed(
                title="❌ Invalid Mob ID",
                description=f"Please use a mob ID between 0 and {len(MOBS) - 1}. Use /moblist to see all mobs.",                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
            
        attack_type = attacktype
        attack_strings = ["Auto", "Special :crossed_swords:", "Special :bow_and_arrow:", "Special :fire:"]
        attack_string = attack_strings[attack_type]
        
        embed = discord.Embed(
            title=f"{attack_string} Damage Calculation",
            color=EMBED_COLOR
        )
        
        header = f"Base: **{base}** {EMOJIS['slime_lord']} Stat: **{stat}** {EMOJIS['slime_lord']} Buffs: **+{buff}** {EMOJIS['slime_lord']} Weapon: **{weaponatk} Atk**\n"
        
        stat_total = stat + buff
        
        if attack_type == 0:  # Auto
            min_raw_damage = Formulas.auto_min_raw_damage_calc(stat_total, weaponatk, base)
            max_raw_damage = Formulas.auto_max_raw_damage_calc(stat_total, weaponatk, base)
        elif attack_type == 3:  # Magic
            min_raw_damage = Formulas.special_magic_min_raw_damage_calc(stat_total, weaponatk, base)
            max_raw_damage = Formulas.special_magic_max_raw_damage_calc(stat_total, weaponatk, base)
        else:  # Melee/Distance
            min_raw_damage = Formulas.special_meldist_min_raw_damage_calc(stat_total, weaponatk, base)
            max_raw_damage = Formulas.special_meldist_max_raw_damage_calc(stat_total, weaponatk, base)
        
        max_raw_crit_damage = Formulas.max_raw_crit_damage_calc(max_raw_damage)
        target_mob = MOBS[mob]
        min_damage = Formulas.min_damage_calc(min_raw_damage, target_mob.defense)
        max_damage = Formulas.max_damage_calc(max_raw_damage, target_mob.defense)
        max_crit_damage = Formulas.max_crit_damage_calc(max_raw_crit_damage, target_mob.defense)
        normal_accuracy = Formulas.normal_accuracy_calc(max_raw_damage, min_raw_damage, target_mob.defense)
        crit_accuracy = Formulas.crit_accuracy_calc(max_raw_crit_damage, max_raw_damage, target_mob.defense)
        
        str0 = f"Mob: **{target_mob.name}{target_mob.emoji}**\n"
        
        if normal_accuracy == 1.00:
            str1 = f"Min. Damage ({attack_string}): **{int(min_damage)}** {EMOJIS['slime_lord']} Max. Damage ({attack_string}): **{int(max_damage)}**\n"
        elif normal_accuracy > 0:
            str1 = f"Max. Damage ({attack_string}): **{int(max_damage)}**\n"
        else:
            str1 = "You aren't strong enough to deal normal damage to this mob.\n"
            
        if crit_accuracy > 0:
            str2 = f"Maximum Critical Damage ({attack_string}): **{int(max_crit_damage)}**\n"
        else:
            str2 = "You aren't strong enough to deal critical damage to this mob.\n"
            
        embed.description = header + str0 + str1 + str2
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="stat", description="Calculates the amount of ticks and time needed to reach a certain stat level")
    async def stat_command(interaction: discord.Interaction, stat1: int, stat2: int, statrate: Optional[int] = None):
            
        if stat1 >= stat2:
            embed = discord.Embed(
                title="❌ Invalid Input",
                description="stat2 must be greater than stat1",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
            
        embed = discord.Embed(
            title="Stat Calculation",
            color=EMBED_COLOR
        )
        
        # Calculate ticks 
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
            embed.description = (
                f"Initial Stat: **{format_number(stat1)}** {EMOJIS['slime_lord']} Goal Stat: **{format_number(stat2)}**\n"
                f"You need approximately **{format_number(int(total_ticks))}** ticks until you reach stat level **{format_number(stat2)}**!\n"
                f"This is around **{format_float(total_ticks * 60 / statrate)}** minutes, or **{format_float(total_ticks / statrate)}** hours of training at a rate of **{format_number(statrate)}** exp/hr!"
            )
        else:
            mana_1 = int(50 * total_ticks / 4)  
            mana_1_5 = int(50 * total_ticks / 6)  
            mana_2 = int(50 * total_ticks / 8)  
            mana_2_5 = int(50 * total_ticks / 10)  
            
            embed.description = (
                f"Initial Stat: **{format_number(stat1)}** {EMOJIS['slime_lord']} Goal Stat: **{format_number(stat2)}**\n"
                f"You need approximately **{format_number(int(total_ticks))}** ticks until you reach stat level **{format_number(stat2)}**!\n\n"
                
                f"This is around **{format_float(total_ticks * 60 / 3600)}** minutes, or **{format_float(total_ticks / 3600)}** hours of afk training without bonuses!\n"
                f"This is around **{format_float(total_ticks * 60 / 14400)}** minutes, or **{format_float(total_ticks / 14400)}** hours of **4-tick** power training without bonuses!\n"
                f"Which will cost you around **{format_number(mana_1 // 100)}{EMOJIS['mana_potion']}**, **{format_number(mana_1 // 250)}{EMOJIS['greater_mana_potion']}**, **{format_number(mana_1 // 500)}{EMOJIS['super_mana_potion']}**, or **{format_number(mana_1 // 750)}{EMOJIS['ultimate_mana_potion']}**\n\n"
                
                f"This is around **{format_float(total_ticks * 60 / (3600 * 1.5))}** minutes, or **{format_float(total_ticks / (3600 * 1.5))}** hours of afk training with a **1.5x** bonus!\n"
                f"This is around **{format_float(total_ticks * 60 / (14400 * 1.5))}** minutes, or **{format_float(total_ticks / (14400 * 1.5))}** hours of **4-tick** power training with a **1.5x** bonus!\n"
                f"Which will cost you around **{format_number(mana_1_5 // 100)}{EMOJIS['mana_potion']}**, **{format_number(mana_1_5 // 250)}{EMOJIS['greater_mana_potion']}**, **{format_number(mana_1_5 // 500)}{EMOJIS['super_mana_potion']}**, or **{format_number(mana_1_5 // 750)}{EMOJIS['ultimate_mana_potion']}**\n\n"
                
                f"This is around **{format_float(total_ticks * 60 / (3600 * 2))}** minutes, or **{format_float(total_ticks / (3600 * 2))}** hours of afk training with a **2x** bonus!\n"
                f"This is around **{format_float(total_ticks * 60 / (14400 * 2))}** minutes, or **{format_float(total_ticks / (14400 * 2))}** hours of **4-tick** power training with a **2x** bonus!\n"
                f"Which will cost you around **{format_number(mana_2 // 100)}{EMOJIS['mana_potion']}**, **{format_number(mana_2 // 250)}{EMOJIS['greater_mana_potion']}**, **{format_number(mana_2 // 500)}{EMOJIS['super_mana_potion']}**, or **{format_number(mana_2 // 750)}{EMOJIS['ultimate_mana_potion']}**\n\n"
                
                f"This is around **{format_float(total_ticks * 60 / (3600 * 2.5))}** minutes, or **{format_float(total_ticks / (3600 * 2.5))}** hours of afk training with a **2.5x** bonus!\n"
                f"This is around **{format_float(total_ticks * 60 / (14400 * 2.5))}** minutes, or **{format_float(total_ticks / (14400 * 2.5))}** hours of **4-tick** power training with a **2.5x** bonus!\n"
                f"Which will cost you around **{format_number(mana_2_5 // 100)}{EMOJIS['mana_potion']}**, **{format_number(mana_2_5 // 250)}{EMOJIS['greater_mana_potion']}**, **{format_number(mana_2_5 // 500)}{EMOJIS['super_mana_potion']}**, or **{format_number(mana_2_5 // 750)}{EMOJIS['ultimate_mana_potion']}**\n"
            )
        
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="offline", description="Calculates the time needed between stat1 and stat2, or the stat gain from specified hours")
    async def offline_command(interaction: discord.Interaction, stat1: int, stat2: Optional[int] = None, hours: Optional[int] = None):
            
        embed = discord.Embed(
            title="Offline Training Calculation",
            color=EMBED_COLOR
        )
        
        if stat2 is not None and stat2 > 0 and (hours is None or hours <= 0):
            if stat1 >= stat2:
                embed = discord.Embed(
                    title="❌ Invalid Input",
                    description="Stat2 must be greater than Stat1",
                    color=0xFF0000
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
                
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
            
        elif hours is not None and hours > 0 and (stat2 is None or stat2 <= 0):
            ticks_trained = 600 * hours
            
            if stat1 <= 54:
                ticks1 = Formulas.stat0to54_calc(stat1)
            else:
                ticks1 = Formulas.stat55to99_calc(stat1)
                
            ticks2 = ticks_trained + ticks1
            new_stat = round(Formulas.find_stat_level_calc(ticks2) * 100) / 100
            
            if new_stat < 5:
                embed = discord.Embed(
                    title="❌ Calculation Error",
                    description="Something went wrong: Could not find new stat",
                    color=0xFF0000
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
                
            embed.description = (
                f"Initial Stat: **{format_number(stat1)}** {EMOJIS['slime_lord']} Hours: **{format_number(hours)}**\n"
                f"Your new stat will be approximately: **{new_stat}** with **{hours}** hours of offline training"
            )
            
        else:
            embed.description = "Something went wrong: Please enter either hours OR stat2"
        
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="weapon", description="Calculates the weapon needed to train on a certain mob")
    @discord.app_commands.choices(attacktype=[
        discord.app_commands.Choice(name="Afk Train (Auto)", value=0),
        discord.app_commands.Choice(name="Power Train (Melee)", value=1),
        discord.app_commands.Choice(name="Power Train (Distance)", value=2),
        discord.app_commands.Choice(name="Power Train (Magic)", value=3)
    ])
    async def weapon_command(interaction: discord.Interaction, attacktype: int, mob: int, base: int, stat: int, buff: Optional[int] = 0):
            
        if mob < 0 or mob >= len(MOBS):
            embed = discord.Embed(
                title="❌ Invalid Mob ID",
                description=f"Please use a mob ID between 0 and {len(MOBS) - 1}. Use /moblist to see all mobs.",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
            
        attack_type = attacktype
        tick = 1 if attack_type == 0 else 4
        
        if attack_type == 0:  # Auto
            threshold = 0.1749
            attack_strings = ["(Auto)", "train"]
        else:  # Special attacks
            threshold = Formulas.threshold_calc(tick)
            class_names = ["power train **Melee :crossed_swords:**", "power train **Distance :bow_and_arrow:**", "power train **Magic :fire:**"]
            attack_strings = ["(Spec)", class_names[attack_type - 1]]
        
        embed = discord.Embed(
            title="Weapon Calculation",
            color=EMBED_COLOR
        )
        
        target_mob = MOBS[mob]
        header = f"Mob: **{target_mob.name}{target_mob.emoji}** {EMOJIS['slime_lord']} Base: **{base}** {EMOJIS['slime_lord']} Stat: **{stat}** {EMOJIS['slime_lord']} Buffs: **+{buff}**\n"

        pos = 0
        stat_total = stat + buff
        
        for i, weapon in enumerate(WEAPONS):
            effective_stat = stat_total + weapon.buffs
            
            if attack_type == 0:  # Auto
                min_raw_damage = Formulas.auto_min_raw_damage_calc(effective_stat, weapon.attack, base)
                max_raw_damage = Formulas.auto_max_raw_damage_calc(effective_stat, weapon.attack, base)
            elif attack_type == 3:  # Magic
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

        if attack_type == 0:  # Auto
            min_raw_damage = Formulas.auto_min_raw_damage_calc(effective_stat, weapon.attack, base)
            max_raw_damage = Formulas.auto_max_raw_damage_calc(effective_stat, weapon.attack, base)
        elif attack_type == 3:  # Magic
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
        
        if attack_type == 0:
            all_tickrate = Formulas.tickrate_calc(accuracy, 3600)
        else:
            total_accuracy = Formulas.total_accuracy_calc(accuracy, tick)
            all_tickrate = Formulas.powertickrate_calc(total_accuracy, max_tickrate)
        
        time = Formulas.time_to_kill_calc(avgdmg, target_mob.health)
        
        str0 = f"You can {attack_strings[1]} effectively on **{target_mob.name}{target_mob.emoji}** with a **{weapon.name}{weapon.get_emoji()}**!\n"
        str2 = f"Average time to kill **{target_mob.name}{target_mob.emoji}**: **{format_time(time)}**\n"

        check_next_weapon = 0 < pos < len(WEAPONS) - 1
        stat_add = 0
        new_accuracy = 0
        str1 = ""
        str3 = ""
        
        if check_next_weapon:
            next_weapon = WEAPONS[pos - 1] 

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

    @bot.tree.command(name="oneshot", description="Calculates the stat needed to one-shot a certain mob")
    @discord.app_commands.choices(attacktype=[
        discord.app_commands.Choice(name="Auto", value=0),
        discord.app_commands.Choice(name="Special (Melee)", value=1),
        discord.app_commands.Choice(name="Special (Distance)", value=2),
        discord.app_commands.Choice(name="Special (Magic)", value=3)
    ])
    async def oneshot_command(interaction: discord.Interaction, attacktype: int, mob: int, base: int, weaponatk: int, stat: Optional[int] = None, buff: Optional[int] = 0, consistency: Optional[int] = 80):
            
        if mob < 0 or mob >= len(MOBS):
            embed = discord.Embed(
                title="❌ Invalid Mob ID",
                description=f"Please use a mob ID between 0 and {len(MOBS) - 1}. Use /moblist to see all mobs.",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
            
        attack_type = attacktype
        attack_strings = [
            ["(Auto)", "**Auto Attack**"],
            ["(Special :crossed_swords:)", "**Melee Special :crossed_swords:**"],
            ["(Special :bow_and_arrow:)", "**Distance Special :bow_and_arrow:**"],
            ["(Special :fire:)", "**Magic Special :fire:**"]
        ]
        attack_string = attack_strings[attack_type]
        
        embed = discord.Embed(
            title=f"{attack_string[1]} One-shot Calculation",
            color=EMBED_COLOR
        )
        
        target_mob = MOBS[mob]
        
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
        
        if stat is not None and stat >= 5:
            stat_total = stat + buff
            
            if attack_type == 0:  # Auto
                min_raw_damage = Formulas.auto_min_raw_damage_calc(stat_total, weaponatk, base)
                max_raw_damage = Formulas.auto_max_raw_damage_calc(stat_total, weaponatk, base)
            elif attack_type == 3:  # Magic
                min_raw_damage = Formulas.special_magic_min_raw_damage_calc(stat_total, weaponatk, base)
                max_raw_damage = Formulas.special_magic_max_raw_damage_calc(stat_total, weaponatk, base)
            else:  # Melee/Distance
                min_raw_damage = Formulas.special_meldist_min_raw_damage_calc(stat_total, weaponatk, base)
                max_raw_damage = Formulas.special_meldist_max_raw_damage_calc(stat_total, weaponatk, base)
            
            max_raw_crit_damage = Formulas.max_raw_crit_damage_calc(max_raw_damage)

            current_consistency = Formulas.consistency_calc(max_raw_crit_damage, max_raw_damage, min_raw_damage, target_mob.health, target_mob.defense)
            
            if current_consistency > 0:
                str0 = f"You **can** already one-shot a **{target_mob.name}{target_mob.emoji}** with {attack_string[1]} at **{int(current_consistency * 100)}%** consistency!\n"
            else:
                str0 = f"You **cannot** one-shot a **{target_mob.name}{target_mob.emoji}** with {attack_string[1]} yet!\n"
            
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

        if current_consistency * 100 < consistency:
            stat_needed = 5
            stat_found = False
            
            while not stat_found and stat_needed < 1000:
                if attack_type == 0:  # Auto
                    new_min_raw_damage = Formulas.auto_min_raw_damage_calc(stat_needed, weaponatk, base)
                    new_max_raw_damage = Formulas.auto_max_raw_damage_calc(stat_needed, weaponatk, base)
                elif attack_type == 3:  # Magic
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
