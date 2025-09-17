import discord
from discord import app_commands
from discord.ext import commands
import aiohttp

from config import EMBED_COLOR, EMOJIS
from .api import RucoyAPI


async def setup_player_logs_command(bot: commands.Bot):
    """Configure the /player-logs command"""
    
    @bot.tree.command(name="player-logs", description="Shows PvP logs for a player (kills and deaths)")
    @app_commands.describe(player="The player name to search for")
    async def player_logs_command(interaction: discord.Interaction, player: str):
        """
        Displays a player's PvP logs (kills and deaths)
        
        Args:
            interaction: The Discord interaction
            player: The player name to search for
        """
        embed = discord.Embed(
            title="PvP Logs",
            color=EMBED_COLOR
        )
        
        try:
            async with aiohttp.ClientSession() as session:
                # Encode the player name for the URL
                encoded_name = player.replace(" ", "+")
                url = f"{RucoyAPI.BASE_URL}/characters?utf8=%E2%9C%93&name={encoded_name}"
                html_content = await RucoyAPI.fetch_page(session, url)
                
                if html_content:
                    # First check if the player exists
                    character_data = RucoyAPI.parse_character_data(html_content)
                    
                    if character_data and character_data.get('name'):
                        exact_name = character_data.get('name', player)
                        logs_slime = f" {EMOJIS['slime_lord']}{EMOJIS['slime']}" 
                        
                        # Parse PvP logs
                        pvp_logs = RucoyAPI.parse_pvp_logs(html_content, exact_name)
                        
                        if pvp_logs:
                            embed.title = f"PvP Logs{logs_slime}: {exact_name}"
                            embed.description = ""
                            
                            # Stats counters
                            kills = 0
                            deaths = 0
                            
                            # Build log entries
                            log_entries = []
                            
                            for log in pvp_logs[:20]:  # Limit to the 20 most recent
                                if log['type'] == 'kill':
                                    kills += 1
                                    victim = log.get('victim', 'Unknown')
                                    time_ago = log.get('time_ago', 'Unknown')
                                    log_entries.append(f"{EMOJIS['pvp']} **Killed** {victim} - *{time_ago}*")
                                    
                                elif log['type'] == 'death':
                                    deaths += 1
                                    killers = log.get('killers', [])
                                    time_ago = log.get('time_ago', 'Unknown')
                                    
                                    if len(killers) == 1:
                                        log_entries.append(f"{EMOJIS['death']} **Killed by** {killers[0]} - *{time_ago}*")
                                    elif len(killers) > 1:
                                        killers_text = ", ".join(killers[:-1]) + f" and {killers[-1]}"
                                        log_entries.append(f"{EMOJIS['death']} **Killed by** {killers_text} - *{time_ago}*")
                                    else:
                                        log_entries.append(f"{EMOJIS['death']} **Died** - *{time_ago}*")
                            
                            # Add the summary at the top
                            embed.description = f"**PvP Activity:**\n"
                            embed.description += f"Kills: **{kills}** | Deaths: **{deaths}**"
                            
                            if kills > 0 and deaths > 0:
                                kd_ratio = kills / deaths
                                embed.description += f" | K/D: **{kd_ratio:.2f}**"
                            elif kills > 0 and deaths == 0:
                                embed.description += f" | K/D: **∞**"
                            
                            embed.description += "\n\n"
                            
                            # Add log entries
                            if log_entries:
                                embed.description += "**Recent Activity:**\n"
                                embed.description += "\n".join(log_entries)
                            
                            if len(pvp_logs) > 20:
                                embed.description += f"\n\n*Showing 20 most recent logs out of {len(pvp_logs)} total*"
                            
                            # Add detailed statistics
                            if pvp_logs:
                                # Analyze most frequent victims and killers
                                victim_count = {}
                                killer_count = {}
                                
                                for log in pvp_logs:
                                    if log['type'] == 'kill':
                                        victim = log.get('victim', 'Unknown')
                                        victim_count[victim] = victim_count.get(victim, 0) + 1
                                    elif log['type'] == 'death':
                                        for killer in log.get('killers', []):
                                            killer_count[killer] = killer_count.get(killer, 0) + 1
                                            
                        else:
                            embed.description = f"No PvP logs found for **{exact_name}**{logs_slime}"
                            embed.add_field(
                                name="Possible Reasons",
                                value=(
                                    "• Player has no recent PvP activity\n"
                                    "• Player is peaceful and avoids PvP\n"
                                    "• Logs may have expired"
                                ),
                                inline=False
                            )
                    else:
                        embed.description = f"Player **{player}** not found!"
                        embed.color = 0xFF0000
                else:
                    embed.description = f"Player **{player}** not found!"
                    embed.color = 0xFF0000
                    
        except Exception as e:
            embed.description = f"Error fetching PvP logs for **{player}**: {str(e)}"
            embed.color = 0xFF0000
        
        await interaction.response.send_message(embed=embed)