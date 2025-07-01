import discord
from discord.ext import commands
from config import EMBED_COLOR, EMOJIS, ADMIN_IDS

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help_command(self, ctx):
        """Display help information"""
        
        # Check if user is admin
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
        await ctx.send(embed=embed)
