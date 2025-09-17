import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import asyncio
import re

from config import EMBED_COLOR, EMOJIS
from utils import format_number
from .api import RucoyAPI


async def setup_player_stats_command(bot: commands.Bot):
    """Configure the /player-stats command"""
    
    @bot.tree.command(name="player-stats", description="Shows detailed statistics for a player")
    @app_commands.describe(player="The player name to search for")
    async def player_stats_command(interaction: discord.Interaction, player: str):
        """
        Displays detailed statistics for a player
        
        Args:
            interaction: The Discord interaction
            player: The player name to search for
        """
        # Defer the response as this may take a moment
        await interaction.response.defer()
        
        embed = discord.Embed(
            title="Player Statistics",
            color=EMBED_COLOR
        )
        
        try:
            async with aiohttp.ClientSession() as session:
                # First, get character data to have the exact name and born date
                encoded_name = player.replace(" ", "+")
                char_url = f"{RucoyAPI.BASE_URL}/characters?utf8=%E2%9C%93&name={encoded_name}"
                char_html = await RucoyAPI.fetch_page(session, char_url)
                
                if not char_html:
                    embed.description = f"Player **{player}** not found!"
                    embed.color = 0xFF0000
                    await interaction.followup.send(embed=embed)
                    return
                
                character_data = RucoyAPI.parse_character_data(char_html)
                
                if not character_data or not character_data.get('name'):
                    embed.description = f"Player **{player}** not found!"
                    embed.color = 0xFF0000
                    await interaction.followup.send(embed=embed)
                    return
                
                # Get the exact name and born date
                exact_name = character_data.get('name', player)
                born_date = character_data.get('born', 'Unknown')
                
                # Parse the born date to get month and year
                # Default values
                year = 2016
                month = 1
                
                # Try to parse the born date
                if born_date and born_date != 'Unknown':
                    # Format: "March 18, 2020"
                    month_names = {
                        'January': 1, 'February': 2, 'March': 3, 'April': 4,
                        'May': 5, 'June': 6, 'July': 7, 'August': 8,
                        'September': 9, 'October': 10, 'November': 11, 'December': 12
                    }
                    
                    # Try to match the format "Month Day, Year"
                    match = re.match(r'(\w+)\s+\d+,\s+(\d{4})', born_date)
                    if match:
                        month_name = match.group(1)
                        year = int(match.group(2))
                        month = month_names.get(month_name, 1)
                
                # Now search across all leaderboards using parallel requests
                stat_types = ['experience', 'melee', 'distance', 'magic', 'defense']
                leaderboard_stats = {}
                
                # Create tasks for parallel requests
                tasks = []
                for stat_type in stat_types:
                    url = f"{RucoyAPI.BASE_URL}/highscores/{stat_type}/{year}/{month}"
                    task = asyncio.create_task(RucoyAPI.fetch_page(session, url))
                    tasks.append((stat_type, task))
                
                # Wait for all requests to finish
                results = await asyncio.gather(*[task for _, task in tasks])
                
                # Process results
                player_found_in_any = False
                player_info = None
                
                for (stat_type, _), html_content in zip(tasks, results):
                    if html_content:
                        lb_data = RucoyAPI.parse_leaderboard_data(html_content, stat_type)
                        
                        # Search for the player in this leaderboard
                        for player_data in lb_data:
                            if player_data['name'].lower() == exact_name.lower():
                                leaderboard_stats[stat_type] = {
                                    'rank': player_data['rank'],
                                    'level': player_data['level']
                                }
                                # Store player info from the first match
                                if not player_found_in_any:
                                    player_info = player_data
                                    player_found_in_any = True
                                break
                
                # Build the embed with all information
                embed.title = f"Player {EMOJIS['slime_lord']}{EMOJIS['slime']}: {exact_name}"
                description = f"**Account Created:** {born_date}\n\n"
                
                # Leaderboards
                description += f"**Statistics {EMOJIS['slime']}:**\n"
                
                # Define stat emojis
                stat_emojis = {
                    'experience': EMOJIS['slime_lord'],
                    'melee': EMOJIS['melee'],
                    'distance': EMOJIS['distance'],
                    'magic': EMOJIS['magic'],
                    'defense': EMOJIS['defense']
                }

                if leaderboard_stats:
                    for stat_type in stat_types:
                        stat_name = stat_type.title()
                        stat_emoji = stat_emojis.get(stat_type, '')
                        if stat_type in leaderboard_stats:
                            level = leaderboard_stats[stat_type]['level']
                            description += f"• {stat_emoji} **{stat_name}:** Level {format_number(level)}\n"
                        else:
                            description += f"• {stat_emoji} **{stat_name}:** Not in top 100\n"
                else:
                    description += "*Player not found in any top 100 leaderboards*\n"
                
                embed.description = description
               
                # Footer
                embed.set_footer(
                    text="Stats based on current leaderboards",
                    icon_url=bot.user.avatar.url if bot.user.avatar else None
                )
                
        except Exception as e:
            embed.description = f"Error fetching player statistics: {str(e)}"
            embed.color = 0xFF0000
        
        await interaction.followup.send(embed=embed)