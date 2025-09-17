from config import EMOJIS


class Mob:
    """
    Represents a monster in the game with its statistics
    
    Attributes:
        name (str): Monster name with its level
        emoji_key (str): Key used to retrieve the emoji from the EMOJIS dictionary
        defense (int): Monster's defense
        health (int): Monster's hit points
    """
    
    def __init__(self, name: str, emoji_key: str, defense: int, health: int):
        self.name = name
        self.emoji_key = emoji_key
        self.defense = defense
        self.health = health
    
    @property
    def emoji(self) -> str:
        """Get the monster's emoji from configuration"""
        return EMOJIS.get(self.emoji_key, "")
    
    def __str__(self) -> str:
        """String representation of the monster with its emoji"""
        return f"{self.name} {self.emoji}"
    
    def __repr__(self) -> str:
        """Detailed representation for debugging"""
        return f"Mob(name='{self.name}', defense={self.defense}, health={self.health})"


class Weapon:
    """
    Represents a weapon in the game with its statistics
    
    Attributes:
        name (str): Weapon name
        melee_emoji_key (str | list): Key(s) for the melee emoji
        distance_emoji_key (str | list): Key(s) for the distance emoji
        magic_emoji_key (str | list): Key(s) for the magic emoji
        attack (int): Weapon's attack power
        buffs (int): Stat bonus provided by the weapon
    """
    
    def __init__(self, name: str, melee_emoji_key, distance_emoji_key, 
                 magic_emoji_key, attack: int, buffs: int):
        self.name = name
        self.melee_emoji_key = melee_emoji_key
        self.distance_emoji_key = distance_emoji_key
        self.magic_emoji_key = magic_emoji_key
        self.attack = attack
        self.buffs = buffs
    
    def _get_emoji_from_key(self, key) -> str:
        """
        Retrieve one or more emojis from a key or a list of keys
        
        Args:
            key: Unique key (str) or list of keys for emojis
            
        Returns:
            str: Concatenated emoji(s)
        """
        if isinstance(key, list):
            return "".join(EMOJIS.get(k, "") for k in key)
        else:
            return EMOJIS.get(key, "")
    
    @property
    def melee_emoji(self) -> str:
        """Emoji for the melee class"""
        return self._get_emoji_from_key(self.melee_emoji_key)
    
    @property
    def distance_emoji(self) -> str:
        """Emoji for the distance class"""
        return self._get_emoji_from_key(self.distance_emoji_key)
    
    @property
    def magic_emoji(self) -> str:
        """Emoji for the magic class"""
        return self._get_emoji_from_key(self.magic_emoji_key)
    
    def get_emoji(self, class_type: int = None) -> str:
        """
        Get the emoji for a specific class or all emojis
        
        Args:
            class_type (int, optional): 0=Melee, 1=Distance, 2=Magic, None=All
            
        Returns:
            str: Corresponding emoji(s)
        """
        if class_type == 0:  # Melee
            return self.melee_emoji
        elif class_type == 1:  # Distance
            return self.distance_emoji
        elif class_type == 2:  # Magic
            return self.magic_emoji
        else:  # All emojis
            return self.melee_emoji + self.distance_emoji + self.magic_emoji
    
    def __str__(self) -> str:
        """String representation of the weapon"""
        return f"{self.name} ({self.attack} ATK, +{self.buffs} buffs)"
    
    def __repr__(self) -> str:
        """Detailed representation for debugging"""
        return f"Weapon(name='{self.name}', attack={self.attack}, buffs={self.buffs})"