def format_number(num: int) -> str:
    """
    Format numbers with commas as thousand separators
    
    Args:
    num (int): The number to format
        
    Returns:
    str: The number formatted with commas
        
    Examples:
        >>> format_number(1000)
        '1,000'
        >>> format_number(1234567)
        '1,234,567'
    """
    return f"{num:,}"


def format_float(num: float, decimals: int = 1) -> str:
    """
    Format floating point numbers with a specific number of decimals
    
    Args:
    num (float): The number to format
    decimals (int): Number of decimals to display (default 1)
        
    Returns:
    str: The number formatted with the specified decimals
        
    Examples:
        >>> format_float(1234.567)
        '1,234.6'
        >>> format_float(1234.567, 2)
        '1,234.57'
    """
    return f"{num:,.{decimals}f}"


def format_time(seconds: float) -> str:
    """
    Format a time in seconds into minutes and seconds
    
    Args:
    seconds (float): Time in seconds
        
    Returns:
    str: The time formatted as "X min. Y sec."
        
    Examples:
        >>> format_time(90)
        '1 min. 30 sec.'
        >>> format_time(3661)
        '61 min. 1 sec.'
    """
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes} min. {remaining_seconds} sec."


def format_hours(hours: float) -> str:
    """
    Format a time in hours into days, hours, and minutes
    
    Args:
    hours (float): Time in hours
        
    Returns:
    str: The time formatted in a human-readable way
        
    Examples:
        >>> format_hours(25.5)
        '1 day, 1 hour, 30 minutes'
        >>> format_hours(2.25)
        '2 hours, 15 minutes'
    """
    days = int(hours // 24)
    remaining_hours = int(hours % 24)
    minutes = int((hours % 1) * 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days > 1 else ''}")
    if remaining_hours > 0:
        parts.append(f"{remaining_hours} hour{'s' if remaining_hours > 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    
    return ", ".join(parts) if parts else "0 minutes"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format a value as a percentage
    
    Args:
    value (float): The value to format (between 0 and 1)
    decimals (int): Number of decimals (default 1)
        
    Returns:
    str: The formatted percentage
        
    Examples:
        >>> format_percentage(0.856)
        '85.6%'
        >>> format_percentage(0.999, 0)
        '100%'
    """
    percentage = value * 100
    return f"{percentage:.{decimals}f}%"


def validate_input(value: int, min_val: int = None, max_val: int = None) -> bool:
    """
    Validate that a value is within acceptable bounds
    
    Args:
    value (int): The value to validate
    min_val (int, optional): Minimum acceptable value
    max_val (int, optional): Maximum acceptable value
        
    Returns:
    bool: True if the value is valid, False otherwise
        
    Examples:
        >>> validate_input(50, min_val=1, max_val=100)
        True
        >>> validate_input(150, max_val=100)
        False
    """
    if min_val is not None and value < min_val:
        return False
    if max_val is not None and value > max_val:
        return False
    return True


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text if it exceeds a maximum length
    
    Args:
    text (str): The text to truncate
    max_length (int): Maximum length
    suffix (str): Suffix to add if truncated (default "...")
        
    Returns:
    str: The truncated or original text
        
    Examples:
        >>> truncate_text("Hello World", 8)
        'Hello...'
        >>> truncate_text("Hi", 10)
        'Hi'
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_stat_range(stat1: int, stat2: int) -> str:
    """
    Format a range of stats
    
    Args:
    stat1 (int): Starting stat
    stat2 (int): Ending stat
        
    Returns:
    str: The formatted range
        
    Examples:
        >>> format_stat_range(50, 100)
        '50 → 100'
    """
    return f"{stat1} → {stat2}"


def format_gold_amount(amount: int) -> str:
    """
    Format a gold amount in a compact form
    
    Args:
    amount (int): The amount of gold
        
    Returns:
    str: The formatted amount (K for thousands, M for millions)
        
    Examples:
        >>> format_gold_amount(1500)
        '1.5K'
        >>> format_gold_amount(2500000)
        '2.5M'
    """
    if amount >= 1_000_000:
        return f"{amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"{amount / 1_000:.1f}K"
    else:
        return str(amount)