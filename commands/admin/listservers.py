import discord
from discord.ext import commands

from config import EMBED_COLOR, EMOJIS, ADMIN_IDS


class ServerListView(discord.ui.View):
    """View for paginating the server list"""
    
    def __init__(self, guilds, per_page=20):
        super().__init__(timeout=60)
        self.guilds = guilds
        self.per_page = per_page
        self.current_page = 0
        self.max_pages = (len(guilds) - 1) // per_page + 1 if guilds else 1
        
        # Update the state of the buttons
        self.update_buttons()
    
    def update_buttons(self):
        """Enable/disable buttons based on the current page"""
        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= self.max_pages - 1
    
    def get_embed(self):
        """Generate the embed for the current page"""
        embed = discord.Embed(
            title=f"Bot Servers {EMOJIS['slime_lord']}{EMOJIS['slime']}",
            color=EMBED_COLOR
        )
        
        if not self.guilds:
            embed.description = "The bot is not in any servers."
            return embed
        
        # Calculate start and end indices
        start_idx = self.current_page * self.per_page
        end_idx = min(start_idx + self.per_page, len(self.guilds))
        
        # Create the description
        embed.description = f"**Total servers: {len(self.guilds)}**\n"
        embed.description += f"**Page {self.current_page + 1}/{self.max_pages}**\n\n"
        
        # Add the servers for the current page
        for i in range(start_idx, end_idx):
            guild = self.guilds[i]
            member_count = guild.member_count
            embed.description += f"**{i + 1}.** `{guild.id}` - **{guild.name}** ({member_count} members)\n"
        
        return embed
    
    @discord.ui.button(label='Previous', style=discord.ButtonStyle.primary, emoji='◀️')
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Button to go to the previous page"""
        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
    
    @discord.ui.button(label='Next', style=discord.ButtonStyle.primary, emoji='▶️')
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Button to go to the next page"""
        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
    
    async def on_timeout(self):
        """Disable all buttons when the view expires"""
        for item in self.children:
            item.disabled = True


class ListServersCog(commands.Cog):
    """Cog for the server list command"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='listservers')
    async def list_servers(self, ctx):
        """
        List all servers where the bot is present
        
        Args:
            ctx: The command context
        """
        # Check if the user is an admin
        if ctx.author.id not in ADMIN_IDS:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don't have permission to use this command.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        
        # Get all servers
        guilds = list(self.bot.guilds)
        
        # Sort by member count (descending)
        guilds.sort(key=lambda g: g.member_count, reverse=True)
        
        # Create the view with pagination
        view = ServerListView(guilds)
        embed = view.get_embed()
        
        # Add global statistics
        total_members = sum(guild.member_count for guild in guilds)
        avg_members = total_members // len(guilds) if guilds else 0
        
        embed.add_field(
            name="Statistics",
            value=(
                f"Total Members: **{total_members:,}**\n"
                f"Average per Server: **{avg_members:,}**"
            ),
            inline=False
        )
        
        # Send the message with the view
        message = await ctx.send(embed=embed, view=view)
        
        # Wait for timeout and update the message
        await view.wait()
        await message.edit(view=view)


async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(ListServersCog(bot))