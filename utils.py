import math

class Formulas:

    @staticmethod
    def auto_min_raw_damage_calc(stat, weapon_atk, base):
        return (stat * weapon_atk) / 20 + base / 4
    
    @staticmethod
    def auto_max_raw_damage_calc(stat, weapon_atk, base):
        return (stat * weapon_atk) / 10 + base / 4
    
    @staticmethod
    def special_meldist_min_raw_damage_calc(stat, weapon_atk, base):
        return 1.5 * ((stat * weapon_atk) / 20 + base / 4)
    
    @staticmethod
    def special_meldist_max_raw_damage_calc(stat, weapon_atk, base):
        return 1.5 * ((stat * weapon_atk) / 10 + base / 4)
    
    @staticmethod
    def special_magic_min_raw_damage_calc(stat, weapon_atk, base):
        return 1.5 * (((1.05 * stat * weapon_atk) / 20) + 9 * base / 32)
    
    @staticmethod
    def special_magic_max_raw_damage_calc(stat, weapon_atk, base):
        return 1.5 * (((1.05 * stat * weapon_atk) / 10) + 9 * base / 32)
    
    @staticmethod
    def min_damage_calc(min_raw_damage, mob_defense):
        min_damage = min_raw_damage - mob_defense
        return max(0, min_damage)
    
    @staticmethod
    def max_damage_calc(max_raw_damage, mob_defense):
        return max_raw_damage - mob_defense
    
    @staticmethod
    def max_raw_crit_damage_calc(max_raw_damage):
        return max_raw_damage * 1.05
    
    @staticmethod
    def max_crit_damage_calc(max_raw_crit_damage, mob_defense):
        return max_raw_crit_damage - mob_defense
    
    @staticmethod
    def normal_accuracy_calc(max_raw_damage, min_raw_damage, mob_defense):
        normal_accuracy = (max_raw_damage - mob_defense) / (max_raw_damage - min_raw_damage)
        return min(1.0, normal_accuracy)
    
    @staticmethod
    def crit_accuracy_calc(max_raw_crit_damage, max_raw_damage, mob_defense):
        crit_accuracy = (max_raw_crit_damage - mob_defense) / (max_raw_crit_damage - max_raw_damage)
        return min(1.0, crit_accuracy)
    
    @staticmethod
    def accuracy_calc(max_raw_crit_damage, max_raw_damage, min_raw_damage, mob_defense):
        normal_acc = Formulas.normal_accuracy_calc(max_raw_damage, min_raw_damage, mob_defense)
        crit_acc = Formulas.crit_accuracy_calc(max_raw_crit_damage, max_raw_damage, mob_defense)
        return (normal_acc * 0.99) + (crit_acc * 0.01)
    
    @staticmethod
    def total_accuracy_calc(accuracy, tick):
        return 1.0 - math.pow(math.pow(1.0 - accuracy, tick), 10)
    
    @staticmethod
    def time_to_kill_calc(avg_dmg, mob_health):
        return mob_health / avg_dmg if avg_dmg > 0 else float('inf')
    
    @staticmethod
    def average_damage_calc(accuracy, max_damage, min_damage, max_crit_damage):
        return (accuracy) * (0.99 * ((max_damage + min_damage) / 2)) + 0.01 * ((max_crit_damage + max_damage) / 2)
    
    @staticmethod
    def tickrate_calc(accuracy, max_tickrate):
        return max_tickrate * (1.0 - math.pow(1.0 - accuracy, 10.0))
    
    @staticmethod
    def powertickrate_calc(total_accuracy, max_tickrate):
        return max_tickrate * total_accuracy
    
    @staticmethod
    def max_tickrate_calc(tick):
        if tick <= 5:
            return tick * 3600
        else:
            return 18000
    
    @staticmethod
    def exp_calc(base):
        return math.pow(base, (base / 1000) + 3)
    
    @staticmethod
    def stat0to54_calc(stat):
        return math.pow(stat, (stat / 1000) + 2.373)
    
    @staticmethod
    def stat55to99_calc(stat):
        return math.pow(stat, (stat / 1000) + 2.171)
    
    @staticmethod
    def find_stat_level_calc(ticks2):
        if ticks2 <= Formulas.stat0to54_calc(54):
            for stat in range(5, 55):
                if ticks2 <= Formulas.stat0to54_calc(stat):
                    fract = (ticks2 - Formulas.stat0to54_calc(stat - 1)) / (Formulas.stat0to54_calc(stat) - Formulas.stat0to54_calc(stat - 1))
                    return (stat - 1) + fract
        else:
            for stat in range(55, 1001):
                if ticks2 <= Formulas.stat55to99_calc(stat):
                    fract = (ticks2 - Formulas.stat55to99_calc(stat - 1)) / (Formulas.stat55to99_calc(stat) - Formulas.stat55to99_calc(stat - 1))
                    return (stat - 1) + fract
        return -1
    
    @staticmethod
    def threshold_calc(tick):
        return 1.0 - math.pow(0.8251, (1.0 / tick))
    
    @staticmethod
    def consistency_calc(max_raw_crit_damage, max_raw_damage, min_raw_damage, mob_health, mob_defense):
        total_defense = mob_health + mob_defense
        
        if total_defense - max_raw_crit_damage > 0:
            return 0
        
        range_damage = max_raw_damage - min_raw_damage
        normal_oneshots = max_raw_damage - total_defense
        
        if normal_oneshots > 0:
            normal_consistency = normal_oneshots / range_damage
            return normal_consistency * 0.99 + 0.01
        else:
            crit_range = max_raw_crit_damage - max_raw_damage
            critical_oneshots = max_raw_crit_damage - total_defense
            return (critical_oneshots / crit_range) * 0.01


def format_number(num):
    return f"{num:,}"

def format_float(num, decimals=1):
    return f"{num:,.{decimals}f}"

def format_time(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes} min. {remaining_seconds} sec."

def validate_input(value, min_val=None, max_val=None):
    if min_val is not None and value < min_val:
        return False
    if max_val is not None and value > max_val:
        return False
    return True
