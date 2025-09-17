import discord
from discord import app_commands
from discord.ext import commands
import aiohttp

from config import EMBED_COLOR, EMOJIS
from utils import format_number
from .api import RucoyAPI


async def setup_characters_command(bot: commands.Bot):
    """Configure the /characters command"""
    
    @bot.tree.command(name="characters", description="Search for a player and show their stats")
    @app_commands.describe(player="The player name to search for")
    async def characters_command(interaction: discord.Interaction, player: str):
        """
        Search for a player and display their statistics
        
        Args:
            interaction: The Discord interaction
            player: The player name to search for
        """
        embed = discord.Embed(
            title="Character Information",
            color=EMBED_COLOR
        )
        
        try:
            async with aiohttp.ClientSession() as session:
                # Encode the player name for the URL
                encoded_name = player.replace(" ", "+")
                url = f"{RucoyAPI.BASE_URL}/characters?utf8=%E2%9C%93&name={encoded_name}"
                html_content = await RucoyAPI.fetch_page(session, url)
                
                if html_content:
                    character_data = RucoyAPI.parse_character_data(html_content)
                    
                    if character_data and character_data.get('name'):
                        # Online status emoji
                        status_emoji = EMOJIS['online'] if character_data.get('online', False) else "🔴"
                        supporter_text = f" {EMOJIS['slime']}" if character_data.get('supporter', False) else ""
                        
                        # Use offline time information
                        offline_info = character_data.get('offline_time', character_data.get('last_online', 'Unknown'))
                        
                        # Build the description
                        embed.description = (
                            f"**Player:** {character_data.get('name', 'Unknown')}{supporter_text}\n"
                            f"**Level:** {format_number(character_data.get('level', 0))} {EMOJIS['slime_lord']}\n"
                            f"**Guild:** {character_data.get('guild', 'No Guild')}\n"
                            f"**Title:** {character_data.get('title', 'None')}\n"
                            f"**Status:** {status_emoji} {offline_info}\n"
                            f"**Born:** {character_data.get('born', 'Unknown')}"
                        )
                        
                        # Footer with tip
                        embed.set_footer(
                            text="Use /player-stats for detailed statistics",
                            icon_url=bot.user.avatar.url if bot.user.avatar else None
                        )
                    else:
                        embed.description = f"Player **{player}** not found!"
                        embed.color = 0xFF0000  # Red for error
                else:
                    embed.description = f"Player **{player}** not found!"
                    embed.color = 0xFF0000
                    
        except Exception as e:
            embed.description = f"Error searching for **{player}**: {str(e)}"
            embed.color = 0xFF0000
        
        await interaction.response.send_message(embed=embed)