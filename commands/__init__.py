from .admin import setup_admin_commands
from .info import setup_info_commands
from .economy import setup_economy_commands
from .stats import setup_stats_commands
from .training import setup_training_commands
from .players import setup_players_commands


async def setup_all_commands(bot):
    """
    Configure all bot commands
    
    Args:
        bot: The Discord bot instance
    """
    # Admin commands (prefix !)
    await setup_admin_commands(bot)
    
    # Info commands (/help, /info, /invite)
    await setup_info_commands(bot)
    
    # Economy commands (/skull, /potioncost)
    await setup_economy_commands(bot)
    
    # Stats commands (/exp, /grind, /offline, /stat)
    await setup_stats_commands(bot)
    
    # Training commands (/train, /ptrain, /dmg, /weapon, /oneshot, /moblist)
    await setup_training_commands(bot)
    
    # Player commands (/leaderboard, /characters, /guild-infos, /player-stats, /player-logs)
    await setup_players_commands(bot)


__all__ = ['setup_all_commands']