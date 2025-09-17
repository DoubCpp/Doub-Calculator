from .help import HelpCog
from .listservers import ListServersCog


async def setup_admin_commands(bot):
    """
    Configure all administrator commands
    
    Args:
        bot: The Discord bot instance
    """
    await bot.add_cog(HelpCog(bot))
    await bot.add_cog(ListServersCog(bot))


__all__ = ['setup_admin_commands', 'HelpCog', 'ListServersCog']