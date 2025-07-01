from config import EMOJIS

class Mob:
    def __init__(self, name, emoji_key, defense, health):
        self.name = name
        self.emoji_key = emoji_key
        self.defense = defense
        self.health = health
    
    @property
    def emoji(self):
        return EMOJIS.get(self.emoji_key, "")
    
    def __str__(self):
        return f"{self.name} {self.emoji}"


class Weapon:
    def __init__(self, name, melee_emoji_key, distance_emoji_key, magic_emoji_key, attack, buffs):
        self.name = name
        self.melee_emoji_key = melee_emoji_key
        self.distance_emoji_key = distance_emoji_key
        self.magic_emoji_key = magic_emoji_key
        self.attack = attack
        self.buffs = buffs
    
    def _get_emoji_from_key(self, key):
        if isinstance(key, list):
            return "".join(EMOJIS.get(k, "") for k in key)
        else:
            return EMOJIS.get(key, "")
    
    @property
    def melee_emoji(self):
        return self._get_emoji_from_key(self.melee_emoji_key)
    
    @property
    def distance_emoji(self):
        return self._get_emoji_from_key(self.distance_emoji_key)
    
    @property
    def magic_emoji(self):
        return self._get_emoji_from_key(self.magic_emoji_key)
    
    def get_emoji(self, class_type=None):
        if class_type == 0:  # Melee
            return self.melee_emoji
        elif class_type == 1:  # Distance
            return self.distance_emoji
        elif class_type == 2:  # Magic
            return self.magic_emoji
        else:  # All emojis
            return self.melee_emoji + self.distance_emoji + self.magic_emoji


# Mob data 
MOBS = [
    # Index 0-12: Power trainable mobs
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
    # Index 13: Not power trainable
    Mob("Skeleton Archer Lv.80", "80_skeleton_archer", 101, 300),
    # Index 14-18: Power trainable
    Mob("Zombie Lv.65", "65_zombie", 106, 200),
    Mob("Skeleton Lv.75", "75_skeleton", 121, 300),
    Mob("Skeleton Warrior Lv.90", "90_skeleton_warrior", 146, 375),
    Mob("Vampire Lv.100", "100_vampire", 171, 450),
    Mob("Vampire Lv.110", "110_vampire", 186, 530),
    # Index 19-20: Not power trainable
    Mob("Drow Ranger Lv.125", "120_drow_ranger", 191, 600),
    Mob("Drow Mage Lv. 130", "130_drow_mage", 191, 600),
    # Index 21: Power trainable
    Mob("Drow Assassin Lv.120", "125_drow_assassin", 221, 620),
    # Index 22: Not power trainable
    Mob("Drow Sorceress Lv.140", "140_drow_sorceress", 221, 600),
    # Index 23: Power trainable
    Mob("Drow Fighter Lv.135", "135_drow_fighter", 246, 680),
    # Index 24-26: Not power trainable
    Mob("Lizard Archer Lv.160", "160_lizard_archer", 271, 650),
    Mob("Lizard Shaman Lv.170", "170_lizard_shaman", 276, 600),
    Mob("Dead Eyes Lv.170", "170_dead_eyes", 276, 600),
    # Index 27-28: Power trainable
    Mob("Lizard Warrior Lv.150", "150_lizard_warrior", 301, 680),
    Mob("Djinn Lv.150", "150_djinn", 301, 640),
    # Index 29: Not power trainable
    Mob("Lizard High Shaman Lv.190", "190_lizard_high_shaman", 326, 740),
    # Index 30: Power trainable
    Mob("Gargoyle Lv.190", "190_gargoyle", 326, 740),
    # Index 31: Not power trainable
    Mob("Dragon Hatchling Lv. 240", "240_dragon_hatchling", 331, 10000),
    # Index 32: Power trainable
    Mob("Lizard Captain lv.180", "180_lizard_captain", 361, 815),
    # Index 33: Not power trainable
    Mob("Dragon Lv.250", "250_dragon", 501, 20000),
    # Index 34-35: Power trainable
    Mob("Minotaur Lv.225", "225_minotaur", 511, 4250),
    Mob("Minotaur Lv.250", "250_minotaur", 591, 5000),
    # Index 36-37: Not power trainable
    Mob("Dragon Warden Lv.280", "280_dragon_warden", 626, 30000),
    Mob("Ice Elemental Lv.300", "300_ice_elemental", 676, 40000),
    # Index 38: Power trainable
    Mob("Minotaur Lv.275", "275_minotaur", 681, 5750),
    # Index 39+: Not power trainable
    Mob("Ice Dragon Lv.320", "320_ice_dragon", 726, 50000),
    Mob("Yeti Lv.350", "350_yeti", 826, 60000),
]

