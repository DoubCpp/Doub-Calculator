from .skull import setup_skull_command
from .potioncost import setup_potioncost_command


async def setup_economy_commands(bot):
    """
    Configure all economy commands
    
    Args:
        bot: The Discord bot instance
    """
    await setup_skull_command(bot)
    await setup_potioncost_command(bot)


__all__ = ['setup_economy_commands']