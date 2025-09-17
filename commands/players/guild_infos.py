import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import math

from config import EMBED_COLOR, EMOJIS
from utils import format_number
from .api import RucoyAPI


class GuildMembersView(discord.ui.View):
    """View for paginating guild members"""
    
    def __init__(self, guild_data, items_per_page=20):
        super().__init__(timeout=300)  # 5 minutes timeout
        self.guild_data = guild_data
        self.items_per_page = items_per_page
        self.current_page = 0
        
    # Separate the leader and regular members
        self.leader = None
        self.regular_members = []
        
        for member in guild_data.get('members', []):
            if member['is_leader']:
                self.leader = member
            else:
                self.regular_members.append(member)
        
        self.total_pages = max(1, math.ceil(len(self.regular_members) / items_per_page))
        
        # Update button state
        self.update_buttons()
    
    def update_buttons(self):
        """Update button state based on the current page"""
        self.previous_button.disabled = (self.current_page == 0)
        self.next_button.disabled = (self.current_page == self.total_pages - 1)
    
    def get_embed(self):
        """Generate the embed for the current page"""
        embed = discord.Embed(
            title=f"Guild: {self.guild_data.get('name', 'Unknown')}",
            color=EMBED_COLOR
        )
        
        description = self.guild_data.get('description', 'No description available')
        if len(description) > 400:
            description = description[:400] + "..."
        
        embed.description = f"**Description:**\n{description}\n\n"
        embed.description += f"**Founded:** {self.guild_data.get('founded', 'Unknown')}\n"
        embed.description += f"**Members:** {self.guild_data.get('member_count', 0)}\n\n"
        
        # Add the list of members with pagination
        embed.description += f"**Members (Page {self.current_page + 1}/{self.total_pages}):**\n"
        
        # Show the leader first (always on each page)
        if self.leader:
            online_status = f" {EMOJIS['online']}" if self.leader.get('is_online', False) else ""
            supporter_text = f" {EMOJIS['slime']}" if self.leader['is_supporter'] else ""
            embed.description += f"👑 **{self.leader['name']}**{online_status}{supporter_text} - Level {format_number(self.leader['level'])} *(Leader)*\n"
        
        # Show paginated regular members
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_members = self.regular_members[start_idx:end_idx]
        
        for member in page_members:
            online_status = f" {EMOJIS['online']}" if member.get('is_online', False) else ""
            supporter_text = f" {EMOJIS['slime']}" if member['is_supporter'] else ""
            embed.description += f"• **{member['name']}**{online_status}{supporter_text} - Level {format_number(member['level'])}\n"
        
        if not page_members and not self.leader:
            embed.description += "**No members found**"
        
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


async def setup_guild_infos_command(bot: commands.Bot):
    """Configure the /guild-infos command"""
    
    @bot.tree.command(name="guild-infos", description="Shows information about a guild and its members")
    @app_commands.describe(guild="The guild name to search for")
    async def guild_infos_command(interaction: discord.Interaction, guild: str):
        """
        Displays information about a guild and its members
        
        Args:
            interaction: The Discord interaction
            guild: The guild name to search for
        """
        embed = discord.Embed(
            title="Guild Information",
            color=EMBED_COLOR
        )
        
        try:
            async with aiohttp.ClientSession() as session:
                # Encode the guild name for the URL
                encoded_name = guild.replace(" ", "%20")
                url = f"{RucoyAPI.BASE_URL}/guild/{encoded_name}"
                html_content = await RucoyAPI.fetch_page(session, url)
                
                if html_content:
                    guild_data = RucoyAPI.parse_guild_data(html_content)
                    
                    if guild_data and guild_data.get('name'):
                        # Check if pagination is necessary
                        members = guild_data.get('members', [])
                        regular_members_count = len([m for m in members if not m['is_leader']])
                        
                        if regular_members_count > 20:
                            # Use pagination for more than 20 members
                            view = GuildMembersView(guild_data)
                            embed = view.get_embed()
                            await interaction.response.send_message(embed=embed, view=view)
                        else:
                            # Use a simple embed for 20 members or fewer
                            embed.title = f"Guild: {guild_data.get('name', 'Unknown')}"
                            
                            description = guild_data.get('description', 'No description available')
                            if len(description) > 800:
                                description = description[:800] + "..."
                            
                            embed.description = f"**Description:**\n{description}\n\n"
                            embed.description += f"**Founded:** {guild_data.get('founded', 'Unknown')}\n"
                            embed.description += f"**Members:** {guild_data.get('member_count', 0)}\n\n"
                            
                            # Add the list of members
                            if members:
                                embed.description += "**Members:**\n"
                                
                                # Separate the leader and members
                                leader = None
                                regular_members = []
                                
                                for member in members:
                                    if member['is_leader']:
                                        leader = member
                                    else:
                                        regular_members.append(member)
                                
                                # Show the leader first
                                if leader:
                                    online_status = f" {EMOJIS['online']}" if leader.get('is_online', False) else ""
                                    supporter_text = f" {EMOJIS['slime']}" if leader['is_supporter'] else ""
                                    embed.description += f"👑 **{leader['name']}**{online_status}{supporter_text} - Level {format_number(leader['level'])} *(Leader)*\n"
                                
                                # Show regular members
                                for member in regular_members:
                                    online_status = f" {EMOJIS['online']}" if member.get('is_online', False) else ""
                                    supporter_text = f" {EMOJIS['slime']}" if member['is_supporter'] else ""
                                    embed.description += f"• **{member['name']}**{online_status}{supporter_text} - Level {format_number(member['level'])}\n"
                            else:
                                embed.description += "**No members found**"
                            
                            # Add statistics
                            if members:
                                online_count = sum(1 for m in members if m.get('is_online', False))
                                supporter_count = sum(1 for m in members if m.get('is_supporter', False))
                                avg_level = sum(m['level'] for m in members) // len(members) if members else 0
                                
                                embed.add_field(
                                    name="Guild Statistics",
                                    value=(
                                        f"Online Members: **{online_count}/{len(members)}**\n"
                                        f"Supporters: **{supporter_count}**\n"
                                        f"Average Level: **{avg_level}**"
                                    ),
                                    inline=False
                                )
                            
                            await interaction.response.send_message(embed=embed)
                    else:
                        embed.description = f"Guild **{guild}** not found!"
                        embed.color = 0xFF0000
                        await interaction.response.send_message(embed=embed)
                else:
                    embed.description = f"Guild **{guild}** not found!"
                    embed.color = 0xFF0000
                    await interaction.response.send_message(embed=embed)
                    
        except Exception as e:
            embed.description = f"Error searching for guild **{guild}**: {str(e)}"
            embed.color = 0xFF0000
            await interaction.response.send_message(embed=embed)