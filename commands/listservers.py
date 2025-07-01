import discord
from discord.ext import commands
from config import EMBED_COLOR, EMOJIS, ADMIN_IDS

class ListServersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='listservers')
    async def list_servers(self, ctx):

        if ctx.author.id not in ADMIN_IDS:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You don't have permission to use this command.",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return

        guilds = self.bot.guilds
        
        embed = discord.Embed(
            title=f"Bot Servers {EMOJIS['slime_lord']}{EMOJIS['slime']}",
            color=EMBED_COLOR
        )
        
        if not guilds:
            embed.description = "The bot is not in any servers."
        else:
            embed.description = f"**Total servers: {len(guilds)}**\n\n"
            
            server_list = []
            for i, guild in enumerate(guilds, 1):
                member_count = guild.member_count
                server_list.append(f"**{i}.** `{guild.id}` - **{guild.name}** ({member_count} members)")

            if len(server_list) <= 20:
                embed.description += "\n".join(server_list)
            else:
                embed.description += "\n".join(server_list[:20])
                embed.description += f"\n\n*... and {len(server_list) - 20} more servers*"
        
        await ctx.send(embed=embed)
