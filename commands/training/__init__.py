from .train import setup_train_command
from .ptrain import setup_ptrain_command
from .dmg import setup_dmg_command
from .weapon import setup_weapon_command
from .oneshot import setup_oneshot_command
from .moblist import setup_moblist_command


async def setup_training_commands(bot):
    """
    Configure all training commands
    
    Args:
        bot: The Discord bot instance
    """
    await setup_train_command(bot)
    await setup_ptrain_command(bot)
    await setup_dmg_command(bot)
    await setup_weapon_command(bot)
    await setup_oneshot_command(bot)
    await setup_moblist_command(bot)


__all__ = ['setup_training_commands']