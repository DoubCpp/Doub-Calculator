from .models import Mob

# Complete list of monsters in the game
# Format: Mob(name, emoji_key, defense, health)
MOBS = [
    # Index 0-12: Power-trainable monsters
    Mob("Rat Lv.1", "1_rat", 4, 25),
    Mob("Rat Lv.3", "3_rat", 7, 35),
    Mob("Crow Lv.6", "6_crow", 13, 40),
    Mob("Wolf Lv.9", "9_wolf", 17, 50),
    Mob("Scorpion Lv.12", "12_scorpion", 18, 50),
    Mob("Cobra Lv.13", "14_cobra", 18, 50),
    Mob("Worm Lv.14", "14_worm", 19, 55),
    Mob("Goblin Lv.15", "15_goblin", 21, 60),
    Mob("Mummy Lv.25", "25_mummy", 36, 80),
    Mob("Pharaoh Lv.35", "35_pharaoh", 51, 100),
    Mob("Assassin Lv.45", "45_assassin", 71, 120),
    Mob("Assassin Lv.50", "50_assassin", 81, 140),
    Mob("Assassin Ninja Lv.55", "55_ninja_assassin", 91, 160),
    
    # Index 13: Not power-trainable
    Mob("Skeleton Archer Lv.80", "80_skeleton_archer", 101, 300),
    
    # Index 14-18: Power-trainable
    Mob("Zombie Lv.65", "65_zombie", 106, 200),
    Mob("Skeleton Lv.75", "75_skeleton", 121, 300),
    Mob("Skeleton Warrior Lv.90", "90_skeleton_warrior", 146, 375),
    Mob("Vampire Lv.100", "100_vampire", 171, 450),
    Mob("Vampire Lv.110", "110_vampire", 186, 530),
    
    # Index 19-20: Not power-trainable
    Mob("Drow Ranger Lv.125", "120_drow_ranger", 191, 600),
    Mob("Drow Mage Lv. 130", "130_drow_mage", 191, 600),
    
    # Index 21: Power-trainable
    Mob("Drow Assassin Lv.120", "125_drow_assassin", 221, 620),
    
    # Index 22: Not power-trainable
    Mob("Drow Sorceress Lv.140", "140_drow_sorceress", 221, 600),
    
    # Index 23: Power-trainable
    Mob("Drow Fighter Lv.135", "135_drow_fighter", 246, 680),
    
    # Index 24-26: Not power-trainable
    Mob("Lizard Archer Lv.160", "160_lizard_archer", 271, 650),
    Mob("Lizard Shaman Lv.170", "170_lizard_shaman", 276, 600),
    Mob("Dead Eyes Lv.170", "170_dead_eyes", 276, 600),
    
    # Index 27-28: Power-trainable
    Mob("Lizard Warrior Lv.150", "150_lizard_warrior", 301, 680),
    Mob("Djinn Lv.150", "150_djinn", 301, 640),
    
    # Index 29: Not power-trainable
    Mob("Lizard High Shaman Lv.190", "190_lizard_high_shaman", 326, 740),
    
    # Index 30: Power-trainable
    Mob("Gargoyle Lv.190", "190_gargoyle", 326, 740),
    
    # Index 31: Not power-trainable
    Mob("Dragon Hatchling Lv. 240", "240_dragon_hatchling", 331, 10000),
    
    # Index 32: Power-trainable
    Mob("Lizard Captain lv.180", "180_lizard_captain", 361, 815),
    
    # Index 33: Not power-trainable
    Mob("Dragon Lv.250", "250_dragon", 501, 20000),
    
    # Index 34-35: Power-trainable
    Mob("Minotaur Lv.225", "225_minotaur", 511, 4250),
    Mob("Minotaur Lv.250", "250_minotaur", 591, 5000),
    
    # Index 36-37: Not power-trainable
    Mob("Dragon Warden Lv.280", "280_dragon_warden", 626, 30000),
    Mob("Ice Elemental Lv.300", "300_ice_elemental", 676, 40000),
    
    # Index 38: Power-trainable
    Mob("Minotaur Lv.275", "275_minotaur", 681, 5750),
    
    # Index 39+: Not power-trainable
    Mob("Ice Dragon Lv.320", "320_ice_dragon", 726, 50000),
    Mob("Yeti Lv.350", "350_yeti", 826, 60000),
]


def get_mob(index: int) -> Mob:
    """
    Retrieve a monster by its index
    
    Args:
        index (int): Index of the monster in the list
        
    Returns:
        Mob: The corresponding monster or None if the index is invalid
    """
    if 0 <= index < len(MOBS):
        return MOBS[index]
    return None


def is_power_trainable(mob_index: int) -> bool:
    """
    Check if a monster is power-trainable
    
    Args:
        mob_index (int): Index of the monster to check
        
    Returns:
        bool: True if the monster is power-trainable, False otherwise
    """
    # Monsters that are not power-trainable: 13, 19-20, 22, 24-26, 29, 31, 33, 36-37, 39+
    non_power_trainable = [13, 19, 20, 22, 24, 25, 26, 29, 31, 33, 36, 37]
    non_power_trainable.extend(range(39, len(MOBS)))
    return mob_index not in non_power_trainable