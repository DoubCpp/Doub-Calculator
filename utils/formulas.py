import math


class Formulas:
    """Class containing all calculation formulas for Rucoy Online"""
    
    # ========== Raw damage formulas ==========
    
    @staticmethod
    def auto_min_raw_damage_calc(stat: int, weapon_atk: int, base: int) -> float:
        """
        Calculate minimum raw damage for auto attacks
        
        Args:
            stat: Stat level (with buffs)
            weapon_atk: Weapon attack power
            base: Player base level
            
        Returns:
            float: Minimum raw damage
        """
        return (stat * weapon_atk) / 20 + base / 4
    
    @staticmethod
    def auto_max_raw_damage_calc(stat: int, weapon_atk: int, base: int) -> float:
        """
        Calculate maximum raw damage for auto attacks
        
        Args:
            stat: Stat level (with buffs)
            weapon_atk: Weapon attack power
            base: Player base level
            
        Returns:
            float: Maximum raw damage
        """
        return (stat * weapon_atk) / 10 + base / 4
    
    @staticmethod
    def special_meldist_min_raw_damage_calc(stat: int, weapon_atk: int, base: int) -> float:
        """
        Calculate minimum raw damage for special (Melee/Distance) attacks
        
        Args:
            stat: Stat level (with buffs)
            weapon_atk: Weapon attack power
            base: Player base level
            
        Returns:
            float: Minimum special raw damage
        """
        return 1.5 * ((stat * weapon_atk) / 20 + base / 4)
    
    @staticmethod
    def special_meldist_max_raw_damage_calc(stat: int, weapon_atk: int, base: int) -> float:
        """
        Calculate maximum raw damage for special (Melee/Distance) attacks
        
        Args:
            stat: Stat level (with buffs)
            weapon_atk: Weapon attack power
            base: Player base level
            
        Returns:
            float: Maximum special raw damage
        """
        return 1.5 * ((stat * weapon_atk) / 10 + base / 4)
    
    @staticmethod
    def special_magic_min_raw_damage_calc(stat: int, weapon_atk: int, base: int) -> float:
        """
        Calculate minimum raw damage for special Magic attacks
        
        Args:
            stat: Stat level (with buffs)
            weapon_atk: Weapon attack power
            base: Player base level
            
        Returns:
            float: Minimum magic raw damage
        """
        return 1.5 * (((1.05 * stat * weapon_atk) / 20) + 9 * base / 32)
    
    @staticmethod
    def special_magic_max_raw_damage_calc(stat: int, weapon_atk: int, base: int) -> float:
        """
        Calculate maximum raw damage for special Magic attacks
        
        Args:
            stat: Stat level (with buffs)
            weapon_atk: Weapon attack power
            base: Player base level
            
        Returns:
            float: Maximum magic raw damage
        """
        return 1.5 * (((1.05 * stat * weapon_atk) / 10) + 9 * base / 32)
    
    # ========== Effective damage formulas ==========
    
    @staticmethod
    def min_damage_calc(min_raw_damage: float, mob_defense: int) -> float:
        """
        Calculate minimum effective damage after defense
        
        Args:
            min_raw_damage: Minimum raw damage
            mob_defense: Monster defense
            
        Returns:
            float: Minimum effective damage (min 0)
        """
        min_damage = min_raw_damage - mob_defense
        return max(0, min_damage)
    
    @staticmethod
    def max_damage_calc(max_raw_damage: float, mob_defense: int) -> float:
        """
        Calculate maximum effective damage after defense
        
        Args:
            max_raw_damage: Maximum raw damage
            mob_defense: Monster defense
            
        Returns:
            float: Maximum effective damage
        """
        return max_raw_damage - mob_defense
    
    @staticmethod
    def max_raw_crit_damage_calc(max_raw_damage: float) -> float:
        """
        Calculate maximum raw critical damage (5% bonus)
        
        Args:
            max_raw_damage: Normal maximum raw damage
            
        Returns:
            float: Maximum raw critical damage
        """
        return max_raw_damage * 1.05
    
    @staticmethod
    def max_crit_damage_calc(max_raw_crit_damage: float, mob_defense: int) -> float:
        """
        Calculate maximum effective critical damage after defense
        
        Args:
            max_raw_crit_damage: Maximum raw critical damage
            mob_defense: Monster defense
            
        Returns:
            float: Maximum effective critical damage
        """
        return max_raw_crit_damage - mob_defense
    
    # ========== Accuracy formulas ==========
    
    @staticmethod
    def normal_accuracy_calc(max_raw_damage: float, min_raw_damage: float, mob_defense: int) -> float:
        """
        Calculate accuracy for normal attacks
        
        Args:
            max_raw_damage: Maximum raw damage
            min_raw_damage: Minimum raw damage
            mob_defense: Monster defense
            
        Returns:
            float: Normal accuracy (0-1)
        """
        if max_raw_damage <= min_raw_damage:
            return 0.0
        normal_accuracy = (max_raw_damage - mob_defense) / (max_raw_damage - min_raw_damage)
        return min(1.0, max(0.0, normal_accuracy))
    
    @staticmethod
    def crit_accuracy_calc(max_raw_crit_damage: float, max_raw_damage: float, mob_defense: int) -> float:
        """
        Calculate accuracy for critical attacks
        
        Args:
            max_raw_crit_damage: Maximum raw critical damage
            max_raw_damage: Normal maximum raw damage
            mob_defense: Monster defense
            
        Returns:
            float: Critical accuracy (0-1)
        """
        if max_raw_crit_damage <= max_raw_damage:
            return 0.0
        crit_accuracy = (max_raw_crit_damage - mob_defense) / (max_raw_crit_damage - max_raw_damage)
        return min(1.0, max(0.0, crit_accuracy))
    
    @staticmethod
    def accuracy_calc(max_raw_crit_damage: float, max_raw_damage: float, 
                     min_raw_damage: float, mob_defense: int) -> float:
        """
        Calculate total accuracy (normal + critical)
        
        Args:
            max_raw_crit_damage: Maximum raw critical damage
            max_raw_damage: Normal maximum raw damage
            min_raw_damage: Minimum raw damage
            mob_defense: Monster defense
            
        Returns:
            float: Total accuracy (0-1)
        """
        normal_acc = Formulas.normal_accuracy_calc(max_raw_damage, min_raw_damage, mob_defense)
        crit_acc = Formulas.crit_accuracy_calc(max_raw_crit_damage, max_raw_damage, mob_defense)
        return (normal_acc * 0.99) + (crit_acc * 0.01)
    
    @staticmethod
    def total_accuracy_calc(accuracy: float, tick: int) -> float:
        """
        Calculate total accuracy for power training
        
        Args:
            accuracy: Base accuracy
            tick: Number of ticks
            
        Returns:
            float: Total accuracy for power training
        """
        return 1.0 - math.pow(math.pow(1.0 - accuracy, tick), 10)
    
    # ========== Combat formulas ==========
    
    @staticmethod
    def time_to_kill_calc(avg_dmg: float, mob_health: int) -> float:
        """
        Calculate time to kill a monster
        
        Args:
            avg_dmg: Average damage per second
            mob_health: Monster health points
            
        Returns:
            float: Time in seconds (inf if damage <= 0)
        """
        return mob_health / avg_dmg if avg_dmg > 0 else float('inf')
    
    @staticmethod
    def average_damage_calc(accuracy: float, max_damage: float, 
                          min_damage: float, max_crit_damage: float) -> float:
        """
        Calculate average damage per attack
        
        Args:
            accuracy: Total accuracy
            max_damage: Normal maximum damage
            min_damage: Minimum damage
            max_crit_damage: Maximum critical damage
            
        Returns:
            float: Average damage per attack
        """
        # Correct formula: both crits and normals depend on accuracy
        normal_avg = (max_damage + min_damage) / 2
        crit_avg = (max_crit_damage + max_damage) / 2
        return accuracy * (0.99 * normal_avg + 0.01 * crit_avg)
    
    # ========== Tickrate formulas ==========
    
    @staticmethod
    def tickrate_calc(accuracy: float, max_tickrate: int) -> float:
        """
        Calculate effective tickrate for normal training
        
        Args:
            accuracy: Accuracy
            max_tickrate: Maximum possible tickrate
            
        Returns:
            float: Effective tickrate
        """
        return max_tickrate * (1.0 - math.pow(1.0 - accuracy, 10.0))
    
    @staticmethod
    def powertickrate_calc(total_accuracy: float, max_tickrate: int) -> float:
        """
        Calculate effective tickrate for power training
        
        Args:
            total_accuracy: Total accuracy
            max_tickrate: Maximum possible tickrate
            
        Returns:
            float: Effective tickrate for power training
        """
        return max_tickrate * total_accuracy
    
    @staticmethod
    def max_tickrate_calc(tick: int) -> int:
        """
        Calculate maximum tickrate based on the number of ticks
        
        Args:
            tick: Number of ticks
            
        Returns:
            int: Maximum tickrate (3600 per tick up to 5, then 18000)
        """
        if tick <= 5:
            return tick * 3600
        else:
            return 18000
    
    # ========== Experience formulas ==========
    
    @staticmethod
    def exp_calc(base: int) -> float:
        """
        Calculate total experience for a base level
        
        Args:
            base: Base level
            
        Returns:
            float: Total required experience
        """
        return math.pow(base, (base / 1000) + 3)
    
    @staticmethod
    def stat0to54_calc(stat: int) -> float:
        """
        Calculate ticks required for stats 0-54
        
        Args:
            stat: Stat level (0-54)
            
        Returns:
            float: Number of required ticks
        """
        return math.pow(stat, (stat / 1000) + 2.373)
    
    @staticmethod
    def stat55to99_calc(stat: int) -> float:
        """
        Calculate ticks required for stats 55+
        
        Args:
            stat: Stat level (55+)
            
        Returns:
            float: Number of required ticks
        """
        return math.pow(stat, (stat / 1000) + 2.171)
    
    @staticmethod
    def find_stat_level_calc(ticks2: float) -> float:
        """
        Find the stat level corresponding to a number of ticks
        
        Args:
            ticks2: Number of ticks
            
        Returns:
            float: Stat level (with decimals) or -1 if not found
        """
        if ticks2 <= Formulas.stat0to54_calc(54):
            for stat in range(5, 55):
                if ticks2 <= Formulas.stat0to54_calc(stat):
                    prev_ticks = Formulas.stat0to54_calc(stat - 1)
                    curr_ticks = Formulas.stat0to54_calc(stat)
                    fract = (ticks2 - prev_ticks) / (curr_ticks - prev_ticks)
                    return (stat - 1) + fract
        else:
            for stat in range(55, 1001):
                if ticks2 <= Formulas.stat55to99_calc(stat):
                    prev_ticks = Formulas.stat55to99_calc(stat - 1)
                    curr_ticks = Formulas.stat55to99_calc(stat)
                    fract = (ticks2 - prev_ticks) / (curr_ticks - prev_ticks)
                    return (stat - 1) + fract
        return -1
    
    # ========== Special formulas ==========
    
    @staticmethod
    def threshold_calc(tick: int) -> float:
        """
        Calculate the accuracy threshold for power training
        
        Args:
            tick: Number of ticks
            
        Returns:
            float: Required accuracy threshold
        """
        return 1.0 - math.pow(0.8251, (1.0 / tick))
    
    @staticmethod
    def consistency_calc(max_raw_crit_damage: float, max_raw_damage: float, 
                        min_raw_damage: float, mob_health: int, mob_defense: int) -> float:
        """
        Calculate the consistency to one-shot a monster
        
        Args:
            max_raw_crit_damage: Maximum raw critical damage
            max_raw_damage: Normal maximum raw damage
            min_raw_damage: Minimum raw damage
            mob_health: Monster health points
            mob_defense: Monster defense
            
        Returns:
            float: Consistency percentage (0-1)
        """
        total_defense = mob_health + mob_defense
        
        # Impossible to one-shot
        if total_defense - max_raw_crit_damage > 0:
            return 0
        
        range_damage = max_raw_damage - min_raw_damage
        normal_oneshots = max_raw_damage - total_defense
        
        # One-shot with normal attacks
        if normal_oneshots > 0:
            normal_consistency = normal_oneshots / range_damage
            return normal_consistency * 0.99 + 0.01
        else:
            # One-shot only with critical hits
            crit_range = max_raw_crit_damage - max_raw_damage
            critical_oneshots = max_raw_crit_damage - total_defense
            return (critical_oneshots / crit_range) * 0.01