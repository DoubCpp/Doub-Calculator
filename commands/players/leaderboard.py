import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
import aiohttp
import math

from config import EMBED_COLOR, EMOJIS
from utils import format_number
from .api import RucoyAPI


class LeaderboardView(discord.ui.View):
    """View for leaderboard pagination"""
    
    def __init__(self, leaderboard_data, choice, month, year, items_per_page=50):
        super().__init__(timeout=300)  # 5 minutes timeout
        self.leaderboard_data = leaderboard_data
        self.choice = choice
        self.month = month
        self.year = year
        self.items_per_page = items_per_page
        self.current_page = 0
        self.total_pages = math.ceil(len(leaderboard_data) / items_per_page)
        
        # Update button state
        self.update_buttons()
    
    def update_buttons(self):
        """Update button states based on the current page"""
        self.previous_button.disabled = (self.current_page == 0)
        self.next_button.disabled = (self.current_page == self.total_pages - 1)
    
    def get_embed(self):
        """Generate the embed for the current page"""
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_data = self.leaderboard_data[start_idx:end_idx]
        
        embed = discord.Embed(
            title=f"{self.choice.title()} Leaderboard",
            color=EMBED_COLOR
        )
        
        embed.description = f"**Top {self.choice.title()} players (Born Since {self.month:02d}/{self.year}) - Page {self.current_page + 1}/{self.total_pages}:**\n\n"
        
        for player in page_data:
            rank = player['rank']
            name = player['name']
            level = player['level']
            online_status = f" {EMOJIS['online']}" if player['online'] else ""
            
            embed.description += f"**{rank}.** {name}{online_status} - Level **{format_number(level)}**\n"
        
        return embed
    
    @discord.ui.button(label="Previous", style=discord.ButtonStyle.secondary, emoji="⬅️")
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            embed = self.get_embed()
            await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Next", style=discord.ButtonStyle.secondary, emoji="➡️")
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_buttons()
            embed = self.get_embed()
            await interaction.response.edit_message(embed=embed, view=self)
    
    async def on_timeout(self):
        """Disable buttons when the view expires"""
        for item in self.children:
            item.disabled = True


async def setup_leaderboard_command(bot: commands.Bot):
    """Configure the /leaderboard command"""
    
    @bot.tree.command(name="leaderboard", description="Shows the leaderboard for a specific class")
    @app_commands.describe(
        choice="The class/stat to show leaderboard for",
        born="Born since date (format: MM/YYYY, default: 01/2016)",
        list="Number of players to show (default: 20, max: 100)"
    )
    @app_commands.choices(choice=[
        app_commands.Choice(name="Experience", value="experience"),
        app_commands.Choice(name="Melee", value="melee"),
        app_commands.Choice(name="Distance", value="distance"),
        app_commands.Choice(name="Magic", value="magic"),
        app_commands.Choice(name="Defense", value="defense")
    ])
    async def leaderboard_command(
        interaction: discord.Interaction,
        choice: str,
        born: Optional[str] = "01/2016",
        list: Optional[int] = 20
    ):
        """
        Show the leaderboard for a specific class
        
        Args:
            interaction: The Discord interaction
            choice: Type of leaderboard
            born: Minimum 'born since' date (MM/YYYY)
            list: Number of players to display
        """
        # Validate the 'list' parameter
        if list is None or list < 1:
            list = 20
        elif list > 100:
            list = 100
        
        # Parse the 'born' parameter
        try:
            if born and "/" in born:
                month_str, year_str = born.split("/")
                month = int(month_str)
                year = int(year_str)
            else:
                month = 1
                year = 2016
        except (ValueError, IndexError):
            month = 1
            year = 2016
        
        embed = discord.Embed(
            title=f"{choice.title()} Leaderboard",
            color=EMBED_COLOR
        )
        
        try:
            async with aiohttp.ClientSession() as session:
                # Build the URL for highscores with date filter
                url = f"{RucoyAPI.BASE_URL}/highscores/{choice}/{year}/{month}"
                html_content = await RucoyAPI.fetch_page(session, url)
                
                if html_content:
                    leaderboard_data = RucoyAPI.parse_leaderboard_data(html_content, choice)
                    
                    if leaderboard_data:
                        # Limit results to the requested number
                        limited_data = leaderboard_data[:list]
                        
                        # If more than 50 items, use pagination
                        if len(limited_data) > 50:
                            view = LeaderboardView(limited_data, choice, month, year)
                            embed = view.get_embed()
                            await interaction.response.send_message(embed=embed, view=view)
                        else:
                            # Use a simple embed for 50 items or fewer
                            embed.description = f"**Top {len(limited_data)} {choice.title()} players (Born Since {month:02d}/{year}):**\n\n"
                            
                            for player in limited_data:
                                rank = player['rank']
                                name = player['name']
                                level = player['level']
                                online_status = f" {EMOJIS['online']}" if player['online'] else ""
                                
                                embed.description += f"**{rank}.** {name}{online_status} - Level **{format_number(level)}**\n"
                            
                            await interaction.response.send_message(embed=embed)
                    else:
                        embed.description = f"No leaderboard data found for {choice.title()} (Born Since {month:02d}/{year})!"
                        await interaction.response.send_message(embed=embed)
                else:
                    embed.description = f"Could not fetch leaderboard for {choice.title()} (Born Since {month:02d}/{year})!"
                    await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed.description = f"Error fetching leaderboard: {str(e)}"
            await interaction.response.send_message(embed=embed)