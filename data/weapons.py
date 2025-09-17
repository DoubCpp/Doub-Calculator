from .models import Weapon

# Complete list of weapons in the game
# Format: Weapon(name, melee_emoji, distance_emoji, magic_emoji, attack, buffs)
WEAPONS = [
    # Basic training weapons
    Weapon("Training Weapon(4)", "4_7_9_11_13_golden_dagger", "4_7_9_11_13_golden_bow", "4_7_9_11_13_golden_wand", 4, 0),
    Weapon("Training Weapon(5)", "4_5_15_17_19_dagger", "4_5_15_17_19_bow", "4_5_15_17_19_wand", 5, 0),
    Weapon("Training Weapon(7)", "4_7_9_11_13_golden_dagger", "4_7_9_11_13_golden_bow", "4_7_9_11_13_golden_wand", 7, 0),
    Weapon("Training Weapon(9)", "4_7_9_11_13_golden_dagger", "4_7_9_11_13_golden_bow", "4_7_9_11_13_golden_wand", 9, 0),
    Weapon("Training Weapon(11)", "4_7_9_11_13_golden_dagger", "4_7_9_11_13_golden_bow", "4_7_9_11_13_golden_wand", 11, 0),
    Weapon("Training Weapon(13)", "4_7_9_11_13_golden_dagger", "4_7_9_11_13_golden_bow", "4_7_9_11_13_golden_wand", 13, 0),
    
    # Basic weapons
    Weapon("Weapon(15)", "4_5_15_17_19_dagger", "4_5_15_17_19_bow", "4_5_15_17_19_wand", 15, 0),
    Weapon("Weapon(17)", "4_5_15_17_19_dagger", "4_5_15_17_19_bow", "4_5_15_17_19_wand", 17, 0),
    Weapon("Weapon(19)", "4_5_15_17_19_dagger", "4_5_15_17_19_bow", "4_5_15_17_19_wand", 19, 0),
    
    # Level 20+ weapons
    Weapon("Weapon(20)", "20_22_24_short_sword", "20_22_24_studded_bow", "20_22_24_novice_wand", 20, 0),
    Weapon("Weapon(22)", "20_22_24_short_sword", "20_22_24_studded_bow", "20_22_24_novice_wand", 22, 0),
    Weapon("Weapon(24)", "20_22_24_short_sword", "20_22_24_studded_bow", "20_22_24_novice_wand", 24, 0),
    
    # Level 25+ weapons
    Weapon("Weapon(25)", "25_27_29_sword", "25_27_29_iron_bow", "25_27_29_priest_wand", 25, 0),
    Weapon("Weapon(27)", "25_27_29_sword", "25_27_29_iron_bow", "25_27_29_priest_wand", 27, 0),
    Weapon("Weapon(29)", "25_27_29_sword", "25_27_29_iron_bow", "25_27_29_priest_wand", 29, 0),
    
    # Drow weapons
    Weapon("Drow Weapon(30)", "30_32_34_341_broadsword", "30_32_34_341_drow_bow", "30_32_34_341_royal_priest_wand", 30, 0),
    Weapon("Drow Weapon(32)", "30_32_34_341_broadsword", "30_32_34_341_drow_bow", "30_32_34_341_royal_priest_wand", 32, 0),
    Weapon("Drow Weapon(34)", "30_32_34_341_broadsword", "30_32_34_341_drow_bow", "30_32_34_341_royal_priest_wand", 34, 0),
    Weapon("Drow Weapon(34+1)", "30_32_34_341_broadsword", "30_32_34_341_drow_bow", "30_32_34_341_royal_priest_wand", 34, 1),
    
    # Lizard/Gargoyle weapons (with multiple emojis)
    Weapon("Lizard/Gargoyle Weapon(35)", 
           ["35_37_39_391_lizard_slayer", "35_37_39_391_gargoyle_slayer"], 
           ["35_37_39_391_lizard_bow", "35_37_39_391_gargoyle_bow"], 
           ["35_37_39_391_shaman_wand", "35_37_39_391_gargoyle_wand"], 35, 0),
    Weapon("Lizard/Gargoyle Weapon(37)", 
           ["35_37_39_391_lizard_slayer", "35_37_39_391_gargoyle_slayer"], 
           ["35_37_39_391_lizard_bow", "35_37_39_391_gargoyle_bow"], 
           ["35_37_39_391_shaman_wand", "35_37_39_391_gargoyle_wand"], 37, 0),
    Weapon("Lizard/Gargoyle Weapon(39)", 
           ["35_37_39_391_lizard_slayer", "35_37_39_391_gargoyle_slayer"], 
           ["35_37_39_391_lizard_bow", "35_37_39_391_gargoyle_bow"], 
           ["35_37_39_391_shaman_wand", "35_37_39_391_gargoyle_wand"], 39, 0),
    Weapon("Lizard/Gargoyle Weapon(39+1)", 
           ["35_37_39_391_lizard_slayer", "35_37_39_391_gargoyle_slayer"], 
           ["35_37_39_391_lizard_bow", "35_37_39_391_gargoyle_bow"], 
           ["35_37_39_391_shaman_wand", "35_37_39_391_gargoyle_wand"], 39, 1),
    
    # Dragon/Minotaur weapons (with multiple emojis)
    Weapon("Dragon/Minotaur Weapon(40+1)", 
           ["401_422_443_dragon_slayer", "401_422_443_minotaur_slayer"], 
           ["401_422_443_dragon_bow", "401_422_443_minotaur_bow"], 
           ["401_422_443_dragon_wand", "401_422_443_minotaur_wand"], 40, 1),
    Weapon("Dragon/Minotaur Weapon(42+2)", 
           ["401_422_443_dragon_slayer", "401_422_443_minotaur_slayer"], 
           ["401_422_443_dragon_bow", "401_422_443_minotaur_bow"], 
           ["401_422_443_dragon_wand", "401_422_443_minotaur_wand"], 42, 2),
    Weapon("Dragon/Minotaur Weapon(44+3)", 
           ["401_422_443_dragon_slayer", "401_422_443_minotaur_slayer"], 
           ["401_422_443_dragon_bow", "401_422_443_minotaur_bow"], 
           ["401_422_443_dragon_wand", "401_422_443_minotaur_wand"], 44, 3),
    
    # Icy weapons
    Weapon("Icy Weapon(45+1)", "451_472_493_icy_broadsword", "451_472_493_icy_bow", "451_472_493_icy_wand", 45, 1),
    Weapon("Icy Weapon(47+2)", "451_472_493_icy_broadsword", "451_472_493_icy_bow", "451_472_493_icy_wand", 47, 2),
    Weapon("Icy Weapon(49+3)", "451_472_493_icy_broadsword", "451_472_493_icy_bow", "451_472_493_icy_wand", 49, 3),
    
    # Golden weapons (the best)
    Weapon("Golden Weapon(50+1)", "501_522_543_golden_broadsword", "501_522_543_golden_bow", "501_522_543_golden_wand", 50, 1),
    Weapon("Golden Weapon(52+2)", "501_522_543_golden_broadsword", "501_522_543_golden_bow", "501_522_543_golden_wand", 52, 2),
    Weapon("Golden Weapon(54+3)", "501_522_543_golden_broadsword", "501_522_543_golden_bow", "501_522_543_golden_wand", 54, 3),
    Weapon("Golden Weapon(56+4)", "501_522_543_golden_broadsword", "501_522_543_golden_bow", "501_522_543_golden_wand", 56, 4),
    Weapon("Golden Weapon(58+5)", "501_522_543_golden_broadsword", "501_522_543_golden_bow", "501_522_543_golden_wand", 58, 5),
]


def get_weapon(index: int) -> Weapon:
    """
    Retrieve a weapon by its index
    
    Args:
        index (int): Index of the weapon in the list
        
    Returns:
        Weapon: The corresponding weapon or None if the index is invalid
    """
    if 0 <= index < len(WEAPONS):
        return WEAPONS[index]
    return None


def get_weapon_by_attack(attack: int, buffs: int = 0) -> Weapon:
    """
    Find a weapon by its attack power and buffs
    
    Args:
        attack (int): Desired attack power
        buffs (int): Number of buffs (default 0)
        
    Returns:
        Weapon: The corresponding weapon or None if not found
    """
    for weapon in WEAPONS:
        if weapon.attack == attack and weapon.buffs == buffs:
            return weapon
    return None