# Weapon data 
WEAPONS = [
    Weapon("Training Weapon(4)", "4_7_9_11_13_golden_dagger", "4_7_9_11_13_golden_bow", "4_7_9_11_13_golden_wand", 4, 0),
    Weapon("Training Weapon(5)", "4_5_15_17_19_dagger", "4_5_15_17_19_bow", "4_5_15_17_19_wand", 5, 0),
    Weapon("Training Weapon(7)", "4_7_9_11_13_golden_dagger", "4_7_9_11_13_golden_bow", "4_7_9_11_13_golden_wand", 7, 0),
    Weapon("Training Weapon(9)", "4_7_9_11_13_golden_dagger", "4_7_9_11_13_golden_bow", "4_7_9_11_13_golden_wand", 9, 0),
    Weapon("Training Weapon(11)", "4_7_9_11_13_golden_dagger", "4_7_9_11_13_golden_bow", "4_7_9_11_13_golden_wand", 11, 0),
    Weapon("Training Weapon(13)", "4_7_9_11_13_golden_dagger", "4_7_9_11_13_golden_bow", "4_7_9_11_13_golden_wand", 13, 0),
    Weapon("Weapon(15)", "4_5_15_17_19_dagger", "4_5_15_17_19_bow", "4_5_15_17_19_wand", 15, 0),
    Weapon("Weapon(17)", "4_5_15_17_19_dagger", "4_5_15_17_19_bow", "4_5_15_17_19_wand", 17, 0),
    Weapon("Weapon(19)", "4_5_15_17_19_dagger", "4_5_15_17_19_bow", "4_5_15_17_19_wand", 19, 0),
    Weapon("Weapon(20)", "20_22_24_short_sword", "20_22_24_studded_bow", "20_22_24_novice_wand", 20, 0),
    Weapon("Weapon(22)", "20_22_24_short_sword", "20_22_24_studded_bow", "20_22_24_novice_wand", 22, 0),
    Weapon("Weapon(24)", "20_22_24_short_sword", "20_22_24_studded_bow", "20_22_24_novice_wand", 24, 0),
    Weapon("Weapon(25)", "25_27_29_sword", "25_27_29_iron_bow", "25_27_29_priest_wand", 25, 0),
    Weapon("Weapon(27)", "25_27_29_sword", "25_27_29_iron_bow", "25_27_29_priest_wand", 27, 0),
    Weapon("Weapon(29)", "25_27_29_sword", "25_27_29_iron_bow", "25_27_29_priest_wand", 29, 0),
    Weapon("Drow Weapon(30)", "30_32_34_341_broadsword", "30_32_34_341_drow_bow", "30_32_34_341_royal_priest_wand", 30, 0),
    Weapon("Drow Weapon(32)", "30_32_34_341_broadsword", "30_32_34_341_drow_bow", "30_32_34_341_royal_priest_wand", 32, 0),
    Weapon("Drow Weapon(34)", "30_32_34_341_broadsword", "30_32_34_341_drow_bow", "30_32_34_341_royal_priest_wand", 34, 0),
    Weapon("Drow Weapon(34+1)", "30_32_34_341_broadsword", "30_32_34_341_drow_bow", "30_32_34_341_royal_priest_wand", 34, 1),    Weapon("Lizard/Gargoyle Weapon(35)", ["35_37_39_391_lizard_slayer", "35_37_39_391_gargoyle_slayer"], ["35_37_39_391_lizard_bow", "35_37_39_391_gargoyle_bow"], ["35_37_39_391_shaman_wand", "35_37_39_391_gargoyle_wand"], 35, 0),
    Weapon("Lizard/Gargoyle Weapon(37)", ["35_37_39_391_lizard_slayer", "35_37_39_391_gargoyle_slayer"], ["35_37_39_391_lizard_bow", "35_37_39_391_gargoyle_bow"], ["35_37_39_391_shaman_wand", "35_37_39_391_gargoyle_wand"], 37, 0),
    Weapon("Lizard/Gargoyle Weapon(39)", ["35_37_39_391_lizard_slayer", "35_37_39_391_gargoyle_slayer"], ["35_37_39_391_lizard_bow", "35_37_39_391_gargoyle_bow"], ["35_37_39_391_shaman_wand", "35_37_39_391_gargoyle_wand"], 39, 0),
    Weapon("Lizard/Gargoyle Weapon(39+1)", ["35_37_39_391_lizard_slayer", "35_37_39_391_gargoyle_slayer"], ["35_37_39_391_lizard_bow", "35_37_39_391_gargoyle_bow"], ["35_37_39_391_shaman_wand", "35_37_39_391_gargoyle_wand"], 39, 1),
    Weapon("Dragon/Minotaur Weapon(40+1)", ["401_422_443_dragon_slayer", "401_422_443_minotaur_slayer"], ["401_422_443_dragon_bow", "401_422_443_minotaur_bow"], ["401_422_443_dragon_wand", "401_422_443_minotaur_wand"], 40, 1),
    Weapon("Dragon/Minotaur Weapon(42+2)", ["401_422_443_dragon_slayer", "401_422_443_minotaur_slayer"], ["401_422_443_dragon_bow", "401_422_443_minotaur_bow"], ["401_422_443_dragon_wand", "401_422_443_minotaur_wand"], 42, 2),
    Weapon("Dragon/Minotaur Weapon(44+3)", ["401_422_443_dragon_slayer", "401_422_443_minotaur_slayer"], ["401_422_443_dragon_bow", "401_422_443_minotaur_bow"], ["401_422_443_dragon_wand", "401_422_443_minotaur_wand"], 44, 3),
    Weapon("Icy Weapon(45+1)", "451_472_493_icy_broadsword", "451_472_493_icy_bow", "451_472_493_icy_wand", 45, 1),
    Weapon("Icy Weapon(47+2)", "451_472_493_icy_broadsword", "451_472_493_icy_bow", "451_472_493_icy_wand", 47, 2),
    Weapon("Icy Weapon(49+3)", "451_472_493_icy_broadsword", "451_472_493_icy_bow", "451_472_493_icy_wand", 49, 3),
    Weapon("Golden Weapon(50+1)", "501_522_543_golden_broadsword", "501_522_543_golden_bow", "501_522_543_golden_wand", 50, 1),
    Weapon("Golden Weapon(52+2)", "501_522_543_golden_broadsword", "501_522_543_golden_bow", "501_522_543_golden_wand", 52, 2),
    Weapon("Golden Weapon(54+3)", "501_522_543_golden_broadsword", "501_522_543_golden_bow", "501_522_543_golden_wand", 54, 3),
    Weapon("Golden Weapon(56+4)", "501_522_543_golden_broadsword", "501_522_543_golden_bow", "501_522_543_golden_wand", 56, 4),
    Weapon("Golden Weapon(58+5)", "501_522_543_golden_broadsword", "501_522_543_golden_bow", "501_522_543_golden_wand", 58, 5),
]

def get_mob(index):
    if 0 <= index < len(MOBS):
        return MOBS[index]
    return None

def get_weapon(index):
    if 0 <= index < len(WEAPONS):
        return WEAPONS[index]
    return None

def is_power_trainable(mob_index):
    non_power_trainable = [13, 19, 20, 22, 24, 25, 26, 29, 31, 33, 36, 37]
    non_power_trainable.extend(range(39, len(MOBS)))
    return mob_index not in non_power_trainable
