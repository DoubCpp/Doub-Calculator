import discord
from discord import app_commands
from discord.ext import commands

from config import EMBED_COLOR, EMOJIS
from data import MOBS


async def setup_moblist_command(bot: commands.Bot):
    """Configure the /moblist command"""
    
    @bot.tree.command(name="moblist", description="Returns a list of mob IDs")
    async def moblist_command(interaction: discord.Interaction):
        """
        Show the full list of mobs with their IDs
        
        Args:
            interaction: The Discord interaction
        """
        embed = discord.Embed(
            title="Moblist",
            color=EMBED_COLOR
        )
        
        mob_list = []
        for i, mob in enumerate(MOBS):
            mob_list.append(f"Mob ID: **{i}** - **{mob.name} {mob.emoji}**")
        
        embed.description = "\n".join(mob_list)
        await interaction.response.send_message(embed=embed)