import discord
from discord import app_commands
from discord.ext import commands

from config import EMBED_COLOR, EMOJIS


async def setup_help_command(bot: commands.Bot):
    """Configure the /help command"""
    
    @bot.tree.command(name="help", description="Returns a list of commands")
    async def help_command(interaction: discord.Interaction):
        """
        Displays an embed with all available bot commands
        
        Args:
            interaction: The Discord interaction
        """
        embed = discord.Embed(
            title=f"Commands {EMOJIS['slime_lord']}{EMOJIS['slime']}",
            color=EMBED_COLOR
        )
        
        # Full help message with all commands
        message = (
            # Training commands
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

            # Statistics commands
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

            # Economy commands
            "**/skull [base]**\n"
            "Calculates the amount of gold needed to skull for a certain base level.\n\n"

            "**/potioncost [numpotions]**\n"
            "Calculates the amount of gold needed for a certain number potions.\n\n"

            # Player commands
            "**/leaderboard [choice] [born] [list]**\n"
            "Shows the leaderboard for a specific class (Experience, Melee, Distance, Magic, Defense).\n"
            "Born format: MM/YYYY (default: 01/2016). List: number of players (default: 20, max: 100).\n\n"

            "**/characters [player]**\n"
            "Search for a player and show their stats, guild, title, and online status.\n\n"

            "**/guild-infos [guild]**\n"
            "Shows information about a guild including description, members, and founded date.\n\n"

            "**/player-stats [player]**\n"
            "Shows the stats of a specific player.\n\n"

            "**/player-logs [player]**\n"
            "Shows the pvp logs of a specific player.\n\n"

            # Information commands
            "**/help**\n"
            "Displays the command list, but it looks like you already know how to use this!\n\n"

            "**/invite**\n" 
            "Get the bot invitation link.\n\n"
            
            "**/info**\n"
            "Shows more information about the bot.\n\n"

            "\n*If you have suggestions or bugs to report, message me!*: ***doub.cpp***\n"
        )
        
        embed.description = message
        await interaction.response.send_message(embed=embed)