from .exp import setup_exp_command
from .grind import setup_grind_command
from .offline import setup_offline_command
from .stat import setup_stat_command


async def setup_stats_commands(bot):
    """
    Configure all statistics commands
    
    Args:
        bot: The Discord bot instance
    """
    await setup_exp_command(bot)
    await setup_grind_command(bot)
    await setup_offline_command(bot)
    await setup_stat_command(bot)


__all__ = ['setup_stats_commands']