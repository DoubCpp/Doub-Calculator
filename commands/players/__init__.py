from .api import RucoyAPI
from .leaderboard import setup_leaderboard_command, LeaderboardView
from .characters import setup_characters_command
from .guild_infos import setup_guild_infos_command, GuildMembersView
from .player_stats import setup_player_stats_command
from .player_logs import setup_player_logs_command


async def setup_players_commands(bot):
    """
    Configure all player-related commands
    
    Args:
        bot: The Discord bot instance
    """
    await setup_leaderboard_command(bot)
    await setup_characters_command(bot)
    await setup_guild_infos_command(bot)
    await setup_player_stats_command(bot)
    await setup_player_logs_command(bot)


__all__ = [
    'setup_players_commands',
    'RucoyAPI',
    'LeaderboardView',
    'GuildMembersView'
]