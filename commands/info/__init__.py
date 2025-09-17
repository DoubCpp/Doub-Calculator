from .help import setup_help_command
from .info import setup_info_command
from .invite import setup_invite_command


async def setup_info_commands(bot):
    """
    Configure all information commands
    
    Args:
        bot: The Discord bot instance
    """
    await setup_help_command(bot)
    await setup_info_command(bot)
    await setup_invite_command(bot)


__all__ = ['setup_info_commands']