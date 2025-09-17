import discord
from discord.ext import commands

from config import EMBED_COLOR, EMOJIS, ADMIN_IDS


class HelpCog(commands.Cog):
    """Cog for the admin help command"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help_command(self, ctx):
        """
        Display available admin commands
        
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
        
        embed = discord.Embed(
            title=f"Admin Commands {EMOJIS['slime_lord']}{EMOJIS['slime']}",
            color=EMBED_COLOR
        )
        
    # Description of admin commands
        description = (
            "**Admin Commands (Prefix: `!`)**\n\n"
            
            "**!listservers**\n"
            "Shows all servers where the bot is present.\n\n"
            
            "**!help**\n"
            "Shows this help message.\n\n"
            
            "**Slash Commands for Users:**\n"
            "Use `/help` to see all available slash commands!\n\n"
            
            "*Note: Only bot administrators can use prefix commands.*\n"
            "*Regular users should use slash commands like `/help`, `/train`, etc.*"
        )
        
        embed.description = description
        
    # Add extra information
        embed.add_field(
            name="Admin Status",
            value=f"✅ You are a bot administrator",
            inline=False
        )
        
        embed.add_field(
            name="Bot Statistics",
            value=(
                f"Servers: **{len(self.bot.guilds)}**\n"
                f"Users: **{sum(guild.member_count for guild in self.bot.guilds)}**"
            ),
            inline=True
        )
        
        embed.add_field(
            name="Support",
            value="Contact **doub.cpp** for help",
            inline=True
        )
        
    # Footer
        embed.set_footer(
            text="Admin commands are restricted to authorized users only",
            icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None
        )
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(HelpCog(bot))