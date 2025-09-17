import discord
from discord import app_commands
from discord.ext import commands

from config import EMBED_COLOR, EMOJIS


async def setup_invite_command(bot: commands.Bot):
    """Configure the /invite command"""
    
    @bot.tree.command(name="invite", description="Get the bot invitation link")
    async def invite_command(interaction: discord.Interaction):
        """
        Generates and displays the bot's invitation link
        
        Args:
            interaction: The Discord interaction
        """
        embed = discord.Embed(
            title=f"Invite Me! {EMOJIS['slime_lord']}{EMOJIS['slime']}",
            color=EMBED_COLOR
        )
        
        # Retrieve the bot ID
        bot_id = bot.user.id if bot.user else "YOUR_BOT_ID"
        
        # Generate the invite URL with the necessary permissions
        # Included permissions:
        # - Send messages
        # - Use slash commands
        # - Embed links
        # - Read message history
        # - Add reactions
        # - Use external emojis
        permissions = discord.Permissions(
            send_messages=True,
            embed_links=True,
            read_message_history=True,
            add_reactions=True,
            use_external_emojis=True,
            use_application_commands=True
        )
        
        invite_url = discord.utils.oauth_url(
            bot_id,
            permissions=permissions,
            scopes=["bot", "applications.commands"]
        )
        
        # Invitation message
        message = (
            f"**Invite Doub' Rucoy Calculator to your server!** {EMOJIS['slime_lord']}\n\n"
            f"Click the link below to add me to your Discord server:\n"
            f"[**Invite Bot**]({invite_url})\n\n"
            f"**Permissions needed:**\n"
            f"{EMOJIS['slime']} Send Messages\n"
            f"{EMOJIS['slime']} Use Slash Commands\n"
            f"{EMOJIS['slime']} Embed Links\n"
            f"{EMOJIS['slime']} Read Message History\n"
            f"{EMOJIS['slime']} Add Reactions\n"
            f"{EMOJIS['slime']} Use External Emojis\n\n"

            f"*Need help? Contact: **doub.cpp***"
        )
        
        embed.description = message
        
        # Add a button for the invitation
        view = discord.ui.View()
        invite_button = discord.ui.Button(
            label="Invite Bot",
            style=discord.ButtonStyle.link,
            url=invite_url,
            emoji=EMOJIS['slime']
        )
        view.add_item(invite_button)
        
        # Footer
        embed.set_footer(
            text="Thank you for your trust!",
            icon_url=bot.user.avatar.url if bot.user and bot.user.avatar else None
        )
        
        await interaction.response.send_message(embed=embed, view=view)